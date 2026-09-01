# Manus Integration

DealOS uses Manus only as an optional high-cost deep research/browser worker.

## API

Base: `https://api.manus.ai`
Authentication header: `x-manus-api-key: <key>`

Task creation uses `/v2/task.create` with:

```json
{
  "message": {"content": "..."},
  "agent_profile": "manus-1.6-lite",
  "interactive_mode": false,
  "hide_in_task_list": true,
  "share_visibility": "private",
  "structured_output_schema": {}
}
```

## Webhook

Register:

```text
https://YOUR_DEALOS_DOMAIN/hooks/manus
```

DealOS verifies `X-Webhook-Signature` and `X-Webhook-Timestamp`, rejects stale requests, hashes the raw body and validates the RSA-SHA256 signature against Manus's public webhook key.

## Cost control

Manus is not the default research path. `policies/model_routing.yaml` requires both a research need and expected value above `MANUS_MIN_EXPECTED_VALUE_USD`.
