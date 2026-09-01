---
name: dealos-inbox
description: "DealOS governed wrapper. Classify inbound messages, update deal state, respond to routine messages, honor opt-outs, and escalate only true exceptions."
version: 1.0.0
---
# dealos-inbox

## Purpose
Classify inbound messages, update deal state, respond to routine messages, honor opt-outs, and escalate only true exceptions.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/ibm-sales-agentic-orchestration/SKILL.md`
- `skills/source_505/ibm-sales-ext-evidence-claim-adjudicate/SKILL.md`
- `skills/source_505/tls-lead-tracker-analytics-agent/SKILL.md`

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
