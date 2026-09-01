#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.eventing import process_one,drain,daemon
p=argparse.ArgumentParser();p.add_argument('--db',default='state/capabilities.db');p.add_argument('--max-events',type=int,default=100);p.add_argument('--daemon',action='store_true');p.add_argument('--seconds',type=float,default=1.0);a=p.parse_args()
if a.daemon: daemon(a.db,a.seconds)
else: print(json.dumps(drain(a.db,a.max_events),indent=2))
