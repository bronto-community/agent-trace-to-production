<template>
  <div class="slidev-layout pk-agenda">
    <div class="pk-agenda-l">
      <i class="pk-hero-rule" />
      <h1>Agenda</h1>
      <div class="pk-agenda-bits"><i /><i /><i class="b" /><i class="g" /></div>
    </div>
    <div class="pk-agenda-r">
      <img class="pk-mark" src="/img/packt/p-mark.svg" alt="" />
      <!-- items: plain strings, or { t, who, d } for a chapter with its persona -->
      <ol :class="{ 'pk-ag-who': $frontmatter.items.some(it => typeof it === 'object') }">
        <li v-for="(it, i) in $frontmatter.items" :key="i">
          <span>{{ String(i + 1).padStart(2, '0') }}</span>
          <template v-if="typeof it === 'string'">{{ it }}</template>
          <template v-else>
            <Portrait v-if="it.who" class="pk-ag-pt" :who="it.who" :size="44" face />
            <div v-else-if="it.icon === 'trace'" class="pk-ag-ic" title="the trace from Session 1">
              <i style="left: 8px; width: 28px" /><i style="left: 12px; width: 6px" /><i style="left: 16px; width: 14px" /><i style="left: 22px; width: 12px" />
            </div>
            <div v-else-if="it.icon === 'check'" class="pk-ag-ic ck" title="the checklist">
              <b>✓</b><i style="left: 22px; width: 12px" /><b>✓</b><i style="left: 22px; width: 12px" /><b>✓</b><i style="left: 22px; width: 12px" />
            </div>
            <i v-else class="pk-ag-gap" />
            <b>{{ it.t }}</b><em v-if="it.d">{{ it.d }}</em>
          </template>
        </li>
      </ol>
    </div>
  </div>
</template>

<style>
.pk-ag-who li { display: flex; align-items: center; gap: 0.7rem; min-height: 3.1rem; }
.pk-ag-who li b { font-weight: 500; }
.pk-ag-who .pk-ag-gap { display: block; width: 44px; flex: none; }
.pk-ag-who li em { font-style: normal; color: #6A6A6A; font-size: 0.9rem; margin-left: auto; }
.pk-ag-who li span { top: 50% !important; transform: translateY(-50%); }
/* Intro: a mini trace waterfall in the same circle as the portraits */
.pk-ag-ic { position: relative; flex: none; width: 44px; height: 44px; border-radius: 50%; background: var(--green-soft); }
.pk-ag-ic i { position: absolute; display: block; height: 4px; border-radius: 2px; background: var(--green-ink); }
.pk-ag-ic i:nth-child(1) { top: 12px; } .pk-ag-ic i:nth-child(2) { top: 18px; } .pk-ag-ic i:nth-child(3) { top: 24px; } .pk-ag-ic i:nth-child(4) { top: 30px; }
/* Summary: a mini checklist, same circle */
.pk-ag-ic.ck b { position: absolute; left: 10px; font-size: 7px; line-height: 7px; color: var(--green-ink); font-weight: 700; }
.pk-ag-ic.ck b:nth-of-type(1) { top: 11px; } .pk-ag-ic.ck b:nth-of-type(2) { top: 19px; } .pk-ag-ic.ck b:nth-of-type(3) { top: 27px; }
.pk-ag-ic.ck i:nth-of-type(1) { top: 13px; } .pk-ag-ic.ck i:nth-of-type(2) { top: 21px; } .pk-ag-ic.ck i:nth-of-type(3) { top: 29px; }
.pk-ag-ic.ck i { height: 3px; }
</style>
