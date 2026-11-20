<template>
  <div class="slidev-layout pk-about">
    <img class="pk-wordmark" src="/img/packt/packt-wordmark.svg" alt="packt" />
    <div class="pk-about-who">
      <img class="pk-photo" :src="$frontmatter.photo" alt="" />
      <b>{{ $frontmatter.name }}</b>
      <span>{{ $frontmatter.role }}</span>
    </div>
    <div class="pk-about-text"><slot /></div>
  </div>
</template>
