# From Agent Trace to Production

Slides and lab for "From Agent Trace to Production: Governing, Shaping, and Debugging GenAI Telemetry",
Session 2 of Packt's *Agentic Observability Engineering with OpenTelemetry* (21 November 2026).

Session 1, by Juraci Paixão Kröhling, ends with a small bookshop support agent that emits one
OpenTelemetry trace. This session takes that agent to production in five steps: connect it to a
Collector, govern prompt and response content, measure tokens and latency, sample, and debug four failures.

- `slides/`: the deck ([Slidev](https://sli.dev)). `npm install`, then `npm run dev`.
  The terminal slides need `./demo-terminal.sh` (ttyd) and the lab running.
- `lab/`: the Session 1 lab (Apache-2.0, see `lab/LICENSE`) with the additions for this session:
  `agent_v5.py`, one Collector config for each of steps 5 to 8 in `collector/`, a Jaeger that keeps
  traces on disk, and saved runs of the failures (`./load-saved-runs.sh`).

## Run the lab

```bash
cd lab
cp .env.example .env          # add your model API key
docker compose up -d          # Jaeger on :16686, a Collector on :4318
uv run --env-file .env opentelemetry-instrument python agent_v5.py
```

Pick the step with `COLLECTOR_CONFIG`, for example
`COLLECTOR_CONFIG=step8-sample.yaml docker compose up -d --no-deps collector`.
Reproduce a failure with `FAILURE=slow`, `FAILURE=loop` or `FAILURE=wrong`; add `CHECKS=on` for the
ownership check from step 9. To send to an OTLP backend as well, set `BACKEND_ENDPOINT` and the
auth header in `collector/*.yaml`.

The Collector configs are sized for a laptop: they have no memory limiter, queue settings or
batching. Don't copy them to production unchanged.
