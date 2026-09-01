# Proactivity Model

FAOS is event-driven and goal-driven rather than chat-turn-driven.

## Durable triggers
- goal created/changed;
- blocked goal whose dependencies changed;
- schedule/obligation due;
- MCP/connector capability surface changed or became certified;
- data/telemetry condition changed;
- evaluation/release gate failed;
- approved recurring scan;
- human approval state changed.

## Bounded autonomous loop
`EVENT -> DEDUPE -> SELECT GOAL -> PLAN ONE BOUNDED JOB -> POLICY -> HYDRATE -> EXECUTE/DRAFT -> VERIFY -> PERSIST -> ACK`

Every cycle ends. Follow-on work requires another durable event, an approved schedule, or a reconciliation event. Job completion alone does not recursively prompt the system forever.

## Reconciliation safety net
A low-frequency reconciliation loop may re-scan goals/capabilities to recover from missed webhooks. The production default is hourly, not a permanent model-generation loop. It can be disabled when the deployment's event infrastructure and SLOs justify it.

## What the system may do without repeated prompting
Within configured authority it may research, analyze, classify, draft, run local tests, maintain internal state, generate internal artifacts, hydrate skills, assimilate tool schemas, re-evaluate blockers and prepare approval-ready actions.

External communication, commitments, production changes, spending, signatures, legal filings, employment decisions and other consequential writes remain governed by `policies/global_autonomy.yaml`, connector certification and effect-receipt/idempotency rules.
