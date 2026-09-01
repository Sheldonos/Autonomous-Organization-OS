# Production Architecture

## Planes
1. **Goal/mission plane** — durable objectives, definitions of done, blockers and next-action state.
2. **Event plane** — durable event queue/broker, dedupe, backpressure, retries and DLQ. It wakes work; it does not keep a model running continuously.
3. **Federation plane** — EnterpriseOS routes objectives across 7 sectors / 48 pockets / 492 execution teams.
4. **Capability plane** — 3,212 canonical skills plus generated dynamic connector skills.
5. **Connector plane** — provider instances, schemas, trust state, read/write certification and read-back.
6. **Policy plane** — authority, approvals, global deny rules, budgets, kill switches and risk controls.
7. **State/evidence plane** — goals, jobs, events, effect receipts, outcomes, provenance, approvals and connector hashes.
8. **Evaluation/release plane** — validation, simulation, regression, security, provenance and promotion gates.
9. **Resilience/continuity plane** — drain, zero-downtime upgrades, rollback, backups, DR, hybrid/air-gap and egress controls.

## Execution rule
`DURABLE EVENT -> ONE BOUNDED JOB -> POLICY -> HYDRATE -> EXECUTE/DRAFT -> VERIFY -> DURABLE RECEIPT/EVIDENCE -> ACK`

Infrastructure queue consumers may remain online, but model/agent work is event-triggered and bounded. Low-frequency reconciliation exists only to catch missed events.

## Scaling rule
The shared substrate is a registry/archive, not one giant prompt. Job execution hydrates the smallest sufficient team bundle. Large blobs stay in object storage or their source systems; events carry references/hashes. Compute is placed near authoritative data where possible.

The bundled SQLite WAL state/event implementation is the standalone/local/cold-room profile. Multi-site/active-active deployments must bind tenant-approved HA transactional state and an external durable event bus. Readiness explicitly rejects presenting the standalone event queue as an HA configuration.

## Upgrade rule
Containers are disposable and immutable. State is external. Releases use digest-pinned images, drain consequential writes, pre-upgrade backups, expand-migrate-contract schemas, Green readiness/read-back tests and traffic cutover with a rollback window. Queued work/evidence survive a code rollback.

## Tenant production boundary
The software release can be production-ready; a tenant becomes production-certified only after its actual connector instances, credentials, permissions, data contracts, event/state backend, recovery paths, data-residency controls and external-write read-back tests pass.
