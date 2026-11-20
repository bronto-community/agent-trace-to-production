<script setup lang="ts">
// One receiver, two trace pipelines, in plain words.
//   step 0  only the every-run lane
//   step 1  the payload lane joins
//   redact  show the redaction step on both lanes (chapter 3)
withDefaults(defineProps<{ step?: number; redact?: boolean }>(), { step: 1, redact: false })
</script>

<template>
  <div class="tp">
    <div class="tp-src">
      <span class="k">Collector</span>
      <span class="d">every span of every run, with content</span>
    </div>
    <div class="tp-lanes">
      <div class="tp-lane">
        <span class="tp-tag meta">every run</span>
        <span class="n">drop the content</span><span class="a">→</span>
        <span v-if="redact" class="n hl">redact</span><span v-if="redact" class="a">→</span>
        <span class="n">derive metrics</span><span class="a">→</span>
        <span class="n dst"><b>bookshop-runs</b><br><small>metadata · long retention · ~5 KB a run</small></span>
      </div>
      <div class="tp-lane" :class="{ off: step < 1 }">
        <span class="tp-tag pay">some runs</span>
        <span class="n hl">tail sampling</span><span class="a">→</span>
        <span v-if="redact" class="n hl">redact</span><span v-if="redact" class="a">→</span>
        <span class="n ghost" /><span class="a" />
        <span class="n dst"><b>bookshop-payloads</b><br><small>full content · short retention · ~11 KB a kept run</small></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tp { display: grid; grid-template-columns: 9rem 1fr; gap: 1rem; align-items: center; margin-top: 1rem; }
.tp-src { display: flex; flex-direction: column; gap: 0.3rem; padding: 0.9rem; border-radius: 14px; background: var(--sand); }
.tp-src .k { font-weight: 700; font-size: 0.95rem; }
.tp-src .d { font-size: 0.75rem; color: var(--ink-dim); }
.tp-lanes { display: flex; flex-direction: column; gap: 0.9rem; }
.tp-lane { display: flex; align-items: center; gap: 0.5rem; transition: opacity 0.4s; }
.tp-lane.off { opacity: 0.12; }
.tp-tag { width: 5.6rem; flex: none; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
.tp-tag.meta { color: var(--green-ink); }
.tp-tag.pay { color: #B23F14; }
.n { padding: 0.5rem 0.7rem; border-radius: 10px; background: var(--surface); font-size: 0.85rem; white-space: nowrap; }
.n.hl { background: var(--orange-soft); }
.n.ghost { background: transparent; flex: 1; }
.n.dst { margin-left: auto; width: 17.5rem; flex: none; white-space: normal; background: var(--green-soft); font-size: 0.85rem; line-height: 1.35; }
.n.dst small { font-size: 0.68rem; color: var(--ink-dim); }
.a { color: var(--ink-dim); }
</style>
