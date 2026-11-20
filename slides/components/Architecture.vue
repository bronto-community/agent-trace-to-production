<script setup lang="ts">
// Slide 11: where the telemetry goes. `stage` (pass $clicks + 1):
//   1  Session 1: both processes send OTLP straight to Jaeger on :4318
//   2  the Collector takes the port and ships to debug + Jaeger
//   3  backends are config: add one (Bronto), swap one, or split data
// The model call to OpenRouter is a span, not a box, so it isn't drawn.
const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 1 })
const s = (n: number) => props.stage >= n
</script>

<template>
  <svg class="arch" viewBox="0 0 540 300" :class="`st${props.stage}`">
    <defs>
      <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" fill="currentColor" />
      </marker>
    </defs>

    <!-- the two services -->
    <g class="svc">
      <rect x="0" y="50" width="150" height="62" rx="10" />
      <text x="14" y="76" class="k">bookshop-agent</text>
      <text x="14" y="96" class="d">Python, util-genai</text>
      <rect x="0" y="188" width="150" height="62" rx="10" />
      <text x="14" y="214" class="k">bookshop-mcp</text>
      <text x="14" y="234" class="d">MCP server, own process</text>
      <line x1="75" y1="112" x2="75" y2="188" class="stdio" />
      <text x="84" y="154" class="d">stdio</text>
    </g>

    <!-- stage 1: straight to Jaeger -->
    <g class="fade" :class="{ on: !s(2) }">
      <path d="M150 81 C 260 81, 280 150, 384 150" class="wire" marker-end="url(#ah)" />
      <path d="M150 219 C 260 219, 280 150, 384 150" class="wire" marker-end="url(#ah)" />
    </g>

    <!-- stage 2+: the Collector -->
    <g class="fade" :class="{ on: s(2) }">
      <path d="M150 81 C 175 81, 175 150, 196 150" class="wire" marker-end="url(#ah)" />
      <path d="M150 219 C 175 219, 175 150, 196 150" class="wire" marker-end="url(#ah)" />
      <rect x="198" y="104" width="134" height="92" rx="10" class="col" />
      <text x="212" y="132" class="k">Collector</text>
      <text x="212" y="152" class="d">otlp receiver</text>
      <text x="212" y="168" class="d">on the same :4318</text>
      <path d="M265 196 L265 236" class="wire" marker-end="url(#ah)" />
      <rect x="215" y="240" width="100" height="34" rx="8" class="term" />
      <text x="229" y="262" class="k sm inv">debug</text>
    </g>

    <!-- Jaeger: centre in stages 1-2, top in stage 3 -->
    <g class="jg" :style="{ transform: s(3) ? 'translateY(-90px)' : 'none' }">
      <rect x="388" y="120" width="150" height="60" rx="10" class="be" />
      <text x="402" y="146" class="k">Jaeger</text>
      <text x="402" y="165" class="d">{{ s(2) ? 'otlp/jaeger' : 'OTLP on :4318' }}</text>
    </g>
    <path class="wire fade" :class="{ on: s(2) && !s(3) }" d="M332 150 L384 150" marker-end="url(#ah)" />

    <!-- stage 3: more backends -->
    <g class="fade" :class="{ on: s(3) }">
      <path d="M332 130 C 360 130, 360 60, 384 60" class="wire" marker-end="url(#ah)" />
      <path d="M332 150 L384 150" class="wire hot" marker-end="url(#ah)" />
      <path d="M332 170 C 360 170, 360 240, 384 240" class="wire dash" marker-end="url(#ah)" />
      <rect x="388" y="120" width="150" height="60" rx="10" class="be new" />
      <text x="402" y="146" class="k">Bronto</text>
      <text x="402" y="165" class="d">otlphttp/bronto</text>
      <rect x="388" y="210" width="150" height="60" rx="10" class="be ghost" />
      <text x="402" y="236" class="k">any OTLP backend</text>
      <text x="402" y="255" class="d">add, swap, split</text>
    </g>
  </svg>
</template>

<style scoped>
.arch { width: 100%; height: auto; color: var(--ink-dim); overflow: visible; }
rect { fill: var(--surface); }
.svc rect { fill: var(--sand); }
.col { fill: var(--green-soft); stroke: var(--green); stroke-width: 2; }
.term { fill: var(--code-bg); }
.be.new { fill: var(--green-soft); }
.be.ghost { fill: transparent; stroke: var(--border); stroke-width: 1.5; stroke-dasharray: 5 4; }
.k { font-family: var(--mono); font-size: 14px; font-weight: 700; fill: var(--ink); }
.k.sm { font-size: 13px; }
.k.inv { fill: #fff; }
.d { font-family: var(--sans); font-size: 12px; fill: var(--ink-dim); }
.d.mid { font-family: var(--mono); }
.wire { fill: none; stroke: currentColor; stroke-width: 1.6; }
.wire.hot { stroke: var(--green-ink); stroke-width: 2.2; color: var(--green-ink); }
.wire.dash { stroke-dasharray: 5 4; }
.stdio { stroke: var(--ink-dim); stroke-width: 1.4; stroke-dasharray: 3 3; }
.fade { opacity: 0; transition: opacity 0.45s; }
.fade.on { opacity: 1; }
.jg { transition: transform 0.5s ease; }
</style>
