from __future__ import annotations
from .mission import plan
from .state import MissionStore
def start(intent,db_path,max_pockets=4):
    p=plan(intent,max_pockets); store=MissionStore(db_path); store.put_mission(p); store.event(p['mission_id'],'MISSION_PLANNED',payload={'pockets':p['pockets']}); return p
