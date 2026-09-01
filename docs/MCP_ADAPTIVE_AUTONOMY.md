# Adaptive MCP Capability Assimilation & Goal-Directed Autonomy

## What happens when the user says “I connected a new MCP”

FAOS does not need a human to manually write dozens of new agent prompts for the connector. The capability assimilation pipeline is:

`CONNECTION EVENT → DISCOVER → SNAPSHOT → DIFF → CLASSIFY → MAP → GENERATE WRAPPERS → QUARANTINE → TEST/CERTIFY → ROUTE → RE-EVALUATE BLOCKED GOALS → CONTINUE`

### 1. Discover the provider surface
For MCP revision **2026-07-28**, the direct HTTP probe uses `server/discover` when available and paginates `tools/list`, `resources/list`, `resources/templates/list`, and `prompts/list`. The 2026-07-28 revision also supports opt-in change streams via `subscriptions/listen`; a host integration may use that to trigger re-assimilation when tools/resources/prompts change.

References:
- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://modelcontextprotocol.io/

For host-managed connectors (ChatGPT/Claude/Bob or a gateway that owns auth/transport), the host exports the same normalized capability snapshot and calls `aos.py assimilate-mcp --snapshot ...` or `POST /mcp/assimilate`.

### 2. “Train itself” means capability learning, not hidden weight updates
FAOS records:
- provider/server identity and protocol revision;
- tool names/descriptions;
- exact input/output JSON schemas when advertised;
- resources/resource templates;
- prompts;
- capability hash/version;
- risk and side-effect classification;
- pocket/team affinity;
- trust/certification state.

It then generates a **quarantined dynamic SKILL.md wrapper** for each advertised capability. This makes the capability addressable by the planner without modifying the canonical 3,212-skill substrate or claiming that a model was retrained.

### 3. New capability ≠ new permission
Discovery only proves that a server advertises a capability. The lifecycle is:

`DISCOVERED → PROFILED → QUARANTINED → READ_ENABLED → WRITE_CERTIFIED`

Writes additionally require policy/decision rights and read-back verification. High-risk classes—money, signatures, destructive actions, production deployment, permissions, legal filings, employment decisions—remain gated even when the connector exposes them.

### 4. Proactive continuation
FAOS stores active goals separately from conversation context. A capability change can trigger a blocker re-evaluation. If the new connector can plausibly satisfy a blocker, the system queues a bounded `RESUME_BLOCKED_GOAL` job.

It may also queue bounded next actions when:
- an active goal has an unresolved next step;
- a scheduled obligation becomes due;
- a connector capability changes;
- an evaluation fails and a recoverable repair is available;
- a monitored condition defined by the goal changes materially.

### 5. Self-prompting is a job queue, not infinite recursion
The system creates structured next-action jobs with dedupe keys, budgets, retry caps, cooldowns and stop conditions. Each job is routed to only the necessary pockets/teams and hydrated with only the required skills.

The agent is **not** allowed to keep inventing new goals indefinitely or recursively prompt itself without an external goal/state trigger.

### 6. Self-improvement is staged
FAOS can propose a new adapter, wrapper, evaluation, route or workflow based on evidence. Changes are written to `proposals/<id>/` in `QUARANTINED` state. Production code is not silently rewritten. Promotion requires tests, policy review and authorized release acceptance.

### 7. Context scaling
Thousands of canonical skills are never placed in one model context. The accountability ledger and registries remain durable state; the hydrator loads the narrow pocket/team skill bundle required for the current job. New MCP-generated skills follow the same progressive-disclosure pattern.

## 8. Autonomous worker plane
The scheduler and worker are separate. `autonomy_tick.py` creates deduplicated jobs from durable triggers. `run_worker.py` claims jobs transactionally. Internal jobs such as direct HTTP MCP re-discovery run automatically. Reasoning jobs are converted into bounded mission plans and sent to `FAOS_AGENT_EXECUTOR_URL` when configured (for example a Bob/watsonx/host execution service). Without an executor, the job stops at `READY_FOR_AGENT` rather than pretending it executed.
