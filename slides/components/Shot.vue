<script setup lang="ts">
// A real screenshot from the lab, with optional highlight boxes.
//   src    path under /img/shots
//   marks  [{ x, y, w, h, label? }] in percent of the image
//   pending  text shown instead of the image while the capture is still missing
withDefaults(defineProps<{ src?: string; marks?: { x: number; y: number; w: number; h: number; label?: string; tone?: string; at?: string; ls?: string }[]; pending?: string; h?: string }>(), { marks: () => [], h: 'auto' })
</script>

<template>
  <div v-if="pending" class="shot-pending"><span class="todo">SCREENSHOT PENDING</span><p>{{ pending }}</p></div>
  <div v-else class="shot" :style="{ height: h }">
    <img :src="src" alt="" />
    <i v-for="(m, i) in marks" :key="i" class="shot-mark" :class="[m.tone, m.at]" :style="{ left: m.x + '%', top: m.y + '%', width: m.w + '%', height: m.h + '%' }"><b v-if="m.label" :style="m.ls">{{ m.label }}</b></i>
  </div>
</template>

<style scoped>
.shot { position: relative; display: inline-block; max-width: 100%; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; line-height: 0; }
.shot img { display: block; max-width: 100%; height: 100%; }
.shot-mark { position: absolute; border: 3px solid var(--orange); border-radius: 6px; box-shadow: 0 0 0 9999px rgba(255, 255, 255, 0); }
.shot-mark b { position: absolute; left: -3px; top: -1.5rem; background: var(--orange); color: #fff; font: 700 0.7rem/1.3rem var(--sans); padding: 0 0.5em; border-radius: 4px; white-space: nowrap; font-style: normal; }
.shot-mark.ok { border-color: var(--green); background: rgba(0, 205, 143, 0.08); }
.shot-mark.ok b { background: var(--green-ink); }
.shot-mark.bad { background: rgba(250, 112, 64, 0.1); }
.shot-mark.right b { left: calc(100% + 8px); top: 50%; transform: translateY(-50%); }
.shot-mark.left b { left: auto; right: calc(100% + 8px); top: 50%; transform: translateY(-50%); }
.shot-mark.below b { top: calc(100% + 4px); }
.shot-mark.ibr b { top: auto; bottom: 3px; left: auto; right: 3px; }
.shot-mark.in b { top: 3px; left: auto; right: 3px; }
.shot-pending { border: 2px dashed var(--border); border-radius: 10px; padding: 2.2rem 1.5rem; text-align: center; color: var(--ink-dim); }
.shot-pending p { margin: 0.6rem 0 0; font-size: 0.95rem; }
</style>
