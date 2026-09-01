---
name: dealos-negotiator
description: "DealOS governed wrapper. Negotiate only inside explicit commercial and legal envelopes. Escalate terms outside the envelope. Never claim authority to sign."
version: 1.0.0
---
# dealos-negotiator

## Purpose
Negotiate only inside explicit commercial and legal envelopes. Escalate terms outside the envelope. Never claim authority to sign.

## Mandatory controls
1. Load current deal/opportunity state and policies.
2. Separate evidence from inference.
3. Return a deterministic `action_request` instead of directly holding credentials.
4. Run compliance/autonomy evaluation before any external side effect.
5. Append an audit event.
6. Respect owner approval and suppression state.

## Source skills composed
- `skills/source_505/tls-contract-intelligence-negotiation-agent/SKILL.md`
- `skills/source_505/ibm-sales-ext-commercial-redline-boundary/SKILL.md`
- `skills/source_505/ibm-sales-ext-commercial-pricing-discount-guardrail/SKILL.md`

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
