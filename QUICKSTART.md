# Quickstart

## 1. Validate the software release
```bash
python scripts/validate_release.py
python scripts/smoke_test.py
python scripts/audit_package.py
```

## 2. Explore and route
```bash
python aos.py list
python aos.py route "Find an RFP, build the winning submission, and pursue the deal"
python aos.py accountability accounting-accounts-payable-analyst
```

## 3. Create a durable goal and let the bounded proactivity loop advance it
```bash
python aos.py goal "Build and sell a new AI product" --priority 80
python aos.py tick
```
Run `python scripts/autonomy_tick.py --daemon --seconds 300` to schedule bounded jobs and `python scripts/run_worker.py --daemon --seconds 10` to execute internal jobs / hand prepared reasoning jobs to the configured agent executor. Review `policies/autonomy_budget.yaml` first.

## 4. Connect a new MCP/tool
If the host controls the connector transport/auth, export a normalized capability snapshot and run:
```bash
python aos.py assimilate-mcp --snapshot capability_snapshot.json --connector-id my-mcp
```
For a directly reachable MCP 2026-07-28 HTTP endpoint:
```bash
python aos.py assimilate-mcp --url https://example.com/mcp --connector-id my-mcp --token-env MY_MCP_TOKEN
```
Generated skills begin in `QUARANTINED`. Enable/certify the connector only after testing:
```bash
python aos.py certify-connector my-mcp
python aos.py certify-connector my-mcp --write --readback
```

## 5. Hydrate only the team needed
```bash
python aos.py hydrate dealos --team t01 --max-skills 12 --dest /tmp/deal-discovery
```

## 6. Production deploy
```bash
cp config/production.example.json config/production.json
# Bind connector classes to discovered/certified connector instance IDs.
export FAOS_API_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
docker compose up -d
```
`/ready` fails deployment certification while required connector classes remain unbound or uncertified.
