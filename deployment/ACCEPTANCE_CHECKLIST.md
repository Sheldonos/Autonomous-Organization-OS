# Deployment Acceptance Checklist

A production tenant is accepted only when all applicable items pass:

- [ ] production config identifies enabled pockets and deployment owner
- [ ] identity/SSO and tenant boundaries verified
- [ ] secrets live in an approved secret manager or environment injection path
- [ ] every required connector class is bound to a discovered instance
- [ ] connector capability hash recorded
- [ ] read permissions tested with least privilege
- [ ] external-write connectors tested for idempotency/retry semantics
- [ ] write read-back independently verified
- [ ] decision rights and approval paths configured
- [ ] backups/recovery and state DB durability tested
- [ ] observability and alerting configured
- [ ] autonomy budgets and recurring jobs reviewed
- [ ] high-risk actions remain gated
- [ ] representative end-to-end pocket missions pass
- [ ] failure/recovery and connector-revocation tests pass
- [ ] provenance/license obligations reviewed for intended distribution model
- [ ] event source/broker path tested; no continuous model loop is required
- [ ] dedupe, retry, backpressure and dead-letter behavior tested
- [ ] consequential effects use idempotency keys/effect receipts
- [ ] deployment drain/kill switch tested
- [ ] pre-upgrade backup and restore verification passed
- [ ] blue/green or equivalent backout path exercised with prior image digest retained
- [ ] schema migration follows expand-migrate-contract or has an equally safe compatibility plan
- [ ] RPO/RTO documented; off-site and immutable/offline copies exist for critical data
- [ ] restore drill has been completed from a copy independent of the primary failure domain
- [ ] hybrid/data-sovereignty boundaries and allowed egress are documented
- [ ] air-gapped deployments have no public route and no external telemetry/MCP path
- [ ] OCI images are immutable/digest-pinned; SBOM/signing/scanning policy is satisfied
- [ ] egress-cost budget, locality and export/portability plan reviewed
