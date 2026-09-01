from __future__ import annotations
import json,pathlib,tempfile,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.mcp_assimilator import assimilate
from runtime.capability_registry import CapabilityRegistry
from runtime.proactivity import tick
from runtime.context_manager import context_plan
from runtime.policy import evaluate
from runtime.readiness import check

def test_accountability_complete():
    d=json.load(open(ROOT/'registry/skill_accountability.json'))
    assert d['canonical_skill_count']==3212
    sl=[x['slug'] for x in d['skills']]
    assert len(sl)==len(set(sl))==3212

def test_wrappers_complete():
    d=json.load(open(ROOT/'registry/wrappers.json'))
    assert d['count']==540
    assert sum(1 for x in d['wrappers'] if x['type']=='pocket_orchestrator')==48

def test_mcp_assimilation_and_goal_resume():
    snap=json.load(open(ROOT/'tests/sample_mcp_snapshot.json'))
    with tempfile.TemporaryDirectory() as td:
        db=pathlib.Path(td)/'c.db';dyn=pathlib.Path(td)/'dyn';reg=CapabilityRegistry(db)
        gid=reg.add_goal('Pursue a CRM sales opportunity',blocked_by=['CRM opportunity creation']); reg.update_goal(gid,status='BLOCKED')
        out=assimilate(snap,db,dyn)
        assert out['dynamic_skills_generated']==5
        caps=reg.capabilities('sample-crm')
        by={x['name']:x for x in caps}
        assert by['search_accounts']['side_effect_class']=='read_only'
        assert by['create_opportunity']['side_effect_class'] in {'write','consequential_write'}
        assert by['delete_account']['risk_class']=='high'
        assert gid in out['resume_candidates']
        jobs=tick(db)['new_jobs']; assert jobs

def test_context_plan_bounded():
    p=context_plan('dealos','t01',8); assert 1<=len(p['canonical_skill_slugs'])<=8

def test_policy_stays_gated():
    assert evaluate('external_message')['decision']=='REQUIRE_APPROVAL'
    assert evaluate('analysis')['decision']=='ALLOW'

def test_readiness_fails_closed():
    with tempfile.TemporaryDirectory() as td:
        cfg=pathlib.Path(td)/'p.json'; cfg.write_text(json.dumps({'enabled_pockets':['dealos'],'connector_instances':{},'connector_registry_db':str(pathlib.Path(td)/'c.db')}))
        CapabilityRegistry(pathlib.Path(td)/'c.db')
        r=check(cfg); assert r['status']=='FAIL' and r['warnings']

def test_worker_prepares_agent_job_without_recursive_loop():
    from runtime.job_runner import run_one
    with tempfile.TemporaryDirectory() as td:
        db=pathlib.Path(td)/'c.db'; reg=CapabilityRegistry(db)
        gid=reg.add_goal('Research a market and decide the next product experiment')
        out=tick(db,1); assert out['count']==1
        result=run_one(db,pathlib.Path(td)/'dyn')
        assert result['state']=='READY_FOR_AGENT'
        jobs=reg.jobs(None,10); assert jobs[0]['status']=='READY_FOR_AGENT'

def test_event_queue_is_durable_and_bounded():
    from runtime.eventing import drain
    with tempfile.TemporaryDirectory() as td:
        db=pathlib.Path(td)/'c.db'; reg=CapabilityRegistry(db)
        gid=reg.add_goal('Prepare a bounded product research step')
        ev=reg.queued_events('QUEUED',10); assert ev and ev[0]['event_type']=='GOAL_ADDED'
        r=drain(db,10); assert r['processed']>=1
        jobs=reg.jobs('QUEUED',10); assert jobs and jobs[0]['goal_id']==gid

def test_deployment_drain_preserves_job_without_executor_handoff():
    from runtime.eventing import drain
    from runtime.job_runner import run_one
    with tempfile.TemporaryDirectory() as td:
        db=pathlib.Path(td)/'c.db'; reg=CapabilityRegistry(db)
        reg.add_goal('Research and prepare an outreach plan')
        drain(db,10); reg.set_flag('drain_external_writes',True)
        result=run_one(db,pathlib.Path(td)/'dyn')
        assert result['state']=='DRAINED_READY_FOR_AGENT'
        assert reg.jobs(None,10)[0]['status']=='DRAINED'

def test_airgap_readiness_fails_open_network():
    with tempfile.TemporaryDirectory() as td:
        db=pathlib.Path(td)/'c.db';CapabilityRegistry(db)
        cfg=pathlib.Path(td)/'p.json';cfg.write_text(json.dumps({'deployment_tier':'air_gapped','enabled_pockets':[],'connector_instances':{},'connector_registry_db':str(db),'eventing':{'mode':'event_driven','backend':'sqlite_durable_queue'},'autonomy':{'continuous_model_loop':False},'upgrade':{'drain_external_writes':True,'pre_upgrade_backup':True},'dr':{'restore_test':True},'data_sovereignty':{'mode':'air_gapped','external_network_allowed':True}}))
        r=check(cfg); assert r['status']=='FAIL' and any('air_gapped' in x for x in r['errors'])
