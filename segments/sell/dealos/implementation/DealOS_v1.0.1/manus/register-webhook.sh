#!/usr/bin/env bash
set -euo pipefail
: "${MANUS_API_KEY:?set MANUS_API_KEY}"
: "${MANUS_WEBHOOK_URL:?set MANUS_WEBHOOK_URL}"
curl -sS -X POST "https://api.manus.ai/v2/webhook.create" \
  -H "x-manus-api-key: ${MANUS_API_KEY}" \
  -H "content-type: application/json" \
  --data "{\"url\":\"${MANUS_WEBHOOK_URL}\"}"
echo
