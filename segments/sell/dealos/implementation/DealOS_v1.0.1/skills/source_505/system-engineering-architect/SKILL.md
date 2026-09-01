---
name: system-engineering-architect
description: Use when the user wants to design a system, architect a distributed service, create a technical architecture, or asks Bob to plan infrastructure, APIs, storage, or scalability for any application. Guides Bob through the IBM 5-Phase Architectural Workflow — requirements, API design, functional decomposition, scale optimization, and resilience review — enforcing storage justification, path separation, and NFR-driven decisions.
---

# System Engineering Architect Playbook

Activate this skill for any system design, architecture, or infrastructure planning request.
Never generate diagrams, scaffolding, or storage decisions before completing Phases 1–2.
Keep the companion `reference.md` file open for storage rules, scale thresholds, and archetype constraints.

---

## Phase 1 — Orchestrator Mode: Requirements & Scope

**Goal:** Establish exact system parameters before any design begins.

1. Use `ask_followup_question` to gather:
   - **Functional requirements** — what must the system do? (e.g., "users can upload video", "drivers stream location")
   - **NFRs (all five dimensions):** Scale (QPS / data size / user count), Latency (p50/p99 targets), Availability (SLA %), Consistency (ACID vs. BASE), Durability (retention, backup SLA)
   - **Out-of-scope** — explicitly declare what will NOT be built to prevent architectural bloat

2. Do not proceed to Phase 2 until all five NFR dimensions are quantified. If the user cannot provide them, supply reasonable defaults and confirm them explicitly.

3. Identify the **canonical archetype** (see `reference.md` § Archetypes). If a match exists, all archetype-specific constraints are mandatory.

---

## Phase 2 — Architect Mode: API & Sequence Design

**Goal:** Map user and system interactions before defining any components.

1. Draft the **System API surface** — generate OpenAPI endpoint stubs or a summary table covering primary user-facing operations and async event triggers. Keep it tightly bounded around user intent.

2. Produce **sequence diagrams** (Mermaid or prose) tracing at least one happy-path user action from the API through backend services to persistence and back.

3. **Separate paths explicitly:**
   - Synchronous serving path (reads, low-latency responses)
   - Asynchronous processing path (writes, heavy computation, fan-out)

   Do not continue to Phase 3 if both paths are not explicitly identified.

---

## Phase 3 — Architect Mode: Functional Decomposition

**Goal:** Decompose the system into bounded, domain-specific services.

1. Define each service by its **single responsibility** — no service owns two distinct domains.

2. For every service that requires persistent storage, apply the **Storage Selection Protocol** (see `reference.md` § Storage):
   - State the access pattern (e.g., "point lookup by key, <10ms")
   - State the consistency requirement (ACID or BASE)
   - Select the storage type and document the justification
   - **Rule 5:** Every SQL selection must cite the specific ACID requirement. If none exists, NoSQL or K/V is preferred.

3. Confirm that **Rules 1–5** from `reference.md` are not violated before finalizing any service's storage choice.

---

## Phase 4 — Plan Mode: Scale & Performance Optimization

**Goal:** Apply targeted optimizations for each NFR that crosses a scale threshold.

1. Check every scale trigger in `reference.md` § Scale Thresholds against the NFRs defined in Phase 1. For each threshold crossed, apply the required optimization — no exceptions.

2. Run the **Async Pipeline Decision Tree** (`reference.md` § Decision Tree) for every write operation or background task. Any "Yes" answer mandates an async pipeline.

3. Document optimization traceability: every CDN, queue, cache, Bloom filter, or Geohash must reference the specific NFR or scale trigger that justifies it.

---

## Phase 5 — Review Mode: Resilience & Dependency Auditing

**Goal:** Audit for failure modes before finalizing the design.

1. **SPOF analysis** — identify every single point of failure and document the mitigation (e.g., multi-AZ, replica sets, queue buffering).

2. **External dependency review** — for every third-party service (payment processor, banking API, email provider, CDN):
   - Define the failure mode
   - Define the compensation strategy (circuit breaker, retry with backoff, fallback, dead-letter queue)

3. **Depth Score Check** — before delivering the final design, verify all six mandatory elements are present:
   - [ ] All five NFR dimensions quantified
   - [ ] API-first artifact (OpenAPI stubs or sequence diagram) produced before components
   - [ ] Every storage choice has a documented access-pattern justification
   - [ ] Sync and async paths are explicitly separated
   - [ ] Every optimization traces to a scale trigger or NFR
   - [ ] Every external dependency has a documented failure mode and compensation strategy

   If any item is unchecked, complete it before delivering the output.

---

## Output Format

Deliver the final architecture as a structured document:

```
1. System Overview (1 paragraph)
2. Functional Requirements (bulleted)
3. Non-Functional Requirements (table: dimension / target / rationale)
4. System API (endpoint table or OpenAPI summary)
5. Sequence Diagram (at least one happy path)
6. Service Decomposition (service name / responsibility / storage choice / justification)
7. Scale Optimizations (optimization / trigger / traceability)
8. Resilience & Failure Modes (dependency / failure mode / compensation)
```

Reference `reference.md` at any point for storage rules, scale thresholds, decision trees, and archetype constraints.
