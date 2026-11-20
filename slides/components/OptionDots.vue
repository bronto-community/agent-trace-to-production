<script setup lang="ts">
// 60 runs, 6 of them the ones you will need later. What is left under each option?
//   all   every run, complete            head  a random tenth, decided up front
//   tail  the runs a rule picked         lean  every run, without its content
const props = defineProps<{ mode: 'all' | 'head' | 'tail' | 'lean' }>()
const hot = new Set([7, 19, 26, 38, 44, 53])
const head = new Set([3, 14, 22, 35, 47, 58])
const base = new Set([11, 30, 49])
function cls(i: number) {
  const h = hot.has(i)
  if (props.mode === 'all') return h ? 'hot' : 'on'
  if (props.mode === 'head') return head.has(i) ? 'on' : 'gone'
  if (props.mode === 'tail') return h ? 'hot' : base.has(i) ? 'on' : 'gone'
  return h ? 'hot lean' : 'lean'
}
</script>

<template>
  <div class="od"><i v-for="i in 60" :key="i" :class="cls(i - 1)" /></div>
</template>

<style scoped>
.od { display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; padding: 0.7rem; background: var(--surface); border-radius: 12px; }
.od i { display: block; aspect-ratio: 1; border-radius: 4px; background: #BDBDBD; }
.od i.hot { background: var(--orange); }
.od i.gone { background: transparent; box-shadow: inset 0 0 0 1px #DDDDDD; }
.od i.lean { background: transparent; box-shadow: inset 0 0 0 2px #9A9A9A; }
.od i.hot.lean { box-shadow: inset 0 0 0 2px var(--orange); }
</style>
