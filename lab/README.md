# The bookshop agent lab

The lab for the Packt workshop "Agentic Observability Engineering with OpenTelemetry" (2026-11-21). A bookshop support agent answers one customer question by retrieving from a catalog, calling a language model through OpenRouter, and using two MCP tools. Both sessions use it:

- **Session 1, Instrumenting the agent** (Juraci Paixão Kröhling): steps 0 to 4 take the agent from no telemetry to one trace that covers the agent, the model calls and the MCP server. It stops where production work starts.
- **Session 2, From agent trace to production** (Severin Neumann): steps 5 to 9 put a Collector in between, govern prompt and response content, derive metrics, sample, and debug four failures.

Session 1 is Juraci's lab, originally at [ollygarden-demo/instrumenting-the-agent](https://github.com/ollygarden-demo/instrumenting-the-agent). The files for Session 2 were added on top of it; what changed is listed under [Session 2](#session-2-from-one-trace-to-production-steps-5-to-9).

## Setup

You need Docker, [uv](https://docs.astral.sh/uv/), and an OpenRouter API key.

```bash
cp .env.example .env          # then set OPENROUTER_API_KEY, or export it in your shell instead
docker compose up -d          # Jaeger 2.22 UI on http://localhost:16686; a Collector takes OTLP/HTTP on 4318
uv sync
```

Variables already exported in your shell take precedence over `.env`. The model defaults to `deepseek/deepseek-v4-flash`; set `DEMO_MODEL` to any OpenRouter model that supports tool calling. A full run takes about five seconds and costs a fraction of a cent.

## The application

`agent_v0.py` is a plain agent loop. It searches `data/catalog.json` with keyword retrieval (`retrieval.py`), sends the excerpt and the question to the model with the MCP tools attached, executes the tool calls the model asks for, and returns the final answer. `bookshop_mcp.py` is the MCP server, started by the agent over stdio, with two tools: `check_inventory` and `get_order_status`.

The question asks about order `ORD-1044`, which does not exist. The tool fails, the model apologizes politely, and the customer gets a reasonable answer. That failure is the point: nothing in the output tells you a tool failed, and in step 0 all you have is one line on stderr.

The agent versions are separate files so each step is a small diff you can show on screen with `diff -u agent_v2.py agent_v3.py`.

## Session 1: steps 0 to 4

The agent sends to `localhost:4318`. In Session 1 that was Jaeger itself; here it is a Collector that passes everything on to Jaeger unchanged (`collector/step5-connect.yaml`, the default), so these steps behave as they did.

### Step 0: no telemetry

```bash
uv run --env-file .env python agent_v0.py
```

The answer looks fine. Ask the audience: which step failed, how long did each part take, and how many tokens did this cost? Nobody can tell.

### Step 1: zero-code instrumentation

```bash
uv run --env-file .env opentelemetry-instrument python agent_v0.py
```

Same code, run under `opentelemetry-instrument`. `opentelemetry-instrumentation-genai-openai` (from the new `opentelemetry-python-genai` repository) traces every OpenAI SDK call, and OpenRouter is OpenAI-compatible, so each model call becomes a `chat deepseek/deepseek-v4-flash` span with token usage, reasoning tokens, cached input tokens, and finish reasons. The MCP Python SDK 2.x has OpenTelemetry built in, so its client calls show up as `MCP send tools/call ...` spans with no extra package.

Open Jaeger and show the problem: about six separate traces, one per call, with nothing tying them together. Two details to point out on the `chat` span: `gen_ai.provider.name` is `openai` because it reflects the client SDK, while `server.address` is `openrouter.ai`. And the failed tool call is not marked as an error anywhere.

### Step 2: give the agent its own spans

```bash
diff -u agent_v0.py agent_v2.py
uv run --env-file .env opentelemetry-instrument python agent_v2.py
```

`TelemetryHandler` from `opentelemetry-util-genai` creates spans that follow the GenAI semantic conventions without writing attribute names by hand: `invoke_agent bookshop-support` around the run, `retrieval book-catalog` around the search, and `execute_tool <name>` around each tool call. Everything becomes one trace. The `get_order_status` tool span is now red with `error.type=tool_error`, the value the MCP conventions define for a tool result with `isError` set.

This is the moment to read the trace as a story: retrieval, the first model call deciding which tools to call, two tool calls, the second model call writing the answer. Point at the relative widths of model time versus tool time.

### Step 3: follow the call into the MCP server

```bash
diff -u agent_v2.py agent_v3.py
uv run --env-file .env opentelemetry-instrument python agent_v3.py
```

The only change is how the agent launches the MCP server: under `opentelemetry-instrument`, with the `OTEL_*` variables passed through, because stdio MCP clients only hand a small allowlist of environment variables to the server process. There is no propagation code. The MCP SDK client injects W3C `traceparent` into the request's `params._meta` (MCP SEP-414), and the server middleware extracts it, so `tools/call get_order_status` spans from the `bookshop-mcp` service appear as children of the agent's client spans. Jaeger now shows two services in one trace, and the error is visible on both sides of the boundary.

### Step 4: what did this run cost?

```bash
diff -u agent_v3.py agent_v4.py
uv run --env-file .env opentelemetry-instrument python agent_v4.py
```

The agent adds the token counts from each response to the `invoke_agent` span (`gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`) and records the billed cost that OpenRouter returns in `usage.cost` as `bookshop.llm.cost_usd`. Cost uses an application namespace on purpose: the GenAI conventions do not define a cost attribute, and inventing one under `gen_ai.*` would collide with whatever the conventions add later.

### Optional: capture content

```bash
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY \
  uv run --env-file .env opentelemetry-instrument python agent_v4.py
```

Content is off by default. With `SPAN_ONLY`, the same code records the prompts and completions on `chat` spans, tool arguments and results on `execute_tool` spans, and the query, document ids, and scores on the `retrieval` span. The retrieval span is worth a look: the book the model recommends is only the third-ranked document. These attributes now carry customer data, so they need a decision about capture, redaction, and retention before production.

## Session 2: from one trace to production (steps 5 to 9)

Session 2 runs `agent_v5.py` and changes the Collector, one config per step. Each config contains the ones before it.

| Step | Config | What it adds |
| --- | --- | --- |
| 5 Connect | `collector/step5-connect.yaml` | One Collector between the agent and the backends: Jaeger, and one OTLP backend |
| 6 Govern | `collector/step6-govern.yaml` | `filter`: content events only from approved services, and no handshake noise. `redaction`: masks email addresses and card numbers. `transform`: drops tool results from tool spans and caps attribute sizes |
| 7 Measure | `collector/step7-measure.yaml` | `signal_to_metrics`: tokens per run (`bookshop.run.tokens`) and billed cost per run (`bookshop.run.cost`), from the run span |
| 8 Sample | `collector/step8-sample.yaml` | `tail_sampling`: keeps errors, slow retrieval, expensive runs, unusual tool sequences and failed checks. Jaeger sits before the sampler and still sees every run |
| 9 Debug | (step 8 config) | Four failures to reproduce, see below |

Switch the step by recreating the Collector:

```bash
COLLECTOR_CONFIG=step8-sample.yaml docker compose up -d --no-deps collector
```

For the metrics and logs that steps 7 and 9 use, uncomment the four Session 2 lines at the end of `.env`.

### What changed from the Session 1 lab

- `compose.yaml`: adds the Collector and a second Collector, `sink`, that stands in for a backend and writes what it receives to `./out`. Jaeger now keeps traces on disk in `./jaeger-data` (`jaeger.yaml`), so they survive a restart.
- `agent_v5.py`: `agent_v4.py` plus a handful of lines. The run span records the customer (`bookshop.customer.id`) and the tools the run called, in order (`bookshop.run.tools`). `QUESTION` sets the question, `CHECKS=on` adds one outcome check, `FAILURE` switches a failure on.
- `bookshop_mcp.py`: with `FAILURE=loop`, the order lookup answers "pending".
- `data/inventory.json`: orders have a customer.
- New: `collector/`, `kept.py`, `saved-runs/` with `load-saved-runs.sh`, `demo.rc`.

### Step 6: content

```bash
# content on the spans, with personal data in the question
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY \
QUESTION="Hi, Maria Lopez here (maria.lopez@example.com). I paid with card 4111 1111 1111 1111. Where is order ORD-1043?" \
  uv run --env-file .env opentelemetry-instrument python agent_v5.py

# content as log events instead; the filter lets them through only for an approved service
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=EVENT_ONLY \
OTEL_RESOURCE_ATTRIBUTES=bookshop.content.approved=true \
  uv run --env-file .env opentelemetry-instrument python agent_v5.py
```

What to look for, including where these controls stop:

- The email address and the card number are masked. The name is not: a pattern cannot find a name.
- Every ISBN is masked too, because 13 digits look like a card number to this pattern.
- Redaction masks string attributes. Content sent as log events is structured, and the processor passes it through unmasked.
- The tool result is removed from the tool span, but the next model call repeats it in its input messages.
- The size cap cuts long JSON strings mid-value.
- The approval mark is a resource attribute the service sets itself. In production, set it from the platform or list service names in the Collector config.

### Step 8: what the sampler keeps

With the default backend (the local sink), run a few different runs and compare:

```bash
for m in "" slow loop wrong wrong; do
  FAILURE=$m uv run --env-file .env opentelemetry-instrument python agent_v5.py &
done; wait
sleep 35 && python3 kept.py     # the sampler waits up to 30 s before it decides
```

`kept.py` lists every run Jaeger saw and marks the ones that reached the sink. There is no random baseline in this config, so the result is repeatable; in production keep a few percent of normal runs as well.

### Step 9: the four failures

| Switch | What happens | How it shows |
| --- | --- | --- |
| `FAILURE=slow` | Retrieval sleeps for 8 seconds (simulated) | The retrieval duration metric, then one long span in the trace |
| `FAILURE=loop` | One line in the system prompt plus an order system that answers "pending" make the model look up the order five times, until the agent's five-round cap ends the run | About three times the tokens; the same tool span five times |
| `FAILURE=wrong` | The customer asks about "my order" without a number. Often the agent skips the order tool: an unexpected path | `bookshop.run.tools` on the run span |
| `FAILURE=wrong`, some of the time | The agent looks up `ORD-1042`, the example ID from the tool description, which is another customer's order | Nothing, unless you run with `CHECKS=on`: then `bookshop.check.order_owned` is `false` on the tool span |

The last two are the model's own behaviour on the unchanged Session 1 prompt and tools, so they do not happen on every run: in our runs the wrong order came up in 5 of 30. `saved-runs/` has one recorded run of each failure. Load them into Jaeger under their original trace IDs with:

```bash
./load-saved-runs.sh
```

### Sending to your backend

By default the Collector sends to the local sink. To send to an OTLP backend, set `BACKEND_ENDPOINT` before `docker compose up` and change the auth headers of the `otlp_http/backend` exporter in `collector/*.yaml`. The headers in the files are Bronto's (`x-bronto-api-key` from `BACKEND_API_KEY`, `x-bronto-dataset` from `BACKEND_DATASET`); any OTLP backend works.

### The demo shell

`demo.rc` is the shell behind the terminal slides: `bash --rcfile demo.rc -i` gives you `connect`, `govern`, `sample`, `slow` and `loop`, each of which prints the real commands before running them.

### Not for production as it is

The Collector configs are sized for a laptop. They have no `memory_limiter`, no batching and no queue settings, the sampler runs in a single instance, and the unusual-tools policy allows exactly one tool sequence. The GenAI semantic conventions these configs match on are still in Development, and several of the components (`filter`, `signal_to_metrics`, `redaction` on logs) are alpha in Collector 0.165.

## Talking points from the current conventions

The GenAI, `openai.*`, and `mcp.*` conventions now live in [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai), split out of the main semantic conventions repository in v1.42, and they are still in Development status. Attribute names can change; pin versions, as `pyproject.toml` does.

Python GenAI instrumentation moved to [opentelemetry-python-genai](https://github.com/open-telemetry/opentelemetry-python-genai). The contrib packages such as `opentelemetry-instrumentation-openai-v2` are deprecated, and `opentelemetry-bootstrap` still installs them, so install the `-genai-*` packages explicitly.

The MCP SDK names its client spans `MCP send tools/call <tool>`, while the conventions specify `{mcp.method.name} {target}`, which is what the server side emits. The conventions also say MCP instrumentation should not create a separate span when an outer GenAI span already traces the tool call; the SDK does not detect that yet, so step 2 shows `execute_tool` wrapping `MCP send tools/call`. Both are visible on screen and make good examples of conventions and implementations converging.

## Before the session

Run every step once on the presenting machine with Jaeger open, keep a terminal with `diff -u` output ready for each step, and prepare a fallback screenshot of the step 3 trace in case OpenRouter or the network fails during the session.

## License

Apache License 2.0. See [LICENSE](LICENSE).

The Session 1 lab is by Juraci Paixão Kröhling (OllyGarden). The Session 2 additions listed above are by Severin Neumann (Bronto).

OpenTelemetry is a registered trademark and Jaeger is a trademark of The Linux Foundation. OllyGarden products are not endorsed by The Linux Foundation, the Cloud Native Computing Foundation, or the OpenTelemetry or Jaeger projects.
