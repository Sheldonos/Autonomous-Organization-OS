---
name: dealos-opportunity-hunter
description: "DealOS governed wrapper. Continuously identify opportunities from approved sources, deduplicate them, record provenance, and queue only opportunities above configured relevance thresholds."
version: 1.0.0
---
# dealos-opportunity-hunter

## Purpose
Continuously identify opportunities from approved sources, deduplicate them, record provenance, and queue only opportunities above configured relevance thresholds.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/gov-contract-broker/SKILL.md`
- `skills/source_505/tls-territory-intelligence-agent/SKILL.md`
- `skills/source_505/tls-strategic-intelligence-agent/SKILL.md`
- `skills/source_505/ibm-bob-lead-intelligence/SKILL.md`

## Output contract
```json
{
  "summary": "...",
  "confidence": 0.0,
  "evidence": [],
  "recommended_next_action": "...",
  "action_request": null,
  "risk_level": "green|blue|yellow|orange|red",
  "requires_owner_approval": false
}
```
