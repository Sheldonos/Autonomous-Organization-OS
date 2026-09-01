---
name: ibm-sales-proactive-guidance
description: Generate timely, evidence-backed, low-noise IBM Sales guidance from approved workflow events, pending decisions, completed artifacts, data-quality changes, and operational exceptions. Use after a validated event when an entitled seller or owner would benefit from one clear next action or decision request.
---

# IBM Sales Proactive Guidance

Convert a validated state change into one useful, dismissible `GuidanceNudge` or `DecisionRequest`. Help the user move work forward without acting on their behalf, exposing unnecessary data, creating alert fatigue, or treating speculation as a trigger.

## Eligible Triggers

Use only durable, validated events or current-state conditions from approved systems. A trigger must have a correlation ID, owner, scope, policy decision, and data classification.

| Trigger | Allowed guidance | Prohibited behavior |
| --- | --- | --- |
| Validated artifact completed | Offer to review, approve, compare, or route the result. | Claim customer action or outcome occurred without receipt. |
| Approval awaiting action | Explain the decision, expiry, impact, and approver. | Pressure the approver or bypass the gate. |
| Approval declined | Summarize recorded reason and offer allowed revision route. | Retry the same action or imply approval will be overridden. |
| Workflow blocked | Ask for exact missing input, owner decision, or connection remediation. | Start broad research or request sensitive data unnecessarily. |
| Evidence stale/conflicted | Offer refresh/reconciliation before customer use. | Reuse stale content as fact. |
| Connector failure | State business-safe status and recovery owner. | Retry unknown writes/sends before receipt reconciliation. |
| Approved account/opportunity event | Suggest permitted preparation or review step. | Make an external claim, outreach, or commercial recommendation without evidence. |
| Upcoming entitled meeting | Offer review of an approved preparation plan. | Access calendar/contact content outside scope. |
| Data-quality issue | Offer record review or permitted remediation workflow. | Alter source records automatically. |

Do not trigger from raw web content, unreviewed social signals, inferred personal traits, private relationship data, loosely correlated activity, or model-generated speculation.

## Recipient and Frequency Controls

Before creating a nudge, confirm the recipient has current entitlement to the account/opportunity/work item and the supporting data. Deliver only to the named owner or an approved role. Default to the least intrusive visible channel in the seller dashboard; use external notifications only if the organization configured and approved them.

Respect per-user quiet hours, role preferences, regional rules, and dismissal/snooze signals. Limit to one unresolved nudge per work item unless a new material event changes the required decision. Group related updates into a single status item. Do not surface a low-confidence suggestion merely to increase engagement.

## Relevance Test

Create guidance only when every condition is met:

1. The trigger is verified and current.
2. The recipient is entitled and accountable or materially affected.
3. The suggested step is permitted and has a named owner.
4. The user can understand why the guidance appears now.
5. The action is reversible or explicitly routed through the required approval gate.
6. The content can be presented without restricted data beyond the recipient’s scope.
7. The expected value exceeds the interruption cost.

If any condition fails, record an internal observability event where appropriate but do not display a user-facing nudge.

## Guidance Construction

Write in seller language. Use this structure:

```yaml
guidance_id: required
work_item_id: required
recipient_ref: required
trigger_event: required
why_now: required
verified_status: required
supporting_artifact_or_evidence_refs: []
recommended_action: required
owner: required
confidence: high|medium|low
approval_required: true|false
expiry_or_freshness: optional
dismissible: true
snooze_options: []
classification: required
```

The rendered message must state: **what changed**, **why it matters**, **what the user can do next**, **who owns the decision**, and **whether approval is required**. Keep it concise. Link to approved artifacts or dashboard views rather than copying sensitive content into the message.

Example pattern:

> **Account research draft is ready for your review.** The evidence check found two current public initiatives and one unresolved assumption. Review the decision packet before using any content for outreach. **Owner:** you. **Status:** internal draft; no message has been sent.

## Decision Request Pattern

When a human decision is required, do not send a generic “please approve.” Create a scoped `DecisionRequest` that specifies the artifact version, action type, account/opportunity/recipient scope, exact diff, evidence summary, risks, expiry, required role, and the results of approve/decline. The IBM Sales action gate remains the authority that validates and releases the action.

## Exception Guidance

For operational failure, avoid exposing implementation details, credentials, or restricted telemetry. State whether the workflow is paused, whether any action may have occurred, and the safe next step. For a potentially ambiguous action result, say that the system is reconciling the action receipt; do not imply that a message, write, or release failed or succeeded until confirmed.

For privacy/security/policy incidents, suppress ordinary nudges, quarantine relevant work items, and follow the configured incident route.

## Feedback and Learning

Capture structured feedback: `helpful`, `not_relevant`, `already_done`, `snooze`, `dismiss`, or a free-text reason if permitted. Use feedback only to improve future guidance after evaluation and change control. Do not self-adjust policy, connection access, skill routing, or notification frequency solely from a single user interaction.

## Boundaries

Never use proactive guidance to send external outreach, change CRM, create meetings, change pipeline/forecast, alter pricing, trigger background customer research, or make commitments. Never use it to make employment, performance, or compensation judgments. Never use a user’s dismissal as evidence that they are underperforming.

## Handoffs

Route a missing process definition to `ibm-sales-workflow-intake-autopilot`; missing role/context to `ibm-sales-role-workflow-cartographer`; missing tool/source to `ibm-sales-mcp-connection-governor`; readiness/benefit questions to `ibm-sales-onboarding-value-data-audit`; and execution planning to `ibm-sales-adaptive-orchestrator`.
