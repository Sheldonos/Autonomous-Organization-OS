#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.mcp_assimilator import assimilate
from runtime.mcp_http_probe import discover
p=argparse.ArgumentParser(description='Discover/import an MCP capability surface and assimilate it into the OS Factory.')
g=p.add_mutually_exclusive_group(required=True);g.add_argument('--snapshot');g.add_argument('--url')
p.add_argument('--connector-id',required=True);p.add_argument('--token-env');p.add_argument('--db',default='state/capabilities.db');p.add_argument('--dynamic-dir',default='dynamic_skills');p.add_argument('--save-snapshot')
a=p.parse_args();
s=json.load(open(a.snapshot)) if a.snapshot else discover(a.url,a.connector_id,a.token_env)
s['connector_id']=a.connector_id
if a.save_snapshot: pathlib.Path(a.save_snapshot).write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(assimilate(s,a.db,a.dynamic_dir),indent=2))
