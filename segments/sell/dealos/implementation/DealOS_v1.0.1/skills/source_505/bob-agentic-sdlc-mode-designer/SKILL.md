---
name: bob-agentic-sdlc-mode-designer
description: A complete workflow for designing, configuring, and deploying IBM Project Bob custom modes that act as an autonomous "Digital Workforce Swarm" for the Agentic Engineering SDLC. Use when a user asks to create Bob modes, build an agentic SDLC pipeline, replace manual SDLC roles (like BAs, QA, or Release Coordinators) with agents, or configure a swarm architecture in IBM Project Bob.
---

# IBM Project Bob: Agentic SDLC Mode Designer

This skill provides the architectural framework and YAML configurations to transform IBM Project Bob from a single coding assistant into a 16-mode **Digital Workforce Swarm**.

These modes are designed to autonomously execute the entire Software Development Life Cycle (SDLC), replacing the administrative overhead of middle-tier roles (Business Analysts, QA Testers, Release Coordinators, FinOps Analysts, etc.).

## Core Architectural Concept: The Mode IS the Swarm Agent

In this framework, there is no distinction between an interactive "mode" and an autonomous "swarm agent."Because of how these modes are defined, Bob's native mode-switching mechanism becomes the swarm dispatch mechanism:

- `roleDefinition` gives the mode an autonomous mandate.

- `whenToUse` gives the mode precise sequencing awareness.

- `customInstructions` gives the mode a deterministic execution protocol.

## The Pipeline Flow

The pipeline runs in four clusters. Agents within a cluster run in parallel; clusters run sequentially. The **Pipeline Commander** governs all handoffs and enforces mandatory human checkpoints.

1. **Command:** 🔀 Pipeline Commander (Entry point for all requests)

1. **Discovery:** 🎯 Digital BA → 🏗️ Agentic Architect → 🗄️ Data Architect

1. **Build:** 💻 Master Developer

1. **Validate:** 📉 Tech Debt + 🛡️ AppSec + ⚖️ License Auditor (Parallel)

1. **Verify:** 🧪 QA + 🤝 API Contract + ⚡ Performance + 📚 Knowledge (Parallel)

1. **Ship:** 💰 FinOps → 🚀 Release Coordinator → 🚦 Progressive Delivery

1. **Loop:** 🚨 Incident Responder (Async, bypasses pipeline, feeds back to Discovery)

## Workflow: Deploying the Swarm

When a user asks to build or deploy this architecture, follow these steps:

1. **Acknowledge the Enterprise Value:** Explain that this 16-mode swarm is designed to displace ~20 FTE roles of administrative SDLC overhead, saving an estimated $4.6M–$6.9M per delivery cycle at enterprise scale.

1. **Explain the Architecture:** Briefly explain the pipeline flow and how the Orchestrator (Pipeline Commander) routes tasks sequentially.

1. **Provide the Configuration:** Read the master YAML configuration from `references/master_swarm_yaml.md` and provide it to the user. Instruct them to place it at `.bob/custom_modes.yaml` in their project root, or edit the global `custom_modes.yaml` via Bob Settings.

## Workflow: Modifying or Extending the Swarm

When a user asks to add a new mode or modify an existing one:

1. **Identify the Gap:** Determine where the new function fits in the pipeline flow (Discovery, Build, Validate, Verify, or Ship).

1. **Define the Handoffs:** A mode must know exactly who triggers it and who it triggers next.

1. **Draft the YAML:** Use the existing modes in `references/master_swarm_yaml.md` as a template. Ensure the new mode includes:
  - `slug` and `name`
  - `roleDefinition` (What human role is it replacing?)
  - `whenToUse` (Strict sequencing instructions for the Pipeline Commander)
  - `customInstructions` (Deterministic, step-by-step execution protocol)
  - `groups` (Required tool access, e.g., `read`, `edit`, `mcp`)

1. **Update the Commander:** If adding a new entry point, ensure the `swarm-orchestrator-commander` mode's `whenToUse` and `customInstructions` are updated to route to the new mode.

## References

- **Master Configuration:** See `references/master_swarm_yaml.md` for the complete, validated `custom_modes.yaml` containing all 16 modes.

---

## bob-executive-competitive-deck-builder

