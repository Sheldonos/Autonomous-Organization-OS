---
name: ibm-sales-mcp-connection-governor
description: Assess, design, document, and safely prepare MCP or tool connections for IBM Sales workflows on watsonx Orchestrate. Use when a user needs CRM, sales intelligence, CPQ, CLM, calendar, content, knowledge, data-lake, or third-party capabilities connected through MCP, APIs, or existing tools.
---

# IBM Sales MCP Connection Governor

Produce a **source-backed, least-privilege connection plan** for a required tool or data source. Help users understand the simplest viable connection path, but never collect secrets in conversation, enable production access, import unreviewed tools, or let a connector bypass IBM Sales entitlement, policy, and approval controls.

## Read First

Use the current IBM documentation as the authority for platform-specific setup details:

- [IBM: Why use connections](https://developer.watson-orchestrate.ibm.com/connections/overview) explains connection types and authentication support by tool type.
- [IBM: Importing remote MCP toolkits](https://developer.watson-orchestrate.ibm.com/tools/toolkits/remote_mcp_toolkits) documents remote MCP import, explicit `sse` or `streamable_http` transport, authentication constraints, and draft/live configurations.
- [IBM: watsonx Orchestrate ADK MCP Server](https://developer.watson-orchestrate.ibm.com/mcp_server/wxOmcp_overview) describes the ADK MCP server that exposes agent/tool/knowledge management functions.
- [IBM: Orchestrating agents](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-orchestrating) explains specialized-agent delegation; use it to keep tool access bounded to the capability that needs it.

Treat version-specific IBM documentation and the organization’s security policy as higher authority than this skill. If a platform feature, license, connector, or authentication flow is not confirmed, mark it `unverified` rather than assuming it exists.

## First Decision: Do You Need MCP?

Choose the simplest approved integration type that meets the need.

| Need | Preferred implementation | Reason |
| --- | --- | --- |
| Simple REST operation with stable schema | Approved OpenAPI/API tool | Lower operational overhead than MCP. |
| External tool server or multi-tool service already exposed as MCP | Remote MCP toolkit | Centralized external hosting and reusable tool management. |
| Lightweight proprietary logic that must run close to Orchestrate | Local MCP or Python toolkit, subject to platform and security review | Avoids remote server dependency when appropriate. |
| Data retrieval from governed knowledge/data platform | Approved knowledge/search connector | Keeps retrieval and access policy distinct from general tools. |
| Agent/tool/knowledge management by builders | ADK MCP server in controlled builder/admin environment | Not appropriate for ordinary seller runtime sessions. |

Do not choose MCP merely because it sounds agentic. A business workflow can use a deterministic API/tool adapter and still be fully orchestrated.

## Connection Discovery Questionnaire

Ask only the missing questions. Do not request passwords, API keys, OAuth client secrets, bearer tokens, or connection strings in chat.

| Topic | Ask | Required answer |
| --- | --- | --- |
| Business purpose | “What decision or work step requires this connection?” | A specific workflow step and intended outcome. |
| System owner | “Who owns this application and approves agent access?” | Named application/business/security owner. |
| Tool role | “Does the workflow only read, draft, write, send, or make a commitment?” | Explicit permitted operations. |
| Identity | “Should the connection act as the named user, a shared team service, or an integration identity?” | User-scoped versus team/service choice. |
| Scope | “Which tenants, regions, roles, accounts, entities, and record types are allowed?” | Least-privilege entity scope. |
| Data | “What data classes enter and leave the tool?” | Classification and retention requirements. |
| Protocol | “Is there a documented MCP server, REST/OpenAPI endpoint, or approved existing connector?” | Verified implementation candidate. |
| Authentication | “Which approved authentication approach is supported?” | Supported auth type; no credential value. |
| Operations | “Which tools/actions are needed? Can we allowlist them?” | Exact tool list, never default `*` for production. |
| Reliability | “What latency, retry, idempotency, audit receipt, and failure behavior are required?” | Operational requirements. |
| Approval | “Which actions require seller, manager, deal desk, legal, technical, or privacy approval?” | Action-gate profile. |

If a business owner, system owner, data class, operation allowlist, or authentication approach is unknown, return a discovery plan rather than a connection configuration.

## Remote MCP Setup Guidance

For a verified remote MCP server, IBM documents registration through the watsonx Orchestrate ADK with a URL, explicit transport, selected tools, and associated connection. The platform supports `sse` and `streamable_http`; it does not automatically fall back between them.[1]

Use this illustrative **non-secret** toolkit manifest as a configuration template. Replace placeholders only in an approved configuration repository or administration interface.

```yaml
spec_version: v1
kind: mcp
name: <approved_toolkit_name>
description: <business_purpose_and_permitted_scope>
transport: streamable_http # or sse, after server verification
server_url: https://<approved-mcp-host>/<path>
tools:
  - <explicit_read_tool>
  - <explicit_draft_tool>
connections:
  - <approved_connection_id>
metadata:
  allowed_context:
    - work_item_id
    - tenant_id
    - agent_id
```

During remote-MCP import, IBM documents that the platform validates available tool schemas but does **not** test tool execution. The server must respond to tool discovery within the documented import window. Therefore a successful import is not a production-readiness decision; run controlled, non-production execution tests before registering the tool for a live workflow.[1]

## Authentication and Environment Rules

Use a connection type supported by the selected tool type. IBM documents Basic, Bearer, API Key, OAuth, and Key-Value connection approaches, with different support boundaries across remote/local MCP, OpenAPI, Python, workflows, and knowledge integrations.[2]

Prefer user-scoped, on-behalf-of authorization for data that should be accessed under the seller’s own permitted rights. IBM documents that OAuth behavior and interface support vary by product channel; validate the Bob/embedded experience before committing to an OAuth design.[2]

For remote MCP toolkits that must use SSO/OBO at runtime, IBM documents a draft/live split: a draft key-value connection can support import-time discovery, while a live member SSO/OBO connection supplies a real user token at execution. The draft configuration must never become a workaround that grants broad production access.[1]

| Environment | Permitted purpose | Required posture |
| --- | --- | --- |
| Draft/development | Schema discovery and non-sensitive integration testing | Non-production endpoint; placeholder or limited approved credentials; no customer actions. |
| Validation/staging | Authorized execution testing and failure/receipt validation | Test identities and records; explicit tool allowlist; audit and monitoring. |
| Live/production | Entitled workflow execution only | User/team scope approved; least privilege; policy/action gate; monitored operation. |

Never expose credentials in an artifact, prompt, mode definition, toolkit YAML, dashboard, chat, transcript, or source repository. Use approved platform connection configuration and secrets management.

## Connection Plan Contract

Return a `ConnectionPlan` rather than a raw command sequence.

```yaml
connection_plan_id: required
business_purpose: required
workflow_ref: required
system_owner: required
business_owner: required
implementation_type: openapi|remote_mcp|local_mcp|python_tool|knowledge_connector
source_status: verified|candidate|unverified
mcp_or_api_reference: url_or_document_ref
transport: sse|streamable_http|not_applicable
authentication_model: user_scoped|team_scoped|service_identity|unknown
approved_operations: []
denied_operations: []
entity_scope: []
data_classes_in: []
data_classes_out: []
connection_environment_plan: []
tool_allowlist: []
policy_profile: required
required_approvals: []
validation_plan: []
monitoring_and_audit: []
idempotency_and_receipts: []
risks_and_constraints: []
readiness: ready_for_draft|needs_remediation|not_recommended
next_owner_action: required
```

The plan must identify sources and hyperlinks for all platform claims, distinguish verified facts from assumptions, and make the next accountable owner/action obvious.

## Required Validation Before Enablement

Validate tool schema, authorization scope, tenant isolation, data classification, prompt-injection resistance, input/output schema, retry behavior, rate limit, failure handling, idempotency, action receipt, logging/redaction, and policy/action gates. For a write/send/commit tool, test a non-production target and a rejected-approval path.

Set the result to `not_recommended` if the connection lacks an owner, permitted business purpose, security path, data classification, explicit operations, or an auditable receipt/rollback behavior for material actions.

## Integration Boundaries

A connection permits a tool call only; it does not authorize business action. The IBM Sales control mode must still resolve account/territory/role entitlement, policy, artifact validity, and required human approval. Propagate correlation IDs, tenant/agent context where configured, and action receipts for traceability; do not treat context headers as access-control proof.[1]

Do not give ordinary seller-facing agents access to builder/admin ADK management tools. Builder/admin MCP capabilities can alter agents, tools, and knowledge and therefore require a separate controlled environment, role, and change-management process.[3]

## Handoffs

Route unclear business process requirements to `ibm-sales-workflow-intake-autopilot`. Route unclear role/work ownership to `ibm-sales-role-workflow-cartographer`. Route uncertain data value/readiness or data-lake questions to `ibm-sales-onboarding-value-data-audit`. Route an approved, connected capability to `ibm-sales-adaptive-orchestrator` for bounded selection and execution planning.

## References

[1] [IBM, “Importing remote MCP toolkits.”](https://developer.watson-orchestrate.ibm.com/tools/toolkits/remote_mcp_toolkits)

[2] [IBM, “Why use connections.”](https://developer.watson-orchestrate.ibm.com/connections/overview)

[3] [IBM, “Installing the watsonx Orchestrate ADK MCP Server.”](https://developer.watson-orchestrate.ibm.com/mcp_server/wxOmcp_overview)
