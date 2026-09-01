---
name: dealos-expansion
description: "DealOS governed wrapper. After a deal closes, measure value, detect renewal/upsell/referral opportunities, and keep recurring revenue healthy."
version: 1.0.0
---
# dealos-expansion

## Purpose
After a deal closes, measure value, detect renewal/upsell/referral opportunities, and keep recurring revenue healthy.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/tls-customer-success-expansion-agent/SKILL.md`
- `skills/source_505/ibm-sales-ext-customer-renewal-risk-route/SKILL.md`
- `skills/source_505/ibm-sales-ext-customer-value-realization-evidence/SKILL.md`

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
