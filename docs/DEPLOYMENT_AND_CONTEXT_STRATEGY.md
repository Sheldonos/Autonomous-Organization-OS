# Deployment and Context Strategy

The 3,212-skill source archive contains tens of thousands of supporting files. Extracting all of them into every Bob/agent workspace is deliberately avoided.

1. Keep the canonical source ZIP in `substrate/source_archives/`.
2. Use compact registries for routing.
3. Pick the minimum pocket set for a mission.
4. Hydrate only that pocket's top routed skills into a clean workspace.
5. Let the runtime refine skill selection as evidence accumulates.
6. Persist mission state externally; context may be dropped and reconstructed from state + evidence.
7. Dispose or archive mission-specific hydrated workspaces after completion.

This design makes the full corpus available without requiring every active agent to index or reason over every file at once.
