#!/usr/bin/env python3
from __future__ import annotations
import json,hashlib,pathlib,zipfile,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
PREFIX='IBM_Enterprise_Autonomous_Operations_OS_v2.0.0-rc1/'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 errors=[]; warnings=[]
 skills=json.load(open(ROOT/'substrate/registry/skills.json')); roles=json.load(open(ROOT/'substrate/registry/roles.json')); pockets=json.load(open(ROOT/'registry/pockets.json'))
 if len(skills)!=3212: errors.append(f'canonical skill count {len(skills)} != 3212')
 if len(roles)!=1244: errors.append(f'role count {len(roles)} != 1244')
 # source archive and every canonical skill payload
 arch=ROOT/'substrate/source_archives/IBM_Enterprise_Autonomous_Operations_OS_v2.0.0-rc1.zip'
 if sha(arch)!='bf1cbdad213c6ec2f9e6d87c3294ef2a1da95694bea5ce4939f6ad5ec84c93fc': errors.append('substrate archive sha mismatch')
 with zipfile.ZipFile(arch) as z:
  names=set(z.namelist())
  for s in skills:
   n=PREFIX+s['path']
   if n not in names: errors.append(f"missing canonical skill {s['slug']}"); continue
   h=hashlib.sha256(z.read(n)).hexdigest()
   if h!=s['sha256']: errors.append(f"canonical skill sha mismatch {s['slug']}")
 # accountability exactly once
 acc=json.load(open(ROOT/'registry/skill_accountability.json'))['skills']; by=[x['slug'] for x in acc]
 if len(acc)!=3212 or len(set(by))!=3212 or set(by)!={s['slug'] for s in skills}: errors.append('skill accountability not exactly 3212 unique canonical skills')
 # sectors/pockets/routes
 seen=set(); connector_types=set()
 for pth in ROOT.glob('segments/*/*/manifest.json'):
  m=json.load(open(pth));pid=m['id'];seen.add(pid);routes=json.load(open(pth.parent/'skill_routes.json')); connector_types.update(json.load(open(pth.parent/'connectors.json')).get('required_or_optional_classes',[]))
  if routes.get('active_route_count',0)<40: errors.append(f'{pid}: less than 40 active routes')
  if routes.get('primary_accountable_count',0)<1: errors.append(f'{pid}: no primary accountable canonical skill')
  unknown=[x['slug'] for x in routes['skills'] if x['slug'] not in set(by)]
  if unknown: errors.append(f'{pid}: unknown active routes')
 if seen!=set(pockets):errors.append('pocket registry/disk mismatch')
 if len(connector_types)!=87:errors.append(f'expected 87 connector requirement types, got {len(connector_types)}')
 # wrappers/frontmatter/routes
 wr=json.load(open(ROOT/'registry/wrappers.json'))
 if wr.get('count')!=540:errors.append(f"wrapper count {wr.get('count')} != 540")
 fm=re.compile(r'^---\nname:\s*([^\n]+)\ndescription:\s*".*"\n---\n',re.S)
 for x in wr.get('wrappers',[]):
  f=ROOT/x['path'];
  if not f.exists():errors.append(f"missing wrapper {x['slug']}");continue
  txt=f.read_text()
  if not fm.match(txt):errors.append(f"bad wrapper frontmatter {x['slug']}")
  route=f.parent/'ROUTES.json'
  if not route.exists() or not json.load(open(route)).get('canonical_children'):errors.append(f"empty wrapper routes {x['slug']}")
 # DealOS exact archive
 deal=ROOT/'segments/sell/dealos/source_archive/DealOS_v1.0.1.zip'
 if sha(deal)!='2df0829e8dbb1b4a1e8704acd0b3973534024604948f4566c91eb2fab31759bf':errors.append('DealOS archive sha mismatch')
 # required production artifacts
 req=['Dockerfile','docker-compose.yml','docs/MCP_ADAPTIVE_AUTONOMY.md','docs/PROACTIVITY_MODEL.md','docs/PRODUCTION_ARCHITECTURE.md','docs/RESILIENCE_ARCHITECTURE.md','docs/EVENTING_AND_BACKPRESSURE.md','docs/ZERO_DOWNTIME_UPGRADES_AND_BACKOUT.md','docs/DISASTER_RECOVERY_AND_SITE_RESILIENCE.md','docs/HYBRID_ON_PREM_AND_AIR_GAPPED.md','docs/STORAGE_VERSIONING_AND_EGRESS.md','market/MARKET_READINESS.md','deployment/ACCEPTANCE_CHECKLIST.md','deployment/docker-compose.airgap.yml','policies/autonomy_budget.yaml','policies/adaptive_capabilities.yaml','policies/resilience.yaml','policies/data_residency.yaml','storage/STORAGE_CLASSES.yaml','scripts/control_api.py','scripts/assimilate_mcp.py','scripts/autonomy_tick.py','scripts/run_worker.py','scripts/process_events.py','scripts/preflight_upgrade.py','scripts/backup_state.py','scripts/restore_state.py','scripts/resilience_smoke.py']
 for r in req:
  if not (ROOT/r).exists():errors.append(f'missing required release artifact {r}')
 result={'status':'PASS' if not errors else 'FAIL','canonical_skills':len(skills),'canonical_skill_hashes_verified':3212 if not any('canonical skill' in e for e in errors) else None,'roles':len(roles),'segments':7,'pockets':len(pockets),'wrappers':wr.get('count'),'connector_requirement_types':len(connector_types),'errors':errors,'warnings':warnings}
 print(json.dumps(result,indent=2));return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
