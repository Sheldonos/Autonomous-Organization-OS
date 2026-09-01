---
name: ibm-sales-onboarding-value-data-audit
description: Audit whether IBM Sales agentic workflows are appropriate for a seller, team, or sales operation; identify benefit hypotheses, process and data readiness, governance gaps, and data-lake opportunities. Use for first onboarding, pilot prioritization, program expansion, data-readiness assessment, or a request to determine whether the package will improve a user’s work.
---

# IBM Sales Onboarding Value and Data Audit

Assess **fit before automation**. Produce an evidence-backed readiness decision that explains what the IBM Sales package can enable now, what it cannot safely enable, which information is missing, and which data/process improvements would make the next use case credible. Do not promise time savings, quota uplift, revenue, ROI, or compliance. Use benefit hypotheses tied to measurable baselines and pilot outcomes.

## Evidence Sources and Boundaries

Use the user’s stated goal, `SellerProfile`, `RoleWorkflowMap`, `WorkflowBlueprint`, approved system inventory, connector registry, policy/entitlement decisions, existing artifacts, quality metrics, and permitted organizational process documentation. Do not expand data access merely to improve the assessment. Treat public research as background only, never as proof of the user’s actual operational readiness.

Use IBM’s governance guidance to keep the audit tied to accountable lifecycle controls. IBM documents governance of generative and machine-learning assets from request through production, monitoring/thresholds, AI Factsheets, and prompt/model lifecycle evidence.[1] IBM also documents programmatic guardrails for input and generated output; guardrails complement, rather than replace, access controls, consent, workflow approvals, or data minimization.[2]

## Audit Dimensions

Evaluate each dimension as `strong`, `adequate`, `weak`, `unknown`, or `not_applicable`. Explain the observed evidence and missing information behind each rating.

| Dimension | What to establish | Strong evidence |
| --- | --- | --- |
| User/job fit | Is there a named user/role with a repeated, important job to be done? | Role owner, outcome, workflow scope, and user commitment are explicit. |
| Process fitness | Is there a definable trigger, path, decision, exception, owner, and completion state? | A shared workflow map or usable blueprint exists. |
| Data fitness | Are sources authoritative, permitted, sufficiently complete/fresh, and classified? | Source owner, quality, access, data class, and lineage are known. |
| Tool/integration fitness | Is a supported, owned, least-privilege connection path available? | Approved connector/API/MCP plan with operations allowlist exists. |
| Decision/approval fitness | Are authority boundaries and approvers known? | Seller/domain action matrix and exception path are explicit. |
| Governance fitness | Are risk tier, retention, evaluation, monitoring, and change owners identified? | Policy profile, AI-use-case/release path, and operational owner exist. |
| Change/adoption fitness | Will users review outputs, provide feedback, and own the changed workflow? | Pilot cohort, training/communications, feedback channel, and champion are named. |
| Measurement fitness | Can the pilot be evaluated against a meaningful baseline? | Baseline, target metric, observation window, and control/compare method are defined. |

## Benefit Hypothesis Method

Write benefits as testable hypotheses rather than outcomes. Use the form:

> For **[named role]**, in **[bounded workflow]**, using **[approved data/tool]**, the package may reduce **[defined manual/friction step]** or improve **[quality/decision/support measure]**, subject to **[control and adoption conditions]**. Validate during **[pilot window]** against **[baseline]**.

Examples are permitted only as patterns, not estimates: reducing duplicate research effort, increasing evidence completeness in account briefs, improving preparation consistency, shortening the time to an internal draft, reducing missing CRM fields, or making approval blockers visible. Never invent a numeric baseline or expected percentage.

## Data-Lake and Knowledge Readiness Review

Do not equate a bigger data lake with a better agentic system. Recommend data-lake or knowledge improvements only when a specific workflow is blocked by missing, fragmented, stale, unowned, inaccessible, or poorly governed data.

Map each required source as follows:

