<script setup lang="ts">
import { computed } from 'vue'
import { traces } from './traces'

// A trace waterfall from components/traces.ts. `reveal` (pass $clicks) turns on
// the tones: before it, every row is neutral, so the audience looks for the
// problem with you.
const props = withDefaults(defineProps<{ preset: string; reveal?: number; tonesAt?: number }>(), {
  reveal: 1, tonesAt: 1,
})

const rows = computed(() => traces[props.preset] ?? [])
const total = computed(() => Math.max(...rows.value.map(r => r.start + r.dur)))
const showTones = computed(() => props.reveal >= props.tonesAt)
const pct = (v: number) => `${(v / total.value) * 100}%`
// notes sit right of the bar, or left of it when the bar runs to the end
function noteStyle(r: { start: number; dur: number }) {
  const end = (r.start + r.dur) / total.value
  if (end < 0.62) return { left: `calc(${pct(r.start + r.dur)} + 6px)` }
  if (r.start / total.value > 0.25) return { right: `calc(${(1 - r.start / total.value) * 100}% + 6px)` }
  return { left: '6px', top: '0.38rem', lineHeight: '0.8rem', color: 'var(--ink)' }  // inside a long bar
}
const secs = (ms: number) => (ms >= 1000 ? `${(ms / 1000).toFixed(1)} s` : `${ms} ms`)
</script>

<template>
  <div class="wf">
    <div class="wf-head"><span>span</span><span>service</span><span>0 → {{ secs(total) }}</span></div>
    <div v-for="(r, i) in rows" :key="i" class="wf-row" :class="showTones ? r.tone : ''">
      <span class="wf-name" :style="{ paddingLeft: r.depth * 14 + 'px' }">{{ r.name }}</span>
      <span class="wf-svc">{{ r.svc }}</span>
      <span class="wf-track">
        <i class="wf-bar" :style="{ left: pct(r.start), width: pct(Math.max(r.dur, total * 0.006)) }" />
        <em v-if="r.note" class="wf-note" :style="noteStyle(r)">{{ r.note }}</em>
      </span>
    </div>
  </div>
</template>

<style scoped>
.wf { background: var(--surface); border-radius: 16px; box-shadow: var(--shadow); padding: 0.7rem 1rem 0.8rem; font-family: var(--mono); font-size: 0.76rem; }
.wf-head, .wf-row { display: grid; grid-template-columns: 19rem 7rem 1fr; align-items: center; gap: 0.6rem; }
.wf-head { color: var(--ink-dim); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.08em; padding-bottom: 0.35rem; border-bottom: 1px solid var(--border); margin-bottom: 0.3rem; }
.wf-row { height: 1.8rem; transition: opacity 0.3s; }
.wf-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wf-svc { color: var(--ink-dim); white-space: nowrap; overflow: hidden; }
.wf-track { position: relative; height: 100%; }
.wf-bar { position: absolute; top: 0.38rem; height: 0.8rem; border-radius: 3px; background: var(--sapphire-soft); transition: background 0.35s; }
.wf-note { position: absolute; top: 0.33rem; white-space: nowrap; font-style: normal; color: var(--ink-dim); font-size: 0.68rem; }
.wf-note { max-width: 14rem; overflow: hidden; text-overflow: ellipsis; }
.hot .wf-bar { background: var(--claim); }
.hot .wf-note { color: var(--claim); font-weight: 600; }
.err .wf-bar { background: repeating-linear-gradient(45deg, var(--claim), var(--claim) 4px, var(--claim-soft) 4px, var(--claim-soft) 8px); }
.err .wf-note { color: var(--claim); }
.ok .wf-bar { background: var(--mint); }
.dim { opacity: 0.45; }
.dim .wf-bar { background: repeating-linear-gradient(90deg, var(--border), var(--border) 6px, transparent 6px, transparent 10px); }
</style>
