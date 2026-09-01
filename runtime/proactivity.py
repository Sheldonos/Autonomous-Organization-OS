from __future__ import annotations
import json, datetime, hashlib, signal, time
from .capability_registry import CapabilityRegistry, stable_hash
from .router import rank

DEFAULT_MAX=8

def utcnow(): return datetime.datetime.now(datetime.timezone.utc)
def queue_goal(reg,goal_id,trigger_type='event'):
    row=reg.db.execute('SELECT * FROM goals WHERE goal_id=?',(goal_id,)).fetchone()
    if not row:return None
    g=dict(row)
    if g['status'] not in {'ACTIVE','BLOCKED'}:return None
    blocked=json.loads(g['blocked_by_json'])
    routes=[x['pocket'] for x in rank(g['objective'],4) if x['score']>0] or ['enterpriseos']
    if len(routes)>1 and 'enterpriseos' not in routes: routes=['enterpriseos']+routes
    jtype='RESUME_BLOCKED_GOAL' if g['status']=='BLOCKED' or blocked else 'ADVANCE_GOAL'
    objective=('Re-evaluate blockers and advance: ' if jtype.startswith('RESUME') else 'Determine and execute/draft the next bounded step toward: ')+g['objective']
    since=(utcnow()-datetime.timedelta(hours=1)).isoformat()
    dk=stable_hash({'goal':g['goal_id'],'type':jtype,'blocked':blocked,'routes':routes})
    if reg.recent_job_with_key(dk,since):return None
    return reg.add_job(jtype,objective,trigger_type,routes,blocked,g['goal_id'],dk)

def tick(db_path,max_new_jobs=DEFAULT_MAX):
    reg=CapabilityRegistry(db_path); created=[]
    since=(utcnow()-datetime.timedelta(hours=1)).isoformat()
    # Direct HTTP MCPs can be re-scanned without user prompting. Host-managed connectors emit/supply snapshots through the host bridge.
    stale_before=(utcnow()-datetime.timedelta(hours=1)).isoformat()
    for c in reg.db.execute('SELECT * FROM connector_instances ORDER BY last_seen_at').fetchall():
        if len(created)>=max_new_jobs: break
        meta=json.loads(c['metadata_json']); src=meta.get('discovery_source',{})
        if src.get('transport')=='http' and c['last_seen_at']<stale_before:
            dk=stable_hash({'type':'CAPABILITY_RESCAN','connector':c['id'],'hour':utcnow().strftime('%Y%m%d%H')})
            if not reg.recent_job_with_key(dk,since):
                created.append(reg.add_job('CAPABILITY_RESCAN',f'Re-scan MCP capability surface for {c["id"]}','capability_freshness',['enterpriseos'],[c['id']],None,dk))
    for g in reg.goals(None):
        if len(created)>=max_new_jobs: break
        if g['status'] not in {'ACTIVE','BLOCKED'}: continue
        if g.get('next_check_at') and g['next_check_at']>utcnow().isoformat(): continue
        jid=queue_goal(reg,g['goal_id'],'reconciliation')
        if jid: created.append(jid)
    reg.event('AUTONOMY_TICK',None,{'new_jobs':created,'count':len(created)})
    return {'status':'PASS','new_jobs':created,'count':len(created),'rule':'Jobs are queued next actions, not unbounded recursive prompts. Side effects still require policy and connector gates.'}

def daemon(db_path,seconds=300,max_new_jobs=DEFAULT_MAX):
    seconds=max(60,int(seconds)); stop={'value':False}
    def _stop(signum,frame): stop['value']=True
    signal.signal(signal.SIGTERM,_stop); signal.signal(signal.SIGINT,_stop)
    while not stop['value']:
        print(json.dumps(tick(db_path,max_new_jobs),sort_keys=True),flush=True)
        if not stop['value']: time.sleep(seconds)
