<script setup lang="ts">
// A persona peeking in from the edge of the slide: half hidden, slides in
// when `show` turns true. Position it inside a `position: relative` parent;
// it sits just past that parent's edge.
withDefaults(defineProps<{ who: string; side?: 'right' | 'left' | 'bottom'; say?: string; show?: boolean; size?: number; at?: string }>(), {
  side: 'right', show: false, size: 110, at: '50%',
})
const NAMES: Record<string, string> = { oncall: 'Ops', finance: 'Finance', security: 'Security' }
</script>

<template>
  <div class="pk" :class="[side, { show }]" :style="{ '--s': size + 'px', '--at': at }">
    <span v-if="say" class="pk-say">{{ say }}</span>
    <Portrait :who="who" :size="size" />
    <span class="pk-name">{{ NAMES[who] }}</span>
  </div>
</template>

<style scoped>
.pk { position: absolute; z-index: 5; display: flex; flex-direction: column; align-items: center; gap: 0.25rem; opacity: 0; transition: transform 0.55s cubic-bezier(.2,.8,.2,1), opacity 0.4s; pointer-events: none; }
.pk.right { right: calc(var(--s) * -0.55); top: var(--at); transform: translate(60%, -50%) rotate(-8deg); }
.pk.right.show { transform: translate(0, -50%) rotate(-8deg); opacity: 1; }
.pk.left { left: calc(var(--s) * -0.55); top: var(--at); transform: translate(-60%, -50%) rotate(8deg); }
.pk.left.show { transform: translate(0, -50%) rotate(8deg); opacity: 1; }
.pk.bottom { bottom: calc(var(--s) * -0.45); right: 8%; transform: translateY(70%); }
.pk.bottom.show { transform: translateY(0); opacity: 1; }
.pk-name { font-size: 0.62rem; color: var(--ink-dim); text-transform: uppercase; letter-spacing: 0.08em; }
.pk-say { position: relative; background: var(--ink); color: var(--bg); font-size: 0.66rem; padding: 0.25rem 0.6rem; border-radius: 10px; white-space: nowrap; }
.pk-say::after { content: ''; position: absolute; left: 50%; bottom: -5px; margin-left: -5px; border: 5px solid transparent; border-bottom: none; border-top-color: var(--ink); }
</style>
