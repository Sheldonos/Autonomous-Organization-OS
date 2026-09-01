---
name: agentic-sdlc-lab-guide-builder
description: A complete workflow for generating end-to-end IBM Agentic SDLC lab guides. Use when a user asks to create a lab guide, workshop, or demo for a codebase that walks developers through Jira, DOORS Next, Solutions Designer, GitLab, and IBM Project Bob.
---

# IBM Agentic SDLC Lab Guide Builder

This skill provides the exact workflow and structural templates required to build high-quality, end-to-end lab guides for the IBM Agentic SDLC pipeline.

These guides are designed for developers (often enterprise or government) to experience the transition from manual coding to AI-assisted architecture and generation.

## The 5-Stage Pipeline

Every lab guide MUST follow this exact 5-stage progression:

1. **Jira:** The raw business requirement (the starting point).

1. **DOORS Next ERM:** AI decomposition into stakeholder requirements.

1. **Solutions Designer:** C4 architectural modeling (Persons, Systems, Containers, Components).

1. **GitLab:** Pushing generated artifacts (OpenAPI, Domain Model, Scaffolded Code).

1. **IBM Project Bob:** The master prompt that generates the final, runnable implementation.

## Workflow

When asked to create a lab guide for a specific codebase or project, follow these steps:

### 1. Audit the Target Codebase

Before writing anything, you MUST understand the target project.

- Clone the repository.

- Read the `README.md` and `ARCHITECTURE.md`.

- Identify a realistic, valuable feature that fits the project's domain (e.g., a Threat Correlation Service for an intelligence dashboard, or a Checkout Saga for an e-commerce site).

### 2. Define the Tangible End Goal

The lab MUST result in a live, runnable piece of code.

- Determine exactly what the user will run (e.g., `npm start` or `./mvnw quarkus:dev`).

- Determine exactly how they will test it (e.g., a specific `curl` or Postman request).

- **CRITICAL:** The generated code MUST NOT require external API keys. Use mock clients, in-memory databases (H2, ConcurrentHashMap), and console loggers for external systems.

### 3. Write the Lab Guide

Use the template provided in `templates/lab_guide_template.md` to write the guide. Do not deviate from the section headers.

### 4. Add Extension Challenges

Always conclude the guide with three "If You Finish Early" extension challenges:

- **Level 1:** Prompt Bob directly for a minor feature addition.

- **Level 2:** Prompt Bob for a new endpoint.

- **Level 3:** Return to Solutions Designer, add a new System/Component, regenerate artifacts, and prompt Bob again. (This teaches the circular nature of the pipeline).

---

## agentic-systems-architect

