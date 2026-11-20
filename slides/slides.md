---
theme: default
title: From Agent Trace to Production
info: |
  ## From Agent Trace to Production
  Governing, shaping and debugging GenAI telemetry. Session 2 of "Agentic Observability
  Engineering with OpenTelemetry", Packt, 21 Nov 2026.
colorSchema: light
transition: fade
mdc: true
class: text-left
favicon: /img/packt/p-mark.svg
fonts:
  sans: Outfit
  serif: Lexend Deca
  mono: Courier Prime
layout: waiting
headline: From Agent Trace to Production
blurb: "Governing, shaping and debugging GenAI telemetry: the agent from Session 1 goes to production, one step at a time."
name: Severin Neumann
role: Head of Community, Bronto
photo: /img/severin.jpg
---

<!--
Waiting screen, on screen during the break between the sessions.

Every screenshot in this deck comes from a real run of the lab (lab/ in the repo). Anything marked LIVE in the notes can be done live instead; the screenshot is the fallback.

Before the session, in the terminal you demo from (lab/): `export OTEL_METRICS_EXPORTER=otlp OTEL_LOGS_EXPORTER=otlp OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true`, and for the Collector `export BACKEND_ENDPOINT=https://ingestion.eu.bronto.io BACKEND_API_KEY=<key> BACKEND_DATASET=bookshop-lab`. Without the three BACKEND variables every `docker compose up` in the cues points the Collector at the local sink and Bronto gets nothing. For the terminal slides: `./demo-terminal.sh` in slides/ (needs `brew install ttyd`); it serves the lab shell on 127.0.0.1:7681 and sets the telemetry and backend variables itself from ../.env. Click into the terminal to type; click outside it before pressing a key for the next slide. Once per machine, after `docker compose up -d` in lab/: `./load-saved-runs.sh` puts the six saved runs into Jaeger under their original trace IDs, so the SAVED RUN links in the notes of failures 3 and 4 open. Time cues assume a 45-minute talk with the live demos.
-->

---
layout: cover
---

<h1>From Agent Trace to Production</h1>
<p>Governing, shaping and debugging GenAI telemetry with OpenTelemetry</p>

---
layout: about
name: Severin Neumann
role: Head of Community, Bronto
photo: /img/severin.jpg
---

## About <em>Severin</em>

- Head of Community at Bronto.
- Member of the OpenTelemetry Governance Committee.
- Long-time OpenTelemetry contributor and maintainer, focused on documentation and community.

<div class="connect">
  <div class="connect-list">
    <span class="connect-h">Questions later? Connect:</span>
    <span><b>LinkedIn</b> linkedin.com/in/severinneumann</span>
    <span><b>GitHub</b> github.com/svrnm</span>
    <span><b>Email</b> severin@bronto.io</span>
    <span><b>CNCF Slack</b> Severin Neumann</span>
  </div>
  <div class="connect-qr"><QrCode url="https://www.linkedin.com/in/severinneumann" :size="96" /><span>LinkedIn</span></div>
</div>

