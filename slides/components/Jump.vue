<script setup lang="ts">
// Links on the right border of a slide, for the places where the talk jumps to a UI.
//   to  [{ label, url }]  (opens in a new tab)
defineProps<{ to: { label: string; url: string }[] }>()
</script>

<template>
  <div class="jump"><a v-for="j in to" :key="j.url" :href="j.url" target="_blank" rel="noopener">{{ j.label }} ↗</a></div>
</template>

<style scoped>
.jump { position: absolute; right: -55px; top: 0; display: flex; flex-direction: column; gap: 0.5rem; z-index: 5; }
.jump a { writing-mode: vertical-rl; background: var(--ink); color: #fff !important; font: 700 0.68rem/1 var(--sans); padding: 0.7rem 0.42rem; border-radius: 6px 0 0 6px; text-decoration: none !important; border: 0 !important; white-space: nowrap; }
.jump a:hover { background: var(--orange); }
</style>
