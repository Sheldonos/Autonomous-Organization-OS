---
name: dealos-outreach
description: "DealOS governed wrapper. Create personalized, truthful outreach inside volume/suppression rules. Optimize for qualified replies, not send volume."
version: 1.0.0
---
# dealos-outreach

## Purpose
Create personalized, truthful outreach inside volume/suppression rules. Optimize for qualified replies, not send volume.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/b2b-personalized-outreach/SKILL.md`
- `skills/source_505/tls-outreach-execution-agent/SKILL.md`
- `skills/source_505/enterprise-sales-playbook/SKILL.md`

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
