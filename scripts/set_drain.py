#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.capability_registry import CapabilityRegistry
p=argparse.ArgumentParser();p.add_argument('state',choices=['on','off']);p.add_argument('--db',default='state/capabilities.db');a=p.parse_args()
r=CapabilityRegistry(a.db);value=a.state=='on';r.set_flag('drain_external_writes',value);print(json.dumps({'status':'PASS','drain_external_writes':value},indent=2))
