---
name: ibm-bob-requirements-orchestrator
description: A framework for writing and executing an IBM Project Bob Orchestrator Mode prompt that ingests DOORS Next requirements and IBM DevOps Solution Workbench artifacts, then drives Bob through its full Architect → Plan → Code → Review cycle with end-to-end traceability from requirements to generated code. Use when a user asks to generate a Bob prompt that is requirements-aware, wants Bob to trace every function back to a DOORS Next SR ID, needs to orchestrate all four Bob modes in a single structured prompt, or wants to automate the requirements-to-code pipeline for any IBM Solution Workbench use case.
---

# IBM Project Bob — Requirements Orchestrator

This skill builds a single structured **Orchestrator Mode prompt** that tells IBM Project Bob:

1. What the DOORS Next requirements baseline is (BRs and SRs)

1. What the Solution Workbench architecture looks like (C4 diagrams, domain model, APIs)

1. How to drive itself through all four modes: Architect → Plan → Code → Review

1. How to enforce traceability: every generated function must cite the SR ID it satisfies

Read `references/bob_modes.md` for the exact behavior of each Bob mode and the traceability rule.

---

## When to Use This Skill

Trigger on any of these:

- "Build a Bob prompt that knows the requirements"

- "Make Bob trace code back to DOORS Next"

- "Orchestrate Bob through all four modes"

- "Generate the requirements-to-code prompt for [Company] / [Use Case]"

- "Run the Bob orchestrator for [Use Case]"

---

## Workflow

### Step 1 — Gather Inputs

Collect or confirm the following. If any are missing, generate them using the `ibm-solution-accelerator` or `ibm-solution-architect-web` skills first.

| Input | Source | Required |
| --- | --- | --- |
| Company name | User | Yes |
| Use case name | User | Yes |
| DOORS Next baseline ID | User or generated | Yes (default: `BL-001`) |
| Business Requirements (BRs) | DOORS Next export or generated | Yes |
| System Requirements (SRs) | DOORS Next export or generated | Yes |
| Domain Model JSON | Solution Workbench output | Yes |
| OpenAPI YAML specs | Solution Workbench output | Yes |
| Scaffolded code stubs | Solution Workbench output | Yes |
| C4 Container Diagram description | Solution Workbench output | Yes |

If requirements do not yet exist, generate them inline using this format before proceeding:

```
BR-01: [Action verb] [measurable outcome]
       Rationale: [business impact]
       Source: [stakeholder role]

SR-01.1: The system SHALL [specific technical behavior]
         Traces to: BR-01
         Priority: Must Have | Should Have | Nice to Have
```

Produce 5–8 BRs and 2–3 SRs per BR. Include a domain glossary.

---

### Step 2 — Build the Requirements JSON

Save requirements to a JSON file using the structure in `templates/sample_requirements.json`. This file is the single source of truth for the orchestrator prompt builder.

Required fields:

- `project`, `company`, `baseline_id`

- `services[]`: name, tech, description for each container

- `business_requirements[]`: id, statement, rationale, source

- `system_requirements[]`: id, statement, traces_to, priority

---

### Step 3 — Run the Prompt Builder Script

```bash
python3 skills/ibm-bob-requirements-orchestrator/scripts/build_orchestrator_prompt.py \
  --company "[Company]" \
  --use-case "[Use Case]" \
  --baseline-id "[BL-XXX]" \
  --requirements [path/to/requirements.json] \
  --domain-model [path/to/domain_model.json] \
  --openapi-specs "[spec1.yaml,spec2.yaml]" \
  --scaffolded-stubs "[stub1.js,stub2.java]" \
  --output bob_orchestrator_prompt.md
```

The script produces a fully assembled `bob_orchestrator_prompt.md` with all four mode sections populated.

---

### Step 4 — Review and Finalize the Prompt

Open the generated `bob_orchestrator_prompt.md` and verify:

- All `{{PLACEHOLDER}}` tokens are replaced (none should remain)

- The domain model JSON is not truncated beyond what Bob needs to understand the entities

- The scaffolded stubs are embedded in full (not summarized) — Bob needs the actual `// TODO [BOB]:` markers

- The traceability matrix rows match the SR count

If any OpenAPI YAML files are large (>500 lines), summarize the endpoints in the prompt and instruct Bob to "attach full YAML" — do not embed the entire file.

---

### Step 5 — Deliver

Deliver three files:

1. `bob_orchestrator_prompt.md` — the complete prompt, ready to paste into Bob

1. `requirements.json` — the structured requirements file for future re-runs

1. A brief usage note explaining how to use the prompt in Bob (see below)

**How to use the prompt in IBM Project Bob:**

1. Open IBM Project Bob in your browser

1. Start a new session or open the relevant project

1. Paste the entire contents of `bob_orchestrator_prompt.md` as a single message

1. Bob will process all four sections sequentially — do not interrupt between sections

1. After Bob completes Review Mode, copy the Traceability Matrix and Bob Session Summary into your DOORS Next project as a linked artifact

---

## Key Rules

- The `// Implements: SR-xx.x` comment is **mandatory** on every non-trivial function. This is the single most important rule — it is what makes the output auditable and traceable back to the requirements baseline.

- Never omit the SECTION 0 context injection. Bob must read the requirements before it enters Architect Mode or it will generate code that is architecturally correct but requirements-blind.

- The Review Mode traceability matrix must be delivered back to DOORS Next as a linked artifact. This closes the loop: DOORS Next → Solution Workbench → Bob → DOORS Next.

- If Bob is being used in an existing project (not a new session), prepend SECTION 0 only and reference the existing architecture context rather than re-injecting the full C4 diagram.

---

## ibm-bob-skills-implementation

