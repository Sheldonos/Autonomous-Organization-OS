---
name: dealos-governor
description: "DealOS governed wrapper. Allocate system attention by expected value, probability, deadline, effort and risk. Enforce autonomy/compliance policies. Never bypass a gate."
version: 1.0.0
---
# dealos-governor

## Purpose
Allocate system attention by expected value, probability, deadline, effort and risk. Enforce autonomy/compliance policies. Never bypass a gate.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/autonomous-capitalist/SKILL.md`
- `skills/source_505/ibm-sales-adaptive-orchestrator/SKILL.md`
- `skills/source_505/ibm-sales-agentic-orchestration/SKILL.md`
- `skills/source_505/ibm-sales-ext-ops-pipeline-governance/SKILL.md`

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
