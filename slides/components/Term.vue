<script setup lang="ts">
// A live terminal in the slide: an iframe onto ttyd (start it with ./demo-terminal.sh).
//   type  the short demo command to type, shown above the terminal
//   runs  one line saying what that command does
withDefaults(defineProps<{ type?: string; runs?: string; h?: string; port?: number }>(), { h: '335px', port: 7681 })
</script>

<template>
  <div class="term">
    <p v-if="type" class="term-hint"><b>type</b><code>{{ type }}</code><span>{{ runs }}</span></p>
    <div class="term-box" :style="{ height: h }">
      <span class="term-off">Terminal not running. Start it with <code>./demo-terminal.sh</code> in slides/.</span>
      <iframe :src="`http://127.0.0.1:${port}/`" title="terminal" />
    </div>
  </div>
</template>

<style scoped>
.term-hint { display: flex; align-items: center; gap: 0.7rem; margin: 0 0 0.4rem; font-size: 0.85rem; color: var(--ink-dim); }
.term-hint b { background: var(--orange); color: #fff; padding: 0.1rem 0.6rem; border-radius: 999px; font-size: 0.72rem; }
.term-hint code { font-size: 0.95rem; font-weight: 700; color: var(--ink); background: var(--surface); padding: 0.1rem 0.5rem; border-radius: 5px; }
.term-box { position: relative; border-radius: 10px; overflow: hidden; background: #1c1c1c; }
.term-off { position: absolute; inset: 0; display: grid; place-content: center; color: #8a8a8a; font-size: 0.85rem; }
.term-off code { color: #fff; }
.term-box iframe { position: relative; width: 100%; height: 100%; border: 0; display: block; }
</style>
