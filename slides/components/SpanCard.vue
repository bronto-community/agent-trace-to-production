<script setup lang="ts">
// One run's attributes (bookshop agent), as the debug exporter would show them.
// mode raw: content capture on, PII highlighted. mode clean: after the
// Collector's allow-list redaction + transform (step 2), values from a real run on 19 Nov. IDs survive on purpose (failure 3 needs them).
const props = withDefaults(defineProps<{ mode?: 'raw' | 'clean' }>(), { mode: 'raw' })

type A = { k: string; raw: string; clean?: string; pii?: boolean; keep?: boolean }
const attrs: A[] = [
  { k: 'gen_ai.operation.name', raw: 'chat' },
  { k: 'gen_ai.request.model', raw: 'deepseek/deepseek-v4-flash' },
  { k: 'gen_ai.usage.input_tokens', raw: '889' },
  { k: 'gen_ai.input.messages', raw: '[{"role":"user","parts":[{"content":"Hi, Maria Lopez here (maria.lopez@example.com). Which book should I buy…', clean: '<dropped> · bookshop.prompt.sha256 a917…f454', pii: true },
  { k: 'gen_ai.output.messages', raw: '[{"role":"assistant","parts":[{"content":"Hi Maria! I\'d recommend Observing LLM Applications…', clean: '<dropped: not on the allow-list>', pii: true },
  { k: 'gen_ai.tool.call.arguments', raw: '{"order_id":"ORD-1043"}', clean: '<dropped: not on the allow-list>', pii: true },
  { k: 'bookshop.order.id', raw: 'ORD-1043', keep: true },
  { k: 'bookshop.customer.id', raw: 'cus_2291', keep: true },
  { k: 'user.email', raw: 'maria.lopez@example.com', clean: '6d996f03fbd2…38fa (HMAC)', pii: true },
  { k: 'bookshop.llm.cost_usd', raw: '0.00021' },
]
</script>

<template>
  <div class="sp" :class="props.mode">
    <div class="sp-h"><b>one run · attributes from its chat and tool spans</b><span>{{ props.mode === 'raw' ? 'as exported · content capture on' : 'after the Collector' }}</span></div>
    <div v-for="a in attrs" :key="a.k" class="sp-row" :class="{ pii: a.pii, keep: a.keep }">
      <span class="sp-k">{{ a.k }}</span>
      <span class="sp-v">{{ props.mode === 'clean' && a.clean ? a.clean : a.raw }}</span>
    </div>
  </div>
</template>

<style scoped>
.sp { background: var(--surface); border-radius: 14px; box-shadow: var(--shadow); overflow: hidden; font-family: var(--mono); font-size: 0.66rem; }
.sp-h { display: flex; justify-content: space-between; padding: 0.45rem 0.9rem; background: var(--sand); color: var(--ink-dim); }
.sp-h b { color: var(--ink); font-weight: 600; }
.sp-row { display: grid; grid-template-columns: 13.5rem 1fr; gap: 0.8rem; padding: 0.28rem 0.9rem; border-top: 1px solid var(--sand); }
.sp-k { color: var(--ink-dim); }
.sp-v { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.raw .pii { background: var(--claim-soft); }
.raw .pii .sp-v { color: #A1300F; }
.clean .pii { background: var(--mint-soft); }
.clean .pii .sp-v { color: var(--mint-ink); }
.clean .keep .sp-k::after { content: '  kept'; color: var(--sapphire); font-weight: 600; }
</style>
