# From Agent Trace to Production · slides

Session 2 of "Agentic Observability Engineering with OpenTelemetry" (Packt, online, 21 Nov 2026).
A Slidev deck in the Packt theme of Juraci Paixão Kröhling's Session 1 deck, built on his demo agent
([ollygarden-demo/instrumenting-the-agent](https://github.com/ollygarden-demo/instrumenting-the-agent)); the lab is in `../lab`.

```bash
npm install
npm run dev      # presenter view at /presenter
npm run build    # static site in dist/, deployed by Vercel (vercel.json)
```

- Speaker notes carry time cues `(h:mm)` for a 45-minute talk and `LIVE` cues.
- Terminal slides embed a shell through ttyd: `./demo-terminal.sh` (loopback only), with the lab running.
- The tabs on the right border of a slide open Jaeger or the backend in a new browser tab.
- `shoot.mjs` takes the Jaeger screenshots in `public/img/shots`.
