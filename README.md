# Federated Autonomous Organization OS · v1.2.0

> **Production-ready software release** — a single autonomous operating system that routes durable enterprise goals through a governed federation of 7 sectors, 48 specialist pockets, 492 execution teams, 3,212 canonical skills, and 540 factory wrapper skills. DealOS v1.0.1 is embedded as the deepest vertical implementation.

[![Release](https://img.shields.io/badge/release-v1.2.0-blue)](RELEASE_NOTES.md)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)](manifest.yaml)
[![Audit](https://img.shields.io/badge/audit-passed-brightgreen)](release/)
[![Skills](https://img.shields.io/badge/canonical%20skills-3212-blue)](registry/skill_accountability.json)
[![Pockets](https://img.shields.io/badge/pockets-48-blue)](registry/pockets.json)

---

## What is FAOS?

The **Federated Autonomous Organization OS** is an autonomous enterprise execution engine. It does not require a human to type "continue" — active goals live in durable state, and a bounded autonomy loop advances work within governed authority boundaries whenever a goal has progress available.

Every canonical skill has exactly one accountable segment/pocket/team in the registry. Skills are hydrated on demand; the 3,212 skills are a shared capability kernel, not 3,212 always-on agents.

```
GOAL
  └─► EnterpriseOS
        └─► sector / pocket (48 specialists)
              └─► team (492 execution / assurance / integration)
                    └─► canonical or dynamic skill
                          └─► certified connector
                                └─► policy check
                                      └─► action / draft
                                            └─► read-back + evidence
                                                  └─► next bounded job
```

---

## Architecture at a glance

| Layer | Technology / Pattern | Key Files |
|-------|---------------------|-----------|
| **Federation control plane** | Python 3.x, `aos.py` CLI | `aos.py`, `manifest.yaml` |
| **Sector / Pocket registry** | JSON manifests, 7 sectors / 48 pockets | `registry/pockets.json`, `registry/segments.json` |
| **Skill accountability ledger** | SHA-256-verified, every skill has one owner | `registry/skill_accountability.json` |
| **Router** | Intent → pocket scoring | `runtime/router.py` |
| **Job runner** | Bounded worker execution, executor handoff | `runtime/job_runner.py` |
| **Durable eventing** | SQLite outbox, dedupe, retry, dead-letter | `runtime/eventing.py` |
| **Proactivity engine** | Autonomy tick, bounded self-start | `runtime/proactivity.py` |
| **MCP assimilator** | Capability discovery, dynamic skill gen | `runtime/mcp_assimilator.py` |
| **Policy plane** | DENY / ALLOW / APPROVAL rules | `runtime/policy.py`, `policies/` |
| **State store** | SQLite mission store | `runtime/state.py` |
| **Capability registry** | SQLite capability DB | `runtime/capability_registry.py` |
| **Control API** | ThreadingHTTPServer REST | `scripts/control_api.py` |
| **Durable self-improvement** | Quarantined proposals | `runtime/self_improvement.py` |
| **Disaster recovery** | Backup/restore, 3-2-1-1-0 DR | `scripts/backup_state.py`, `scripts/restore_state.py` |
| **Deployment** | Docker, docker-compose, Kubernetes, air-gap | `Dockerfile`, `docker-compose.yml`, `deployment/` |
| **Test suite** | pytest (10 tests, all green) | `tests/test_factory.py` |

---

## Segments (7 sectors, 48 pockets)

| Segment | Purpose |
|---------|---------|
| **create** | Product / content / IP generation |
| **sell** | Revenue, GTM, DealOS embedded vertical |
| **make** | Engineering, delivery, SDLC |
| **run** | Operations, infrastructure, SRE |
| **protect** | Security, compliance, GRC |
| **invest** | Finance, portfolio, capital allocation |
| **learn** | Enablement, knowledge, training |

---

## Quick Start

### Prerequisites

- Python 3.10+ (`python3`)
- Docker (optional, for containerized deployment)

### Installation

```bash
git clone https://github.com/Sheldonos/Federated_Autonomous_Organization_OS_v1.2.0.git
cd Federated_Autonomous_Organization_OS_v1.2.0
```

No external Python dependencies are required for the core runtime — the OS uses the standard library only. The optional DealOS sub-package has its own `requirements.txt` inside `segments/sell/dealos/`.

### Validate the release

```bash
python3 scripts/validate_release.py   # SHA-256 integrity + structure check
python3 scripts/smoke_test.py         # 10-check functional smoke test
python3 scripts/audit_package.py      # Secret scan + compile check
```

### Run the CLI

```bash
# List all pockets and their routing weights
python3 aos.py list

# Route a natural-language goal to the best-fit pocket
python3 aos.py route "research the market, build the product and sell it"

# Create a durable goal
python3 aos.py goal "Grow revenue from qualified enterprise opportunities"

# Advance all active goals one bounded tick
python3 aos.py tick

# Assimilate a new MCP connector surface
python3 aos.py assimilate-mcp \
  --snapshot tests/sample_mcp_snapshot.json \
  --connector-id sample-crm
```

### Start the Control API

```bash
python3 scripts/control_api.py --host 127.0.0.1 --port 8080
```

Authenticated endpoints (Bearer token required):

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check |
| `GET` | `/pockets` | List all registered pockets |
| `POST` | `/route` | Score a goal against pockets |
| `POST` | `/goal` | Create a durable goal |
| `POST` | `/tick` | Run one autonomy tick |

### Docker

```bash
docker build -t faos:1.2.0 .
docker-compose up
```

Air-gapped / offline deployment: see `deployment/airgap/` and `docker-compose.airgap.yml`.

---

## Key concepts

### Adaptive MCP assimilation

When a new MCP/tool connector is reported, FAOS:
1. Discovers the full capability surface (tools, resources, prompts)
2. Hashes and diffs against the prior capability state
3. Classifies side effects (read-only vs. write vs. consequential)
4. Maps capabilities to their owning pockets
5. Generates quarantined dynamic wrapper skills
6. Re-evaluates previously blocked goals

This is **capability learning** — not hidden weight retraining. See [`docs/MCP_ADAPTIVE_AUTONOMY.md`](docs/MCP_ADAPTIVE_AUTONOMY.md).

### Governed proactivity

FAOS does not require a human to prompt every step. The autonomy tick advances active goals within hard authority boundaries:

- Every cycle has token/cost/action budgets
- Dedupe prevents duplicate job queuing
- Consequential side effects (money movement, external messages, production deploys) require explicit connector certification + policy approval
- Stop conditions prevent infinite loops

See [`docs/PROACTIVITY_MODEL.md`](docs/PROACTIVITY_MODEL.md).

### Policy plane

Three rule classes govern every action:

| Rule | Effect |
|------|--------|
| `DENY` | Hard block — action is rejected regardless of intent |
| `ALLOW` | Permitted within stated scope |
| `APPROVAL` | Queued for human confirmation before execution |

See [`policies/global_autonomy.yaml`](policies/global_autonomy.yaml) and [`policies/autonomy_budget.yaml`](policies/autonomy_budget.yaml).

### Durable eventing

All inter-component signals travel through a SQLite transactional outbox:
- Exactly-once delivery with deduplication keys
- Exponential-backoff retry
- Dead-letter state for un-retryable failures
- Crash recovery for stale `RUNNING` events

See [`docs/EVENTING_AND_BACKPRESSURE.md`](docs/EVENTING_AND_BACKPRESSURE.md).

---

## Resilience & operations

| Capability | Reference |
|-----------|-----------|
| Zero-downtime blue/green/canary upgrade | [`docs/ZERO_DOWNTIME_UPGRADES_AND_BACKOUT.md`](docs/ZERO_DOWNTIME_UPGRADES_AND_BACKOUT.md) |
| 3-2-1-1-0 disaster recovery | [`docs/DISASTER_RECOVERY_AND_SITE_RESILIENCE.md`](docs/DISASTER_RECOVERY_AND_SITE_RESILIENCE.md) |
| Hybrid / on-prem / air-gap profiles | [`docs/HYBRID_ON_PREM_AND_AIR_GAPPED.md`](docs/HYBRID_ON_PREM_AND_AIR_GAPPED.md) |
| Backup and restore | `scripts/backup_state.py`, `scripts/restore_state.py` |
| Deployment acceptance checklist | [`deployment/ACCEPTANCE_CHECKLIST.md`](deployment/ACCEPTANCE_CHECKLIST.md) |
| Production architecture | [`docs/PRODUCTION_ARCHITECTURE.md`](docs/PRODUCTION_ARCHITECTURE.md) |
| Storage, versioning, egress controls | [`docs/STORAGE_VERSIONING_AND_EGRESS.md`](docs/STORAGE_VERSIONING_AND_EGRESS.md) |

---

## Release & audit

This release was produced under a full 9-stage engineering audit:

| Stage | Result |
|-------|--------|
| Repository Discovery | ✅ |
| Technical Audit | ✅ 0 Critical · 0 High · 1 Medium · 3 Low |
| Product Decision Gate | ✅ Auth-by-default applied to all API endpoints |
| Remediation | ✅ All findings fixed — commit `72c0cc9` |
| Independent Verification | ✅ All fixes source-verified |
| Validation | ✅ All 5 test suites green |
| User Journey Audit | ✅ No broken flows |
| Beta Readiness Triage | ✅ No must-fix items |
| Release Report | ✅ **GO** |

Audit evidence: [`release/`](release/)

---

## Market and deployment packaging

| Document | Description |
|---------|-------------|
| [`market/PRODUCT_CATALOG.md`](market/PRODUCT_CATALOG.md) | Full federation and per-pocket product offerings |
| [`market/DEPLOYMENT_OFFERINGS.md`](market/DEPLOYMENT_OFFERINGS.md) | Deployment tiers and SLA profiles |
| [`market/MARKET_READINESS.md`](market/MARKET_READINESS.md) | Market readiness checklist |
| [`market/BUYER_SECURITY_AND_GOVERNANCE.md`](market/BUYER_SECURITY_AND_GOVERNANCE.md) | Security and governance posture for buyers |

---

## Provenance and licensing

The pinned 3,212-skill capability substrate is preserved as a SHA-256-verified source archive. Every canonical `SKILL.md` is checked against its registered hash at release validation.

User-provided and upstream-origin content retains its original provenance and licensing obligations. Do not invent a blanket license for material whose upstream rights have not been independently verified. See [`market/DISTRIBUTION_RIGHTS_CHECKLIST.md`](market/DISTRIBUTION_RIGHTS_CHECKLIST.md).

---

## Repository structure

```
.
├── aos.py                          # Main CLI entrypoint
├── manifest.yaml                   # Release manifest (version, architecture, substrate hashes)
├── Dockerfile / docker-compose.yml # Container deployment
├── runtime/                        # Core OS runtime modules
│   ├── router.py                   # Intent → pocket scorer
│   ├── job_runner.py               # Bounded job execution
│   ├── eventing.py                 # Durable event queue
│   ├── proactivity.py              # Autonomy tick engine
│   ├── mcp_assimilator.py          # MCP capability ingestion
│   ├── policy.py                   # Policy enforcement
│   ├── state.py                    # Mission state store
│   └── capability_registry.py      # Capability DB
├── segments/                       # 7 sectors, 48 specialist pockets
│   ├── create/ invest/ learn/
│   ├── make/ protect/ run/ sell/
├── registry/                       # Skill accountability ledger + pocket/segment registries
├── policies/                       # Global autonomy and budget policies
├── scripts/                        # Operational scripts (validate, smoke, control API, DR)
├── tests/                          # pytest test suite
├── docs/                           # 16 architecture and operations docs
├── deployment/                     # Acceptance checklist, runbooks, air-gap profiles
├── schemas/                        # JSON schemas for registry + manifests
├── market/                         # Product catalog, deployment offerings, licensing
├── storage/                        # Storage class definitions
├── config/                         # Production config examples
└── release/                        # Audit evidence and release artifacts
```

---

<sub>FAOS v1.2.0 · Audited release · IBM Enterprise Autonomous Operations OS substrate v2.0.0-rc1 · DealOS v1.0.1 embedded</sub>
