# Federated Autonomous Organization OS v1.2.0

A single **OS Factory** built from the pinned 3,212-skill / 1,244-role enterprise capability substrate, organized into **7 sectors, 48 specialist OS pockets, 492 execution/assurance/integration teams, and 540 first-party factory wrapper skills**. DealOS v1.0.1 is embedded intact as the deepest vertical implementation.

## Core idea

The 3,212 skills are a shared capability kernel, not 3,212 always-on agents. Every canonical skill has one accountable segment/pocket/team in `registry/skill_accountability.json`, may have secondary routes, and is hydrated only when a bounded job needs it.

`GOAL → EnterpriseOS → sector/pocket → team → canonical/dynamic skills → connector → policy → action/draft → read-back → evidence → next bounded job`

## Adaptive capability assimilation

When a user or host reports that a new MCP/tool has been connected, FAOS can discover/import its advertised tools/resources/prompts, hash and diff the capability surface, classify side effects, map the capabilities to pockets, generate quarantined dynamic skills, and re-evaluate blocked goals. This is **capability learning**, not hidden model-weight retraining.

See `docs/MCP_ADAPTIVE_AUTONOMY.md`.

## Proactivity

FAOS is not dependent on a human repeatedly typing “continue.” Active goals live in durable state. A bounded autonomy tick may queue the next job when a goal has work to do, a blocker changes, a connector surface changes, an evaluation fails, or an approved schedule/condition becomes due. Every cycle has budgets, dedupe, retries and stop conditions. Consequential side effects remain governed.

## Production boundary

The software distribution is production-ready. A live tenant is separately production-certified after its actual identity, credentials, connectors, permissions, write read-back, data contracts, recovery and decision rights pass `deployment/ACCEPTANCE_CHECKLIST.md`.

## Important entrypoints

```bash
python scripts/validate_release.py
python scripts/smoke_test.py
python scripts/audit_package.py
python aos.py list
python aos.py route "research the market, build the product and sell it"
python aos.py goal "Grow revenue from qualified enterprise opportunities"
python aos.py tick
python aos.py assimilate-mcp --snapshot tests/sample_mcp_snapshot.json --connector-id sample-crm
python scripts/control_api.py --host 127.0.0.1 --port 8080
```

## Market/product packaging

The full federation or any pocket can be deployed as a product. See `market/PRODUCT_CATALOG.md`, `market/DEPLOYMENT_OFFERINGS.md`, and `market/MARKET_READINESS.md`.

## Provenance

The pinned source substrate is preserved as an exact archive and each canonical SKILL.md is checked against its registered SHA-256 at release validation. User-provided/upstream-origin content retains its provenance and licensing obligations; do not invent a blanket license for material whose upstream rights have not been independently verified.

## v1.2 resilience / sustainability plane
The final resilient release adds durable event-driven execution, deployment drain and rollback safety, backup/restore, DR, hybrid/air-gap profiles, immutable OCI/storage guidance and egress-aware data locality. Start with `docs/RESILIENCE_ARCHITECTURE.md` and `RELEASE_NOTES.md`.
