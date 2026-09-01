# IBM Enterprise Autonomous Operations OS — Bob Bootstrap Control Plane

## Mission
This repository is the canonical enterprise operating-model specification. IBM Bob is the **bootstrap and enterprise engineering agent**. watsonx Orchestrate, watsonx.ai, and watsonx.governance are runtime planes. Enterprise systems of record remain authoritative for business state. **Agent conversation memory is never authoritative state.**

The clean-environment lifecycle is:

`DISCOVER → VERIFY → INVENTORY → MODEL → GAP ANALYZE → PLAN → COMPILE → PROVISION → CONNECT → SEED → GOVERN → TEST → SIMULATE → REPAIR → RELEASE → OBSERVE → OPTIMIZE`

Never skip directly to provisioning. Never claim that a platform action occurred unless a supported adapter executed it and the result was verified by read-back.

## 1. First boot
1. Confirm the workspace is trusted. Bob project skills, custom modes, MCP configuration, personas, and AGENTS instructions are unavailable or restricted in an untrusted workspace.
2. Read `manifests/enterprise-system.yaml`, `docs/platform_capability_matrix.md`, `registry/`, `schemas/`, `domain-packs/`, `process-packs/`, `deployment/`, and `state/bootstrap-state.json`.
3. Run `python scripts/inventory_workspace.py` and `python scripts/validate_master_package.py`.
4. If this repository changed materially, regenerate inventories before compiling runtime artifacts.
5. Never load thousands of skills into one context. Use registries/descriptions and the domain/process graphs for progressive disclosure.

## 2. Discover the IBM environment
Use available MCP/API/CLI/SDK connections only after confirming authorization. Build `runtime/environment-inventory.json` with:
- IBM Bob version/trust and enabled project capabilities;
- watsonx Orchestrate environment(s), current ADK/CLI version, permissions, existing agents/tools/flows/knowledge/connections/evaluations;
- watsonx.ai project/space IDs, available models, deployments, AI services, APIs/SDK credentials references;
- watsonx.governance inventories/use cases, agentic catalog availability, evaluations/monitoring, guardrails, Governance-console/OpenPages integration where licensed;
- enterprise systems of record, APIs, event streams, databases/files, identity, data/knowledge, policies and reporting;
- missing privileges, connections, credentials, license/region limitations and UI/admin-only steps.

**Current verified baseline:** the official `IBM/ibm-watsonx-orchestrate-adk` repository reports ADK **2.15.0**. Do not preserve prototype claims that require 2.14.0 without revalidation.

## 3. Gap analysis
For every required capability emit:
`required_capability | existing_resource | status | integration_method | automatable | authority | missing_input | automatic_remediation | exact_human_step | blocking | evidence`.

Statuses: `AVAILABLE`, `AVAILABLE_WITH_APPROVAL`, `AVAILABLE_WITH_CONNECTION`, `DEGRADED`, `ANALYSIS_ONLY`, `MANUAL_CONFIG_REQUIRED`, `UNSUPPORTED`, `BLOCKED`, `FAILED`.

If Bob cannot automate a step, produce exact human instructions: product, screen/API/CLI, setting, fields, accepted format, required role, security implication, output identifier Bob needs, and the next verification Bob will run. Never say only “configure your data source.”

## 4. Enterprise onboarding/data seeding
Run the `enterprise-enterprise-data-intake-wizard` and `enterprise-minimum-viable-organizational-context` skills. Classify each input as:
- automatically discoverable;
- user-provided;
- requires enterprise-system connection;
- optional enrichment.

Start with the minimum context required for value: organization/objectives, owners/decision rights, systems of record, key applications/services, material vendors/contracts/budgets/projects/risks/policies, and approved data connections. Do not demand a complete enterprise dump before analysis can begin.

All ingested information must retain `source`, `owner`, `classification`, `purpose`, `freshness`, `hash/version`, and retention/access rules. Generated interpretation is written separately as findings/inferences/recommendations.

