---
name: dealos-relationship-memory
description: "DealOS governed wrapper. Maintain normalized identities, organizations, relationship history, commitments, last contact, next action, and source provenance."
version: 1.0.0
---
# dealos-relationship-memory

## Purpose
Maintain normalized identities, organizations, relationship history, commitments, last contact, next action, and source provenance.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/ibm-sales-ext-identity-profile-reconcile/SKILL.md`
- `skills/source_505/ibm-sales-ext-data-source-catalog/SKILL.md`
- `skills/source_505/ibm-sales-ext-evidence-source-provenance/SKILL.md`

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
