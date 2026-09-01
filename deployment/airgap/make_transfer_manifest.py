#!/usr/bin/env python3
import argparse,datetime,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('--output',default='TRANSFER_MANIFEST.json');a=p.parse_args();root=pathlib.Path(a.directory).resolve();out=root/a.output
items=[]
for f in sorted(root.rglob('*')):
    if not f.is_file() or f.resolve()==out.resolve():continue
    h=hashlib.sha256()
    with open(f,'rb') as x:
        for b in iter(lambda:x.read(1024*1024),b''):h.update(b)
    items.append({'path':str(f.relative_to(root)),'bytes':f.stat().st_size,'sha256':h.hexdigest()})
out.write_text(json.dumps({'format':'faos-airgap-transfer-v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':items},indent=2)+'\n')
print(out)
