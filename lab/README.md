# Instrumenting the agent

Live demo for the Packt "Agentic Observability Engineering with OpenTelemetry" workshop (2026-11-21). A bookshop support agent answers one customer question by retrieving from a catalog, calling a language model through OpenRouter, and calling two tools on a Model Context Protocol (MCP) server that runs as a separate process. The agent starts with no telemetry, and each step adds one idea until a single trace shows the whole run, across both processes, with token usage and cost.

It covers the opening 20 minutes of Juraci Paixão Kröhling's session. It stops where production work starts: once the trace exists, the next questions are about pipelines, sampling, and governance.

## Setup

You need Docker, [uv](https://docs.astral.sh/uv/), and an OpenRouter API key.

```bash
cp .env.example .env          # then set OPENROUTER_API_KEY, or export it in your shell instead
docker compose up -d          # Jaeger 2.22: UI on http://localhost:16686, OTLP/HTTP on 4318
uv sync
```

Variables already exported in your shell take precedence over `.env`. The model defaults to `deepseek/deepseek-v4-flash`; set `DEMO_MODEL` to any OpenRouter model that supports tool calling. A full run takes about five seconds and costs a fraction of a cent.

## The application

`agent_v0.py` is a plain agent loop. It searches `data/catalog.json` with keyword retrieval (`retrieval.py`), sends the excerpt and the question to the model with the MCP tools attached, executes the tool calls the model asks for, and returns the final answer. `bookshop_mcp.py` is the MCP server, started by the agent over stdio, with two tools: `check_inventory` and `get_order_status`.

The question asks about order `ORD-1044`, which does not exist. The tool fails, the model apologizes politely, and the customer gets a reasonable answer. That failure is the point: nothing in the output tells you a tool failed, and in step 0 all you have is one line on stderr.

The agent versions are separate files so each step is a small diff you can show on screen with `diff -u agent_v2.py agent_v3.py`.

## Steps

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

## Talking points from the current conventions

The GenAI, `openai.*`, and `mcp.*` conventions now live in [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai), split out of the main semantic conventions repository in v1.42, and they are still in Development status. Attribute names can change; pin versions, as `pyproject.toml` does.

Python GenAI instrumentation moved to [opentelemetry-python-genai](https://github.com/open-telemetry/opentelemetry-python-genai). The contrib packages such as `opentelemetry-instrumentation-openai-v2` are deprecated, and `opentelemetry-bootstrap` still installs them, so install the `-genai-*` packages explicitly.

The MCP SDK names its client spans `MCP send tools/call <tool>`, while the conventions specify `{mcp.method.name} {target}`, which is what the server side emits. The conventions also say MCP instrumentation should not create a separate span when an outer GenAI span already traces the tool call; the SDK does not detect that yet, so step 2 shows `execute_tool` wrapping `MCP send tools/call`. Both are visible on screen and make good examples of conventions and implementations converging.

## Before the session

Run every step once on the presenting machine with Jaeger open, keep a terminal with `diff -u` output ready for each step, and prepare a fallback screenshot of the step 3 trace in case OpenRouter or the network fails during the session.

## License

Apache License 2.0. See [LICENSE](LICENSE).

OpenTelemetry is a registered trademark and Jaeger is a trademark of The Linux Foundation. OllyGarden products are not endorsed by The Linux Foundation, the Cloud Native Computing Foundation, or the OpenTelemetry or Jaeger projects.
