---
name: dealos-partner-matcher
description: "DealOS governed wrapper. Translate requirements into capabilities, identify likely delivery partners, verify evidence, compare fit/economics/risk, and coordinate introductions."
version: 1.0.0
---
# dealos-partner-matcher

## Purpose
Translate requirements into capabilities, identify likely delivery partners, verify evidence, compare fit/economics/risk, and coordinate introductions.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/tls-partner-ecosystem-channel-agent/SKILL.md`
- `skills/source_505/ibm-sales-ext-partner-cosell-plan/SKILL.md`
- `skills/source_505/ibm-sales-ext-partner-alliance-governance/SKILL.md`

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
