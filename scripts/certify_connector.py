#!/usr/bin/env python3
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.capability_registry import CapabilityRegistry
p=argparse.ArgumentParser();p.add_argument('connector_id');p.add_argument('--db',default='state/capabilities.db');p.add_argument('--write',action='store_true');p.add_argument('--readback',action='store_true');a=p.parse_args();r=CapabilityRegistry(a.db);r.certify(a.connector_id,a.write,a.readback);print(json.dumps(r.connector(a.connector_id),indent=2))
