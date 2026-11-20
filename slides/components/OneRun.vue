<script setup lang="ts">
// "What Ops works with": the slow run, trimmed. Stage 1 the slow-run search points
// at the retrieval span, stage 2 the WARN log points at the same span.
// Fixed 860×300 canvas so the connectors land on the bar. Pass $clicks.
import { traces } from './traces'
const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 0 })
const rows = traces.slow.filter(r => !r.name.startsWith('MCP send'))
const total = Math.max(...rows.map(r => r.start + r.dur))
const X0 = 262, W = 285, Y0 = 38, H = 30
const x = (ms: number) => X0 + (ms / total) * W
const ri = rows.findIndex(r => r.name.startsWith('retrieval'))
const anchor = { x: x(rows[ri].start + rows[ri].dur) + 4, y: Y0 + ri * H + H / 2 }
</script>

<template>
  <div class="or" :class="`st${props.stage}`">
    <div class="or-wf">
      <div class="or-head"><span>bookshop-agent · one run</span><span>0 → 21.3 s</span></div>
      <div v-for="(r, i) in rows" :key="i" class="or-row" :class="{ anchor: i === ri }" :style="{ top: Y0 + i * H + 'px' }">
        <span class="or-name" :style="{ paddingLeft: r.depth * 12 + 'px' }">{{ r.name }}</span>
        <i class="or-bar" :style="{ left: x(r.start) + 'px', width: Math.max(3, x(r.start + r.dur) - x(r.start)) + 'px' }" />
      </div>
    </div>
    <svg class="or-lines" viewBox="0 0 860 300">
      <circle class="dot a1" :cx="anchor.x" :cy="anchor.y" r="4" />
      <path class="ln a1" :d="`M612 44 C 540 44, 520 ${anchor.y}, ${anchor.x + 6} ${anchor.y}`" />
      <path class="ln a2" :d="`M612 190 C 540 190, 520 ${anchor.y}, ${anchor.x + 6} ${anchor.y}`" />
    </svg>
    <div class="or-chip alert a1"><b>search · .traces</b><span>runs over 15 s → this one</span></div>
    <div class="or-chip log a2"><b>log · WARN</b><span>vector store timed out after 12 s, answering without catalog context</span></div>
  </div>
</template>

<style scoped>
.or { position: relative; width: 860px; height: 300px; margin: 0.8rem auto 0; }
.or-wf { position: absolute; left: 0; top: 0; width: 560px; height: 268px; background: var(--surface); border-radius: 14px; font-family: var(--mono); font-size: 0.7rem; }
.or-head { position: absolute; left: 14px; right: 14px; top: 10px; display: flex; justify-content: space-between; font-size: 0.58rem; color: var(--ink-dim); text-transform: uppercase; letter-spacing: 0.08em; }
.or-row { position: absolute; left: 0; width: 100%; height: 30px; display: flex; align-items: center; }
.or-name { position: absolute; left: 14px; width: 240px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.or-bar { position: absolute; top: 9px; height: 12px; border-radius: 3px; background: var(--sapphire-soft); transition: background 0.4s; }
.st1 .anchor .or-bar, .st2 .anchor .or-bar { background: var(--orange); }
.st1 .anchor .or-name, .st2 .anchor .or-name { color: #B23F14; font-weight: 700; }
.or-lines { position: absolute; inset: 0; width: 860px; height: 300px; fill: none; pointer-events: none; }
.ln { stroke: var(--orange); stroke-width: 1.8; stroke-dasharray: 5 4; }
.dot { fill: var(--orange); }
.or-chip { position: absolute; left: 612px; width: 248px; padding: 0.55rem 0.8rem; border-radius: 10px; display: flex; flex-direction: column; gap: 0.2rem; }
.or-chip b { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.08em; }
.alert { top: 18px; background: var(--orange-soft); }
.alert b { color: #B23F14; }
.alert span { font-family: var(--mono); font-size: 0.85rem; font-weight: 700; }
.log { top: 150px; background: var(--code-bg); color: #EDEDED; }
.log b { color: #F5C451; }
.log span { font-family: var(--mono); font-size: 0.68rem; line-height: 1.4; }
.a1, .a2 { opacity: 0; transition: opacity 0.45s; }
.st1 .a1, .st2 .a1, .st2 .a2 { opacity: 1; }
</style>
