# Storage, Version Control, Images & Egress Sustainability

## Use the right store for each kind of state
| Data | System of record | Protection |
|---|---|---|
| source/config/policies | Git | protected branches, signed releases, immutable tags |
| container images | OCI registry | immutable digest, signature/attestation, SBOM, retention policy |
| structured operational state | transactional DB | WAL/PITR/snapshots, encryption, replicas where supported |
| events/jobs/effect receipts | durable queue/ledger | replay, idempotency, DLQ, retention |
| documents/large artifacts | object storage/BYOS | versioning, lifecycle tiers, object lock where needed |
| secrets | vault/KMS/HSM | never Git, DB payloads or images |
| model/data artifacts | artifact/model registry + object store | immutable version/hash + lineage |
| audit/evidence | append-oriented evidence store | retention/legal hold/WORM as required |

## OCI/container rules
- multi-stage build;
- non-root runtime;
- read-only root filesystem where possible;
- no embedded credentials;
- pin base images and production releases by digest;
- scan vulnerabilities and dependencies before promotion;
- keep the previous known-good digest available for rollback;
- mirror required images internally for on-prem/air-gap use.

## Egress-cost controls
Cloud exit fees can become an architectural tax. FAOS therefore uses:
- compute-to-data placement;
- BYOS/tenant-owned object storage when appropriate;
- metadata and delta synchronization rather than bulk re-copy;
- content-addressed caching/deduplication;
- compression and column/field projection;
- lifecycle tiers and locality-aware retrieval;
- explicit egress budgets and alerts;
- cost-aware routing that considers bytes moved as well as model/token cost;
- export manifests and open formats so a tenant can leave a provider.

A vendor is never allowed to become the only readable copy of authoritative tenant data.
