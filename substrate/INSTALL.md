# Installation and Bootstrap

## 1. Trusted Bob workspace
Open the repository as a trusted IBM Bob project. Read `AGENTS.md` first. Project-native assets are under `.bob/`; copy-paste skills are under `skills/`.

## 2. Local validation
Run:
```bash
python scripts/validate_master_package.py
python scripts/triple_check_use_case_satisfaction.py
pytest -q tests/test_v2_domain_harnesses.py
```

## 3. Environment discovery
Do not add secrets to the repository. Bob must inventory actual permissions, IBM services, models, connections, APIs, systems of record, knowledge sources, governance configuration and target environments. Persist only secret references/connection identifiers.

## 4. Domain harness
Use `harnesses/HARNESS_INDEX.json` to choose the smallest relevant DomainBob. Run its `init.sh` or `python scripts/activate_domain_harness.py <domain>` when local mode activation is desired. The shared kernel defaults to analysis/simulation/state/evidence operations and does not silently execute external business actions.

## 5. Compile to watsonx
Compile capabilities, resolve environment-specific dependencies, validate candidates, and promote only reviewed artifacts to `deployment/*/approved/`. Import/deploy only with explicit authority and read back the created objects.

## 6. Runtime acceptance
Complete `release/DEPLOYMENT_ACCEPTANCE_CHECKLIST.md`, including context-loss recovery, authorization denial, system failure, duplicate event/idempotency, human rejection, rollback/read-back, observability and governance evidence.
