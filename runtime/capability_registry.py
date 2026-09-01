from __future__ import annotations
import sqlite3, json, datetime, pathlib, hashlib, uuid

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS connector_instances(
 id TEXT PRIMARY KEY, kind TEXT NOT NULL, protocol_version TEXT, server_info_json TEXT NOT NULL,
 trust_state TEXT NOT NULL, capability_hash TEXT NOT NULL, discovered_at TEXT NOT NULL, last_seen_at TEXT NOT NULL,
 write_certified INTEGER NOT NULL DEFAULT 0, readback_verified INTEGER NOT NULL DEFAULT 0, metadata_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS capabilities(
 id TEXT PRIMARY KEY, connector_id TEXT NOT NULL, capability_type TEXT NOT NULL, name TEXT NOT NULL,
 description TEXT, input_schema_json TEXT NOT NULL, output_schema_json TEXT NOT NULL, risk_class TEXT NOT NULL,
 side_effect_class TEXT NOT NULL, trust_state TEXT NOT NULL, raw_json TEXT NOT NULL, discovered_at TEXT NOT NULL,
 UNIQUE(connector_id, capability_type, name)
);
CREATE TABLE IF NOT EXISTS dynamic_skills(
 slug TEXT PRIMARY KEY, connector_id TEXT NOT NULL, capability_id TEXT NOT NULL, state TEXT NOT NULL,
 skill_path TEXT NOT NULL, pocket_routes_json TEXT NOT NULL, generated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS goals(
 goal_id TEXT PRIMARY KEY, objective TEXT NOT NULL, status TEXT NOT NULL, priority INTEGER NOT NULL,
 blocked_by_json TEXT NOT NULL, metadata_json TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 next_check_at TEXT
);
CREATE TABLE IF NOT EXISTS jobs(
 job_id TEXT PRIMARY KEY, goal_id TEXT, job_type TEXT NOT NULL, objective TEXT NOT NULL, status TEXT NOT NULL,
 trigger_type TEXT NOT NULL, pocket_routes_json TEXT NOT NULL, required_capabilities_json TEXT NOT NULL,
 dedupe_key TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, result_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_dedupe ON jobs(dedupe_key,created_at);
CREATE TABLE IF NOT EXISTS autonomy_events(
 id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS event_queue(
 event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, status TEXT NOT NULL,
 dedupe_key TEXT NOT NULL, available_at TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_event_queue_status_available ON event_queue(status,available_at);
CREATE INDEX IF NOT EXISTS idx_event_queue_dedupe ON event_queue(dedupe_key,created_at);
CREATE TABLE IF NOT EXISTS dead_letters(
 event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, attempts INTEGER NOT NULL,
 last_error TEXT, failed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS system_flags(
 key TEXT PRIMARY KEY, value_json TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS effect_receipts(
 effect_id TEXT PRIMARY KEY, job_id TEXT, connector_id TEXT, operation TEXT NOT NULL, idempotency_key TEXT NOT NULL,
 request_hash TEXT NOT NULL, status TEXT NOT NULL, remote_ref TEXT, readback_hash TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 UNIQUE(connector_id,idempotency_key)
);
"""

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def stable_hash(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class CapabilityRegistry:
    def __init__(self,path):
        self.path=str(path); pathlib.Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(self.path); self.db.row_factory=sqlite3.Row; self.db.executescript(SCHEMA); self.db.commit()
    def upsert_connector(self, connector_id, kind, protocol_version, server_info, capability_hash, trust_state='PROFILED', metadata=None):
        t=now(); self.db.execute('''INSERT INTO connector_instances(id,kind,protocol_version,server_info_json,trust_state,capability_hash,discovered_at,last_seen_at,metadata_json)
          VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,protocol_version=excluded.protocol_version,server_info_json=excluded.server_info_json,trust_state=excluded.trust_state,capability_hash=excluded.capability_hash,last_seen_at=excluded.last_seen_at,metadata_json=excluded.metadata_json''',
          (connector_id,kind,protocol_version,json.dumps(server_info or {}),trust_state,capability_hash,t,t,json.dumps(metadata or {}))); self.db.commit()
    def connector(self,connector_id):
        r=self.db.execute('SELECT * FROM connector_instances WHERE id=?',(connector_id,)).fetchone(); return dict(r) if r else None
    def certify(self,connector_id,write=False,readback=False):
        state='WRITE_CERTIFIED' if write and readback else 'READ_ENABLED'
        self.db.execute('UPDATE connector_instances SET trust_state=?,write_certified=?,readback_verified=?,last_seen_at=? WHERE id=?',(state,int(bool(write)),int(bool(readback)),now(),connector_id)); self.db.commit()
        self.event('CONNECTOR_CERTIFIED',connector_id,{'state':state,'write':bool(write),'readback':bool(readback)}); self.emit('CONNECTOR_CERTIFIED',connector_id,{'state':state,'write':bool(write),'readback':bool(readback)})
    def upsert_capability(self, connector_id, cap_type, name, description='', input_schema=None, output_schema=None, risk_class='unknown', side_effect_class='unknown', trust_state='QUARANTINED', raw=None):
        cid=hashlib.sha256(f'{connector_id}:{cap_type}:{name}'.encode()).hexdigest()[:32]; t=now()
        self.db.execute('''INSERT INTO capabilities(id,connector_id,capability_type,name,description,input_schema_json,output_schema_json,risk_class,side_effect_class,trust_state,raw_json,discovered_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(connector_id,capability_type,name) DO UPDATE SET description=excluded.description,input_schema_json=excluded.input_schema_json,output_schema_json=excluded.output_schema_json,risk_class=excluded.risk_class,side_effect_class=excluded.side_effect_class,trust_state=excluded.trust_state,raw_json=excluded.raw_json,discovered_at=excluded.discovered_at''',
        (cid,connector_id,cap_type,name,description,json.dumps(input_schema or {}),json.dumps(output_schema or {}),risk_class,side_effect_class,trust_state,json.dumps(raw or {}),t)); self.db.commit(); return cid
    def register_dynamic_skill(self,slug,connector_id,capability_id,state,skill_path,pocket_routes):
        self.db.execute('''INSERT INTO dynamic_skills VALUES(?,?,?,?,?,?,?) ON CONFLICT(slug) DO UPDATE SET state=excluded.state,skill_path=excluded.skill_path,pocket_routes_json=excluded.pocket_routes_json,generated_at=excluded.generated_at''',(slug,connector_id,capability_id,state,skill_path,json.dumps(pocket_routes),now())); self.db.commit()
    def add_goal(self,objective,priority=50,blocked_by=None,metadata=None,goal_id=None):
        gid=goal_id or str(uuid.uuid4()); t=now(); self.db.execute('INSERT OR REPLACE INTO goals VALUES(?,?,?,?,?,?,?,?,?)',(gid,objective,'ACTIVE',int(priority),json.dumps(blocked_by or []),json.dumps(metadata or {}),t,t,None)); self.db.commit(); self.event('GOAL_ADDED',gid,{'objective':objective}); self.emit('GOAL_ADDED',gid,{'objective':objective}); return gid
    def update_goal(self,goal_id,status=None,blocked_by=None,next_check_at=None):
        r=self.db.execute('SELECT * FROM goals WHERE goal_id=?',(goal_id,)).fetchone();
        if not r: raise KeyError(goal_id)
        self.db.execute('UPDATE goals SET status=?,blocked_by_json=?,updated_at=?,next_check_at=? WHERE goal_id=?',(status or r['status'],json.dumps(blocked_by if blocked_by is not None else json.loads(r['blocked_by_json'])),now(),next_check_at,goal_id)); self.db.commit()
    def goals(self,status='ACTIVE'):
        q='SELECT * FROM goals' + (' WHERE status=?' if status else '') + ' ORDER BY priority DESC, created_at'; rows=self.db.execute(q,(status,) if status else ()).fetchall(); return [dict(x) for x in rows]
    def add_job(self,job_type,objective,trigger_type,pocket_routes,required_capabilities=None,goal_id=None,dedupe_key=None):
        jid=str(uuid.uuid4()); t=now(); dk=dedupe_key or stable_hash({'goal':goal_id,'type':job_type,'objective':objective,'pockets':pocket_routes})
        self.db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(jid,goal_id,job_type,objective,'QUEUED',trigger_type,json.dumps(pocket_routes),json.dumps(required_capabilities or []),dk,t,t,json.dumps({}))); self.db.commit(); self.event('JOB_QUEUED',jid,{'goal_id':goal_id,'type':job_type}); return jid
    def recent_job_with_key(self,key,since_iso): return self.db.execute('SELECT 1 FROM jobs WHERE dedupe_key=? AND created_at>=? LIMIT 1',(key,since_iso)).fetchone() is not None

    def claim_job(self):
        self.db.execute('BEGIN IMMEDIATE')
        r=self.db.execute("SELECT * FROM jobs WHERE status='QUEUED' ORDER BY created_at LIMIT 1").fetchone()
        if not r:
            self.db.commit(); return None
        self.db.execute("UPDATE jobs SET status='RUNNING',updated_at=? WHERE job_id=? AND status='QUEUED'",(now(),r['job_id'])); self.db.commit()
        return dict(self.db.execute('SELECT * FROM jobs WHERE job_id=?',(r['job_id'],)).fetchone())
    def finish_job(self,job_id,status,result=None):
        self.db.execute('UPDATE jobs SET status=?,updated_at=?,result_json=? WHERE job_id=?',(status,now(),json.dumps(result or {}),job_id)); self.db.commit(); self.event('JOB_'+status,job_id,result or {}); self.emit('JOB_STATUS_CHANGED',job_id,{'status':status,'result':result or {}})

    def jobs(self,status=None,limit=100):
        if status: rows=self.db.execute('SELECT * FROM jobs WHERE status=? ORDER BY created_at DESC LIMIT ?',(status,limit)).fetchall()
        else: rows=self.db.execute('SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?',(limit,)).fetchall()
        return [dict(x) for x in rows]
    def capabilities(self,connector_id=None):
        rows=self.db.execute('SELECT * FROM capabilities WHERE connector_id=? ORDER BY capability_type,name',(connector_id,)).fetchall() if connector_id else self.db.execute('SELECT * FROM capabilities ORDER BY connector_id,capability_type,name').fetchall(); return [dict(x) for x in rows]
    def event(self,event_type,subject_id=None,payload=None): self.db.execute('INSERT INTO autonomy_events(event_type,subject_id,payload_json,created_at) VALUES(?,?,?,?)',(event_type,subject_id,json.dumps(payload or {}),now())); self.db.commit()

    def emit(self,event_type,subject_id=None,payload=None,dedupe_key=None,available_at=None,dedupe_window_seconds=300):
        t=now(); dk=dedupe_key or stable_hash({'type':event_type,'subject':subject_id,'payload':payload or {}})
        cutoff=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=int(dedupe_window_seconds))).isoformat()
        prior=self.db.execute("SELECT event_id FROM event_queue WHERE dedupe_key=? AND created_at>=? AND status IN ('QUEUED','RUNNING','COMPLETED') LIMIT 1",(dk,cutoff)).fetchone()
        if prior:return prior['event_id']
        eid=str(uuid.uuid4()); self.db.execute('INSERT INTO event_queue VALUES(?,?,?,?,?,?,?,?,?,?,?)',(eid,event_type,subject_id,json.dumps(payload or {}),'QUEUED',dk,available_at or t,0,None,t,t)); self.db.commit(); return eid

    def claim_event(self):
        self.db.execute('BEGIN IMMEDIATE')
        r=self.db.execute("SELECT * FROM event_queue WHERE status='QUEUED' AND available_at<=? ORDER BY available_at,created_at LIMIT 1",(now(),)).fetchone()
        if not r:self.db.commit();return None
        self.db.execute("UPDATE event_queue SET status='RUNNING',attempts=attempts+1,updated_at=? WHERE event_id=? AND status='QUEUED'",(now(),r['event_id'])); self.db.commit()
        return dict(self.db.execute('SELECT * FROM event_queue WHERE event_id=?',(r['event_id'],)).fetchone())

    def finish_event(self,event_id,result=None):
        self.db.execute("UPDATE event_queue SET status='COMPLETED',last_error=NULL,updated_at=? WHERE event_id=?",(now(),event_id)); self.db.commit(); self.event('EVENT_COMPLETED',event_id,result or {})

    def fail_event(self,event_id,error,max_attempts=5,retry_seconds=30):
        r=self.db.execute('SELECT * FROM event_queue WHERE event_id=?',(event_id,)).fetchone()
        if not r:return
        if int(r['attempts'])>=int(max_attempts):
            self.db.execute("UPDATE event_queue SET status='DEAD_LETTER',last_error=?,updated_at=? WHERE event_id=?",(str(error),now(),event_id))
            self.db.execute('INSERT OR REPLACE INTO dead_letters VALUES(?,?,?,?,?,?,?)',(r['event_id'],r['event_type'],r['subject_id'],r['payload_json'],r['attempts'],str(error),now()))
        else:
            at=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=int(retry_seconds)*(2**max(0,int(r['attempts'])-1)))).isoformat()
            self.db.execute("UPDATE event_queue SET status='QUEUED',last_error=?,available_at=?,updated_at=? WHERE event_id=?",(str(error),at,now(),event_id))
        self.db.commit()


    def set_flag(self,key,value):
        self.db.execute('INSERT INTO system_flags(key,value_json,updated_at) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=excluded.updated_at',(key,json.dumps(value),now())); self.db.commit(); self.event('SYSTEM_FLAG_CHANGED',key,{'value':value})

    def get_flag(self,key,default=None):
        r=self.db.execute('SELECT value_json FROM system_flags WHERE key=?',(key,)).fetchone(); return json.loads(r['value_json']) if r else default

    def record_effect(self,effect_id,job_id,connector_id,operation,idempotency_key,request_hash,status,remote_ref=None,readback_hash=None):
        t=now()
        sql="""INSERT INTO effect_receipts(effect_id,job_id,connector_id,operation,idempotency_key,request_hash,status,remote_ref,readback_hash,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(effect_id) DO UPDATE SET status=excluded.status,remote_ref=excluded.remote_ref,readback_hash=excluded.readback_hash,updated_at=excluded.updated_at"""
        self.db.execute(sql,(effect_id,job_id,connector_id,operation,idempotency_key,request_hash,status,remote_ref,readback_hash,t,t)); self.db.commit()

    def recover_stale(self,older_than_seconds=600):
        cutoff=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=int(older_than_seconds))).isoformat()
        a=self.db.execute("UPDATE event_queue SET status='QUEUED',updated_at=? WHERE status='RUNNING' AND updated_at<?",(now(),cutoff)).rowcount
        b=self.db.execute("UPDATE jobs SET status='QUEUED',updated_at=? WHERE status='RUNNING' AND updated_at<?",(now(),cutoff)).rowcount
        self.db.commit(); return {'events_requeued':a,'jobs_requeued':b}

    def queued_events(self,status=None,limit=100):
        if status: rows=self.db.execute('SELECT * FROM event_queue WHERE status=? ORDER BY created_at DESC LIMIT ?',(status,limit)).fetchall()
        else: rows=self.db.execute('SELECT * FROM event_queue ORDER BY created_at DESC LIMIT ?',(limit,)).fetchall()
        return [dict(x) for x in rows]
