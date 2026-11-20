<script setup lang="ts">
// The Collector pipeline the talk builds, in processor order. Parts are the
// steps: 1 connect, 2 measure, 3 keep, 4 govern. `at` = which chapter we're in (0 = map
// of the whole thing, all nodes shown, none built). Nodes from earlier parts
// are built (solid), the current part's nodes are highlighted, later ones are
// ghosts.
const props = withDefaults(defineProps<{ at?: number }>(), { at: 0 })

const nodes = [
  { k: 'agent', d: 'OTLP traces and logs', part: 1, q: 'connect', edge: true },
  { k: 'filter', d: 'drop the one-span notification', part: 4, q: 'govern' },
  { k: 'redaction', d: 'allow-list, HMAC; transform: digest', part: 4, q: 'govern' },
  { k: 'signal_to_metrics', d: 'tokens and cost, every run', part: 2, q: 'measure' },
  { k: 'tail_sampling', d: 'which runs keep their content', part: 3, q: 'keep' },
  { k: 'backend', d: 'the one you already run', part: 1, q: 'connect', edge: true },
]
const state = (p: number) => (props.at === 0 ? 'map' : p < props.at ? 'built' : p === props.at ? 'now' : 'ghost')
</script>

<template>
  <div class="pl">
    <template v-for="(n, i) in nodes" :key="n.k">
      <div class="pl-node" :class="[state(n.part), { edge: n.edge }]">
        <span class="pl-k">{{ n.k }}</span>
        <span class="pl-d">{{ n.d }}</span>
        <span class="pl-p">{{ n.part }} · {{ n.q }}</span>
      </div>
      <div v-if="i < nodes.length - 1" class="pl-arrow">→</div>
    </template>
  </div>
</template>

<style scoped>
.pl { display: flex; align-items: stretch; margin-top: 1.4rem; }
.pl-node { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 0.35rem; padding: 0.8rem 0.6rem 0.7rem; border-radius: 14px; background: var(--surface); box-shadow: var(--shadow); transition: opacity 0.3s, background 0.3s, box-shadow 0.3s; }
.pl-node.edge { background: var(--sand); box-shadow: none; }
.pl-k { font-family: var(--mono); font-size: 0.68rem; font-weight: 700; white-space: nowrap; }
.pl-d { font-size: 0.74rem; color: var(--ink-dim); line-height: 1.3; flex: 1; }
.pl-p { font-family: var(--mono); font-size: 0.6rem; color: var(--ink-dim); text-transform: uppercase; letter-spacing: 0.08em; }
.pl-arrow { flex: 0 0 1.4rem; display: grid; place-items: center; color: var(--ink-dim); }
.ghost { opacity: 0.35; box-shadow: none; background: transparent; outline: 1.5px dashed var(--border); }
.now { background: var(--yellow-bg); box-shadow: 0 0 0 2px var(--yellow-line); }
.now .pl-p { color: var(--yellow-ink); font-weight: 700; }
.built .pl-p::after { content: ' ✓'; color: var(--mint-ink); }
</style>
