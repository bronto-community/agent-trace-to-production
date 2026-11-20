<script setup lang="ts">
// "Who cares": stage 1 Ops, stage 2 Finance, stage 3 Security. Pass $clicks.
const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 0 })
const people = [
  { who: 'oncall', name: 'Ops', q: "What's broken?", at: 1 },
  { who: 'finance', name: 'Finance', q: 'What does it cost?', at: 2 },
  { who: 'security', name: 'Security', q: 'What did it do? What are we storing?', at: 3 },
]
</script>

<template>
  <div class="wc">
    <div v-for="p in people" :key="p.who" class="wc-col" :class="{ on: props.stage >= p.at, minor: p.minor }">
      <Portrait :who="p.who" :size="p.minor ? 115 : 165" />
      <span class="wc-name">{{ p.name }}</span>
      <span class="wc-q">{{ p.q }}</span>
    </div>
  </div>
</template>

<style scoped>
.wc { position: relative; display: grid; grid-template-columns: 1fr 1fr 1fr; align-items: start; column-gap: 2rem; margin-top: 0.2rem; padding-bottom: 2.6rem; }
.wc-col { display: flex; flex-direction: column; align-items: center; gap: 0.35rem; text-align: center; opacity: 0.08; transform: translateY(14px); transition: opacity 0.5s, transform 0.5s; }
.wc-col.on { opacity: 1; transform: none; }
.wc-col.minor.on { opacity: 0.72; }
.wc-name { margin-top: 0.4rem; font-size: 0.72rem; font-weight: 700; color: var(--green-ink); text-transform: uppercase; letter-spacing: 0.1em; }
.wc-q { font-size: 1.5rem; line-height: 1.15; font-weight: 500; }
.minor .wc-q { font-size: 1.15rem; color: var(--ink-dim); }
.wc-why { position: absolute; left: 0; width: calc((100% - 4rem) * 2 / 2.75 + 2rem); bottom: 0; text-align: center; opacity: 0; transition: opacity 0.5s 0.15s; }
.wc-why.on { opacity: 1; }
.wc-why i { display: block; height: 12px; border: 1.5px solid var(--ink); border-top: none; border-radius: 0 0 8px 8px; margin: 0 6%; }
.wc-why span { display: inline-block; margin-top: 0.35rem; font-family: var(--mono); font-size: 0.95rem; color: var(--ink-dim); }
</style>
