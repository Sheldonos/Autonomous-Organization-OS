---
name: startup-builder-architect
description: A complete startup qualification engine. Use when a user provides a raw startup idea and asks to qualify it, map out the technical architecture, score its feasibility, or generate an investor pitch deck. This skill transforms a raw concept into a fully structured, investor-ready business and technical plan.
---

# Startup Builder Architect

This skill is a comprehensive engine for qualifying, architecting, and packaging a startup idea. It takes a raw concept and subjects it to rigorous market analysis, technical mapping, and investor-grade scoring, culminating in a complete pitch deck.

## The 4-Phase Qualification Workflow

When a user asks to qualify a startup idea, map its architecture, or build a pitch deck, execute these four phases sequentially.

### Phase 1: Market Gap & Feasibility Analysis

Before writing any code or drawing any diagrams, you must prove the idea is viable.

1. **Analyze the Market:** Identify the specific friction points and data silos the idea solves.

1. **Identify the Moat:** Determine what makes this idea defensible (e.g., proprietary data, network effects, high switching costs).

1. **Define the Revenue Model:** Map out at least two distinct revenue streams (e.g., B2C subscription + B2B licensing).

### Phase 2: The Composite Confidence Score (CCS)

You must score the idea objectively using the 5-dimension framework.

1. Read the scoring framework: `/home/ubuntu/skills/startup-builder-architect/references/scoring-framework.md`

1. Calculate the score across all 5 dimensions (Market Gap, Technical Feasibility, Moat, Revenue Model, Founder-Market Fit).

1. Output the final CCS (0-100) and the recommended action (e.g., "Investor-Ready" or "Needs Rework").

### Phase 3: Technical Architecture Mapping

Map the idea into a concrete, 5-layer technical architecture.

1. Read the architecture guide: `/home/ubuntu/skills/startup-builder-architect/references/technical-architecture.md`

1. Define the 5 layers: Client, API/Business Logic, AI/Intelligence, Data, and Infrastructure.

1. Generate a visual architecture diagram using the `manus-render-diagram` utility (use D2 for complex architectures, Mermaid for simpler ones).

1. Flag any regulatory or compliance requirements (HIPAA, SOC2, GDPR).

### Phase 4: Investor Pitch Deck Generation

If the CCS is above 60 (or if the user explicitly requests it), generate a complete 14-slide investor pitch deck.

1. Read the pitch deck template: `/home/ubuntu/skills/startup-builder-architect/references/pitch-deck-template.md`

1. Use the `slide_initialize` tool in `image` mode to create the deck structure.

1. Generate high-fidelity mobile or web app screen mockups using the `generate` tool to serve as visual assets for the product slides.

1. Use the `image_slide_generate` tool to build out all 14 slides, incorporating the generated mockups and the cinematic design system.

1. Present the final deck using the `slide_present` tool.

## Execution Guidelines

- **Be Objective:** Do not artificially inflate the Confidence Score. If an idea has no moat or a weak revenue model, score it accordingly and suggest pivots.

- **Be Specific:** In the technical architecture, name specific technologies (e.g., "PostgreSQL for relational data, Redis for caching, FastAPI for the core routing"). Avoid generic terms like "a database."

- **Focus on the "Why Now":** Investors invest in timing as much as technology. Ensure the analysis highlights why this specific idea is possible *today* (e.g., a new AI model release, a regulatory change).

---

## strategic-foresight

