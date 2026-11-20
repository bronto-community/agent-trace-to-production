<script setup lang="ts">
// Ops asks ordinary ops questions; each click reveals the not-ordinary answer.
// Stage 4 (the loop) brings Finance peeking in. Pass $clicks.
const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 0 })
const rows = [
  { q: 'Is it down?', a: 'No. It covered for a failure.', tag: 'swallowed failure' },
  { q: 'Why is it slow?', a: 'It had nothing to work with.', tag: 'weak context' },
  { q: 'What broke?', a: 'Nothing. It chose wrong.', tag: 'wrong turn' },
  { q: 'Why the spike?', a: 'It looped. Tokens.', tag: 'spend per run' },
]
</script>

<template>
  <div class="oq">
    <div class="oq-who"><Portrait who="oncall" :size="150" /><span>Ops</span></div>
    <div class="oq-rows">
      <div v-for="(r, i) in rows" :key="r.q" class="oq-row" :class="{ on: props.stage > i }">
        <span class="oq-q"><i />{{ r.q }}</span>
        <span class="oq-arrow">→</span>
        <span class="oq-a"><b>{{ r.tag }}</b>{{ r.a }}</span>
      </div>
    </div>
    <div class="oq-pk"><Peek who="finance" side="right" :show="props.stage >= 4" say="tokens = money" :size="100" at="78%" /></div>
  </div>
</template>

<style scoped>
.oq { position: relative; display: grid; grid-template-columns: 170px 1fr; gap: 1.6rem; align-items: center; margin-top: 0.8rem; margin-right: 165px; }
.oq-who { display: flex; flex-direction: column; align-items: center; gap: 0.4rem; }
.oq-who span { font-size: 0.72rem; font-weight: 700; color: var(--green-ink); text-transform: uppercase; letter-spacing: 0.1em; }
.oq-rows { display: flex; flex-direction: column; gap: 0.7rem; }
.oq-row { display: grid; grid-template-columns: 13rem 1.6rem 1fr; align-items: center; }
.oq-q { display: flex; align-items: center; gap: 0.6rem; font-family: var(--mono); font-size: 0.95rem; background: var(--code-bg); color: #EDEDED; padding: 0.55rem 0.8rem; border-radius: 8px; }
.oq-q i { width: 9px; height: 9px; border-radius: 50%; background: var(--orange); flex: none; }
.oq-arrow { text-align: center; color: var(--ink-dim); opacity: 0; transition: opacity 0.4s; }
.oq-a { white-space: nowrap; display: flex; flex-direction: column; gap: 0.1rem; padding: 0.45rem 0.9rem; border-radius: 8px; background: var(--green-soft); font-size: 1.15rem; opacity: 0; transform: translateX(-12px); transition: opacity 0.45s, transform 0.45s; }
.oq-a b { font-size: 0.62rem; font-weight: 700; color: var(--green-ink); text-transform: uppercase; letter-spacing: 0.08em; }
.oq-row.on .oq-a, .oq-row.on .oq-arrow { opacity: 1; transform: none; }
.oq-pk { position: absolute; top: 0; bottom: 0; right: -150px; width: 1px; }
</style>
