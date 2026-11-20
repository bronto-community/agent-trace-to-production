<script setup lang="ts">
import { computed } from 'vue'

// 100 agent runs. stage (pass $clicks):
//   0  all runs; the ones that matter are coloured, except the wrong booking,
//      which looks like every other run
//   1  head sampling 10%: a random tenth survives, none of the interesting ones
//   2  tail sampling: errors, slow, expensive, rare paths + 5% baseline
//   3  the wrong booking is ringed: no policy kept it
//   4  sample the payload, not the run: every run kept as metadata,
//      the tail-sampled ones also keep prompts and completions
const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 0 })

type Kind = 'plain' | 'loop' | 'slow' | 'err' | 'rare' | 'wrong'
const special: Record<number, Kind> = {
  17: 'loop', 52: 'loop', 88: 'loop',
  33: 'slow', 71: 'slow',
  9: 'err', 64: 'err',
  80: 'rare',
  45: 'wrong',
}
const head = new Set([2, 13, 24, 38, 41, 57, 66, 79, 90, 97])
const baseline = new Set([6, 28, 59, 76, 93])

const runs = Array.from({ length: 100 }, (_, i) => ({ i, kind: (special[i] ?? 'plain') as Kind }))

function cls(r: { i: number; kind: Kind }) {
  const s = props.stage
  const c: string[] = [r.kind === 'wrong' ? 'plain' : r.kind]
  if (s === 1 && !head.has(r.i)) c.push('gone')
  if (s >= 2) {
    const tail = (r.kind !== 'plain' && r.kind !== 'wrong') || baseline.has(r.i)
    if (s < 4 && !tail) c.push('gone')
    if (s >= 4 && !tail) c.push('meta')
  }
  if (s >= 3 && r.kind === 'wrong') c.push('ring')
  return c
}

const captions = [
  ['100 agent runs', '3 loops · 2 slow · 2 errors · 1 other model'],
  ['Head sampling, 10%', 'Decided at the start of the run. Kept 10 runs, none of the 8 that matter.'],
  ['Tail sampling', 'Decided after the run. Errors, slow, expensive, another model, plus a 5% baseline.'],
  ['…and this one?', 'A customer told about someone else\u2019s order. Green, fast, cheap, normal path. Dropped.'],
  ['Every run, metadata only', 'Payload (prompts, completions, tool args) only where tail sampling says so.'],
]
const cap = computed(() => captions[Math.min(props.stage, 4)])
</script>

<template>
  <div class="sd">
    <div class="sd-grid">
      <i v-for="r in runs" :key="r.i" :class="cls(r)" />
    </div>
    <div class="sd-side">
      <div class="sd-cap"><b>{{ cap[0] }}</b><span>{{ cap[1] }}</span></div>
      <div class="sd-legend">
        <span><i class="loop" />loop</span>
        <span><i class="slow" />slow</span>
        <span><i class="err" />error</span>
        <span><i class="rare" />other model</span>
        <span v-if="stage >= 4"><i class="plain meta" />metadata only</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sd { display: grid; grid-template-columns: 1.5fr 1fr; gap: 2.2rem; align-items: center; margin-top: 1.6rem; }
.sd-grid { display: grid; grid-template-columns: repeat(20, 1fr); gap: 9px; padding: 1.3rem; background: var(--surface); border-radius: 18px; box-shadow: var(--shadow); }
.sd-grid i, .sd-legend i { display: block; aspect-ratio: 1; border-radius: 5px; background: #D3D3D3; transition: opacity 0.35s, transform 0.35s, background 0.35s, box-shadow 0.35s; }
.loop { background: var(--claim) !important; }
.slow { background: #F5B719 !important; }
.err { background: #B3261E !important; }
.rare { background: var(--sapphire) !important; }
.gone { opacity: 0.1; transform: scale(0.6); }
.meta { background: transparent !important; box-shadow: inset 0 0 0 2px #A8A8A8; }
.ring { box-shadow: 0 0 0 3px var(--bg), 0 0 0 6px var(--claim); transform: scale(1.15); opacity: 1 !important; }
.sd-side { display: flex; flex-direction: column; gap: 1.4rem; }
.sd-cap { display: flex; flex-direction: column; gap: 0.5rem; min-height: 8rem; }
.sd-cap b { font-size: 1.7rem; font-weight: 600; letter-spacing: -0.02em; }
.sd-cap span { font-size: 1.05rem; color: var(--ink-dim); line-height: 1.45; }
.sd-legend { display: flex; flex-wrap: wrap; gap: 0.5rem 1.1rem; font-size: 0.78rem; color: var(--ink-dim); }
.sd-legend span { display: inline-flex; align-items: center; gap: 0.4rem; }
.sd-legend i { width: 12px; }
</style>
