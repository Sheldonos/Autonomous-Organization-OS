# Resilience & Sustainability Architecture

This document is the production umbrella for eventing, upgrade safety, DR, hybrid execution, data portability and air-gapped operation.

## Failure domains considered
Process crash; container/node loss; bad release; schema incompatibility; connector outage; queue poison message; accidental duplicate effect; database loss/corruption; region/site outage; cloud/provider outage; utility-grid outage; identity/KMS outage; network partition; egress-cost shock; internet denial; and fully disconnected operation.

## Core invariants
1. No acknowledged consequential effect without a durable intent/effect record.
2. Every effect has an idempotency identity and a verification/read-back path when the target supports it.
3. Model/context memory is never authoritative state.
4. Deployment artifacts are immutable; state lives outside disposable containers.
5. New code must read old state before old code is removed.
6. Queued work survives upgrades and restarts.
7. Every critical backup is restore-tested.
8. Data locality is an architecture input, not an afterthought.
9. Air-gapped mode fails closed on network egress.
10. Autonomy can be killed independently of observability and evidence access.

See the companion documents:
- `EVENTING_AND_BACKPRESSURE.md`
- `ZERO_DOWNTIME_UPGRADES_AND_BACKOUT.md`
- `DISASTER_RECOVERY_AND_SITE_RESILIENCE.md`
- `HYBRID_ON_PREM_AND_AIR_GAPPED.md`
- `STORAGE_VERSIONING_AND_EGRESS.md`
