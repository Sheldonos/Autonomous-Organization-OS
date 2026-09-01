#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib
from runtime.router import rank,load_pockets
from runtime.hydrator import hydrate,locate_pocket
from runtime.mission import plan
from runtime.control_plane import start
from runtime.state import MissionStore
from runtime.policy import evaluate
from runtime.capability_registry import CapabilityRegistry
from runtime.mcp_assimilator import assimilate
from runtime.mcp_http_probe import discover
from runtime.proactivity import tick
from runtime.eventing import drain as drain_events
from runtime.readiness import check as readiness_check

def main():
    p=argparse.ArgumentParser(description='Federated Autonomous Organization OS control plane')
    s=p.add_subparsers(dest='cmd',required=True)
    s.add_parser('list')
    r=s.add_parser('route'); r.add_argument('intent'); r.add_argument('--limit',type=int,default=5)
    i=s.add_parser('inspect'); i.add_argument('pocket')
    h=s.add_parser('hydrate'); h.add_argument('pocket'); h.add_argument('--dest',default=None); h.add_argument('--max-skills',type=int,default=None); h.add_argument('--team')
    m=s.add_parser('mission'); m.add_argument('intent'); m.add_argument('--output',default=None); m.add_argument('--max-pockets',type=int,default=4)
    st=s.add_parser('start'); st.add_argument('intent'); st.add_argument('--db',default='state/federation.db'); st.add_argument('--max-pockets',type=int,default=4)
    ls=s.add_parser('missions'); ls.add_argument('--db',default='state/federation.db'); ls.add_argument('--limit',type=int,default=20)
    pc=s.add_parser('policy'); pc.add_argument('action_type'); pc.add_argument('--preauthorized',action='store_true'); pc.add_argument('--adapter-verified',action='store_true'); pc.add_argument('--readback-supported',action='store_true')
    g=s.add_parser('goal'); g.add_argument('objective'); g.add_argument('--db',default='state/capabilities.db'); g.add_argument('--priority',type=int,default=50); g.add_argument('--blocked-by',action='append',default=[])
    t=s.add_parser('tick'); t.add_argument('--db',default='state/capabilities.db'); t.add_argument('--max-new-jobs',type=int,default=8)
    am=s.add_parser('assimilate-mcp'); gg=am.add_mutually_exclusive_group(required=True); gg.add_argument('--snapshot');gg.add_argument('--url');am.add_argument('--connector-id',required=True);am.add_argument('--token-env');am.add_argument('--db',default='state/capabilities.db');am.add_argument('--dynamic-dir',default='dynamic_skills')
    cr=s.add_parser('certify-connector');cr.add_argument('connector_id');cr.add_argument('--db',default='state/capabilities.db');cr.add_argument('--write',action='store_true');cr.add_argument('--readback',action='store_true')
    rd=s.add_parser('readiness');rd.add_argument('config');rd.add_argument('--db')
    ac=s.add_parser('accountability');ac.add_argument('skill_slug')
    ev=s.add_parser('emit-event');ev.add_argument('event_type');ev.add_argument('--subject-id');ev.add_argument('--payload-json',default='{}');ev.add_argument('--db',default='state/capabilities.db')
    de=s.add_parser('drain-events');de.add_argument('--db',default='state/capabilities.db');de.add_argument('--max-events',type=int,default=100)
    dm=s.add_parser('drain-mode');dm.add_argument('state',choices=['on','off']);dm.add_argument('--db',default='state/capabilities.db')
    a=p.parse_args()
    if a.cmd=='list':
        pockets=load_pockets(); by={}
        for pid,x in pockets.items(): by.setdefault(x['segment'],[]).append((pid,x['title']))
        for seg in sorted(by):
            print(f'[{seg.upper()}]'); [print(f'  {pid:20s} {t}') for pid,t in sorted(by[seg])]
    elif a.cmd=='route': print(json.dumps(rank(a.intent,a.limit),indent=2))
    elif a.cmd=='inspect':
        d=locate_pocket(a.pocket); print((d/'README.md').read_text()); print(json.dumps(json.load(open(d/'manifest.json')),indent=2))
    elif a.cmd=='hydrate': print(json.dumps(hydrate(a.pocket,a.dest or f'workspace_{a.pocket}',a.max_skills,a.team),indent=2))
    elif a.cmd=='mission':
        result=plan(a.intent,a.max_pockets); text=json.dumps(result,indent=2)
        if a.output: pathlib.Path(a.output).write_text(text+'\n'); print(a.output)
        else: print(text)
    elif a.cmd=='start': print(json.dumps(start(a.intent,a.db,a.max_pockets),indent=2))
    elif a.cmd=='missions': print(json.dumps(MissionStore(a.db).list_missions(a.limit),indent=2))
    elif a.cmd=='policy': print(json.dumps(evaluate(a.action_type,a.preauthorized,a.adapter_verified,a.readback_supported),indent=2))
    elif a.cmd=='goal':
        reg=CapabilityRegistry(a.db);gid=reg.add_goal(a.objective,a.priority,a.blocked_by);print(json.dumps({'goal_id':gid},indent=2))
    elif a.cmd=='tick': print(json.dumps(tick(a.db,a.max_new_jobs),indent=2))
    elif a.cmd=='assimilate-mcp':
        snap=json.load(open(a.snapshot)) if a.snapshot else discover(a.url,a.connector_id,a.token_env);snap['connector_id']=a.connector_id;print(json.dumps(assimilate(snap,a.db,a.dynamic_dir),indent=2))
    elif a.cmd=='certify-connector':
        reg=CapabilityRegistry(a.db);reg.certify(a.connector_id,a.write,a.readback);print(json.dumps(reg.connector(a.connector_id),indent=2))
    elif a.cmd=='readiness': print(json.dumps(readiness_check(a.config,a.db),indent=2))
    elif a.cmd=='accountability':
        data=json.load(open(pathlib.Path(__file__).resolve().parent/'registry/skill_accountability.json'))['skills']; row=next((x for x in data if x['slug']==a.skill_slug),None); print(json.dumps(row or {'error':'unknown skill'},indent=2))
    elif a.cmd=='emit-event':
        reg=CapabilityRegistry(a.db);eid=reg.emit(a.event_type,a.subject_id,json.loads(a.payload_json));print(json.dumps({'event_id':eid},indent=2))
    elif a.cmd=='drain-events': print(json.dumps(drain_events(a.db,a.max_events),indent=2))
    elif a.cmd=='drain-mode':
        reg=CapabilityRegistry(a.db);v=a.state=='on';reg.set_flag('drain_external_writes',v);print(json.dumps({'drain_external_writes':v},indent=2))
if __name__=='__main__': main()
