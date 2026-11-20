<template>
  <div class="slidev-layout pk-waiting">
    <div class="pk-starting">Starting Now <i><svg viewBox="0 0 16 16" width="11" height="11"><path d="M6 3.5 10.5 8 6 12.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></i></div>
    <img class="pk-wordmark" src="/img/packt/packt-wordmark.svg" alt="packt" />
    <div class="pk-band">{{ $frontmatter.headline }}</div>
    <p class="pk-blurb">{{ $frontmatter.blurb }}</p>
    <div class="pk-wait-who">
      <div><b>{{ $frontmatter.name }}</b><span>{{ $frontmatter.role }}</span></div>
      <img class="pk-photo" :src="$frontmatter.photo" alt="" />
    </div>
  </div>
</template>