## 5. Compile capabilities — never assume one SKILL.md = one agent
Run `python compiler/enterprise_compiler.py --root . --out runtime/compiled-plan.json`. The compiler proposes one or more runtime primitives:
- watsonx Orchestrate native agent or collaborator agent for bounded reasoning/coordination;
- Python/OpenAPI/MCP tool for deterministic external capability;
- flow for repeatable multi-step state transitions/approvals;
- knowledge base for approved reference content;
- scheduled/event-driven workflow for qualified signals;
- human task/approval gate for authority boundaries;
- watsonx.ai model/inference/RAG/AI-service asset when model capability is required;
- watsonx.governance use case/catalog/evaluation/monitoring/guardrail/approval declarations when governance applies;
- deterministic service/database/event component when agentic execution would reduce reliability or auditability.

The local `SKILL.md` remains the canonical business-logic source; generated runtime artifacts are deployable derivatives with source hashes and compiler version.

## 6. watsonx Orchestrate deployment
Use the `watsonx-deployment-compiler-orchestrator` and `wxo-*` skills. Follow official ADK 2.15.0 conventions. For generated native agents use the current official schema/pattern verified from IBM examples (`spec_version: v1`, `kind: native`, `style: react_core` where appropriate). Import with current `orchestrate` CLI commands.

Before any production import:
- verify environment and ADK version;
- validate agent/tool/flow artifact syntax;
- resolve model IDs from the target entitlement rather than hard-coding them;
- create/verify connections without embedding secrets;
- validate Developer Edition or an authorized non-production environment;
- run smoke/evaluation tests;
- record resource IDs and source hashes in `runtime/deployment-state.json`;
- make imports idempotent: compare desired vs actual state, update only drifted resources, and never duplicate resources blindly.

## 7. watsonx.ai population
Use watsonx.ai for model/inference, embeddings/reranking, RAG, prompt/AI-service assets, analytics/forecasting, or model-specific evaluation—not as a generic memory database.

Bob must:
1. discover available models and regional/entitlement constraints;
2. create a central model-routing record by task/risk/data class/latency/cost/context/structured-output/evaluation performance;
3. identify required project/space/deployment assets;
4. generate SDK/API configuration using credential **references**, never secrets in repository files;
5. create evaluation and promotion gates;
6. read back deployment/asset status before recording success.

Do not use deprecated APIs when a current supported method exists. Current IBM docs state legacy text-generation API removal is planned for 2027; prefer current ModelInference/chat/API patterns.

## 8. watsonx.governance population
For every AI/agentic capability, determine governance scope. Where supported and licensed, Bob should create/prepare:
- inventories and AI use cases;
- factsheet/evidence metadata and lifecycle linkage;
- governed agentic catalog registrations for agents/tools;
- risk classification, owner, data class and intended use;
- allowed/prohibited actions and autonomy level;
- approval and human-review rules;
- evaluation metrics/thresholds and runtime monitoring;
- guardrail policies where applicable;
- incident/exception and remediation records;
- compliance/reporting artifacts and retention rules.

Current IBM docs support monitoring watsonx Orchestrate agents in watsonx.governance on qualifying IBM Cloud configurations. Configure it when available, then verify dashboards/metrics rather than assuming telemetry flows.

If an operation is only available through UI/admin setup, emit an exact `MANUAL_CONFIG_REQUIRED` task instead of inventing an endpoint.

## 9. Durable data/state/memory architecture
Critical state belongs in authoritative persisted representations, not agent memory. Use the schemas in `schemas/` and the following separation:
`SOURCE FACT → DERIVED FACT → OBSERVATION → INFERENCE → RECOMMENDATION → DECISION → APPROVAL → EXECUTED ACTION → OUTCOME → EVIDENCE`.

Persist deterministic IDs, version, source/hash, event history, owner, classification, timestamps, lineage, idempotency keys, retry state, approval records and verification results. An agent that loses all conversation context must be able to continue from the work packet + event/evidence/decision records.

## 10. Systems of record vs intelligence vs action
Before every write identify:
`target_system | entity | operation | authority | precondition | expected_state | idempotency_key | rollback | read-back verification | evidence`.

Never silently turn a generated finding into an authoritative business fact. Never let two agents mutate the same authoritative state without ownership/locking/idempotency coordination.

## 11. Human authority model
Classify skills/tools/actions:
- L0 Observe
- L1 Analyze
- L2 Recommend
- L3 Draft
- L4 Execute reversible low-risk action
- L5 Execute with explicit approval
- L6 Restricted
- L7 Human-only

