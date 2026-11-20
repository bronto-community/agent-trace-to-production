<template>
  <div class="slidev-layout pk-quote">
    <img class="pk-quote-marks" src="/img/packt/quotes.svg" alt="" />
    <img class="pk-mark" src="/img/packt/p-mark.svg" alt="" />
    <div class="pk-quote-text"><slot /></div>
    <div v-if="$frontmatter.by" class="pk-quote-by">- {{ $frontmatter.by }}</div>
  </div>
</template>
