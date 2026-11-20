<script setup lang="ts">
// "Special, but so were the others": stage 0 five domains apart, each with
// its own trait; stage 1 the SAME tiles move into one request path under
// one trace. Pass $clicks. Fixed 860×330 canvas so the tiles can travel.
const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 0 })
const tiles = [
  { k: 'mobile', name: 'Mobile', trait: 'offline', a: [10, 30], b: [0, 15] },
  { k: 'browser', name: 'Browser', trait: 'client', a: [200, 150], b: [0, 165] },
  { k: 'agent', name: 'Agent', trait: 'tokens', a: [375, 10], b: [245, 90], ag: true },
  { k: 'db', name: 'Database', trait: 'queries', a: [560, 140], b: [490, 90] },
  { k: 'mf', name: 'Mainframe', trait: 'batch', a: [725, 25], b: [730, 90] },
]
const pos = (t: typeof tiles[number]) => {
  const [x, y] = props.stage >= 1 ? t.b : t.a
  return { transform: `translate(${x}px, ${y}px)` }
}
</script>

<template>
  <div class="cn" :class="{ joined: props.stage >= 1 }">
    <svg class="cn-wires" viewBox="0 0 860 330">
      <defs><marker id="cnah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" /></marker></defs>
      <path d="M130 75 C 190 75, 190 150, 241 150" marker-end="url(#cnah)" />
      <path d="M130 225 C 190 225, 190 150, 241 150" marker-end="url(#cnah)" />
      <path d="M375 150 L486 150" marker-end="url(#cnah)" />
      <path d="M620 150 L726 150" marker-end="url(#cnah)" />
      <path class="br" d="M0 296 L0 306 Q0 312 6 312 L854 312 Q860 312 860 306 L860 296" />
    </svg>
    <span class="cn-one">one trace</span>
    <div v-for="t in tiles" :key="t.k" class="cn-t" :class="{ ag: t.ag }" :style="pos(t)">
      <svg class="cn-ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <template v-if="t.k === 'mobile'"><rect x="9" y="3" width="14" height="26" rx="2.5" /><path d="M14 25h4" /></template>
        <template v-else-if="t.k === 'browser'"><rect x="3" y="6" width="26" height="20" rx="2.5" /><path d="M3 11h26M7 8.5h.01M10 8.5h.01" /></template>
        <template v-else-if="t.k === 'agent'"><rect x="6" y="10" width="20" height="15" rx="4" /><path d="M16 10V5M13 5h6" /><circle cx="12" cy="17" r="1.6" /><circle cx="20" cy="17" r="1.6" /><path d="M13 21.5h6" /></template>
        <template v-else-if="t.k === 'db'"><ellipse cx="16" cy="7" rx="10" ry="3.5" /><path d="M6 7v18c0 2 4.5 3.5 10 3.5s10-1.5 10-3.5V7M6 16c0 2 4.5 3.5 10 3.5s10-1.5 10-3.5" /></template>
        <template v-else><rect x="5" y="3" width="22" height="26" rx="2" /><path d="M5 10h22M5 17h22M5 24h22M9 6.5h6M9 13.5h6M9 20.5h6" /></template>
      </svg>
      <b>{{ t.name }}</b>
      <span class="cn-trait">{{ t.trait }}</span>
    </div>
  </div>
</template>

<style scoped>
.cn { position: relative; width: 860px; height: 330px; margin: 0.6rem auto 0; }
.cn-wires { position: absolute; inset: 0; width: 100%; height: 100%; color: var(--ink-dim); fill: none; stroke: currentColor; stroke-width: 1.8; opacity: 0; transition: opacity 0.4s 0.45s; }
.cn-wires .br { stroke: var(--ink); stroke-width: 1.5; }
.joined .cn-wires { opacity: 1; }
.cn-one { position: absolute; left: 50%; top: 300px; transform: translateX(-50%); background: var(--bg); padding: 0 0.7rem; font-family: var(--mono); font-size: 0.85rem; font-weight: 700; color: var(--ink); opacity: 0; transition: opacity 0.4s 0.6s; }
.joined .cn-one { opacity: 1; }
.cn-t { position: absolute; left: 0; top: 0; width: 130px; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.3rem; border-radius: 14px; background: var(--surface); transition: transform 0.75s cubic-bezier(.3,.7,.2,1); }
.cn-t.ag { background: var(--green-soft); color: var(--green-ink); box-shadow: 0 0 0 2px var(--green); }
.cn-ic { width: 36px; height: 36px; }
.cn-t b { font-size: 1rem; }
.cn-trait { font-family: var(--mono); font-size: 0.72rem; color: var(--ink-dim); transition: opacity 0.3s; }
.ag .cn-trait { color: var(--green-ink); }
.joined .cn-trait { opacity: 0; }
</style>
