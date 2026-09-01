#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,pathlib,sys
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from runtime.router import load_pockets,rank
from runtime.capability_registry import CapabilityRegistry
from runtime.mcp_assimilator import assimilate
from runtime.proactivity import tick
from runtime.eventing import drain
from runtime.readiness import check as readiness_check

class API(BaseHTTPRequestHandler):
    server_version='FAOS/1.2.0'
    def _json(self,code,obj):
        data=json.dumps(obj,indent=2).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def _auth(self):
        key=os.getenv('FAOS_API_KEY');
        return not key or self.headers.get('Authorization')==f'Bearer {key}' or self.headers.get('X-FAOS-Key')==key
    def _body(self):
        n=int(self.headers.get('Content-Length','0') or 0);return json.loads(self.rfile.read(n) or b'{}')
    def log_message(self,fmt,*args):
        if os.getenv('FAOS_HTTP_LOG','1')!='0': super().log_message(fmt,*args)
    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path=='/health': return self._json(200,{'status':'PASS','service':'faos-control-plane','version':'1.2.0'})
        if path=='/ready':
            cfg=os.getenv('FAOS_PRODUCTION_CONFIG')
            if cfg and pathlib.Path(cfg).exists():
                r=readiness_check(cfg,os.getenv('FAOS_CAPABILITY_DB')); return self._json(200 if r['status']=='PASS' else 503,r)
            return self._json(200,{'status':'PASS','mode':'software_only','deployment_certified':False,'note':'Set FAOS_PRODUCTION_CONFIG for environment certification.'})
        if not self._auth(): return self._json(401,{'error':'unauthorized'})
        if path=='/pockets': return self._json(200,load_pockets())
        if path.startswith('/route/'):
            q=path[len('/route/'):].replace('%20',' ');return self._json(200,rank(q,8))
        reg=CapabilityRegistry(os.getenv('FAOS_CAPABILITY_DB','state/capabilities.db'))
        if path=='/capabilities': return self._json(200,reg.capabilities())
        if path=='/goals': return self._json(200,reg.goals(None))
        if path=='/jobs': return self._json(200,reg.jobs(None,100))
        if path=='/events': return self._json(200,reg.queued_events(None,100))
        if path=='/resilience': return self._json(200,{'drain_external_writes':reg.get_flag('drain_external_writes',False),'queued_events':len(reg.queued_events('QUEUED',1000)),'queued_jobs':len(reg.jobs('QUEUED',1000)),'dead_letters':len(reg.queued_events('DEAD_LETTER',1000))})
        return self._json(404,{'error':'not found'})
    def do_POST(self):
        if not self._auth(): return self._json(401,{'error':'unauthorized'})
        path=self.path.split('?',1)[0]; body=self._body(); db=os.getenv('FAOS_CAPABILITY_DB','state/capabilities.db')
        if path=='/mcp/assimilate': return self._json(200,assimilate(body,db,os.getenv('FAOS_DYNAMIC_SKILLS','dynamic_skills')))
        if path=='/goals':
            reg=CapabilityRegistry(db); gid=reg.add_goal(body['objective'],body.get('priority',50),body.get('blocked_by',[]),body.get('metadata',{})); return self._json(201,{'goal_id':gid})
        if path=='/autonomy/tick': return self._json(200,tick(db,int(body.get('max_new_jobs',8))))
        if path=='/events':
            reg=CapabilityRegistry(db); eid=reg.emit(body['event_type'],body.get('subject_id'),body.get('payload',{}),body.get('dedupe_key'),body.get('available_at')); return self._json(202,{'event_id':eid,'status':'QUEUED'})
        if path=='/events/drain': return self._json(200,drain(db,int(body.get('max_events',100))))
        if path=='/drain':
            reg=CapabilityRegistry(db); state=bool(body.get('enabled',True)); reg.set_flag('drain_external_writes',state); return self._json(200,{'status':'PASS','drain_external_writes':state})
        return self._json(404,{'error':'not found'})

def main():
    p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8080);a=p.parse_args();
    ThreadingHTTPServer((a.host,a.port),API).serve_forever()
if __name__=='__main__': main()
