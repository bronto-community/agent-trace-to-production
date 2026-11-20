#!/bin/bash
# Load the runs in saved-runs/ into the lab's Jaeger, with their original trace IDs.
# Use it on a machine that never produced them: `docker compose up -d`, then ./load-saved-runs.sh
# They go straight to Jaeger, not through the Collector, so nothing is sampled, masked or sent to a backend.
set -e
cd "$(dirname "$0")"
net=$(docker inspect "$(docker compose ps -q jaeger)" --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}')
for f in saved-runs/*.json; do
  id=$(basename "$f" .json); id=${id##*.}
  code=$(docker run --rm --network "$net" -v "$PWD/saved-runs:/runs:ro" curlimages/curl:8.11.1 -s -o /dev/null -w '%{http_code}' \
    -X POST http://jaeger:4318/v1/traces -H 'Content-Type: application/json' --data-binary "@/runs/$(basename "$f")")
  echo "$code  http://localhost:${JAEGER_UI_PORT:-16686}/trace/$id  ($(basename "$f"))"
done
