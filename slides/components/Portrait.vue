<script setup lang="ts">
// One persona portrait (Open Peeps, public/img/people), on a round backdrop.
// Shared by every persona component so they look the same everywhere.
// `face`: zoom in on the face, for small sizes (agenda, header tags). The
// figures are busts drawn low in their canvas, so each needs its own centre.
const props = withDefaults(defineProps<{ who: string; size?: number; dark?: boolean; face?: boolean }>(), { size: 120, dark: false, face: false })
const FACE: Record<string, [number, number]> = { oncall: [0.53, 0.64], finance: [0.56, 0.66], security: [0.55, 0.69] }
const ZOOM = 1.3
function faceStyle() {
  const [fx, fy] = FACE[props.who] ?? [0.5, 0.6]
  return { width: `${ZOOM * 100}%`, height: `${ZOOM * 100}%`, left: `${(0.5 - fx * ZOOM) * 100}%`, top: `${(0.5 - fy * ZOOM) * 100}%` }
}
</script>

<template>
  <div class="pt" :class="{ dark, face }" :style="{ width: size + 'px', height: size + 'px' }">
    <img :src="`/img/people/${who}.svg`" alt="" :style="face ? faceStyle() : undefined" />
  </div>
</template>

<style scoped>
.pt { position: relative; display: inline-block; flex: none; border-radius: 50%; background: var(--sand); overflow: hidden; }
.pt.dark { background: #EDEDED; }
.pt img { width: 100%; height: 100%; object-fit: cover; object-position: center 18%; display: block; }
.pt.face img { position: absolute; max-width: none; object-fit: contain; }
</style>
