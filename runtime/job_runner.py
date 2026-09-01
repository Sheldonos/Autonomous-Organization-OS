from __future__ import annotations
import json,os,urllib.request,time,datetime,signal
from .capability_registry import CapabilityRegistry
from .mcp_http_probe import discover
from .mcp_assimilator import assimilate
from .mission import plan

def _post_executor(url,payload,token=None):
    h={'Content-Type':'application/json'}
    if token:h['Authorization']='Bearer '+token
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=h,method='POST')
    with urllib.request.urlopen(req,timeout=120) as r:return json.loads(r.read().decode())

def run_one(db_path,dynamic_dir='dynamic_skills',executor_url=None,executor_token_env=None):
    reg=CapabilityRegistry(db_path); reg.recover_stale(); job=reg.claim_job()
    if not job:return {'status':'IDLE'}
    try:
        result={}
        if job['job_type']=='CAPABILITY_RESCAN':
            connector_id=json.loads(job['required_capabilities_json'])[0]
            c=reg.connector(connector_id)
            if not c:raise RuntimeError('connector missing')
            meta=json.loads(c['metadata_json']);src=meta.get('discovery_source',{})
            if src.get('transport')!='http':
                result={'state':'WAITING_HOST_DISCOVERY','connector_id':connector_id,'reason':'Host-managed transport must supply a new snapshot.'};reg.finish_job(job['job_id'],'WAITING_HOST',result);return result
            snap=discover(src['url'],connector_id,src.get('token_env')); result=assimilate(snap,db_path,dynamic_dir);reg.finish_job(job['job_id'],'COMPLETED',result);return result
        # For goal advancement, prepare a bounded mission plan first.
        mission=plan(job['objective'],4);payload={'job':{k:job[k] for k in ['job_id','goal_id','job_type','objective','trigger_type']},'mission_plan':mission,'effect_contract':{'idempotency_key':job['job_id'],'durable_receipt_required_for_consequential_writes':True,'readback_required_when_supported':True},'policy_note':'Executor must apply FAOS policy/connector gates before side effects and reuse the supplied idempotency_key on retries.'}
        if reg.get_flag('drain_external_writes',False):
            result={'state':'DRAINED_READY_FOR_AGENT','mission_plan':mission,'reason':'Deployment drain is active. Goal work is preserved but no external executor handoff is attempted.'};reg.finish_job(job['job_id'],'DRAINED',result);return result
        url=executor_url or os.getenv('FAOS_AGENT_EXECUTOR_URL')
        if not url:
            result={'state':'READY_FOR_AGENT','mission_plan':mission,'reason':'No FAOS_AGENT_EXECUTOR_URL configured; the job is fully prepared for Bob/watsonx/host execution.'};reg.finish_job(job['job_id'],'READY_FOR_AGENT',result);return result
        token=os.getenv(executor_token_env or 'FAOS_AGENT_EXECUTOR_TOKEN')
        result=_post_executor(url,payload,token);reg.finish_job(job['job_id'],'COMPLETED',result);return result
    except Exception as e:
        result={'error':type(e).__name__,'message':str(e)};reg.finish_job(job['job_id'],'FAILED_RECOVERABLE',result);return result

def daemon(db_path,seconds=10,dynamic_dir='dynamic_skills',executor_url=None):
    seconds=max(1,int(seconds)); stop={'value':False}
    def _stop(signum,frame): stop['value']=True
    signal.signal(signal.SIGTERM,_stop); signal.signal(signal.SIGINT,_stop)
    while not stop['value']:
        out=run_one(db_path,dynamic_dir,executor_url);print(json.dumps(out,sort_keys=True),flush=True)
        if not stop['value']: time.sleep(seconds)
