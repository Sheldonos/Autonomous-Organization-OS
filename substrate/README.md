# IBM Enterprise Autonomous Operations OS v2.0.0-rc1

A Bob-native, watsonx-targetable enterprise operating system that combines **3,212 copy-paste-ready IBM Bob skills**, **1,244 preserved/expanded roles**, **113 specialist/reviewer personas**, **55 global modes**, and **68 QisBob-derived DomainBob runtime harnesses**.

The design premise is simple: **agents are attached to a durable enterprise data/state/evidence pipeline; conversational memory is never authoritative enterprise state.** Every consequential workflow reconstructs its objective and history from persisted state, produces evidence, creates typed handoffs, verifies outcomes, and can resume after context loss.

## What changed in v2

v1 already had the large skill/role/control-plane library. v2 adds the missing QisBob-style execution envelope around the organization:

- shared durable harness kernel (`harnesses/kernel/`);
- one DomainBob harness profile per supported business/control domain (`harnesses/domain-bobs/`);
- narrow tool surfaces, state machines, loop budgets, bootstrap/init assets and fixtures;
- full skill→harness and role→harness mappings;
- QisBob preserved as the quantum reference implementation plus research/hardware/reviewer extensions;
- explicit business-line use-case satisfaction matrix and triple gate;
- cross-domain saga/transaction coordination and delta impact propagation;
- additive IBM-career role synchronization and capability-evolution loop.

## Canonical skill locations

- `.bob/skills/<slug>/SKILL.md` — project-native IBM Bob skills.
- `skills/<slug>/SKILL.md` — **byte-identical copy-paste library** for the IBM Bob Skills UI.
- `skills/COPY_PASTE_INDEX.json` — searchable index.

No role is removed by career refresh or deduplication. Current role evolution is **additive only**.

## Start in IBM Bob

1. Open this repository as a trusted workspace.
2. Read `AGENTS.md` before provisioning anything.
3. Run `python scripts/validate_master_package.py`.
4. Run `python scripts/triple_check_use_case_satisfaction.py`.
5. Run `python scripts/inventory_workspace.py` and populate the authorized environment inventory.
6. Select the smallest relevant domain harness using `harnesses/HARNESS_INDEX.json`.
7. Optionally activate its local modes with `python scripts/activate_domain_harness.py <domain>`.
8. Compile canonical capabilities with `python compiler/enterprise_compiler.py --root . --out runtime/compiled-plan.json`.
9. Bind real connections/models/knowledge/governance objects only after environment discovery and authorization.
10. Promote reviewed runtime candidates from `candidates/` to `approved/`; production import scripts consume only `approved/`.

## QisBob pattern

The supplied QisBob implementation is retained under `reference-implementations/qisbob-main-2026-08-06/`. It is the reference for the vertical-product pattern:

`skill + mode + bounded tools + runtime service + durable state + evidence + deterministic simulation + install/init + fixtures + tests + truthful external-execution boundary`.

The same pattern is generalized into FinanceBob, SalesBob, CyberBob, DataBob, AIBob, PeopleBob, LegalBob, ProductBob, ResearchBob, SupportBob, CustomerIntelBob and the rest of the DomainBob harness family.

## Use-case release gate

The enterprise specification currently enumerates **243 explicit functional use cases**. The release gate requires every one to have:

1. a canonical skill path;
2. runtime/harness backing;
3. fixture/evidence-backed acceptance coverage.

Current result: **243/243 PASS**.

## watsonx compilation posture

Current compile plan identifies:

- 602 watsonx Orchestrate native-agent candidates;
- 170 flow candidates;
- 3212 tool/integration requirements;
- 122 watsonx.ai candidates;
- 251 watsonx.governance candidates.

These are **candidates**, not proof of deployment. Bob must resolve actual entitlements, connections, model IDs, credentials, policies and read-back verification in the target environment.

## IBM role model

The package preserves all pre-existing roles and adds current IBM career-family observations across AI/watsonx, Cloud, Consulting, Data & Analytics, Design & UX, Enterprise Operations, Infrastructure & Technology, Product Management, Project Management, Research, Sales, Security and Software Engineering. The live-role synchronization skill exists because vacancies change continuously; static snapshots are never treated as permanently exhaustive.

## Release status

`RC_NOT_PRODUCTION_CERTIFIED`.

Local structural, schema, routing, fixture and harness validation can be completed here. Production certification still requires IBM Bob workspace load tests and authorized end-to-end execution/read-back against the target watsonx and enterprise environments.
