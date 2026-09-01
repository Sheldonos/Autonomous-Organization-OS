#!/usr/bin/env python3
from __future__ import annotations
import json,hashlib,pathlib,zipfile,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def main():
 errors=[]; prov=json.load(open(ROOT/'registry/source_provenance.json'))
 arch=ROOT/'substrate/source_archives'/prov['substrate']['name']
 if not arch.exists(): errors.append('missing substrate archive')
 elif sha(arch)!=prov['substrate']['sha256']: errors.append('substrate hash mismatch')
 skills=json.load(open(ROOT/'substrate/registry/skills.json'))
 roles=json.load(open(ROOT/'substrate/registry/roles.json'))
 if len(skills)!=3212: errors.append(f'expected 3212 skills, got {len(skills)}')
 if len(roles)!=1244: errors.append(f'expected 1244 roles, got {len(roles)}')
 known={s['slug'] for s in skills}
 pockets=json.load(open(ROOT/'registry/pockets.json'))
 seen=set()
 for seg in (ROOT/'segments').iterdir():
  if not seg.is_dir(): continue
  for d in seg.iterdir():
   if not d.is_dir() or not (d/'manifest.json').exists(): continue
   m=json.load(open(d/'manifest.json')); pid=m['id']; seen.add(pid)
   routes=json.load(open(d/'skill_routes.json'))['skills']
   bad=[x['slug'] for x in routes if x['slug'] not in known]
   if bad: errors.append(f'{pid}: {len(bad)} unknown routed skills')
   if len(routes)==0: errors.append(f'{pid}: empty skill route')
 if seen!=set(pockets): errors.append(f'pocket registry mismatch missing={sorted(set(pockets)-seen)} extra={sorted(seen-set(pockets))}')
 deal=ROOT/'segments/sell/dealos/implementation/DealOS_v1.0.1/MANIFEST.json'
 if not deal.exists(): errors.append('DealOS implementation missing')
 else:
  dm=json.load(open(deal))
  if dm.get('version')!='1.0.1': errors.append('wrong DealOS version')
 result={'status':'PASS' if not errors else 'FAIL','skills':len(skills),'roles':len(roles),'pockets':len(pockets),'segments':7,'errors':errors}
 print(json.dumps(result,indent=2))
 return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
