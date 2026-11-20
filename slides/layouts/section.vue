<template>
  <div class="slidev-layout pk-hero pk-section">
    <img class="pk-wordmark" src="/img/packt/packt-wordmark.svg" alt="packt" />
    <div class="pk-hero-text">
      <i class="pk-hero-rule" />
      <h1>{{ $frontmatter.section }}</h1>
      <slot />
    </div>
    <!-- `pipeline: n` shows the Collector built so far, part n lit up -->
    <div v-if="$frontmatter.pipeline" class="pk-section-pl">
      <Pipeline :at="$frontmatter.pipeline" />
    </div>
  </div>
</template>
