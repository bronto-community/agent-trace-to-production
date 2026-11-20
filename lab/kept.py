"""Which runs did the sampler keep?

Jaeger sits before the sampler and sees every run. The sink stands in for your backend and
receives only what the sampler let through (it writes to out/traces.jsonl). This prints one
line per run from the last hour: kept or dropped, with what a sampling policy could have seen.

    python3 kept.py

It needs the default backend, the local sink. With BACKEND_ENDPOINT pointing somewhere else,
out/traces.jsonl stays empty and every run shows as dropped.
"""
import datetime
import json
import urllib.parse
import urllib.request

JAEGER = "http://localhost:16686/api/v3/traces?"


def spans_of(resource_spans):
    for rs in resource_spans:
        for ss in rs["scopeSpans"]:
            yield from ss["spans"]


def attributes(span):
    return {a["key"]: next(iter(a["value"].values())) for a in span.get("attributes", [])}


def seconds(span):
    return (int(span["endTimeUnixNano"]) - int(span["startTimeUnixNano"])) / 1e9


kept = set()
try:
    with open("out/traces.jsonl") as sink:
        for line in sink:
            kept.update(s["traceId"] for s in spans_of(json.loads(line)["resourceSpans"]))
except FileNotFoundError:
    pass

now = datetime.datetime.now(datetime.timezone.utc)
query = urllib.parse.urlencode({
    "query.service_name": "bookshop-agent",
    "query.start_time_min": (now - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "query.start_time_max": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "query.search_depth": "200",
})
runs = {}
for span in spans_of(json.load(urllib.request.urlopen(JAEGER + query))["result"]["resourceSpans"]):
    runs.setdefault(span["traceId"], []).append(span)

rows = []
for trace_id, spans in runs.items():
    root = next((s for s in spans if s["name"].startswith("invoke_agent")), None)
    if root is None:
        continue
    a = attributes(root)
    retrieval = next((seconds(s) for s in spans if s["name"].startswith("retrieval")), 0.0)
    checks = [attributes(s).get("bookshop.check.order_owned") for s in spans]
    rows.append((int(root["startTimeUnixNano"]), trace_id in kept, a.get("gen_ai.usage.input_tokens", "?"),
                 retrieval, False in checks, a.get("bookshop.run.tools", "").strip()))

for _, is_kept, tokens, retrieval, failed_check, tools in sorted(rows):
    print(f"{'KEPT   ' if is_kept else 'dropped'}  input tokens {tokens:>5}  retrieval {retrieval:4.1f}s  "
          f"{'check FAILED  ' if failed_check else ''}tools: {tools}")
print(f"{len(rows)} runs in Jaeger, {sum(r[1] for r in rows)} kept by the sampler")
