// Trace shapes used across the deck, from the Session 1 bookshop support agent
// (github.com/ollygarden-demo/instrumenting-the-agent) and our fork of it
// (../demo/agent.py). Span names and services are as emitted. Timings, tokens
// and order IDs are from real runs on 18 Nov 2026 (deepseek/deepseek-v4-flash via
// OpenRouter), rounded; `normal` is the Session 1 step 4 trace (4.2 s, 1,316 tokens).
// The MCP handshake spans stay in every trace: step 2 only filters the separate
// one-span notifications/initialized trace.
//
// start / dur in ms. tone: '' normal · hot (the problem) · err · dim · ok

export interface Row {
  name: string
  svc: string
  depth: number
  start: number
  dur: number
  tone?: '' | 'hot' | 'err' | 'dim' | 'ok'
  note?: string
}

const CHAT = 'chat deepseek/deepseek-v4-flash'
const A = 'bookshop-agent'
const S = 'bookshop-mcp'

export const traces: Record<string, Row[]> = {
  // Where Session 1 ends: step 4, one run, two processes, one trace
  normal: [
    { name: 'invoke_agent bookshop-support', svc: A, depth: 0, start: 0, dur: 4200, note: '1,316 in · 289 out · $0.00015' },
    { name: 'MCP send initialize', svc: A, depth: 1, start: 10, dur: 240 },
    { name: 'MCP send tools/list', svc: A, depth: 1, start: 260, dur: 30 },
    { name: 'retrieval book-catalog', svc: A, depth: 1, start: 300, dur: 15 },
    { name: CHAT, svc: A, depth: 1, start: 320, dur: 1500 },
    { name: 'execute_tool check_inventory', svc: A, depth: 1, start: 1830, dur: 175 },
    { name: 'tools/call check_inventory', svc: S, depth: 2, start: 1840, dur: 155 },
    { name: 'execute_tool get_order_status', svc: A, depth: 1, start: 2010, dur: 320, tone: 'err', note: 'tool_error' },
    { name: 'tools/call get_order_status', svc: S, depth: 2, start: 2020, dur: 305, tone: 'err' },
    { name: CHAT, svc: A, depth: 1, start: 2340, dur: 1850 },
  ],

  // Failure 1 (FAILURE=slow): the vector store times out after 12 s, the agent
  // carries on with no catalog context. Real run, 19 Nov, trace b9851549.
  slow: [
    { name: 'invoke_agent bookshop-support', svc: A, depth: 0, start: 0, dur: 21310, tone: 'hot', note: '21.3 s · no error' },
    { name: 'MCP send initialize', svc: A, depth: 1, start: 20, dur: 1000 },
    { name: 'MCP send tools/list', svc: A, depth: 1, start: 1018, dur: 3 },
    { name: 'retrieval book-catalog', svc: A, depth: 1, start: 1021, dur: 12005, tone: 'hot', note: '12.0 s · 0 documents' },
    { name: CHAT, svc: A, depth: 1, start: 13030, dur: 1930 },
    { name: 'execute_tool get_order_status', svc: A, depth: 1, start: 14960, dur: 320 },
    { name: CHAT, svc: A, depth: 1, start: 15284, dur: 2540 },
    { name: 'execute_tool check_inventory ×2', svc: A, depth: 1, start: 17825, dur: 318 },
    { name: CHAT, svc: A, depth: 1, start: 18144, dur: 2950, note: '"…the catalog returned no results"' },
  ],

  // Failure 2 (FAILURE=loop): one prompt line says "try other spellings until it works"
  loop: [
    { name: 'invoke_agent bookshop-support', svc: A, depth: 0, start: 0, dur: 9720, tone: 'hot', note: '4,457 tokens · 5 rounds' },
    { name: 'MCP send initialize', svc: A, depth: 1, start: 10, dur: 900 },
    { name: 'MCP send tools/list', svc: A, depth: 1, start: 920, dur: 40 },
    { name: 'retrieval book-catalog', svc: A, depth: 1, start: 970, dur: 2 },
    { name: CHAT, svc: A, depth: 1, start: 976, dur: 1478 },
    { name: 'execute_tool get_order_status', svc: A, depth: 1, start: 2610, dur: 306, tone: 'hot', note: '"ORD-1044" · not found' },
    { name: CHAT, svc: A, depth: 1, start: 2916, dur: 855 },
    { name: 'execute_tool get_order_status', svc: A, depth: 1, start: 3772, dur: 319, tone: 'hot', note: '"ORD1044" · not found' },
    { name: CHAT, svc: A, depth: 1, start: 4091, dur: 1420 },
    { name: 'execute_tool get_order_status ×3', svc: A, depth: 1, start: 5512, dur: 925, tone: 'hot', note: '"ord-1044", … · not found' },
    { name: CHAT, svc: A, depth: 1, start: 6438, dur: 1019 },
    { name: 'execute_tool check_inventory', svc: A, depth: 1, start: 7457, dur: 153 },
    { name: CHAT, svc: A, depth: 1, start: 7610, dur: 1958, note: '"…I couldn\'t find that order"' },
  ],

  // Failure 3 (FAILURE=wrong): no order number given, the model copies the
  // example from the tool description. 4 of 4 runs did this.
  wrong: [
    { name: 'invoke_agent bookshop-support', svc: A, depth: 0, start: 0, dur: 5540, tone: 'ok' },
    { name: 'MCP send initialize', svc: A, depth: 1, start: 10, dur: 750, tone: 'ok' },
    { name: 'MCP send tools/list', svc: A, depth: 1, start: 765, dur: 40, tone: 'ok' },
    { name: 'retrieval book-catalog', svc: A, depth: 1, start: 810, dur: 2, tone: 'ok' },
    { name: CHAT, svc: A, depth: 1, start: 812, dur: 1531, tone: 'ok' },
    { name: 'execute_tool check_inventory', svc: A, depth: 1, start: 2344, dur: 158, tone: 'ok' },
    { name: 'execute_tool get_order_status', svc: A, depth: 1, start: 2502, dur: 308, tone: 'hot', note: 'order_id "ORD-1042"' },
    { name: 'tools/call get_order_status', svc: S, depth: 2, start: 2504, dur: 305, tone: 'ok', note: 'shipped · DHL' },
    { name: CHAT, svc: A, depth: 1, start: 2811, dur: 2125, tone: 'ok', note: '"shipped via DHL"' },
  ],

  // Failure 4 (FAILURE=fallback): OpenRouter can't route to the primary and
  // answers with the fallback model. No error anywhere.
  path: [
    { name: 'invoke_agent bookshop-support', svc: A, depth: 0, start: 0, dur: 4450, note: '745 tokens · half the usual' },
    { name: 'MCP send initialize', svc: A, depth: 1, start: 10, dur: 630 },
    { name: 'MCP send tools/list', svc: A, depth: 1, start: 645, dur: 40 },
    { name: 'retrieval book-catalog', svc: A, depth: 1, start: 690, dur: 2 },
    { name: CHAT, svc: A, depth: 1, start: 696, dur: 1663, tone: 'hot', note: 'gpt-4o-mini answered' },
    { name: 'execute_tool check_inventory', svc: A, depth: 1, start: 2359, dur: 158 },
    { name: 'execute_tool get_order_status', svc: A, depth: 1, start: 2517, dur: 305 },
    { name: CHAT, svc: A, depth: 1, start: 2823, dur: 1466, tone: 'hot', note: 'gpt-4o-mini answered' },
  ],
}
