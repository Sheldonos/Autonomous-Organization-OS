# Disaster Recovery & Physical-Site Resilience

FAOS supports a tiered DR model. The exact topology is selected per tenant based on RPO/RTO, regulation, cost and data sovereignty.

## 3-2-1-1-0 baseline
- at least 3 copies of important data;
- on at least 2 media/storage fault domains;
- at least 1 off-site copy;
- at least 1 immutable/offline copy;
- 0 unverified backups: scheduled restore tests must prove integrity.

## Site topology
For high-criticality deployments:
- primary site/AZ;
- secondary site/region physically separated from primary;
- off-site backup repository on a different failure domain;
- for extreme continuity requirements, place the tertiary copy on a different utility/electric-grid dependency and, where justified, a different cloud/provider or owned facility.

Do not assume "multi-AZ" means protection from region-wide identity, control-plane, power, provider or operator failure.

## Modes
- **Cold**: encrypted immutable backup + documented rebuild; lowest cost.
- **Warm**: pre-provisioned compute and replicated state, scaled down until failover.
- **Hot**: continuously ready secondary. Use only when business RTO justifies the operational complexity.

## Required DR artifacts
- dependency map and boot order;
- RPO/RTO per data class;
- backup encryption/key-recovery procedure;
- connector credential recovery or re-issuance procedure;
- DNS/service-discovery failover;
- queue replay/idempotency plan;
- quarterly restore drill and annual site-failover exercise for critical tiers;
- evidence that backups are readable without the failed primary environment.

## Suggested initial SLOs
Control-plane metadata: RPO <= 5 min, RTO <= 60 min for standard enterprise tier. Mission/effect ledger for critical writes: target near-zero acknowledged-event loss by committing before acknowledgment. Tenants may set stricter targets.
