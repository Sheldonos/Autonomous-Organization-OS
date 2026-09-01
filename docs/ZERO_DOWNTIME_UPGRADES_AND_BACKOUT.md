# Invisible Upgrades, Data-Safe Deployment & Backout

## Upgrade objective
Users should not notice normal software upgrades, and an upgrade must not silently lose queued work or corrupt durable state.

## Release strategy
1. Build one immutable OCI image per release and identify it by digest, never mutable `latest` alone.
2. Generate SBOM, provenance, tests and image signature/attestation.
3. Take a state backup/checkpoint and prove restore metadata is readable.
4. Enter **drain mode** for consequential external writes. Reads and safe analysis may continue.
5. Apply only backward-compatible **expand -> migrate -> contract** schema changes.
6. Start Green alongside Blue where the state/backend topology allows it.
7. Run `/health`, `/ready`, connector read tests and representative mission smoke tests on Green.
8. Shift a canary slice or the proxy/service pointer to Green.
9. Observe SLO/error/effect-readback gates.
10. Complete traffic shift; keep Blue available through the rollback window.
11. Only after the rollback window may destructive schema contraction occur.

## Data-loss rule
Deployment is never the source of truth for in-flight state. Goals, events, jobs, approvals, evidence and effect receipts are durable before acknowledgment. A terminated process can therefore be restarted or replaced without losing acknowledged work.

## Backout sequence
If a release misbehaves:
1. activate the global **external-write kill switch**;
2. stop new consequential job claims and drain currently executing effects;
3. preserve the event queue and evidence store—do not purge or recreate them;
4. route traffic back to the prior known-good image digest;
5. do not reverse a database migration unless it is explicitly certified reversible;
6. replay only jobs whose idempotency/effect receipts prove they did not complete;
7. validate connector read-back and state consistency;
8. reopen external writes gradually.

## What to take offline first
Order of containment:
1. autonomous consequential writes;
2. connector write adapters for the affected domain;
3. affected pocket/team;
4. worker pool;
5. control API only if it is itself unsafe.

Do **not** take durable state, evidence, audit logs, backups or the event ledger offline unless containment requires isolation. They are needed to recover.
