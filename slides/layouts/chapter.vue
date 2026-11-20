<template>
  <div class="slidev-layout pk-hero pk-chapter">
    <img class="pk-wordmark" src="/img/packt/packt-wordmark.svg" alt="packt" />
    <div class="pk-ch-text">
      <i class="pk-hero-rule" />
      <span class="pk-ch-label">{{ $frontmatter.chapter }}</span>
      <h1>{{ $frontmatter.question }}</h1>
      <slot />
    </div>
    <div class="pk-ch-who"><Portrait :who="$frontmatter.who" :size="210" dark /></div>
    <!-- `pipeline: n` shows the Collector built so far, chapter n lit up -->
    <div v-if="$frontmatter.pipeline" class="pk-section-pl">
      <Pipeline :at="$frontmatter.pipeline" />
    </div>
  </div>
</template>

<style>
.pk-chapter .pk-ch-text { position: absolute; left: 55px; top: 110px; width: 52%; }
.pk-chapter .pk-ch-label { display: block; margin-top: 0.2rem; font-size: 0.85rem; color: var(--green); text-transform: uppercase; letter-spacing: 0.12em; }
.slidev-layout.pk-chapter h1 { font-weight: 400; font-size: 2.9rem; line-height: 1.15; margin: 0.4rem 0 0; color: #fff; }
.pk-chapter .pk-ch-who { position: absolute; right: 120px; top: 70px; border-radius: 50%; box-shadow: 0 0 0 4px var(--green); }
.pk-chapter .pk-section-pl { top: 335px; }
</style>