<style>
.connect { display: flex; align-items: center; gap: 1.2rem; margin-top: 1.1rem; padding-top: 0.9rem; border-top: 1px solid #3A3A3A; }
.connect-list { display: flex; flex-direction: column; gap: 0.15rem; font-size: 0.72rem; line-height: 1.35; }
.connect-list .connect-h { color: #5CC98F; font-size: 0.78rem; margin-bottom: 0.2rem; }
.connect-list b { display: inline-block; width: 5.6rem; font-weight: 400; color: #9A9A9A; }
.connect-qr { display: flex; flex-direction: column; align-items: center; gap: 0.25rem; font-size: 0.6rem; color: #9A9A9A; }
</style>

<!--
(0:00) Twenty seconds. One disclosure: the backend on screen later is Bronto, where I work. Everything I show is plain OTLP and works with the backend you already run.
-->

---
layout: quote
by: "Juraci, a few minutes ago"
---

Now the trace exists.<br>What you keep is <em>the next question.</em>

<!--
(0:00) This is where Juraci stopped, so this is where we start. He built the trace. This hour is about what happens to it on the way to production.
-->

---
part: Where we start
---

# Session 1 ended with one trace

<div class="tr5">
<Shot src="/img/shots/trace-normal.png" h="318px" />
<span class="co" style="top:11.9%;left:101.2%">one customer question,<br>one run</span>
<span class="br" style="top:16%;height:24.5%;left:48.8%"><span class="co">MCP handshake</span></span>
<span class="co" style="top:44%;left:48.8%">retrieval from the catalog</span>
<span class="co" style="top:50.6%;left:70.8%">model call: picks the tools</span>
<span class="br" style="top:54.6%;height:18.4%;left:73.6%"><span class="co">tool call: check_inventory</span></span>
<span class="br" style="top:74.2%;height:18.4%;left:73.6%"><span class="co">tool call: get_order_status</span></span>
<span class="co r" style="top:96.4%;right:33.5%">model call: writes the answer</span>
</div>

<p class="cap1 dim">One run across two processes, with tokens and cost on the root span, sent straight to Jaeger.</p>

<!--
(0:00) The same agent, the same trace, the same Jaeger. One customer question, a retrieval, two model calls, two tool calls into the MCP server.

Everything from here on uses his lab as he left it. Where I added something, I'll say so.
-->

<style>
.tr5 { position: relative; display: inline-block; line-height: 0; }
.tr5 .co { position: absolute; transform: translateY(-50%); background: var(--orange); color: #fff; font: 700 0.62rem/1.25 var(--sans); padding: 0.2em 0.6em; border-radius: 4px; white-space: nowrap; }
.tr5 .co::before { content: ''; position: absolute; top: 50%; left: -6px; margin-top: -5px; border: 5px solid transparent; border-left: 0; border-right: 6px solid var(--orange); }
.tr5 .co.r::before { left: auto; right: -6px; border: 5px solid transparent; border-right: 0; border-left: 6px solid var(--orange); }
.tr5 .br { position: absolute; border-left: 3px solid var(--orange); border-radius: 2px; }
.tr5 .br .co { top: 50%; left: 8px; }
</style>

---
part: Where we start
---

# From one trace to production

<div class="stp">
  <div class="stp-line" />
  <div><b>Step 5</b><i>5</i><span>A Collector in between</span></div>
  <div><b>Step 6</b><i>6</i><span>Decide what may leave</span></div>
  <div><b>Step 7</b><i>7</i><span>Metrics, budgets, caps</span></div>
  <div><b>Step 8</b><i>8</i><span>Keep the runs that matter</span></div>
  <div><b>Step 9</b><i>9</i><span>Debug four failures</span></div>
</div>

<p class="cap1">Session 1 covered steps 0 to 4. What follows extends the telemetry stack you already run; none of it is a separate AI tool.</p>

<style>
.stp { position: relative; display: grid; grid-template-columns: repeat(5, 1fr); margin: 2.2rem 1rem 1.6rem; text-align: center; }
.stp-line { position: absolute; left: 10%; right: 10%; top: 4.05rem; height: 4px; background: linear-gradient(90deg, #9FE8E4, #3F86CB); }
.stp > div:not(.stp-line) { display: flex; flex-direction: column; align-items: center; gap: 0.9rem; position: relative; }
.stp b { font-size: 1.1rem; }
.stp i { display: grid; place-items: center; width: 4.2rem; height: 4.2rem; border-radius: 50%; color: #fff; font: 700 1.6rem var(--sans); font-style: normal; }
.stp > div:nth-child(2) i { background: #9FE8E4; } .stp > div:nth-child(3) i { background: #74D8D6; }
.stp > div:nth-child(4) i { background: #66C5EA; } .stp > div:nth-child(5) i { background: #52ACD3; }
.stp > div:nth-child(6) i { background: #3F86CB; }
.stp span { font-size: 0.95rem; line-height: 1.35; max-width: 9rem; }
</style>

<!--
(0:01) Juraci's demo ran from step 0, no telemetry, to step 4, tokens and cost. We continue the numbering.

Each step has the same shape: first why, on a real screenshot of what's wrong. Then what and how. Then the proof. And each step ends with one thing you can do on Monday.

The claim for the whole hour, and one of the takeaways you were promised: agent observability is an extension of the stack you have. Same Collector, same signals, same alerts. If you also use an eval or LLM tool, it can sit behind the same Collector as one more destination.
-->

---
layout: section
section: "Step 5: Connect"
---

---
part: Step 5 · Connect · why
---

# Every process talks to the backend

<div class="wire">
  <div class="col"><span class="box">bookshop-agent</span><span class="box">bookshop-mcp</span><span class="box ghost">the next agent</span><span class="box ghost">the next MCP server</span></div>
  <div class="arrows"><i/><i/><i class="g"/><i class="g"/></div>
  <div class="col"><span class="box be">backend</span></div>
</div>

<p class="cap1">To change where telemetry goes or what it may contain, you redeploy every process, in every language.</p>

<style>
.wire { display: grid; grid-template-columns: 16rem 1fr 14rem; align-items: stretch; margin: 1.6rem 2rem 1.2rem; }
.wire .col, .wire .arrows { display: grid; grid-auto-rows: 1fr; gap: 0.7rem; }
.wire .box { font-family: var(--mono); font-size: 1rem; padding: 0.6rem 1rem; border-radius: 10px; background: var(--surface); text-align: center; }
.wire .box.ghost { background: transparent; border: 1.5px dashed var(--border); color: var(--ink-dim); }
.wire .box.be { background: var(--blue-soft); display: flex; align-items: center; justify-content: center; }
.wire .arrows { padding: 0 0.5rem 0 0.4rem; }
.wire .arrows i { position: relative; display: block; color: var(--ink); background: linear-gradient(currentColor, currentColor) left center / calc(100% - 9px) 2.5px no-repeat; }
.wire .arrows i.g { color: var(--border); background: repeating-linear-gradient(90deg, currentColor 0 8px, transparent 8px 14px) left center / calc(100% - 9px) 2px no-repeat; }
.wire .arrows i::after { content: ''; position: absolute; right: 0; top: 50%; margin-top: -6px; border: 6px solid transparent; border-right: 0; border-left: 10px solid currentColor; }
</style>

<!--
(0:02) WHY. In Session 1 the agent and its MCP server each sent straight to Jaeger. That's fine for a demo.

In production it means every decision about telemetry lives in every process: where it goes, which credentials, what's allowed to leave, what gets sampled. Two processes today. Next quarter there's a second agent in TypeScript and three MCP servers someone else wrote.
-->

---
part: Step 5 · Connect · how
---

# Put one Collector in between

<div class="cfg"><div class="cfg-h"><b>collector/step5-connect.yaml</b><span>shortened: no auth header</span></div>

```yaml
receivers:
  otlp:
    protocols:
      http: { endpoint: 0.0.0.0:4318 }   # the port the agent already sends to

exporters:
  otlp_grpc/jaeger: { endpoint: jaeger:4317 }
  otlp_http/backend:                     # any OTLP backend
    endpoint: ${env:BACKEND_ENDPOINT}

service:
  pipelines:
    traces:  { receivers: [otlp], exporters: [otlp_grpc/jaeger, otlp_http/backend] }
    metrics: { receivers: [otlp], exporters: [otlp_http/backend] }
    logs:    { receivers: [otlp], exporters: [otlp_http/backend] }
```

</div>

<style>
.cfg .slidev-code { font-size: 0.78rem !important; line-height: 1.5 !important; }
</style>

<!--
(0:02) HOW.

LIVE on the next slide.

For anyone who hasn't run a Collector: receivers take telemetry in, exporters send it out, a pipeline connects them per signal. Processors go in between; there are none yet.

The Collector takes port 4318, the port the agent already used. So the agent doesn't change, not even an environment variable.

Three signals, not one. Session 1 was about traces. Metrics and logs come through the same door, and we'll need both.

On screen the auth header and the TLS setting are left out; the file has them.
-->

---
part: Step 5 · Connect · live
---

# Live: one run through the Collector

<Term type="connect" runs="switches the Collector to the step 5 config, then runs the agent once" />

<Jump :to="[{ label: 'Jaeger', url: 'http://localhost:16686/search?service=bookshop-agent&lookback=1h&limit=20' }, { label: 'Bronto', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+15+minutes&services=bookshop-agent' }]" />

<!--
LIVE (about 2 min). Type `connect`. It prints the two real commands before it runs them: the `docker compose` line that starts the Collector with step5-connect.yaml, and the agent run, unchanged from Session 1.

Then the Jaeger tab on the right border: Find Traces, open the run, open one chat span and one execute_tool span. Then the Bronto tab: the same trace, the same spans.

If the terminal is empty, ttyd is not running: `./demo-terminal.sh` in slides/. Fallback: the next slide is the screenshot of this.
-->

---
part: Step 5 · Connect · proof
---

# The same trace now arrives in two places

<div class="pair">
  <div><span class="chip">Jaeger</span><Shot src="/img/shots/jaeger-same.png" /></div>
  <div><span class="chip">Bronto · or any OTLP backend</span><Shot src="/img/shots/bronto-trace.png" h="272px" /></div>
</div>

<p class="cap1 dim">Trace 8e8886ac in both. The agent is unchanged, and its telemetry is now configured in one file.</p>

<style>
.pair { display: grid; grid-template-columns: 1.25fr 1fr; gap: 1.2rem; align-items: start; margin-top: 0.3rem; }
.pair .chip { display: block; }
.pair > div:first-child :deep(.shot), .pair > div:first-child :deep(img) { width: 100%; }
</style>

<!--
(0:06) PROOF. The same run in Jaeger, as before, and in a second backend. Today that's Bronto; it's whatever speaks OTLP.

That's the vendor-neutral part of the promise: the agent knows about the Collector, the Collector knows about backends.
-->

---
part: Step 5 · Connect
---

# In production, Collectors run in two places

<img class="dg" src="/img/diagrams/topology.svg" alt="" />

<p class="cap1 dim honest">For mixed frameworks, the <code>gen_ai_normalizer</code> processor (alpha) maps OpenInference and OpenLLMetry spans to <code>gen_ai.*</code>.</p>

<p class="mon"><b>Monday</b> Point one agent at a Collector and change nothing else.</p>

<style>
.dg { width: 100%; height: auto; margin-top: 0.2rem; color: var(--ink); }
</style>

<!--
(0:06) The honest call-out. In the lab there's one Collector. In production, where it runs is a real decision, because two of the jobs in this hour pull in opposite directions.

Masking wants to happen as close to the agent as possible: until then, content travels in plain text. Tail sampling wants a central place, because it has to see every span of a run before it decides.

So most setups end up with both: a Collector next to the workload and a gateway tier. We won't build that today. Know that it's there.

And the takeaway about comparable telemetry across frameworks: Session 1 used the OpenTelemetry GenAI conventions. If some of your agents emit OpenInference or OpenLLMetry attributes, there's a processor in the Collector's contrib distribution that maps them. It exists in the current release, 0.165, and it's marked alpha. I haven't run it in this lab.
-->

---
layout: section
section: "Step 6: Govern"
---

---
part: Step 6 · Govern · why
---

# This is now in your trace backend

<Shot src="/img/shots/content-raw.png" :marks="[{ x: 0.8, y: 85.5, w: 98.4, h: 13.5 }]" />

<p class="cap1 dim">A name, an email address and a card number. Everyone with backend access can read them for as long as traces are kept.</p>

<!--
(0:08) WHY. Juraci's last content slide: one switch decides what leaves the process. This is that switch turned on, in Jaeger's GenAI view. A real run from the lab.

A customer wrote a normal support message. Her name, her email address, and because people do this, her card number. It's now a span attribute.

Whoever can open the trace backend can read it. It's kept as long as traces are kept. And it went there in plain text.
-->

---
part: Step 6 · Govern
---

# People still want the content, so ask who wrote it

<Shot src="/img/shots/content-raw.png" :marks="[{ x: 0.8, y: 10.6, w: 98.4, h: 19, tone: 'ok' }, { x: 0.8, y: 43, w: 98.4, h: 39, tone: 'ok' }, { x: 0.8, y: 86, w: 98.4, h: 13, tone: 'bad' }]" />

<p class="cap1">Your system's text is close to code. <b class="them">The customer's two lines need a decision.</b></p>

<style>
.them { color: #B23F14; }
.slidev-layout .cap1 { color: var(--green-ink); font-weight: 700; }
</style>

<!--
(0:08) There's real appetite for prompts and responses, and it's justified: nothing else tells you why the model did what it did. We'll see that in step 9.

So the question isn't yes or no. The first useful question is who wrote the text.

A system prompt, a tool description, a retrieved catalog entry: your system wrote those. They're close to code. If your agents mostly talk to other systems, storing content is a much smaller problem.

A person's message is different. It's theirs, it's unpredictable, and data protection rules apply to it: a purpose, a retention limit, deletion on request, and a contract with whoever stores it.

Look at the screenshot: SYSTEM is yours. USER is half yours, the catalog excerpt, and half the customer's. The conventions don't separate those two for you.
-->

---
part: Step 6 · Govern
---

# Where the content can travel

<img class="dg" src="/img/diagrams/content-modes.svg" alt="" />

<p class="cap1 dim honest">Avoid turning it on everywhere by default, and avoid relying on masking alone.</p>

<style>
.dg { width: 100%; height: auto; margin-top: 0.1rem; color: var(--ink); }
.slidev-layout .cap1 { margin-top: 0.4rem; font-size: 1.05rem; }
</style>

<!--
(0:10) All four were run on Juraci's lab; the sizes are for his demo question, as OTLP JSON.

Off is the OpenTelemetry default. Check your framework: several popular agent frameworks default to on.

On for a slice is the honest middle: you turn it on where someone decided it's worth it.

On log events is the one people don't know. Same switch, value EVENT_ONLY: the spans stay clean, and the conversation arrives as log events that carry the trace and span ID. Now content can go to a different place, with different access and a shorter retention, and you can still jump from a trace to it. In the lab this worked with zero code changes; it covers the model calls, not tool arguments.

One catch, tested this week: on log events the messages are structured, and the redaction processor two slides on only masks plain strings. An email inside a content event passed through it unmasked. If you take this route, mask in the application or with OTTL on the logs pipeline.

There's a fifth option in the conventions: store content elsewhere and keep only a reference on the span. The library has a hook for it. I couldn't get it to work from configuration alone in this lab, so I'm not showing it.
-->

---
part: Step 6 · Govern · how
---

# The Collector enforces the opt-in

<div class="cfg"><div class="cfg-h"><b>collector/step6-govern.yaml</b><span>filter</span></div>

```yaml
filter/opt-in:      # content events only from services that were approved
  log_conditions:
    - log.event_name == "gen_ai.client.inference.operation.details"
      and resource.attributes["bookshop.content.approved"] != "true"
```

</div>

<p class="cap1">A developer can still flip the switch, but content events only leave the Collector for services marked as approved. Content written onto spans needs its own rule.</p>

<style>
.cfg .slidev-code { font-size: 0.82rem !important; line-height: 1.6 !important; }
</style>

<!--
(0:11) HOW, part one of three. The agenda promised three processors: filter, redaction, transform. Each gets one job.

Filter drops things. Here: content events from any service whose resource doesn't say it was approved. "Capture is an explicit opt-in" stops being a convention between teams and becomes a rule in one place.

Proved in the lab: without the attribute, zero content events arrive. With it, they do.

Be honest about the mark: in the lab it is a resource attribute the service sets itself, which is self-approval. In production the platform sets it, or the rule is a list of service names in the Collector config.

The same processor also drops noise: the lab removes a one-span trace the MCP handshake leaves behind.
-->

---
part: Step 6 · Govern · how
---

# Mask emails and card numbers

<div class="cfg"><div class="cfg-h"><b>collector/step6-govern.yaml</b><span>redaction</span></div>

```yaml
redaction/pii:
  allow_all_keys: true
  blocked_values:
    - '[\w.+-]+@[\w-]+\.[\w.]+'      # email addresses
    - '\b(?:\d[ -]?){13,16}\b'       # card numbers
  summary: info                      # counts what it masked, per span
```

</div>

<p class="cap1 dim">It searches every string attribute on spans: prompts, answers, tool arguments. It does not reach inside content sent as log events.</p>

<style>
.cfg .slidev-code { font-size: 0.82rem !important; line-height: 1.6 !important; }
</style>

<!--
(0:12) Part two: the redaction processor. Two patterns, an email address and a card number. It searches every string attribute, so on spans it reaches prompts, completions and tool arguments alike. On log events the content is structured, not a string, and this processor passes it through untouched. I tested that.

LIVE on the next slide.

`summary: info` adds a count of what was masked to every span it touched. Chart that by service and you see which team just started sending something they shouldn't.

Next slide: what it did to the screenshot you just saw.
-->

---
part: Step 6 · Govern · live
---

# Live: a customer message through the redaction

<Term type="govern" runs="switches to the step 6 config and sends a message with a name, an email and a card number" />

<Jump :to="[{ label: 'Jaeger', url: 'http://localhost:16686/search?service=bookshop-agent&lookback=1h&limit=20' }]" />

<!--
LIVE optional (about 1.5 min). Type `govern`. Jaeger tab: open the run, the first chat span, GenAI view, input messages. Email and card masked, the name untouched, and the ISBNs in the catalog excerpt masked too.

Skip this slide if time is short: the next one shows the same result as a screenshot.
-->

---
part: Step 6 · Govern · proof
---

# What redaction did, and what it got wrong

<Shot src="/img/shots/content-masked.png" :marks="[{ x: 11.8, y: 86.5, w: 9, h: 6.5, label: 'name: still here' }, { x: 24, y: 86.5, w: 5.4, h: 6.5, label: 'email: masked' }, { x: 52.2, y: 92.5, w: 4.4, h: 6.5, label: 'card: masked', at: 'right' }, { x: 37.6, y: 48.5, w: 10, h: 6.5, label: 'ISBN: masked by mistake' }]" />

<p class="cap1 honest">The name is still there, and every ISBN is gone because 13 digits look like a card number.</p>

<!--
(0:15) PROOF, same customer message, after the Collector. The email is masked. The card number is masked. That's the promise kept.

Now look closer, because this is a real result and I didn't stage it.

"Maria Lopez" is still there. A pattern can't find a name.

And every ISBN is gone, here in the catalog excerpt and further down the trace in the tool call arguments. An ISBN is thirteen digits with dashes. My card-number pattern ate it. The redaction just destroyed the one value I'd need to debug an inventory problem.

So: masking in the Collector is a backstop. It catches the obvious, it misses names, and a sloppy pattern costs you evidence. The controls that work are upstream: don't capture what you don't need, keep IDs instead of personal data, and if you need names found, do entity detection in the application before export.
-->

---
part: Step 6 · Govern · how
---

# Drop tool results from tool spans, and cap sizes

<div class="cfg"><div class="cfg-h"><b>collector/step6-govern.yaml</b><span>transform</span></div>

```yaml
transform/content:
  trace_statements:
    - delete_key(span.attributes, "gen_ai.tool.call.result")   # may hold other people's data
    - truncate_all(span.attributes, 2048)                      # a prompt is not a blob store
```

</div>

<p class="cap1 dim honest">The next model call repeats the tool result in its input, and a hard cut can break the JSON. These limit size; they are not privacy controls.</p>

<p class="mon"><b>Monday</b> Find out whether content capture is on anywhere, and who approved it.</p>

<style>
.cfg .slidev-code { font-size: 0.78rem !important; line-height: 1.7 !important; }
</style>

<!--
(0:16) Part three: transform. It rewrites telemetry with a small expression language, OTTL.

Two jobs here. Delete tool results: a tool can return another customer's record, and you rarely need the full result to debug. And cap the size of every value, because conversations grow with every turn.

Two limits I found in the lab's own traces. The tool result is deleted from the tool span, but the next model call carries it again inside its input messages, so the other customer's record is still in the trace. And the cap cuts a JSON string at 2,048 bytes, which leaves it unparseable; what gets cut is the newest part of the conversation. So this controls size. It does not control privacy.

It's also where you rename attributes when the conventions change, in one place. They will change: everything GenAI in OpenTelemetry is still marked Development.

Monday. Not "build this pipeline". First find out what you're sending today: search your deployments for the content capture variable, under both names (`..._CAPTURE_MESSAGE_CONTENT` today, `..._CAPTURE_CONTENT` in the current spec), and check your framework's default.
-->

---
layout: section
section: "Step 7: Measure"
---

---
part: Step 7 · Measure · why
---

# A trace answers one run

<div class="onemany">
  <div><div class="mini"><i style="width:100%"/><i style="width:38%;margin-left:6%"/><i style="width:8%;margin-left:46%"/><i style="width:48%;margin-left:52%"/></div><h3>One run</h3><p>Why did this take 17 seconds?</p><p class="v ok">The trace.</p></div>
  <div><div class="many"><i v-for="i in 96" :key="i" /></div><h3>All runs</h3><p>What did yesterday cost? Is one running away right now?</p><p class="v no">Not the trace.</p></div>
</div>

<p class="cap1 dim honest">Summing the token attribute over all spans counts every token at least twice.</p>

<style>
.onemany { display: grid; grid-template-columns: 1fr 1fr; gap: 2.4rem; margin-top: 0.8rem; }
.onemany h3 { font-size: 1.4rem !important; margin: 0.7rem 0 0.2rem !important; }
.onemany p { margin: 0; font-size: 1.1rem; line-height: 1.4; }
.onemany .v { font-weight: 700; margin-top: 0.3rem; } .onemany .ok { color: var(--green-ink); } .onemany .no { color: #B23F14; }
.mini, .many { height: 6.2rem; background: var(--surface); border-radius: 12px; padding: 0.8rem 1rem; }
.mini { display: flex; flex-direction: column; justify-content: space-between; }
.mini i { display: block; height: 0.7rem; border-radius: 3px; background: var(--blue); }
.many { display: grid; grid-template-columns: repeat(24, 1fr); gap: 5px; align-content: center; }
.many i { display: block; aspect-ratio: 1; border-radius: 3px; background: #BDBDBD; }
.many i:nth-child(17), .many i:nth-child(41), .many i:nth-child(78) { background: var(--orange); }
</style>

<!--
(0:17) WHY. Session 1 put tokens and cost on the trace. That answers questions about one run.

The questions that come with production are about all runs. Spend, trends, something going wrong right now. Those are metrics questions.

The shortcut people take: sum the token attribute across spans in the trace backend. The agent span carries the run's total, and each model call span carries its share. The conventions recommend both. Sum everything and your cost report is double. If your vendor's token chart looks high, this is the first thing to check.
-->

---
part: Step 7 · Measure
---

# The instrumentation already emits metrics

<div class="cfg sw"><div class="cfg-h"><b>environment</b><span>Session 1 had this set to none</span></div>

```bash
OTEL_METRICS_EXPORTER=otlp
```

</div>

<div class="rows m7">
  <div><b class="mono">gen_ai.client.token.usage</b><span>tokens, per model, input and output</span></div>
  <div><b class="mono">gen_ai.client.operation.duration</b><span>latency, per operation and model</span></div>
  <div><b class="mono">gen_ai.execute_tool.duration</b><span>latency, per tool, with the error type</span></div>
  <div><b class="mono">gen_ai.invoke_agent.duration</b><span>latency, per agent</span></div>
</div>

<style>
.sw { width: 60%; } .sw .slidev-code { font-size: 0.9rem !important; }
.m7 { margin-top: 0.9rem; } .m7 > div { grid-template-columns: 22rem 1fr; font-size: 1.02rem; padding: 0.5rem 0; }
.m7 b { font-size: 0.9rem; }
</style>

<!--
(0:18) WHAT, and this surprised me when I ran it. Juraci's lab already produces these. The GenAI instrumentation emits metrics that follow the conventions; the lab just had the metrics exporter set to none.

Turn it on and you get tokens per model, and latency per operation, per tool and per agent. That's most of "per model, tool and agent" from the agenda, with no pipeline work and no double counting: these are measured once, at the call.

So the order is: use what the instrumentation gives you first.

Honest note: these names are moving. On the conventions' main branch the token metric is being replaced by separate counters. The duration metric is splitting too, with separate ones for inference and retrieval. Pin your instrumentation version, and expect to rename.
-->

---
part: Step 7 · Measure · how
---

# Tokens and cost per run come from spans

<div class="cfg"><div class="cfg-h"><b>collector/step7-measure.yaml</b><span>connector, shortened</span></div>

```yaml
signal_to_metrics:
  spans:
    - name: bookshop.run.tokens          # a histogram: tokens per run
      conditions: ['attributes["gen_ai.operation.name"] == "invoke_agent"']
      histogram:
        value: Int(attributes["gen_ai.usage.input_tokens"])
             + Int(attributes["gen_ai.usage.output_tokens"])
    - name: bookshop.run.cost            # what the gateway billed
      conditions: ['attributes["gen_ai.operation.name"] == "invoke_agent"']
      sum: { value: Double(attributes["bookshop.llm.cost_usd"]) }
```

</div>

<p class="cap1 dim">Only the run span knows the whole run. Each metric reads one span type, so nothing is counted twice.</p>

<style>
.cfg .slidev-code { font-size: 0.72rem !important; line-height: 1.55 !important; }
</style>

<!--
(0:19) HOW, for what's missing. The instrumentation's metrics know calls. They don't know the run: how many tokens did this whole customer request use, and what did it cost.

That lives on the run span, the invoke_agent span from Session 1. A connector turns spans into metrics: here, a histogram of tokens per run, and the billed cost.

Each metric reads one span type. That's the double count from two slides ago, solved by construction.

One rule for step 8: these are taken before any sampling, so they count every run.
-->

---
part: Step 7 · Measure
---

# What you can and can't say about cost

<div class="rows c7">
  <div><b>No standard yet</b><span>OpenTelemetry has no cost attribute yet, so use your own name for it.</span></div>
  <div><b>Per run, per agent</b><span>What your gateway billed.</span></div>
  <div><b>Per model</b><span>Tokens per model, times a price list you keep.</span></div>
  <div class="no"><b>Per tool</b><span>Not a real number, because model calls spend the tokens and tools don't.</span></div>
</div>

<style>
.c7 > div { grid-template-columns: 13rem 1fr; padding: 0.95rem 0; font-size: 1.2rem; }
.c7 .no b { color: #B23F14; }
</style>

<!--
(0:20) The agenda says cost per model, tool and agent. Here's what's true.

There's no cost attribute in the conventions. Juraci showed it: his lab stores what the gateway billed under an application name.

Per run and per agent is the solid one, if a gateway tells you what it charged.

Per model is arithmetic: tokens per model you already have, multiply by prices. Someone has to keep that price list current.

Per tool, I'd be selling you something if I drew that chart. A tool call costs time, not tokens. What you can say is which runs used which tools and what those runs cost. That's attribution, and it's your choice how to do it.
-->

---
part: Step 7 · Measure · proof
---

# One hour of the lab in four charts

<Jump :to="[{ label: 'Bronto: metrics', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/metrics?timeRange=Last+1+hour&queries=%5B%7B%22committedFilter%22%3A%22%22%2C%22groupKeys%22%3A%5B%5D%2C%22metricId%22%3A%22b24c67e1-a5ad-3b50-b2e7-46954760f22a%22%2C%22name%22%3A%22A%22%2C%22statFunction%22%3A%22average%22%7D%5D' }]" />

<div class="quad">
  <div><span class="chip">tokens, in and out</span><Shot src="/img/shots/bronto-tokens-type.png" h="150px" /></div>
  <div><span class="chip">tokens per run · from spans</span><Shot src="/img/shots/bronto-run-tokens.png" h="150px" /></div>
  <div><span class="chip">latency per tool</span><Shot src="/img/shots/bronto-tool-latency.png" h="150px" /></div>
  <div><span class="chip">retrieval latency</span><Shot src="/img/shots/bronto-retrieval.png" h="150px" /></div>
</div>

<p class="cap1 dim">About 90 runs. Three charts come from the instrumentation's own metrics and one from spans.</p>

<style>
.quad { display: grid; grid-template-columns: 1fr 1fr; gap: 0.25rem 1.4rem; margin-top: 0; justify-items: start; }
.quad .chip { margin-bottom: 0.1rem; font-size: 0.68rem !important; display: block; }
.slidev-layout .cap1 { margin-top: 0.4rem; font-size: 1rem; }
</style>

<!--
(0:21) PROOF. Four charts from one hour of the lab, about 90 runs, in Bronto's metrics explorer. Nothing exotic.

LIVE optional (under 1 min): Bronto, Metrics: tokens per run, token usage by `gen_ai.token.type`, tool duration by `gen_ai.tool.name`. Charts only show runs from the last hours, so generate a few runs before the session.

Top left, tokens in and out: the instrumentation's own metric. Top right, tokens per run: the one we derived from the run span; the tall bars are the loops. Bottom left, latency per tool. Bottom right, retrieval latency: five spikes at eight seconds, and we'll meet those in step 9.

If you build one view on Monday, build these four.
-->

---
part: Step 7 · Measure
---

# A budget alert comes after the tokens are spent

<Jump :to="[{ label: 'Bronto: monitor', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/monitors/lists?activeMonitorId=9c81d708-3e21-40db-b506-415acde45efc&timeRange=Last+4+hours' }]" />

<p class="rule"><b>monitor</b><span class="mono">P99(bookshop.run.tokens) over 5 minutes &gt; 3,000</span></p>

<div class="al">
  <Shot src="/img/shots/bronto-alert-chart.png" h="215px" />
  <div class="capline"><span class="mono">for _ in range(5):</span><span>The line in Session 1's agent that stopped the run. Without it, there is no upper bound.</span></div>
</div>
<Shot src="/img/shots/bronto-alert-events.png" h="62px" />

<p class="mon"><b>Monday</b> Add a budget alert on tokens per run and a hard cap in the agent or gateway.</p>

<style>
.al { display: grid; grid-template-columns: auto 1fr; gap: 1.6rem; align-items: center; margin-bottom: 0.5rem; }
.al .capline { grid-template-columns: 1fr; gap: 0.7rem; justify-items: start; margin-top: 0; }
.rule { display: flex; gap: 0.8rem; align-items: center; margin: 0 0 0.4rem; font-size: 0.85rem; }
.rule b { background: var(--orange); color: #fff; padding: 0.1rem 0.6rem; border-radius: 999px; font-size: 0.75rem; }
.capline { display: grid; grid-template-columns: auto 1fr; gap: 1.2rem; align-items: center; margin-top: 1rem; font-size: 0.95rem; line-height: 1.35; }
.capline .mono { background: var(--code-bg); color: #fff; padding: 0.35rem 0.8rem; border-radius: 8px; font-size: 0.95rem; }
</style>

<!--
(0:22) Budgets and alerts that catch runaway agents. This is a real monitor in the backend, on the metric from two slides ago: tokens per run, 99th percentile over five minutes, above 3,000.

And this is it firing, this morning. A run got stuck re-checking an order and used about 4,600 tokens; a normal run uses about 1,600. The loop ended at 09:13, the alert opened at 09:15. We'll open that run in step 9.

Two honest limits. A percentile works at lab volume; with real traffic, alert on the count of runs above the budget instead. And the metric comes from the run span, which only exists when the run ends. For a run that is still burning, the signal is the rate of the instrumentation's own token metric.

So the alert arrives after the tokens are spent. What stopped this run was one line in Juraci's agent: a loop that gives up after five rounds. Without that line there's no upper bound.

So: alerts are for knowing. Caps are for stopping. Put a cap where it can't be forgotten: a maximum number of rounds in the agent, a budget per key at the gateway.
-->

---
layout: section
section: "Step 8: Sample"
---

---
part: Step 8 · Sample · why
---

# Agents produce a lot of telemetry

<div class="vol">
  <div><span class="bignum">14</span><span>spans for one question</span></div>
  <div><span class="bignum">10.8 KB</span><span>per run, content off</span></div>
  <div><span class="bignum">18.2 KB</span><span>per run, content on</span></div>
  <div><span class="bignum">×3</span><span>the tokens when a run loops</span></div>
</div>

<p class="cap1 dim">This is one short question with two tool calls. Each model call repeats the conversation so far, so long conversations grow faster than linearly.</p>

<style>
.vol { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.4rem; margin: 2rem 0 1.4rem; }
.vol > div { display: flex; flex-direction: column; gap: 0.5rem; border-top: 3px solid var(--orange); padding-top: 0.8rem; }
.vol .bignum { font-size: 2.6rem; }
.vol span:last-child { font-size: 1rem; color: var(--ink-dim); }
</style>

<!--
(0:23) WHY. Numbers from the lab, for Juraci's one-question demo, as the Collector receives them.

Fourteen spans for one customer question. About eleven kilobytes with content off, eighteen with it on. A run that loops is twenty-nine spans and three times the tokens. The sizes are OTLP JSON for one run; on the wire as protobuf it is less.

This is a small agent. A real support conversation has many turns, and each model call carries the conversation so far, so content doesn't grow in a straight line.

Multiply by your traffic. At some point someone asks whether you need to keep all of it.
-->

---
part: Step 8 · Sample
---

# What survives when you keep less

<div class="opts">
  <div><OptionDots mode="all" /><h3>Keep everything</h3><p>Nothing is lost, and you pay for storage.</p></div>
  <div><OptionDots mode="head" /><h3>Head sampling</h3><p>Cheap, but it can't know which runs matter.</p></div>
  <div class="pick"><OptionDots mode="tail" /><h3>Tail sampling</h3><p>Keeps what a rule picked, at the cost of memory and upkeep.</p></div>
  <div><OptionDots mode="lean" /><h3>Less per run</h3><p>Every run without its content, so you lose the why.</p></div>
</div>

<p class="cap1 dim"><i class="k" /> marks the runs you will need later. Ask first whether you need to sample at all.</p>

<style>
.opts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; margin-top: 0.6rem; }
.opts h3 { font-size: 1.15rem !important; margin: 0.7rem 0 0.2rem !important; }
.opts .pick h3 { color: var(--green-ink); }
.opts p { margin: 0; font-size: 0.95rem; line-height: 1.35; color: var(--ink-dim); }
.cap1 .k { display: inline-block; width: 0.8rem; height: 0.8rem; border-radius: 3px; background: var(--orange); vertical-align: -1px; margin-right: 0.3rem; }
</style>

<!--
(0:24) Before the how: there are four answers to "too much data", and sampling is only two of them.

Keep everything. Legitimate, and the first one to consider. Agent runs are often low volume and high value. Whether it's affordable is a pricing question. Disclosure again: that's the case my employer makes, storage priced so that you don't have to choose. Other backends make it too. Do the arithmetic for yours.

Head sampling: decide at the start of the run. Simple, stateless, and blind.

Tail sampling: decide at the end. It's what's recommended for agents, and it's what the agenda promised, so we'll build it. It has real costs, and I'll show them.

Keep less per run: drop the content, keep the structure. That was step 6.

They combine. A common result: every run without content, plus content for the runs tail sampling picks.
-->

---
part: Step 8 · Sample
---

# Why head sampling loses the interesting runs

<div class="ht">
  <div class="row"><span class="lbl">Head</span><i class="dec">decide</i><div class="bar" /><span class="knows">knows: who is asking, not how it went</span></div>
  <div class="row"><span class="lbl">Tail</span><div class="bar" /><i class="dec">decide</i><span class="knows">knows: duration, tokens, tools, errors</span></div>
</div>

<p class="cap1">An agent's failures are rare, and they look like every other run when they start.</p>

<style>
.ht { margin: 2.2rem 0 1.6rem; display: flex; flex-direction: column; gap: 1.6rem; }
.ht .row { display: grid; grid-template-columns: 5rem auto 22rem auto 1fr; align-items: center; gap: 0.8rem; font-size: 1.15rem; }
.ht .row:first-child { grid-template-columns: 5rem auto 22rem 1fr; }
.ht .row:last-child { grid-template-columns: 5rem 22rem auto 1fr; }
.ht .lbl { font-weight: 700; }
.ht .bar { height: 1.6rem; border-radius: 5px; background: var(--blue-soft); }
.ht .dec { font-style: normal; font-weight: 700; font-size: 0.85rem; background: var(--orange); color: #fff; padding: 0.3rem 0.7rem; border-radius: 999px; }
.ht .knows { color: var(--ink-dim); font-size: 1rem; }
</style>

<!--
(0:25) One picture. Head sampling decides before the run has done anything. Keep ten percent, and you keep ten percent of the failures too, by luck.

For a web request that's acceptable: failures are frequent enough that a tenth of them is plenty.

For agents it isn't. The runs you need are rare, and at the start they're indistinguishable from the rest. Same question, same first span. The loop, the slow retrieval, the odd tool sequence: all of that is only known at the end.
-->

---
part: Step 8 · Sample · how
---

# Tail sampling decides after the run

<div class="cfg"><div class="cfg-h"><b>collector/step8-sample.yaml</b><span>tail_sampling, shortened</span></div>

```yaml
tail_sampling:
  decision_wait: 30s          # longer than your longest normal run
  decision_wait_after_root_received: 2s
  policies:
    - { name: errors,    type: status_code,       status_code: { status_codes: [ERROR] } }
    - { name: expensive, type: numeric_attribute,
        numeric_attribute: { key: gen_ai.usage.input_tokens, min_value: 3000 } }
    - name: unusual-tools     # any tool sequence that isn't the usual one
      type: ottl_condition
      ottl_condition:
        span:
          - 'attributes["bookshop.run.tools"] != nil and not IsMatch(
             attributes["bookshop.run.tools"], "^check_inventory get_order_status $")'
```

</div>

<p class="cap1 dim">Two more in the file: <code>slow-retrieval</code> looks at one slow step, and <code>failed-check</code> is for step 9. Any matching policy keeps the run.</p>

<style>
.cfg .slidev-code { font-size: 0.66rem !important; line-height: 1.5 !important; }
</style>

<!--
(0:26) HOW. The four from the agenda: errors, slow, expensive, unusual tool usage. The file has a fifth for step 9. A run is kept if any one matches.

Errors and expensive are built in. Expensive reads the input tokens on the run span, which is where the cost of a loop shows.

Slow: not "the run took long". Model calls vary so much that a threshold on total duration is noisy; in the lab normal runs took between 4 and 17 seconds. So the policy looks at one step, the retrieval.

Unusual tools needs one thing from the agent, and it's one line added to Juraci's agent: the run span records which tools were called, in order. Then "unusual" is any sequence that isn't the usual one.

Metrics come off the pipeline before this processor. The dashboard from step 7 still counts every run.

Two things the lab leaves out on purpose. No random baseline: in production keep a few percent of normal runs too, or you have nothing to compare against. And the unusual-tools rule allows exactly one sequence; with more than one valid path it needs a list, or it keeps nearly everything.
-->

---
part: Step 8 · Sample · proof
---

# Seven lab runs through the sampler

<table class="kd">
  <thead><tr><th></th><th>Run</th><th>Input tokens</th><th>Tools called</th><th>Kept by</th></tr></thead>
  <tbody>
    <tr class="d"><td>dropped</td><td>normal</td><td>1,430</td><td>inventory, order</td><td></td></tr>
    <tr class="k"><td>kept</td><td>slow retrieval</td><td>1,407</td><td>inventory, order</td><td>slow-retrieval</td></tr>
    <tr class="k"><td>kept</td><td>loop</td><td>4,210</td><td>inventory, order ×5</td><td>expensive, unusual-tools</td></tr>
    <tr class="k"><td>kept</td><td>no order number ×3</td><td>~1,400</td><td>inventory only</td><td>unusual-tools</td></tr>
    <tr class="d w"><td>dropped</td><td>no order number</td><td>1,386</td><td>inventory, order</td><td>nothing: it looks normal</td></tr>
  </tbody>
</table>

<p class="cap1 dim">Jaeger sits before the sampler and saw all seven; the backend received five.</p>

<style>
.kd { width: 100%; border-collapse: collapse; font-size: 1.05rem; margin-top: 0.8rem; }
.kd th { text-align: left; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-dim); padding: 0.3rem 0.7rem; border-bottom: 1.5px solid var(--ink); }
.kd td { padding: 0.6rem 0.7rem; border-bottom: 1px solid var(--border); }
.kd td:first-child { font-weight: 700; font-size: 0.85rem; text-transform: uppercase; }
.kd .k td:first-child { color: var(--green-ink); } .kd .d td:first-child { color: var(--ink-dim); }
.kd .d td { color: var(--ink-dim); }
.kd .w td { background: var(--orange-soft); color: #B23F14; }
</style>

<!--
(0:27) PROOF, a real result, unedited. Seven runs through the pipeline.

LIVE on the next slide.

The normal run is dropped. Good.

The slow one is kept by the retrieval rule. The loop by two rules. Three runs where the customer didn't give an order number and the agent skipped the order tool are kept as unusual.

And the last row. Same question, no order number. This time the agent did call the order tool. Normal tokens, normal tools, no error. Dropped.

Remember that row. It's the worst run on this slide, and step 9 opens it.
-->

---
part: Step 8 · Sample · live
---

# Live: seven runs, and what the sampler keeps

<Term type="sample" runs="switches to the step 8 config and starts seven runs at once: one normal, one slow, one loop, four without an order number" />

<Jump :to="[{ label: 'Jaeger: all runs', url: 'http://localhost:16686/search?service=bookshop-agent&lookback=1h&limit=20' }, { label: 'Bronto: kept runs', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+5+minutes&services=bookshop-agent' }]" />

<!--
LIVE optional (about 1 min, plus half a minute for the sampler to decide). Type `sample`. Jaeger sits before the sampler and shows all seven. The Bronto tab shows only the kept ones.

The split differs every time: expect the normal run dropped, slow and loop kept, and each run without an order number kept only if it skipped the order tool.
-->

---
part: Step 8 · Sample
---

# What tail sampling costs you

<div class="rows t8">
  <div><b>It waits</b><span>Spans sit in memory for a fixed time. A run that outlasts it is judged on what has arrived.</span></div>
  <div><b>It needs the whole run</b><span>With several Collectors, route by trace ID first.</span></div>
  <div><b>It only knows your rules</b><span>The run nobody guessed is the one it drops.</span></div>
</div>

<style>
.t8 > div { grid-template-columns: 16rem 1fr; padding: 1rem 0; font-size: 1.2rem; }
</style>

<!--
(0:29) The honest part of sampling.

It waits: spans sit in memory until the run is judged. Defaults are tuned for requests that take milliseconds. Agent runs take seconds to minutes. Set the wait longer than your longest normal run, and size the memory for it. Recent Collector releases can decide shortly after the root span arrives, which fits agents: the root span ends last.

The case to know: a run longer than the wait is decided without its root span, so without the token total and the tool sequence. That is exactly the runaway run. Configure a decision cache so late spans follow the first decision, and watch the sampler's own metrics for late spans and traces dropped too early.

It needs the whole run in one place. That's the central tier from step 5: a load-balancing exporter in front that routes by trace ID.

And it only knows what you told it. The dropped row on the last slide wasn't a bug in the config.
-->

---
part: Step 8 · Sample
---

# The Collector needs watching too

<div class="rows c8">
  <div><b>Protect it</b><span>A memory limiter first in every pipeline. The lab configs leave it out.</span></div>
  <div><b>Watch it</b><span>Its own metrics: refused and failed sends, queue size, what the filter dropped, spans that came after the sampling decision.</span></div>
  <div><b>Expect it to fail</b><span>If it is down, the SDK retries briefly and then drops. A restart of the sampling tier loses the runs it was holding.</span></div>
  <div><b>Know what it saves</b><span>Tail sampling saves storage. You still emit, ship and buffer every span.</span></div>
</div>

<p class="mon"><b>Monday</b> Decide whether you need to sample at all. If you do, sample at the tail.</p>

<style>
.c8 > div { grid-template-columns: 13rem 1fr; padding: 0.7rem 0; font-size: 1.08rem; }
</style>

<!--
(0:30) One slide on the thing we just made important. Masking and sampling now live in this process, so it is production software like any other.

Protect it: `memory_limiter` goes first in every pipeline. The lab files don't have it, or batching and queue settings, because they are sized for a laptop. Don't copy them unchanged.

Watch it. The Collector reports on itself: `otelcol_receiver_refused_spans`, `otelcol_exporter_send_failed_spans`, `otelcol_exporter_queue_size` against its capacity, the filter processor's filtered counters, and for the sampler the late-span age and dropped-too-early metrics. Alert on those like on any service.

Expect it to fail. If the Collector is unreachable the SDK retries for a short time and then drops. Restart the sampling tier and every run it was holding is gone. A config change there is a rolling restart that splits runs in flight.

And know what sampling saves: storage and query cost. Not the work of emitting and shipping.

Monday: sampling is a decision before it's a project.
-->

---
layout: section
section: "Step 9: Debug"
---

---
part: Step 9 · Debug
---

# Telemetry does two jobs here

<div class="big2">
  <div><h3>Explain a run</h3><p>Once you know which run, the trace tells you what happened and where.</p><p class="v ok">This comes with the instrumentation.</p></div>
  <div><h3>Detect a bad run</h3><p>Something has to stand out: a duration, a token count, an error, a pattern.</p><p class="v no">Only if a signal exists for it.</p></div>
</div>

<p class="cap1 dim">The agenda's four failures, reproduced in the lab, each with what detected it and what explained it.</p>

<style>
.big2 .v { margin-top: 0.9rem; font-weight: 700; }
.big2 .v.ok { color: var(--green-ink); } .big2 .v.no { color: #B23F14; }
</style>

<!--
(0:31) The pipeline is built. Now use it, on the four failures the agenda promised.

One distinction first, because it's the answer to "how does observability work for agents, really".

Explaining a run: given the run, the trace shows the steps, the timings, the tool calls, and with content, the reasoning. You get that from instrumenting, which was Session 1.

Detecting a bad run is a different job. Something about the run has to be different in a way a machine can see. For some failures that signal exists for free. For others it doesn't, and you have to create it.

How I produced the failures, so you know what's real. The slow retrieval is simulated: an eight-second delay. The loop is staged with one line in the system prompt and an order system that answers "pending". The last two are the model's own behaviour on Juraci's unchanged prompt and tools, and it only does them some of the time, so for those I open runs I saved earlier.
-->

---
part: Step 9 · Debug
---

# 1 · Slow retrieval

<div class="pair2">
  <Shot src="/img/shots/bronto-retrieval.png" />
  <Shot src="/img/shots/trace-slow.png" :marks="[{ x: 0.4, y: 40, w: 99.2, h: 6.6, label: '8.0 s in retrieval', ls: 'left:auto;right:-3px' }]" />
</div>

<div class="dx"><span><b>Detected by</b> retrieval latency, a metric the instrumentation already emits</span><span><b>Explained by</b> the trace: 8 s in one span, before the model was even called</span></div>

<!--
(0:32)

LIVE on the next slide.

Slow retrieval. The symptom is in a metric: the duration of the retrieval operation. That's one of the four metrics from step 7 that come for free.

From the metric to a run, from the run to the trace: eight seconds in the retrieval span, and everything after it normal. The model wasn't slow. The vector store was.

This is the easy case, and it's the same as any slow dependency you've ever debugged. That's the point of "an extension of your existing stack".
-->

---
part: Step 9 · Debug · live
---

# Live: the slow run

<Term type="slow" runs="runs the agent once with an 8-second delay in retrieval" />

<Jump :to="[{ label: 'Jaeger', url: 'http://localhost:16686/search?service=bookshop-agent&lookback=1h&limit=20' }, { label: 'Bronto', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+15+minutes&services=bookshop-agent' }]" />

<!--
LIVE (about 1 min). Type `slow`. While it runs: this is the simulated one, an eight-second sleep in the retrieval step.

Jaeger tab: open the run, point at the 8 s retrieval span, everything after it normal.
-->

---
part: Step 9 · Debug
---

# 2 · A token-burning loop

<div class="shotrow">
<Shot src="/img/shots/trace-loop.png" h="372px" />
<div class="dx v"><span><b>Detected by</b> the budget alert on tokens per run: about 4,600 instead of 1,600</span><span><b>Explained by</b> the trace: the same order lookup five times, each answered "pending", no error anywhere</span><span><b>Stopped by</b> the five-round cap in the agent's code</span></div>
</div>

<!--
(0:34)

LIVE on the next slide.

The loop from step 7. Detected by the budget alert from step 7: about 4,600 tokens against a normal 1,600.

The trace explains it: the same order lookup, five times, no error anywhere. Each call succeeded and said "pending".

Why did the model keep asking? Two reasonable things met. The order system answers before its lookup is done. And someone added a line to the system prompt: never tell a customer their order is pending, keep checking until you have a final status. A product requirement. With content captured, that line is right there in the trace.

The next slide shows where that line is visible.

No error, no exception. It ended with "Sorry, I could not finish that request", at the five-round cap.

I tried to get the model to loop without that prompt line, with errors that said "try again" and results that said "call again". It wouldn't. The instruction made it loop.
-->

---
part: Step 9 · Debug · live
---

# Live: the loop

<Term type="loop" runs="runs the agent with the prompt line and the order system that make it loop" />

<Jump :to="[{ label: 'Jaeger', url: 'http://localhost:16686/search?service=bookshop-agent&lookback=1h&limit=20' }, { label: 'Bronto: monitor', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/monitors/lists?activeMonitorId=9c81d708-3e21-40db-b506-415acde45efc&timeRange=Last+4+hours' }, { label: 'Bronto: logs', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/search?display=list&order=newest&timeRange=Last+20+minutes&select=*%2C%40raw&datasetAuthority=manual&logIds=80a64081-3aa2-4e0d-4a80-7a2b938f9d30&where=' }]" />

<!--
LIVE (about 1.5 min). Type `loop`. It ends with "Sorry, I could not finish that request."

Jaeger tab: the five lookups, then the token total and `bookshop.run.tools` on the run span. The monitor tab shows the alert a minute or two later, so come back to it. The logs tab has this run's content events: that is the next slide.
-->

---
part: Step 9 · Debug
---

# The cause of the loop is in a log record

<Jump :to="[{ label: 'Bronto: logs', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/search?display=list&order=newest&timeRange=Last+20+minutes&select=*%2C%40raw&datasetAuthority=manual&logIds=80a64081-3aa2-4e0d-4a80-7a2b938f9d30&where=' }]" />

<div class="shotrow">
<Shot src="/img/shots/bronto-log.png" h="372px" :marks="[{ x: 2.6, y: 29.6, w: 35.4, h: 6.6, label: 'the same trace ID as the spans', at: 'right' }, { x: 33.6, y: 72.8, w: 54, h: 7.6, label: 'the line that made it loop', at: 'left' }]" />
<div class="dx v"><span><b>What this is</b> the model call's content, sent as a log event and not as span attributes</span><span><b>Why it helps</b> the spans stay free of content, and the log record carries the trace ID, so you get from one to the other</span><span><b>Who may send it</b> only services marked as approved: the filter from step 6</span></div>
</div>

<!--
(0:36) This is the third signal: a log record, from the same run, in the same backend.

It's the content option from step 6, the one on log events. The spans of this run carry no prompt. The model call's content arrived as a log event instead, with the trace ID on it. From the trace I get here, and from here back to the trace.

And there is the cause: the last sentence of the system prompt. Never tell a customer their order is pending, keep checking until you have a final status.

So for this failure: a metric detected it, the trace showed what happened, and the log record showed why. Traces, metrics and logs, correlated, in the backend you already run.
-->

---
part: Step 9 · Debug
---

# 3 · An unexpected path

<Jump :to="[{ label: 'Jaeger: saved run', url: 'http://localhost:16686/trace/e0cd242502148b225b1518c177b925cf' }, { label: 'Bronto: saved run', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+2+days&services=bookshop-agent&traceId=e0cd242502148b225b1518c177b925cf' }]" />

<div class="bars">
  <div><span class="mono">check_inventory → get_order_status</span><i style="width:100%"/><b>55</b></div>
  <div class="odd"><span class="mono">check_inventory</span><i style="width:52.7%"/><b>29</b></div>
  <div><span class="mono">check_inventory → get_order_status ×5</span><i style="width:18.2%"/><b>10</b></div>
  <div><span class="mono">check_inventory ×3 → get_order_status</span><i style="width:1.8%"/><b>1</b></div>
</div>

<div class="cfg pl"><div class="cfg-h"><b>agent_v5.py</b><span>the one line that makes a path visible</span></div>

```python
agent.attributes["bookshop.run.tools"] += call.function.name + " "
```

</div>

<div class="dx"><span><b>Detected by</b> the tool sequence on the run span: count runs per path</span><span><b>Explained by</b> the trace: no order number given, and the agent never looked</span></div>

<style>
.bars { display: flex; flex-direction: column; gap: 0.45rem; margin-top: 0.5rem; }
.bars > div { display: grid; grid-template-columns: 22rem 1fr 2.4rem; align-items: center; gap: 0.8rem; font-size: 0.92rem; }
.bars i { display: block; height: 1.15rem; border-radius: 0 4px 4px 0; background: #BDBDBD; }
.bars .odd i { background: var(--orange); } .bars .odd span { font-weight: 700; }
.bars b { font-variant-numeric: tabular-nums; }
.pl { margin-top: 0.8rem; } .pl .slidev-code { font-size: 0.8rem !important; }
</style>

<!--
(0:38) An unexpected execution path. This one I didn't have to cause.

A customer asks about "my order" without giving a number. Same question, several runs. Sometimes the agent calls both tools. Sometimes it calls one, and either asks for the order number or says nothing about the order at all.

Nothing is slow, nothing is expensive, nothing errors. What's different is the shape of the run.

A trace backend can't group by shape unless you give it something to group by. So the agent writes the tools it called, in order, onto the run span. One line. Now the path is an attribute: you can count runs per path, alert on a new one, and it's what the unusual-tools sampling rule read.

If you take one code change home from this session, it's this line.

SAVED RUN (the model only does this some of the time): Jaeger http://localhost:16686/trace/e0cd242502148b225b1518c177b925cf , or Bronto https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+2+days&services=bookshop-agent&traceId=e0cd242502148b225b1518c177b925cf . One tool call, then an answer that never mentions the order.
-->

---
part: Step 9 · Debug
---

# 4 · A wrong tool call

<div class="shotrow">
<Shot src="/img/shots/trace-wrong.png" h="330px" :marks="[{ x: 6, y: 84, w: 24, h: 9, label: 'her order is ORD-1043', at: 'right' }]" />
<div class="dx v"><span><b>Detected by</b> nothing. Right tools, normal tokens, no error. The sampler dropped it.</span><span><b>Explained by</b> the tool description: "…by order ID (for example ORD-1042)"</span></div>
</div>

<!--
(0:39) The fourth, and the dropped row from the sampling slide.

Same question again: "where is my order", no number. This time the agent called the order tool. With ORD-1042. The customer's order is ORD-1043. ORD-1042 belongs to someone else, and the agent told her its status.

Where did 1042 come from? Juraci's tool description, written to be helpful: look up an order by ID, for example ORD-1042. The model needed an ID and took the only one in sight. In the lab this happened in 5 of 30 runs with that question, one in six; the other 25 took the path from the last slide. I didn't change his prompt or his tool.

Now ask what detected it. Latency normal. Tokens normal. Tool sequence the usual one. Every span green. No alert, and the sampler threw it away. A customer would have found this one.

Everything green and the answer wrong: that's the failure that's specific to agents.
-->

---
part: Step 9 · Debug
---

# Give the wrong answer a signal

<Jump :to="[{ label: 'Jaeger: saved run', url: 'http://localhost:16686/trace/457bd8a5df33ebb2fc504d5c4d903e63' }, { label: 'Bronto: saved run', url: 'https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+2+days&services=bookshop-agent&traceId=457bd8a5df33ebb2fc504d5c4d903e63' }]" />

<div class="cfg"><div class="cfg-h"><b>agent_v5.py</b><span>an outcome check, written on the span</span></div>

```python
# the tool answered, but was it this customer's order?
tool.attributes["bookshop.check.order_owned"] = order["customer"] == CUSTOMER_ID
```

</div>

<div class="rows sig">
  <div><b>A check in the run</b><span>Cheap and certain, and on the span before the run ends, so alerts and sampling can use it.</span></div>
  <div><b>An eval after the run</b><span>A model scores the answer later and the score is joined by trace ID. The convention is still in Development.</span></div>
  <div><b>A person</b><span>A thumbs-down or a ticket arrives late but is real, so attach it to the run.</span></div>
</div>

<p class="mon"><b>Monday</b> Put the tool sequence on the run span, and one check on your riskiest tool.</p>

<style>
.cfg .slidev-code { font-size: 0.76rem !important; line-height: 1.6 !important; }
.sig { margin-top: 0.8rem; } .sig > div { grid-template-columns: 13rem 1fr; padding: 0.55rem 0; font-size: 1.02rem; }
</style>

<!--
(0:40) So you create the signal. Three kinds.

SAVED RUN, not live: the model picked the wrong order in only 1 of 4 attempts. Say so, then open the saved run: Jaeger http://localhost:16686/trace/457bd8a5df33ebb2fc504d5c4d903e63 , or Bronto https://app.eu.bronto.io/org/3cf39069-b798-4b37-b0a4-08f02ec7f17c/tracing/traces?timeRange=Last+2+days&services=bookshop-agent&traceId=457bd8a5df33ebb2fc504d5c4d903e63 . Open the `execute_tool get_order_status` span: arguments ORD-1042, and `bookshop.check.order_owned = false`. The sampler kept this run because of that attribute.

A check in the run: after the lookup, compare the order's owner with the customer who's asking, and write the result on the span. It's two lines in the lab. Now "false" is something you can alert on, and one more sampling rule keeps that run. It's cheap and certain, and it exists before the run ends.

The real fix is next to it: the tool itself should refuse an order that isn't the customer's. Authorization belongs in the tool, not in the prompt. The check tells you how often it would have mattered.

An eval after the run: a second model reads the answer and scores it. Slower, costs money, catches things a simple check can't. OpenTelemetry has an event for evaluation results; it's in Development. It arrives after the sampling decision, which is one more reason to keep every run in some form.

And people: the ticket, the thumbs-down. Tie it to the run ID.

This is where an eval tool earns its place, behind the same Collector, joined by the same trace ID.
-->

---
part: Monday
---

# The checklist

<div class="ck">
  <span><i>5</i>Point one agent at a Collector and change nothing else.</span>
  <span><i>6</i>Find out whether content capture is on anywhere, and who approved it.</span>
  <span><i>7</i>Add a budget alert on tokens per run and a hard cap in the agent or gateway.</span>
  <span><i>8</i>Decide whether you need to sample at all. If you do, sample at the tail.</span>
  <span><i>9</i>Put the tool sequence on the run span, and one check on your riskiest tool.</span>
</div>

<div class="ck-qr"><QrCode url="https://github.com/bronto-community/agent-trace-to-production" :size="104" /><span>The lab: Session 1's agent, a Collector config for steps 5 to 8, the four failures</span></div>

<style>
.ck { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem; width: 74%; }
.ck span { display: grid; grid-template-columns: 2.4rem 1fr; align-items: center; gap: 0.9rem; font-size: 1.12rem; line-height: 1.35; }
.ck i { display: grid; place-items: center; width: 2.2rem; height: 2.2rem; border-radius: 50%; background: var(--green); color: #fff; font: 700 1rem var(--sans); font-style: normal; }
.ck-qr { position: absolute; right: 0; top: 4.2rem; width: 9.5rem; display: flex; flex-direction: column; align-items: center; gap: 0.5rem; text-align: center; font-size: 0.72rem; color: var(--ink-dim); }
</style>

<!--
(0:44) The checklist from the agenda. You've seen every line already: it's the Monday line of each step. Five things, none of them a project.

The lab is in the repo: Juraci's agent with a handful of added lines, a Collector file for each of steps 5 to 8, and switches for the failures.
-->

---
part: Monday
---

# What is still moving

<div class="rows mv">
  <div><b>The GenAI conventions</b><span>Still Development, with no stable release. Names change. Pin versions; rename in the Collector.</span></div>
  <div><b>Cost, evaluations, guardrails</b><span>Proposals or Development. Use your own names until they land.</span></div>
  <div><b>The newer Collector pieces</b><span>Filter, the span-to-metrics connector, redaction on logs and the normalizer are alpha. Tail sampling, transform and redaction on traces are beta.</span></div>
</div>

<p class="cap1">The five checklist items don't depend on any of this and work today.</p>

<style>
.mv > div { grid-template-columns: 17rem 1fr; padding: 0.9rem 0; }
</style>

<!--
(0:44) What I can't promise you. The conventions this all rests on are not stable. The lab pins its versions for that reason, and so should you.

Cost, evaluation results and guardrail telemetry aren't settled.

Several Collector components this hour built on are alpha, including the filter and the connector that made our per-run metric. They work in 0.165; their configuration can still change.

And none of that changes the checklist. A Collector in between, a decision about content, a budget and a cap, a sampling decision, one check: those don't depend on a name being final.

Q&A. Juraci joins (TODO: confirm with Packt).
-->

---
layout: cover
---

<h1>Thank You</h1>
<p class="end-who">Severin Neumann, Head of Community, Bronto</p>
<p class="end-contact mono">linkedin.com/in/severinneumann · severin@bronto.io</p>
<p class="end-url mono">github.com/bronto-community/agent-trace-to-production</p>
<div class="end-qr"><QrCode url="https://github.com/bronto-community/agent-trace-to-production" :size="110" /></div>
<p class="end-legal">OpenTelemetry is a registered trademark and Jaeger is a trademark of The Linux Foundation.</p>

<style>
.slidev-layout .end-who { font-size: 1rem !important; margin-top: 0.6rem !important; }
.slidev-layout .end-contact { font-size: 0.8rem !important; color: #fff; margin-top: 0.2rem !important; }
.slidev-layout .end-url { font-size: 0.9rem !important; color: #CFCFCF; }
.end-qr { position: absolute; left: 0; top: 150px; background: #fff; border-radius: 10px; padding: 6px; }
.slidev-layout .end-legal { position: absolute; top: 300px; left: 180px; width: 26rem; font-size: 0.55rem !important; color: #9A9A9A; }
</style>
