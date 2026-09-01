#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,pathlib,shutil,sqlite3

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def verify(path,expected):
    if sha256(path)!=expected: raise RuntimeError(f'hash mismatch: {path}')
    c=sqlite3.connect(str(path)); v=c.execute('PRAGMA integrity_check').fetchone()[0];c.close()
    if v!='ok': raise RuntimeError(f'integrity check failed: {path}: {v}')

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--verify-only',action='store_true');p.add_argument('--target-root');p.add_argument('--force',action='store_true');a=p.parse_args()
    mp=pathlib.Path(a.manifest); d=json.load(open(mp)); results=[]
    for e in d['entries']:
        if e.get('status')!='PASS':continue
        src=pathlib.Path(e['backup']);
        if not src.is_absolute():src=mp.parent/src
        verify(src,e['sha256']); item={'backup':str(src),'verified':True}
        if not a.verify_only:
            dst=(pathlib.Path(a.target_root)/pathlib.Path(e['source']).name) if a.target_root else pathlib.Path(e['source'])
            if dst.exists() and not a.force:raise RuntimeError(f'refusing to overwrite {dst}; use --force')
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);verify(dst,e['sha256']);item['restored_to']=str(dst)
        results.append(item)
    print(json.dumps({'status':'PASS','verify_only':a.verify_only,'results':results},indent=2))
if __name__=='__main__':main()
