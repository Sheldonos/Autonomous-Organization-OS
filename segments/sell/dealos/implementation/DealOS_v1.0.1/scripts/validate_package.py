from pathlib import Path
import json, yaml, sys, re
root=Path(__file__).resolve().parents[1]
errors=[]
source=list((root/'skills'/'source_505').glob('*/SKILL.md'))
wrappers=[p for p in (root/'skills').glob('dealos-*/SKILL.md')]
if len(source)!=505: errors.append(f'Expected 505 source skills, found {len(source)}')
if len(wrappers)!=12: errors.append(f'Expected 12 DealOS wrappers, found {len(wrappers)}')
for p in root.rglob('*.json'):
    try: json.loads(p.read_text())
    except Exception as e: errors.append(f'Invalid JSON {p.relative_to(root)}: {e}')
for p in list((root/'policies').glob('*.yaml'))+[root/'skills'/'routing.yaml',root/'chatgpt'/'action-openapi.yaml']:
    try: yaml.safe_load(p.read_text())
    except Exception as e: errors.append(f'Invalid YAML {p.relative_to(root)}: {e}')
for rel in ['README.md','QUICKSTART.md','.env.example','docker-compose.yml','TOOLING_AND_CONFIGURATION.md','supabase/schema.sql']:
    if not (root/rel).exists(): errors.append(f'Missing {rel}')
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'PASS: {len(source)} source skills + {len(wrappers)} DealOS wrappers; JSON/YAML/configuration validated.')
