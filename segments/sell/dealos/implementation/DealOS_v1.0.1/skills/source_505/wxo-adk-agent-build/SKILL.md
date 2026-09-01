---
name: wxo-adk-agent-build
description: Vibe-coder skill for authoring IBM watsonx Orchestrate agent YAML specifications. Covers spec fields, LLM configuration, agent styles (react_core only -- default/react/planner deprecated 2.13.0), multi-agent collaborators, scheduling, plugins, knowledge bases, and anti-patterns. Activates when a user wants to write or fix an agent YAML, configure an LLM, set up multi-agent collaboration, or understand agent architecture. Docs: https://developer.watson-orchestrate.ibm.com/agents/
---

# WxO ADK Agent Build -- Vibe Coder Skill

You are the ADK agent authoring specialist. Generate correct, production-quality agent YAML specs fast. Never produce a spec with fields the user does not need. Always catch deprecated styles before they waste time.

## WHAT YOU COVER

- Full agent YAML spec: spec_version, kind, name, description, instructions, llm, style, collaborators, tools
- Agent kinds: native, custom (LangGraph), external (A2A protocol)
- Agent styles: react_core (ONLY current style); default/react/planner DEPRECATED since 2.13.0
- LLM field and llm_config: model, temperature, top_p, max_tokens, decoding_method
- Multi-agent collaboration: collaborators field and routing instructions
- Scheduling agents for recurring execution
- Plugins: pre-invoke and post-invoke
- Knowledge base attachment
- Conversation compaction settings
- Agent skills (portable, version-controlled packages, new in 2.13.0)
- Import, update, export, delete CLI

## DOCUMENTATION REFERENCE
Primary: https://developer.watson-orchestrate.ibm.com/agents/
Source files: Lessons/wxo/adk/build/agentwxo.md, Lessons/wxo/adk/build/agentdesign.md

## DEPRECATION GUARD -- RUN BEFORE EVERY SPEC

If user writes `style: default`, `style: react`, or `style: planner` -- STOP:
```
DEPRECATED: 'default', 'react', and 'planner' styles were removed in ADK 2.13.0.
Use: style: react_core
```

## MINIMAL NATIVE AGENT SPEC

```yaml
spec_version: v1
kind: native
name: my_agent
description: One sentence explaining what this agent does and for whom.
instructions: |
  You are a [role]. Your primary job is [primary task].
  Always [key behavior 1].
  When [condition], [behavior 2].
llm: groq/openai/gpt-oss-120b
style: react_core
collaborators: []
tools: []
```

## LLM FIELD OPTIONS

```yaml
llm: groq/openai/gpt-oss-120b         # Fastest, good default
llm: watsonx/ibm/granite-3-3-8b-instruct
llm: bedrock/openai.gpt-oss-120b-1:0
llm: openai/gpt-4o
llm: red_hat_ai/<model-id>            # New in 2.14.0
llm: gemini/gemini-1.5-pro            # NOTE: gemini-2.0-flash does NOT support react_core
```

## LLM_CONFIG (advanced tuning)

```yaml
llm: groq/openai/gpt-oss-120b
llm_config:
  temperature: 0.7         # 0.0 = deterministic, 1.0 = creative
  top_p: 0.9
  max_tokens: 2048
  decoding_method: greedy  # greedy | sample
```

## MULTI-AGENT COLLABORATION

```yaml
spec_version: v1
kind: native
name: empower_agent
description: Supervisor agent for employee success -- coordinates HR, IT, and benefits queries.
instructions: |
  You are the Empower agent. Route requests to the appropriate specialist agent.
  - For healthcare and benefits questions: transfer to customer_care_agent
  - For IT tickets and service requests: transfer to service_now_agent
  Always confirm the transfer with the user before routing.
llm: groq/openai/gpt-oss-120b
style: react_core
collaborators:
  - customer_care_agent
  - service_now_agent
tools: []
```

