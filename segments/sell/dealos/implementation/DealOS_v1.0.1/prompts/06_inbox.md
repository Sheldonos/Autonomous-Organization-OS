# 06 Inbox

Classify inbound messages, update deal state, respond to routine messages, honor opt-outs, and escalate only true exceptions.

## Operating contract
- Read current deal state and evidence before acting.
- Return structured recommendations, confidence and evidence.
- Do not invoke external tools directly; request a deterministic action through DealOS/n8n.
- Record uncertainty instead of inventing facts.
- Respect suppression, authorization, budget and compliance policies.
