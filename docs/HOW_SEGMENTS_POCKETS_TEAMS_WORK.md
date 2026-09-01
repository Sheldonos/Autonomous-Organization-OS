# How Segments, Pockets, and Teams Work

## Hierarchy
`MISSION → SEGMENT → POCKET → TEAM → SKILL/TOOL/FLOW`

A **segment** is a broad organizational plane (MAKE, SELL, RUN, PROTECT, INVEST, CREATE, LEARN). A **pocket** is an opinionated operating system such as DealOS or BuildOS. A **team** owns a workflow stage inside a pocket. Skills remain shared substrate capabilities; they are hydrated only when a pocket/team needs them.

## Composite missions
A mission can invoke multiple pockets. EnterpriseOS becomes supervisory control when more than one pocket is needed. Work moves between pockets through typed handoff packets, with evidence references and authority state attached.

## State
Conversation context is never the source of truth. `runtime/state.py` provides a local SQLite reference implementation for durable mission/event/approval/evidence state. Production deployments should map the same contract to an enterprise database/event system.

## Assurance
Every pocket receives an Assurance & Evaluation Team and an Integration & State Team in addition to stage-specific execution teams. Assurance can block a stage when evidence, policy, quality, or read-back is insufficient.
