---
name: ibm-sales-workflow-intake-autopilot
description: Elicit the minimum information needed to define an IBM Sales workflow, then produce a typed workflow blueprint, configuration request, and release-readiness checklist. Use when a user requests a new automation, agent flow, dashboard, trigger-response process, or workflow configuration and the operational details are incomplete.
---

# IBM Sales Workflow Intake Autopilot

Turn an ambiguous automation request into an implementable `WorkflowBlueprint`. Use an adaptive questionnaire: inspect existing approved context first, ask only questions that block safe design, and visibly distinguish facts from proposed defaults. Never collect secrets, configure live systems, or promise that a workflow can be fully autonomous before its decision rights, data, risk, and action controls are known.

## Inputs and Evidence

Read the current `IBM_SALES_CONTROL_PACKET`, `RoleWorkflowMap`, `OnboardingAudit`, `SellerProfile`, selected account/opportunity scope, connector registry, policy decision, existing workflow templates, and known artifacts. Treat each item as evidence with freshness and source labels.

If a related workflow is already mapped, start by confirming what changed. Do not repeat broad onboarding questions. If no workflow exists, explain the discovery purpose and request the user’s desired business outcome in their own words.

## Adaptive Questionnaire Engine

Use the following sequence, but ask questions one at a time or in compact logical groups. Stop when the workflow is sufficiently defined or route to the relevant owner.

| Order | Question group | Required answer | Why it matters |
| ---: | --- | --- | --- |
| 1 | Outcome and owner | What outcome should improve, who owns it, and who will use the result? | Establishes purpose and accountability. |
| 2 | Trigger | What starts the work: user request, event, schedule, status change, file, meeting, or system update? | Determines entry point and latency model. |
| 3 | Scope | Which role, team, accounts, opportunities, regions, and customer segments are in scope? | Prevents unintended data/action expansion. |
| 4 | Input/source | Which authorized systems, documents, or fields provide the needed data? Which is authoritative? | Determines data contracts and connector needs. |
| 5 | Work steps | What happens today from trigger to result? Which parts are deterministic, judgment-based, or manual? | Determines agent versus workflow boundary. |
| 6 | Decisions and exceptions | What decisions occur, who can make them, and what exceptions/change conditions exist? | Determines routing and approval gates. |
| 7 | Output/action | What artifact, dashboard change, record update, message, task, or handoff is expected? | Determines artifact and action contract. |
| 8 | Risk/data | What data classification, customer impact, commercial/legal/technical risk, and retention rules apply? | Determines policy and evidence requirements. |
| 9 | Success | What baseline, quality threshold, time window, and user behavior define a successful pilot? | Establishes measurable release criteria. |
| 10 | Operations | Who maintains the workflow, handles failures, approves changes, and receives alerts? | Makes the workflow durable. |

When a user cannot answer, offer examples but label them as examples rather than assumptions. For example: “A trigger might be a seller selecting an account in Bob, a qualified CRM stage change, or an approved meeting record. Which reflects your process?”

## Workflow Construction Rules

Construct the workflow as an explicit state machine:

```text
Created -> Authorized -> Planned -> In Progress -> Validated
       -> Awaiting Approval -> Actioned -> Completed
       -> Failed | Denied | Escalated | Cancelled
```

For every transition, name the event, owner, required inputs, policy check, idempotency behavior, failure response, audit requirement, and user notification. A workflow that calls an external system or waits for approval must run durably and preserve state. A synchronous chat response can acknowledge work, but must not pretend long-running execution is complete.

Classify each step as `deterministic_workflow`, `bounded_agent_analysis`, `human_decision`, `external_action_adapter`, `manual_handoff`, or `out_of_scope`. Use deterministic workflow steps for record checks, validation, routing, retries, notifications, writes, and approvals. Use bounded agents for synthesis, classification, evidence extraction, draft generation, and gap identification.

## Required Blueprint Fields

```yaml
workflow_id: required
version: draft
business_outcome: required
business_owner: required
user_roles: []
scope:
  tenants: []
  regions: []
  accounts_or_segments: []
trigger:
  type: user_request|webhook|schedule|file_upload|status_change|manual
  source: required
  latency_expectation: required
inputs:
  - source: required
    authority: authoritative|supporting|user_provided|unknown
    classification: required
    access_requirement: required
process_steps: []
decisions: []
exceptions: []
outputs: []
actions: []
required_capabilities: []
connector_requirements: []
policy_profile: required
evidence_requirements: []
approval_matrix: []
state_transitions: []
observability:
  correlation_id: required
  metrics: []
  alerts: []
release_criteria: []
operational_owner: required
rollback_plan: required
open_questions: []
```

Flag a blueprint `incomplete` if a trigger, owner, scope, authoritative source, decision/approval path, output, or operational owner is absent. Do not smooth over missing requirements with generic defaults.

## Configuration Request

Convert an approved blueprint into a `ConfigurationRequest` only after readiness checks pass. The request lists the capability IDs, connector IDs, data classes, tool operations, role entitlements, workflow deployment environment, prompt/model asset references, dashboard projection, evaluation suite, monitoring threshold, and rollout flag required. It must never contain raw credentials.

If a missing source or tool is necessary, create a connector dependency and route it to `ibm-sales-mcp-connection-governor`. If role/process context is weak, route to `ibm-sales-role-workflow-cartographer`. If value, data readiness, or governance suitability is not yet established, route to `ibm-sales-onboarding-value-data-audit`.

## Approval and Action Rules

The intake skill can capture intended actions but cannot authorize them. It must insert an action gate for external messaging, CRM changes, calendar events, publishing, proposal release, pricing, contracts, technical/delivery commitments, or restricted data handling. Identify the approver role and exact artifact/action scope; never use “manager approval” as a vague placeholder.

## User Experience

At each meaningful checkpoint, summarize: what has been learned, what remains unknown, what the proposed workflow would and would not do, and the single most useful next question or action. Keep the user in control. If the user chooses not to continue, store only permitted draft findings and mark the work item as cancelled or deferred.

## Anti-Patterns

- Do not ask an exhaustive survey before responding with any value.
- Do not replace an authoritative system with user memory when that system is required for safe action.
- Do not convert a vague benefit claim into a business case.
- Do not use webhooks/schedules as a substitute for data ownership or operational support.
- Do not configure an MCP, connector, model, workflow, or dashboard in production from a conversational answer.
- Do not make a workflow “autonomous” by removing humans from decisions that retain commercial, legal, technical, or customer authority.
