# Federated Autonomous Organization OS

> **FAOS v1.2.0** — A production-ready autonomous organization operating system built on a pinned 3,212-skill / 1,244-role enterprise capability substrate. Seven sectors, 48 specialist OS pockets, 492 execution teams, and 540 factory wrapper skills — with DealOS v1.0.1 embedded as its deepest vertical.

[![Version](https://img.shields.io/badge/version-1.2.0-0F62FE?style=flat-square)](https://github.com/Sheldonos/Autonomous-Organization-OS)
[![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen?style=flat-square)](https://github.com/Sheldonos/Autonomous-Organization-OS)
[![Skills](https://img.shields.io/badge/canonical%20skills-3%2C212-blueviolet?style=flat-square)](./registry)
[![Pockets](https://img.shields.io/badge/OS%20pockets-48-orange?style=flat-square)](./registry)

---

## What This Is

FAOS is an **OS factory for autonomous enterprise operations**. It turns a structured goal into a governed execution chain without requiring a human to repeatedly say "continue."

```
GOAL → EnterpriseOS → sector/pocket → team → canonical/dynamic skills
     → connector → policy → action/draft → read-back → evidence → next bounded job
```

The 3,212 skills are a **shared capability kernel**, not 3,212 always-on agents. Every canonical skill has one accountable segment/pocket/team in `registry/skill_accountability.json`, may have secondary routes, and is hydrated only when a bounded job needs it.

---

## Architecture

| Layer | What It Does |
|---|---|
| **Federation Control Plane** | Routes durable goals through the smallest sufficient pocket/team bundle |
| **7 Sectors / 48 Pockets** | Domain-organized OS pockets owning bounded capability surfaces |
| **492 Execution Teams** | Execution, assurance, and integration teams within each pocket |
| **540 Wrapper Skills** | First-party OS factory skills wrapping the canonical substrate |
| **Adaptive MCP Assimilation** | Discovers, hashes, classifies, and maps new tools/connectors at runtime |
| **Goal-Directed Proactivity** | Bounded autonomy tick advances durable goals without human "continue" prompts |
| **Global Policy Plane** | Connector certification, read-back contracts, and consequential-action governance |
| **Resilience / Continuity Plane** | Durable event queue, blue/green rollout, DR, air-gap, and OCI supply chain |

### Embedded Products

| Product | Version | Description |
|---|---|---|
| **DealOS** | v1.0.1 | Full enterprise deal execution vertical — 505 source skills, 12 wrappers, 13 n8n workflows |

---

## Key Capabilities

### 🔄 Adaptive Capability Assimilation
When a new MCP/tool connects, FAOS discovers its advertised tools/resources/prompts, hashes and diffs the capability surface, classifies side effects, maps capabilities to pockets, generates quarantined dynamic skills, and re-evaluates blocked goals. This is **capability learning** — not model retraining.

### ⚡ Bounded Self-Starting Job Loop
Active goals live in durable state. A bounded autonomy tick queues the next job when:
- A goal has pending work
- A blocker changes or a connector surface changes
- An evaluation fails
- An approved schedule/condition becomes due

Every cycle enforces budgets, deduplication, retries, and stop conditions.

### 🔒 Production Governance
Tool availability is never authorization. External messages, production deployments, purchases, permission changes, and legal filings remain gated by the policy plane and connector certification read-back rules.

### 🏗️ Resilience Plane (v1.2.0)
- Durable event queue with dedupe, retry, exponential backoff, and dead-letter state
- Zero-downtime blue/green/canary deployment with schema expand-migrate-contract
- Data-safe rollback preserving queued work and evidence
- 3-2-1-1-0 DR model with off-site/immutable copies
- Air-gapped/cold-room profile with internal-only container networking
- OCI image versioning and egress-cost controls

---

## Quickstart

### 1. Validate the release
```bash
python scripts/validate_release.py
python scripts/smoke_test.py
python scripts/audit_package.py
```

### 2. Explore and route
```bash
python aos.py list
python aos.py route "Find an RFP, build the winning submission, and pursue the deal"
python aos.py accountability accounting-accounts-payable-analyst
```

### 3. Create a durable goal and let the proactivity loop advance it
```bash
python aos.py goal "Build and sell a new AI product" --priority 80
python aos.py tick
```
Run the daemon workers to schedule and execute bounded jobs automatically:
```bash
python scripts/autonomy_tick.py --daemon --seconds 300
python scripts/run_worker.py --daemon --seconds 10
```
Review `policies/autonomy_budget.yaml` before enabling daemon execution.

### 4. Connect a new MCP/tool
```bash
# From a normalized capability snapshot
python aos.py assimilate-mcp --snapshot capability_snapshot.json --connector-id my-mcp

# From a live MCP 2026-07-28 HTTP endpoint
python aos.py assimilate-mcp --url https://example.com/mcp --connector-id my-mcp --token-env MY_MCP_TOKEN

# Certify after testing
python aos.py certify-connector my-mcp
python aos.py certify-connector my-mcp --write --readback
```

### 5. Hydrate only the team you need
```bash
python aos.py hydrate dealos --team t01 --max-skills 12 --dest /tmp/deal-discovery
```

### 6. Production deploy
```bash
cp config/production.example.json config/production.json
export FAOS_API_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
docker compose up -d
```
`/ready` fails until all required connector classes are bound and certified.

---

## Repository Structure

```
Autonomous-Organization-OS/
├── aos.py                      ← Primary CLI entrypoint
├── manifest.yaml               ← System manifest (versions, substrate SHA-256)
├── AGENTS.md                   ← Federation agent operating contract
├── QUICKSTART.md               ← Quickstart guide
├── RELEASE_NOTES.md            ← v1.2.0 release notes
├── Dockerfile / docker-compose.yml
├── compiler/                   ← Goal compilation and routing logic
├── config/                     ← Environment and production configuration
├── connectors/                 ← Connector certification and adapter layer
├── deployment/                 ← Acceptance checklist and deployment tooling
├── docs/                       ← Architecture docs, MCP assimilation, resilience
├── market/                     ← Product catalog, deployment offerings, market readiness
├── policies/                   ← Global autonomy, budget, and governance policies
├── registry/                   ← Segments, pockets, skill accountability ledger
├── release/                    ← Release gates and validation artifacts
├── runtime/                    ← MCP assimilator, worker, tick engine
├── schemas/                    ← Data contracts and output schemas
├── scripts/                    ← Validate, audit, smoke test, control API
├── segments/                   ← 7-sector factory segment definitions
├── skills/                     ← 540 OS factory wrapper skills
├── storage/                    ← Durable state, event queue, backup/restore
├── substrate/                  ← 3,212-skill / 1,244-role canonical capability substrate
├── teams/                      ← 492 execution/assurance/integration team definitions
└── tests/                      ← Test suite and sample MCP snapshots
```

---

## Capability Substrate

| Metric | Value |
|---|---|
| Canonical Skills | 3,212 |
| Roles | 1,244 |
| OS Factory Wrapper Skills | 540 |
| Sectors | 7 |
| OS Pockets | 48 |
| Execution Teams | 492 |
| Substrate SHA-256 | `bf1cbdad213c6ec2f9e6d87c3294ef2a1da95694bea5ce4939f6ad5ec84c93fc` |

---

## Production Boundary

The software distribution is **production-ready**. A live tenant is separately production-certified after its actual identity, credentials, connectors, permissions, write read-back, data contracts, recovery procedures, and decision rights pass `deployment/ACCEPTANCE_CHECKLIST.md`.

Completion truth: a tool call is not proof of a business outcome. FAOS records identifiers, timestamps, partial failures, authoritative read-back, evidence, and residual risk at every consequential step.

---

## Market / Product Packaging

The full federation or any individual pocket can be deployed as a standalone product. See:
- `market/PRODUCT_CATALOG.md`
- `market/DEPLOYMENT_OFFERINGS.md`
- `market/MARKET_READINESS.md`

---

## What's New in v1.2.0

See [`RELEASE_NOTES.md`](./RELEASE_NOTES.md) for the full changelog. Highlights:
- Durable event-driven execution with transactional outbox
- Event-triggered goal advancement (bite-sized model work, no continuous reasoning loop)
- Deployment drain/kill switch for executor handoffs
- Idempotent consequential-action receipt contract
- Zero-downtime blue/green/canary rollout
- 3-2-1-1-0 DR with restore/failover drills
- Air-gapped/cold-room runtime profile
- OCI immutable container supply chain

---

<div align="center">
  <sub>Federated Autonomous Organization OS · v1.2.0 · Production Ready Software Release</sub>
</div>
