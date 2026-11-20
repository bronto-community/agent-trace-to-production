<script setup lang="ts">
// Packt content-slide chrome, measured from the Session 1 deck (1920×1080 → 980×552):
// section label + rule on top, the <p> mark top right, rule + "Pg: n" + an
// orange chevron at the bottom. `dark` is his black variant for code slides.
// `who` in a slide's frontmatter (security | finance | oncall) shows whose
// question the slide answers, as a small portrait next to the <p> mark.
defineProps<{ dark?: boolean }>()
const WHO: Record<string, string> = { security: 'Security', finance: 'Finance', oncall: 'On-call' }
</script>

<template>
  <div class="slidev-layout pk-frame" :class="{ 'pk-dark': dark }">
    <div class="pk-label">{{ $frontmatter.part }}</div>
    <i class="pk-rule top" />
    <img class="pk-mark" src="/img/packt/p-mark.svg" alt="" />
    <div v-if="$frontmatter.who" class="pk-who">
      <template v-for="w in [].concat($frontmatter.who)" :key="w">
        <Portrait :who="w" :size="34" face /><span>{{ WHO[w] }}</span>
      </template>
    </div>
    <div class="pk-body"><slot /></div>
    <i class="pk-rule bottom" />
    <div class="pk-pg">Pg: {{ $page }}</div>
    <div class="pk-next">&gt;</div>
  </div>
</template>
