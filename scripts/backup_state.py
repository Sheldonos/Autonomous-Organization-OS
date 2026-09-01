#!/usr/bin/env python3
from __future__ import annotations
import argparse,datetime,hashlib,json,pathlib,sqlite3,shutil,sys

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def backup_sqlite(src,dst):
    srcp=pathlib.Path(src)
    if not srcp.exists(): return {'source':str(srcp),'status':'MISSING'}
    dst.parent.mkdir(parents=True,exist_ok=True)
    a=sqlite3.connect(str(srcp)); b=sqlite3.connect(str(dst))
    try:a.backup(b)
    finally:b.close();a.close()
    c=sqlite3.connect(str(dst));check=c.execute('PRAGMA integrity_check').fetchone()[0];c.close()
    if check!='ok': raise RuntimeError(f'integrity_check failed for {src}: {check}')
    return {'source':str(srcp),'backup':str(dst),'status':'PASS','bytes':dst.stat().st_size,'sha256':sha256(dst),'integrity_check':check}

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='config/production.json');p.add_argument('--output',required=True);a=p.parse_args()
    cfg=json.load(open(a.config)); out=pathlib.Path(a.output); out.mkdir(parents=True,exist_ok=True)
    paths=[]
    for key in ('connector_registry_db','state_db'):
        v=cfg.get(key)
        if v and v not in paths:paths.append(v)
    entries=[]
    for i,src in enumerate(paths): entries.append(backup_sqlite(src,out/f'{i:02d}_{pathlib.Path(src).name}'))
    manifest={'format':'faos-backup-v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deployment_id':cfg.get('deployment_id'),'entries':entries}
    (out/'backup-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'PASS','manifest':str(out/'backup-manifest.json'),'entries':entries},indent=2))
if __name__=='__main__':main()
