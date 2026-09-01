#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.capability_registry import CapabilityRegistry
p=argparse.ArgumentParser();p.add_argument('objective');p.add_argument('--db',default='state/capabilities.db');p.add_argument('--priority',type=int,default=50);p.add_argument('--blocked-by',action='append',default=[]);a=p.parse_args();r=CapabilityRegistry(a.db);gid=r.add_goal(a.objective,a.priority,a.blocked_by);print(json.dumps({'goal_id':gid,'objective':a.objective},indent=2))