| Source category | Questions | Preferred treatment |
| --- | --- | --- |
| CRM/territory/CPQ/CLM | Is it authoritative? Which fields/objects are needed? Who may read/write? | Query through scoped approved integration; do not bulk-copy by default. |
| Sales content/playbooks | Is content approved, current, and tagged by offer/region/audience? | Curate/version in permissioned knowledge collection. |
| Call/meeting data | Is recording/transcription permitted? What is retention/consent? | Process scoped records with explicit policy and confirmation steps. |
| Account research | Which sources are permitted and how fresh must they be? | Keep evidence handles and source terms; avoid unsupported claims. |
| Product/technical knowledge | Is it versioned and owned? | Use approved knowledge source with release metadata. |
| Operational metrics | Are definitions, granularity, and access rights consistent? | Build governed metrics layer; avoid direct ambiguous dashboard queries. |
| Unstructured files | Can they be classified, scanned, attributed, and retained lawfully? | Quarantine/process by policy; index only approved collections. |

Recommend a `data_lake_candidate` only after a data owner, business purpose, classification, access policy, quality plan, lineage method, retention rule, and operating model are identified. Prefer a scoped data product, governed retrieval index, or API view over broad ingestion of sales information.

## Audit Interview Sequence

Start with the highest-information questions:

1. “What work would you like this package to make easier or more reliable?”
2. “Who owns that outcome and who would use or approve the result?”
3. “What happens today from trigger to completion, and where does it fail or consume effort?”
4. “Which systems/documents are relied on, and which one is the source of truth?”
5. “What data is sensitive or restricted, and what cannot leave the current system?”
6. “What result would be useful enough to keep using after a pilot?”
7. “How would we observe improvement without relying on a vague claim?”

Ask deeper questions only where a readiness decision depends on them. Respect a user’s refusal to share sensitive details; record the limitation and propose a lower-risk public/read-only pilot where feasible.

## Decision Logic

| Decision | Use when | Required next step |
| --- | --- | --- |
| `ready_for_read_only_pilot` | A bounded user/workflow, owner, permitted source, risk profile, and measurement approach are sufficiently evidenced. | Create a controlled read/draft pilot blueprint and evaluation plan. |
| `ready_after_targeted_remediation` | A valuable use case exists, but named finite gaps remain. | Produce accountable remediation actions, then reassess. |
| `discovery_needed` | Role, workflow, data, or authority is too unclear to evaluate. | Invoke cartographer and/or workflow intake. |
| `not_recommended_now` | No supported problem, owner, permitted data, or operating commitment exists. | Explain conditions that could change the conclusion; do not force automation. |

Avoid aggregating ratings into a deceptive single score. If a summary score is requested, disclose weights, evidence gaps, and the fact that it is a prioritization aid rather than a prediction.

## Output Contract

Return a versioned `OnboardingAudit`:

```yaml
audit_id: required
scope: seller|role|team|workflow
business_problem: required
observed_evidence: []
assumptions: []
unknowns: []
readiness_dimensions: []
benefit_hypotheses: []
current_capabilities_enabled: []
capabilities_blocked: []
required_information: []
data_source_inventory: []
data_quality_and_governance_gaps: []
data_lake_or_knowledge_recommendations: []
pilot_design: {}
risk_and_policy_requirements: []
conclusion: ready_for_read_only_pilot|ready_after_targeted_remediation|discovery_needed|not_recommended_now
recommended_next_step: required
accountable_owners: []
review_date: required
```

Present a readable summary with: what is known; what the package can enable now; what it cannot enable yet; evidence-backed candidate workflows; data/system improvements; required owners; risks; and the next smallest decision.

## Handoffs

Route role/work ambiguity to `ibm-sales-role-workflow-cartographer`. Route process definition gaps to `ibm-sales-workflow-intake-autopilot`. Route tool, data access, MCP/API, or app-connection gaps to `ibm-sales-mcp-connection-governor`. Route a ready bounded use case to `ibm-sales-adaptive-orchestrator` and the IBM Sales control mode.

## Boundaries

Do not make employment, credit, eligibility, pricing, legal, or regulatory decisions. Do not recommend data ingestion without a business purpose and governance path. Do not turn broad sensitive data access into a default “better data lake” recommendation. Do not present IBM platform capabilities as a guarantee that sensitive uploads or integrations satisfy an organization’s policy.

## References

[1] [IBM, “Governing assets with watsonx.governance.”](https://www.ibm.com/docs/en/watsonx/saas?topic=governing-ai)

[2] [IBM, “Configuring AI guardrails in watsonx.governance.”](https://www.ibm.com/docs/en/watsonx/w-and-w/2.2.0?topic=content-configuring-ai-guardrails-in-watsonxgovernance)
