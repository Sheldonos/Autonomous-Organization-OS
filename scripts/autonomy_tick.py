#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.proactivity import tick,daemon
p=argparse.ArgumentParser();p.add_argument('--db',default='state/capabilities.db');p.add_argument('--max-new-jobs',type=int,default=8);p.add_argument('--daemon',action='store_true');p.add_argument('--seconds',type=int,default=300);a=p.parse_args()
if a.daemon: daemon(a.db,a.seconds,a.max_new_jobs)
else: print(json.dumps(tick(a.db,a.max_new_jobs),indent=2))