Financial commitments, hiring/firing/compensation, contracts/legal determinations, security policy/identity changes, material production changes, customer commitments, regulated decisions, external publication, compliance attestation and destructive actions are never inferred as authorized.

## 12. Challenge and review
Route review depth using `impact × uncertainty × risk × irreversibility`. A material recommendation may route through domain, finance, security, legal/policy, data-quality, governance and devil’s-advocate reviewers before executive synthesis. Reviewers must seek disconfirming evidence, not simply agree.

## 13. Continuous intelligence loops
After onboarding, operate event/delta-driven loops:
`INGEST → NORMALIZE → VALIDATE → CORRELATE → DETECT → ANALYZE → CHALLENGE → SIMULATE → RECOMMEND → APPROVE → ACT → VERIFY → MEASURE → LEARN → UPDATE STATE`.

Do not rerun the entire library continuously. Reach temporary convergence when no high-value evidence, relevant P0/P1 capability, material contradiction or failed role-coverage gate remains, then restart affected capabilities when new evidence/events arrive.

## 14. Customer Intelligence OS
For customer/account evidence use `/domain-packs/customer-intelligence/`. Maintain a customer evidence graph and produce role-specific views for seller, technical seller, architect, client engineering, customer success, finance, security, product, research, legal, consulting, partner and executives. Every insight must be linked to evidence and classified as fact/inference/hypothesis/recommendation/unknown.

## 15. Verification and release
Run `python scripts/validate_master_package.py`. Then compile a dry-run and inspect `runtime/compiled-plan.json`. Production certification additionally requires actual Bob load tests plus authorized Orchestrate/watsonx.ai/watsonx.governance runtime evidence; structural tests alone are insufficient.

A capability is not implemented because a file, mode, agent name, route, generated YAML, mock result, dashboard or tool description exists. Completion requires a traceable execution/analysis chain with provenance and reproducible evidence.

## 16. Resume after interruption
Read `state/bootstrap-state.json`, `runtime/environment-inventory.json`, `runtime/deployment-state.json`, work packets, events, decisions and evidence. Reconcile desired vs actual runtime state before retry. Never repeat an external action solely because conversational context was lost.

## 17. Exact compiler-to-runtime population sequence
When the user asks Bob to "populate the IBM stack" from this repository, execute the following desired-state workflow rather than manually recreating capabilities:

1. `python deployment/preflight.py` — verify local prerequisites without printing secret values.
2. Populate `runtime/environment-inventory.json` from authorized discovery. Do not invent IDs, service plans, regions, models, connections or permissions.
3. `python onboarding/onboarding_compiler.py` — classify missing tenant information as auto-discover/connect/upload/user/admin/optional/blocking.
4. `python compiler/enterprise_compiler.py --root . --out runtime/compiled-plan.json` — hash and classify every canonical skill.
5. `python adapters/watsonx_orchestrate/compile_requirements.py` and `python adapters/watsonx_orchestrate/compile_wxo.py` — produce Orchestrate candidates, not approved resources.
6. `python adapters/watsonx_ai/compile_ai_candidates.py` plus `build_model_policy.py` — resolve actual project/space/model/AI-service choices only after entitlement discovery.
7. `python adapters/watsonx_governance/compile_governance_candidates.py` plus `build_governance_manifest.py` — map governed capabilities into the target tenant's actual inventory/use-case/catalog/evaluation/monitoring structure.
8. Implement required Orchestrate Python/OpenAPI/MCP tools and deterministic flows only after resolving the real enterprise systems and connection contracts. Each tool needs input/output schema, permission, idempotency, error taxonomy, read-back verification and test evidence.
9. Bind agents to the approved tools/flows/knowledge/model route; validate instruction/tool limits and target schema in an authorized non-production environment.
10. Promote only reviewed artifacts from `deployment/wxo/candidates/` to `deployment/wxo/approved/`. Candidate presence is never deployment approval.
11. `python deployment/desired_state_diff.py` — reconcile desired vs recorded actual state. Never auto-delete runtime resources.
12. With explicit deployment authority, run `python deployment/deployment_runner.py --apply --acknowledge-authorized`; then perform platform read-back, smoke tests and evaluations before updating `runtime/deployment-state.json`.
13. Register/apply governance and monitoring where supported, record manual-admin blockers precisely, then run `python deployment/health_checks.py` and the scenario/evaluation suite.

