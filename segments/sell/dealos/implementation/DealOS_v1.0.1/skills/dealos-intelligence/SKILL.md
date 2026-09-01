---
name: dealos-intelligence
description: "DealOS governed wrapper. Build evidence-backed company, buyer, seller, prime, subcontractor and opportunity dossiers. Distinguish verified facts from inference."
version: 1.0.0
---
# dealos-intelligence

## Purpose
Build evidence-backed company, buyer, seller, prime, subcontractor and opportunity dossiers. Distinguish verified facts from inference.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/b2b-lead-intelligence-generator/SKILL.md`
- `skills/source_505/sales-seller-intelligence-mcp-integration/SKILL.md`
- `skills/source_505/tls-competitive-intelligence-battlecard-agent/SKILL.md`
- `skills/source_505/tls-contract-intelligence-negotiation-agent/SKILL.md`

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
