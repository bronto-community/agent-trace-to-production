<script setup lang="ts">
// A backend moment: what Ops/Finance/Security actually look at.
// Renders a mock window (view name, query, result rows, optional spike chart)
// until a real screenshot exists; then pass `img` and the mock is replaced.
//   view   e.g. "Search · .traces", "Monitor", "Dashboard"
//   query  the query as typed (shown in mono)
//   rows   result lines; prefix a line with "!" to highlight it
//   series numbers for a small bar chart (the last bar is the spike, unless :spike="false")
//   note   one line under the result, e.g. "1 run · 27 Oct 10:14"
const props = withDefaults(defineProps<{
  view?: string; query?: string; rows?: string[]; series?: number[]
  note?: string; img?: string; tone?: 'neutral' | 'alert'; spike?: boolean
}>(), { view: 'Search', rows: () => [], tone: 'neutral', spike: true })
const max = () => Math.max(...(props.series ?? [1]))
</script>

<template>
  <div class="bv" :class="props.tone">
    <div class="bv-bar"><i /><i /><i /><span>Bronto · {{ props.view }}</span></div>
    <img v-if="props.img" :src="props.img" class="bv-img" alt="" />
    <div v-else class="bv-body">
      <p v-if="props.query" class="bv-q">{{ props.query }}</p>
      <div v-if="props.series" class="bv-chart">
        <i v-for="(v, i) in props.series" :key="i" :class="{ hot: props.spike && i === props.series.length - 1 }" :style="{ height: (v / max()) * 100 + '%' }" />
      </div>
      <div v-for="(r, i) in props.rows" :key="i" class="bv-row" :class="{ hl: r.startsWith('!') }">{{ r.replace(/^!/, '') }}</div>
      <p v-if="props.note" class="bv-note">{{ props.note }}</p>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.bv { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; background: var(--bg); }
.bv-bar { display: flex; align-items: center; gap: 0.35rem; padding: 0.45rem 0.8rem; background: var(--surface); border-bottom: 1px solid var(--border); }
.bv-bar i { width: 9px; height: 9px; border-radius: 50%; background: var(--border); }
.bv-bar span { margin-left: 0.5rem; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-dim); }
.alert .bv-bar { background: var(--orange-soft); }
.alert .bv-bar span { color: #B23F14; font-weight: 700; }
.bv-img { display: block; width: 100%; }
.bv-body { padding: 0.8rem 1rem; display: flex; flex-direction: column; gap: 0.4rem; }
.bv-q { font-family: var(--mono); font-size: 0.78rem; line-height: 1.5; padding: 0.45rem 0.6rem; background: var(--surface); border-radius: 6px; margin: 0 !important; }
.bv-chart { display: flex; align-items: flex-end; gap: 4px; height: 70px; margin: 0.3rem 0; }
.bv-chart i { flex: 1; background: var(--blue-soft); border-radius: 2px 2px 0 0; }
.bv-chart i.hot { background: var(--orange); }
.bv-row { font-family: var(--mono); font-size: 0.72rem; padding: 0.2rem 0.4rem; border-radius: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bv-row.hl { background: var(--orange-soft); color: #B23F14; font-weight: 700; }
.bv-note { font-size: 0.8rem !important; color: var(--green-ink) !important; font-weight: 700; margin: 0.2rem 0 0 !important; }
</style>
