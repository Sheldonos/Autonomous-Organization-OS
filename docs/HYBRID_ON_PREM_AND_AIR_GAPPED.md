# Hybrid, On-Premises & Air-Gapped Operation

## Principle: compute to the data
The federation control plane does not require raw enterprise information to be centralized. A pocket/team may execute near the authoritative data and return only approved structured results, hashes, metrics or evidence references.

## Hybrid topology
- global/federated policy and capability registry;
- local execution cells in cloud, on-prem, sovereign region, factory/edge, or restricted enclave;
- local connector bridge holds local credentials and enforces local authorization;
- event envelopes cross boundaries only when policy allows;
- large datasets stay in place; remote agents receive bounded retrievals rather than bulk copies.

## Cold-room / disconnected enclave
An air-gapped FAOS cell can be built with:
- pre-approved OCI images imported by digest;
- offline package/wheel/image mirror;
- local durable state, local event bus and local object/artifact store;
- local secrets/HSM/KMS equivalent;
- local model/agent executor if autonomous reasoning is required;
- no default route to the public internet;
- signed removable-media or guarded transfer workflow for updates;
- import/export manifests with hashes and malware/content inspection;
- local logs/evidence retained inside the enclave.

### Information confinement
In `air_gapped` data-sovereignty mode:
- external MCP discovery is disabled;
- external telemetry and crash reporting are disabled;
- internet research is unavailable unless an approved gateway exists;
- no prompts, documents, embeddings, traces or model inputs leave the enclave;
- egress attempts fail closed and are audited.

## IBM Bob boundary
As of this release, IBM's public Bob installation documentation lists an active internet connection as a system requirement. Therefore FAOS does **not** claim that the current public Bob product is itself a supported air-gapped executor. A cold-room deployment uses the FAOS headless runtime plus a locally approved executor; Bob can be used in connected environments, or in a disconnected environment only if IBM supplies and supports the required deployment for that tenant.