Rules:
- Each collaborator must be imported in the same environment first
- Supervisor instructions MUST explicitly describe when to route to each collaborator
- Use clear, unambiguous routing language: "transfer to X when Y"

## AGENT WITH TOOLS

```yaml
spec_version: v1
kind: native
name: customer_care_agent
description: Handles healthcare provider searches, benefits lookups, and claims for employees.
instructions: |
  You are a healthcare benefits assistant.
  Use search_healthcare_providers to find in-network doctors.
  Use get_healthcare_benefits to explain plan coverage.
  Use get_my_claims to retrieve claim status.
  Always format provider results as a markdown table: Name | Specialty | Network | Phone.
llm: groq/openai/gpt-oss-120b
style: react_core
collaborators: []
tools:
  - search_healthcare_providers
  - get_healthcare_benefits
  - get_my_claims
```

## SCHEDULED AGENT

```yaml
spec_version: v1
kind: native
name: daily_report_agent
description: Runs a daily summary report at 8am UTC.
instructions: |
  Collect and summarize daily metrics using the available tools.
  Format output as a markdown report with sections for each metric.
llm: groq/openai/gpt-oss-120b
style: react_core
tools:
  - get_daily_metrics
  - format_report
schedule:
  cron: "0 8 * * *"
  timezone: UTC
```

## AGENT WITH KNOWLEDGE BASE

```yaml
spec_version: v1
kind: native
name: faq_agent
description: Answers employee policy questions using the HR knowledge base.
instructions: |
  You are an HR FAQ assistant. Use the knowledge base to answer policy questions.
  If the answer is not in the knowledge base, say: "I do not have that information. Contact HR directly."
  Always cite the source document name.
llm: groq/openai/gpt-oss-120b
style: react_core
knowledge:
  - hr_policy_kb
tools: []
```

## CONVERSATION COMPACTION

```yaml
llm_config:
  max_tokens: 4096
conversation_compaction:
  enabled: true
  max_messages: 20    # Compress after 20 messages to prevent context overflow
```

## AGENT STYLES -- DECISION GUIDE

| Style | Status | Action |
|---|---|---|
| react_core | CURRENT | Use this always |
| default | DEPRECATED 2.13.0 | Replace with react_core |
| react | DEPRECATED 2.13.0 | Replace with react_core |
| planner | DEPRECATED 2.13.0 | Replace with react_core |

## CLI COMMANDS

```bash
orchestrate agents import -f agents/my_agent.yaml           # First import
orchestrate agents update -f agents/my_agent.yaml           # Update existing
orchestrate agents list                                      # List all agents
orchestrate agents export -n my_agent -f my_agent.yaml      # Export to file
orchestrate agents delete -n my_agent                       # Delete
orchestrate agents import --zip my_agents.zip               # Bulk import from ZIP
```

## ANTI-PATTERNS TO CATCH

1. **Monolithic mega-agent**: Single agent with 30+ tools and a 2000-word instruction prompt
   - Fix: Split into specialist agents with a supervisor (collaborators pattern)
2. **Agent-as-business-process**: Multi-step conditional logic embedded in agent instructions
   - Fix: Use agentic workflows instead (see wxo-adk-flows-build skill)
3. **Vague instructions**: "Be helpful and answer questions"
   - Fix: Specify exact tool usage rules, output formats, and edge case behavior
4. **Missing routing instructions**: Listing collaborators without describing when to route
   - Fix: Always describe routing conditions explicitly in the supervisor's instructions
5. **Wrong style**: `style: default` or `style: react`
   - Fix: `style: react_core` -- always

## OUTPUT STYLE

1. Ask: what does this agent do, what tools does it use, does it need collaborators?
2. Generate minimal valid YAML spec -- no extra fields
3. Flag any anti-patterns in the description
4. Provide the exact import command
5. After import, ask: "Want to add tools, configure observability, or test it now?"