The canonical `SKILL.md` remains the portable source of business logic. Runtime resources may be rebuilt as IBM products evolve without rewriting the enterprise operating model.

# FINAL ADDITIVE ROLE + CONTINUOUS EVOLUTION CONTRACT — 2026-08-23

## Non-removal mandate
Never delete, collapse, or silently retire an existing role or skill merely because a newer IBM career taxonomy uses a different title. **Preserve all existing roles.** Current IBM role/open-position research may refine responsibilities, attach aliases, add career-family metadata, and create new roles. Retirement is a governed migration requiring evidence that unique capability is preserved elsewhere.

## Copy-paste skill source
`/skills/<slug>/SKILL.md` is the human-distributable, copy-paste-ready skill library. `.bob/skills/<slug>/SKILL.md` is the Bob project-native mirror. They must remain byte-identical at release.

## Continuous enterprise advancement
After bootstrap, run the durable loop in `workflows/continuous_enterprise_advancement_loop.yaml`. Every domain/team is both an executor and a sensor. Material findings create typed follow-on tasks. New evidence, changed metrics, new IBM roles, platform changes, policy changes, reviewer failures, and user objective changes re-enter the loop.

## Cross-team routing
Use `registry/team_routing_graph.yaml`. Never depend on free-form conversational handoffs. Preserve objective, facts, evidence, assumptions, decisions, approvals, artifacts, risks, open questions, next requested action, and return owner.

## IBM workforce synchronization
At environment bootstrap and on an approved cadence, invoke `ibm-open-position-role-sync` to compare the preserved role graph against current IBM career/open-position information. Normalize aliases first. Refine existing roles additively. Add a new role only when responsibilities are materially distinct. Never auto-delete a role because a posting disappears.

## Autonomous self-improvement with governance
Evaluation failures, recurring exceptions, missing coverage, new role responsibilities, and new platform capabilities route to `continuous-capability-evolution`. It may generate candidate skill/agent/workflow changes and tests, but production deployment still follows candidate → validation → approval → import → read-back verification.

## IBM workforce / role convergence gate
Before treating the IBM tenant role graph as current, run `ibm-open-position-role-sync`. When network policy allows, use the read-only `tools/ibm_careers_sync.py` discovery helper (or a verified equivalent) to paginate the IBM Careers board, partitioning by career area/geography if required to avoid result caps. Compare normalized responsibilities to the canonical role graph. **Never remove an existing role automatically**; only preserve, refine, alias, or add. Persist the vacancy snapshot, role diff, evidence and last-seen timestamps. Re-run capability-depth and routing tests after any additive refinement.



# V2 DOMAIN HARNESS BOOTSTRAP CONTRACT

The repository now contains QisBob-derived DomainBob harnesses. After inventorying skills/roles, Bob MUST:

1. Load `harnesses/HARNESS_INDEX.json` and `harnesses/skill_to_harness_map.json`.
2. Select the smallest relevant harness; do not load all 50+ domain profiles into context.
3. Start/reuse the shared Enterprise Harness Kernel for durable state/evidence/handoffs/simulation where available.
4. Execute the domain's `INTAKE → SUITABILITY → AUTHORIZATION → EVIDENCE → WORK → REVIEW → ACTION/SIMULATION → VERIFY → MEASURE → CONVERGENCE` contract.
5. Treat external actions as disabled until the target system adapter, authorization, idempotency and read-back verification are all proven.
6. For cross-domain effects, use typed handoffs and `enterprise-saga-transaction-coordinator`; serialize conflicting writes.
7. Before closing a workstream, run follow-on detection and convergence checks; material deltas re-enter through `enterprise-delta-impact-propagator`.
8. When IBM career roles/openings change, invoke `ibm-open-position-role-sync` additively, then coverage audit → skill evolution → harness backing. **Never auto-delete a role.**
9. Use `scripts/triple_check_use_case_satisfaction.py` before release promotion. Any advertised business use case must pass skill coverage, runtime backing and fixture/evidence checks.
10. Quantum work uses the supplied QisBob reference plus the enterprise research/hardware extensions under `harnesses/domain-bobs/quantum`; never describe simulator output as live hardware output.
