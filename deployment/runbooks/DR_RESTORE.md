# DR Restore Drill

- Select the newest off-site/immutable backup that satisfies the target RPO.
- Verify the backup manifest and hashes before modifying a recovery environment.
- Restore into an isolated recovery path first.
- Run SQLite/database integrity checks and FAOS release validation.
- Start the control plane with external writes drained.
- Reconnect read-only dependencies before write-capable connectors.
- Inspect dead letters and effect receipts before replaying queued work.
- Re-enable one pocket at a time and record achieved RTO/RPO.
