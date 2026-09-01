#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.capability_registry import CapabilityRegistry
from runtime.eventing import drain
from runtime.job_runner import run_one
from runtime.readiness import check

def main():
    out={}
    with tempfile.TemporaryDirectory() as td:
        td=pathlib.Path(td); db=td/'cap.db'; reg=CapabilityRegistry(db)
        gid=reg.add_goal('Research a supplier opportunity and prepare the next bounded action')
        assert reg.queued_events('QUEUED',10), 'goal did not emit durable event'
        r=drain(db,20); assert r['processed']>=1
        assert reg.jobs('QUEUED',10), 'event did not create bounded job'
        reg.set_flag('drain_external_writes',True)
        jr=run_one(db,td/'dyn'); assert jr['state']=='DRAINED_READY_FOR_AGENT'
        cfg=td/'production.json';cfg.write_text(json.dumps({'deployment_id':'test','deployment_tier':'standalone','enabled_pockets':[],'connector_instances':{},'connector_registry_db':str(db),'eventing':{'mode':'event_driven','backend':'sqlite_durable_queue'},'autonomy':{'continuous_model_loop':False},'upgrade':{'drain_external_writes':True,'pre_upgrade_backup':True},'dr':{'restore_test':True},'data_sovereignty':{'mode':'air_gapped','external_network_allowed':False}}))
        rd=check(cfg); assert rd['status']=='PASS',rd
        bdir=td/'backup'; subprocess.check_call([sys.executable,str(ROOT/'scripts/backup_state.py'),'--config',str(cfg),'--output',str(bdir)],stdout=subprocess.DEVNULL)
        subprocess.check_call([sys.executable,str(ROOT/'scripts/restore_state.py'),str(bdir/'backup-manifest.json'),'--verify-only'],stdout=subprocess.DEVNULL)
        out={'status':'PASS','event_driven_goal':gid,'event_processing':r['processed'],'drain_state':jr['state'],'airgap_readiness':rd['status'],'backup_restore_verify':'PASS'}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
