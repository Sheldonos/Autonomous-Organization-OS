#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.job_runner import run_one,daemon
p=argparse.ArgumentParser();p.add_argument('--db',default='state/capabilities.db');p.add_argument('--dynamic-dir',default='dynamic_skills');p.add_argument('--executor-url');p.add_argument('--daemon',action='store_true');p.add_argument('--seconds',type=int,default=10);a=p.parse_args()
if a.daemon:daemon(a.db,a.seconds,a.dynamic_dir,a.executor_url)
else:print(json.dumps(run_one(a.db,a.dynamic_dir,a.executor_url),indent=2))
