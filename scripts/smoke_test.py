#!/usr/bin/env python3
import json,tempfile,pathlib,sys,subprocess,os
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from runtime.router import rank
from runtime.mission import plan
from runtime.hydrator import hydrate
from runtime.policy import evaluate
from runtime.control_plane import start
from runtime.state import MissionStore
from runtime.capability_registry import CapabilityRegistry
from runtime.mcp_assimilator import assimilate
from runtime.proactivity import tick
from runtime.context_manager import context_plan
checks=[]
r=rank('Find a high-value RFP, qualify it, create the proposal and pursue the deal',5);checks.append(('router_has_deal_or_bid',any(x['pocket'] in {'dealos','bidos'} for x in r)))
m=plan('Research a market, build the product, then sell it');checks.append(('mission_composes',len(m['pockets'])>=2 and m['pockets'][0]=='enterpriseos'))
checks.append(('policy_requires_approval',evaluate('external_message')['decision']=='REQUIRE_APPROVAL'));checks.append(('policy_allows_analysis',evaluate('analysis')['decision']=='ALLOW'))
with tempfile.TemporaryDirectory() as d:
 h=hydrate('researchos',pathlib.Path(d)/'ws',max_skills=3);checks.append(('hydration_extracts',h['skills_extracted']==3))
 ht=hydrate('dealos',pathlib.Path(d)/'teamws',max_skills=4,team='t01');checks.append(('team_hydration_extracts',ht['skills_extracted']>=1 and ht['skills_extracted']<=4))
 db=pathlib.Path(d)/'state.db';sm=start('Research and evaluate a market',db,2);store=MissionStore(db);checks.append(('durable_state',store.get_mission(sm['mission_id']) is not None))
 cdb=pathlib.Path(d)/'cap.db';reg=CapabilityRegistry(cdb);gid=reg.add_goal('Use CRM to create and pursue qualified sales opportunities',blocked_by=['crm create opportunity']);reg.update_goal(gid,status='BLOCKED')
 out=assimilate(json.load(open(ROOT/'tests/sample_mcp_snapshot.json')),cdb,pathlib.Path(d)/'dynamic');checks.append(('mcp_assimilation',out['dynamic_skills_generated']==5 and gid in out['resume_candidates']))
 jobs=tick(cdb,4);checks.append(('proactivity_queues_bounded_job',0<len(jobs['new_jobs'])<=4))
 planctx=context_plan('securityos','t01',5);checks.append(('bounded_context',0<len(planctx['canonical_skill_slugs'])<=5))
print(json.dumps({'status':'PASS' if all(v for _,v in checks) else 'FAIL','checks':checks},indent=2));raise SystemExit(0 if all(v for _,v in checks) else 1)
