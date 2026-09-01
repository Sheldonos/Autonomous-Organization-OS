#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.capability_registry import CapabilityRegistry

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='config/production.json');p.add_argument('--set-drain',action='store_true');a=p.parse_args()
    cfg=json.load(open(a.config)); db=cfg.get('connector_registry_db') or cfg.get('state_db'); errors=[];warnings=[]
    if not db:errors.append('no state database configured')
    elif not pathlib.Path(db).exists():warnings.append('state database does not yet exist')
    else:
        reg=CapabilityRegistry(db); reg.recover_stale()
        running=reg.jobs('RUNNING',1000); running_events=reg.queued_events('RUNNING',1000)
        if running:errors.append(f'{len(running)} jobs are RUNNING; drain/finish before cutover')
        if running_events:errors.append(f'{len(running_events)} events are RUNNING; drain/finish before cutover')
        if a.set_drain:reg.set_flag('drain_external_writes',True)
    out={'status':'PASS' if not errors else 'FAIL','drain_requested':a.set_drain,'errors':errors,'warnings':warnings,'next':'Create a verified backup, deploy Green, run readiness/smoke tests, then shift traffic.'}
    print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()
