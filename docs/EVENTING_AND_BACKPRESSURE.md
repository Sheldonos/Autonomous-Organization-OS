# Eventing, Bite-Sized Execution & Backpressure

FAOS must not keep a model "thinking" continuously. Infrastructure processes may stay alive, but expensive/agentic execution occurs only because a durable event or schedule created a bounded job.

## Default execution contract
`EVENT -> DURABLE QUEUE -> DEDUPE -> CLAIM -> ONE BOUNDED JOB -> VERIFY -> COMMIT EVIDENCE -> ACK`

Every job has a definition of done and terminates. Follow-on work requires another durable event, an explicit schedule, or a reconciliation event. Job completion never creates an unbounded recursive prompt chain.

## Event sources
- goal created/changed;
- connector/MCP capability changed or became certified;
- webhook from an enterprise system;
- schedule/obligation due;
- telemetry threshold or SLO breach;
- deployment/restore completed;
- evaluation or policy gate failed;
- human approval changed state.

## Durability pattern
The embedded runtime implements a transactional durable event queue with dedupe, retry and dead-letter behavior. For larger deployments use a durable broker (Kafka-compatible/IBM Event Streams, or another approved enterprise event bus) and keep the same event envelope. The SQLite queue is the standalone/local fallback, not an active-active multi-site broker.

## Required semantics
- idempotency key on every consequential effect;
- at-least-once delivery assumed;
- consumer must tolerate duplicates;
- exponential retry with bounded attempts;
- poison messages move to DLQ, never retry forever;
- payloads should contain references/hashes, not multi-GB objects;
- backpressure may delay work rather than overflow context, spend, memory or downstream APIs;
- per-tenant/pocket concurrency and spend quotas;
- replay must be deterministic wherever possible.

## Reconciliation
A low-frequency reconciliation event is permitted as a safety net for missed webhooks. It is not the primary work loop and should normally run every 30–60 minutes or longer, depending on business RTO.
