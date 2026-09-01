---
name: dealos-proposal-factory
description: "DealOS governed wrapper. Generate evidence-grounded capability packages, compliance matrices, proposals and SOW drafts from approved source material."
version: 1.0.0
---
# dealos-proposal-factory

## Purpose
Generate evidence-grounded capability packages, compliance matrices, proposals and SOW drafts from approved source material.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/ibm-sales-ext-commercial-proposal-release-qa/SKILL.md`
- `skills/source_505/enterprise-sales-playbook/SKILL.md`
- `skills/source_505/ibm-sales-ext-evidence-artifact-quality/SKILL.md`

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
