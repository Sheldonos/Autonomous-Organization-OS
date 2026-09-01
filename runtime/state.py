from __future__ import annotations
import sqlite3,json,datetime
SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS missions(mission_id TEXT PRIMARY KEY,intent TEXT NOT NULL,status TEXT NOT NULL,plan_json TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,mission_id TEXT NOT NULL,event_type TEXT NOT NULL,pocket TEXT,payload_json TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS approvals(approval_id TEXT PRIMARY KEY,mission_id TEXT NOT NULL,action_type TEXT NOT NULL,status TEXT NOT NULL,request_json TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS evidence(id INTEGER PRIMARY KEY AUTOINCREMENT,mission_id TEXT NOT NULL,pocket TEXT,ref TEXT NOT NULL,kind TEXT,sha256 TEXT,created_at TEXT NOT NULL);
"""
class MissionStore:
    def __init__(self,path):
        self.path=str(path); self.db=sqlite3.connect(self.path); self.db.row_factory=sqlite3.Row; self._init()
    def _init(self): self.db.executescript(SCHEMA); self.db.commit()
    def now(self): return datetime.datetime.now(datetime.timezone.utc).isoformat()
    def put_mission(self,plan):
        now=self.now(); self.db.execute('INSERT OR REPLACE INTO missions VALUES(?,?,?,?,?,?)',(plan['mission_id'],plan['intent'],plan['status'],json.dumps(plan),now,now)); self.db.commit(); return plan['mission_id']
    def event(self,mission_id,event_type,pocket=None,payload=None):
        self.db.execute('INSERT INTO events(mission_id,event_type,pocket,payload_json,created_at) VALUES(?,?,?,?,?)',(mission_id,event_type,pocket,json.dumps(payload or {}),self.now())); self.db.commit()
    def get_mission(self,mission_id):
        r=self.db.execute('SELECT * FROM missions WHERE mission_id=?',(mission_id,)).fetchone(); return dict(r) if r else None
    def list_missions(self,limit=20):
        return [dict(x) for x in self.db.execute('SELECT mission_id,intent,status,created_at,updated_at FROM missions ORDER BY created_at DESC LIMIT ?',(limit,)).fetchall()]
