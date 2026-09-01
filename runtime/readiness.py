from __future__ import annotations
import json, pathlib
from .capability_registry import CapabilityRegistry

ROOT=pathlib.Path(__file__).resolve().parents[1]

def required_connectors(pid):
    for p in ROOT.glob(f'segments/*/{pid}/connectors.json'):
        return json.load(open(p)).get('required_or_optional_classes',[])
    raise KeyError(pid)

def check(config_path,capability_db=None):
    cfg=json.load(open(config_path)); db=capability_db or cfg.get('connector_registry_db')
    errors=[]; warnings=[]; connectors={}
    ev=cfg.get('eventing',{}); auto=cfg.get('autonomy',{}); up=cfg.get('upgrade',{}); dr=cfg.get('dr',{}); ds=cfg.get('data_sovereignty',{})
    if ev and ev.get('mode')!='event_driven': errors.append('eventing.mode must be event_driven for production')
    if auto.get('continuous_model_loop') is True: errors.append('continuous_model_loop must be false')
    if up and not up.get('drain_external_writes',False): errors.append('upgrade drain_external_writes must be enabled')
    if up and not up.get('pre_upgrade_backup',False): errors.append('pre_upgrade_backup must be enabled')
    if dr and not dr.get('restore_test',False): errors.append('DR restore_test must be enabled')
    if ds.get('mode')=='air_gapped' and ds.get('external_network_allowed') is not False: errors.append('air_gapped mode requires external_network_allowed=false')
    if cfg.get('deployment_tier') in {'ha','multi_site','active_active'} and ev.get('backend')=='sqlite_durable_queue': errors.append('HA/multi-site tier requires an external durable event bus; sqlite queue is standalone only')
    if db and pathlib.Path(db).exists():
        reg=CapabilityRegistry(db)
        for row in reg.db.execute('SELECT * FROM connector_instances').fetchall(): connectors[row['id']]=dict(row)
    inst=cfg.get('connector_instances',{})
    for pid in cfg.get('enabled_pockets',[]):
        for cls in required_connectors(pid):
            cid=inst.get(cls)
            if not cid: warnings.append(f'{pid}: connector class {cls} is not bound to an instance')
            elif cid not in connectors: errors.append(f'{pid}: connector instance {cid} for {cls} is not in adaptive registry')
            elif connectors[cid]['trust_state'] not in {'READ_ENABLED','WRITE_CERTIFIED'}: errors.append(f'{pid}: connector {cid} is not enabled/certified ({connectors[cid]["trust_state"]})')
    return {'status':'PASS' if not errors and not warnings else 'FAIL','errors':errors,'warnings':warnings,'enabled_pockets':cfg.get('enabled_pockets',[]),'deployment_certified':not errors and not warnings}
