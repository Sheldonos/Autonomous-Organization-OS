# Federated Autonomous Organization OS v1.2.0 — Final Resilient Production Release

v1.2.0 preserves the complete v1.1.0 capability/accountability release and adds the resilience/continuity architecture required for long-lived autonomous operation.

## Capability foundation retained
- 3,212 / 3,212 canonical skills, individually integrity-verified and accountable to the 7-sector / 48-pocket factory.
- 1,244 roles and 540 OS-factory wrapper skills.
- Embedded DealOS v1.0.1 with its original validation/test boundary intact.
- Adaptive MCP/tool assimilation, goal-directed proactivity, bounded worker execution and staged self-improvement.

## New in v1.2.0
- durable event queue with dedupe, retry, exponential backoff and dead-letter state;
- event-triggered goal advancement so model work is bite-sized rather than a continuous reasoning loop;
- low-frequency reconciliation retained only as a safety net;
- deployment drain/kill switch for external executor handoffs;
- durable effect-receipt contract for idempotent consequential actions;
- crash recovery for stale RUNNING jobs/events;
- zero-downtime blue/green/canary architecture with expand-migrate-contract schema rules;
- data-safe rollback/backout runbook that preserves queued work/evidence;
- verified SQLite backup/restore tooling for standalone/cold-room profiles;
- 3-2-1-1-0 DR model, off-site/immutable copies and restore/failover drills;
- hybrid compute-to-data and data-sovereignty model;
- explicit air-gapped/cold-room profile with an internal-only container network;
- OCI image/versioning/storage policy and egress-cost controls;
- deployment readiness checks that fail closed on an incorrectly network-enabled air-gap profile.

## Scalability boundary
The embedded SQLite durable queue/database is a supported standalone/local/cold-room control-state profile. Multi-site or active-active deployments must bind a tenant-approved HA transactional state backend and external durable event bus; the release architecture and contracts are designed for that substitution and readiness rejects use of the standalone queue as an HA claim.

## Bob boundary
The package does not claim that the current publicly documented IBM Bob product is itself air-gapped. The cold-room profile uses FAOS plus a local approved executor. Bob remains a connected integration unless an IBM-supported disconnected deployment is available for the tenant.
