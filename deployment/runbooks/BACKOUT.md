# Backout Runbook

1. `python scripts/set_drain.py on --db <capability.db>`
2. Confirm no new external executor handoffs are occurring.
3. Snapshot/backup current state even if the release is unhealthy.
4. Route API traffic to the previous known-good OCI digest.
5. Keep the current database unless the migration plan explicitly certifies a reverse migration.
6. Run `python scripts/process_events.py --db <capability.db>` to drain safe control events after rollback.
7. Validate `/health`, `/ready`, connector read-back, queue depth and effect receipts.
8. Re-enable writes with `python scripts/set_drain.py off ...` only after validation.

Never delete the event queue, jobs, evidence, or effect receipts to make a rollback appear clean.
