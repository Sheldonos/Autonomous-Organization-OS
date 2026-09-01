from __future__ import annotations
import json, time, signal
from .capability_registry import CapabilityRegistry
from .proactivity import queue_goal, tick

GOAL_EVENTS={'GOAL_ADDED','GOAL_WAKE','SCHEDULE_DUE','GOAL_POTENTIALLY_UNBLOCKED'}

def process_one(db_path,max_attempts=5):
    reg=CapabilityRegistry(db_path); ev=reg.claim_event()
    if not ev:return {'status':'IDLE'}
    try:
        typ=ev['event_type']; payload=json.loads(ev['payload_json'] or '{}'); created=[]
        if typ in GOAL_EVENTS and ev.get('subject_id'):
            jid=queue_goal(reg,ev['subject_id'],typ.lower())
            if jid:created.append(jid)
        elif typ in {'CAPABILITY_CHANGED','GOALS_POTENTIALLY_UNBLOCKED'}:
            for gid in payload.get('goal_ids',[]):
                jid=queue_goal(reg,gid,'capability_change')
                if jid:created.append(jid)
        elif typ in {'RECONCILE','SYSTEM_WAKE'}:
            created.extend(tick(db_path,int(payload.get('max_new_jobs',8)))['new_jobs'])
        elif typ=='JOB_STATUS_CHANGED':
            # Completion is durable evidence. Follow-on work is triggered by an explicit goal wake or reconciliation event,
            # preventing an accidental recursive job chain.
            pass
        elif typ=='CONNECTOR_CERTIFIED':
            reg.emit('SYSTEM_WAKE',ev.get('subject_id'),{'reason':'connector_certified'},dedupe_window_seconds=60)
        else:
            reg.event('EVENT_NO_HANDLER',ev.get('subject_id'),{'event_type':typ})
        result={'status':'PASS','event_id':ev['event_id'],'event_type':typ,'jobs_created':created}
        reg.finish_event(ev['event_id'],result); return result
    except Exception as e:
        reg.fail_event(ev['event_id'],f'{type(e).__name__}: {e}',max_attempts=max_attempts); return {'status':'RETRY_OR_DLQ','event_id':ev['event_id'],'error':str(e)}

def drain(db_path,max_events=100):
    out=[]
    for _ in range(max(1,int(max_events))):
        x=process_one(db_path)
        if x.get('status')=='IDLE':break
        out.append(x)
    return {'status':'PASS','processed':len(out),'results':out}

def daemon(db_path,seconds=1):
    # Lightweight queue consumer only. It does not invoke models unless an event creates a bounded job.
    stop={'value':False}
    def _stop(signum,frame): stop['value']=True
    signal.signal(signal.SIGTERM,_stop); signal.signal(signal.SIGINT,_stop)
    while not stop['value']:
        out=process_one(db_path)
        if out.get('status')=='IDLE': time.sleep(max(0.25,float(seconds)))
        else: print(json.dumps(out,sort_keys=True),flush=True)
