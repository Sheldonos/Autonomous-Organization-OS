from __future__ import annotations
import json, uuid, pathlib
from .router import rank,load_pockets
ROOT=pathlib.Path(__file__).resolve().parents[1]
def plan(intent, max_pockets=4):
    ranked=rank(intent,limit=max_pockets)
    if not ranked: raise RuntimeError('No pockets available')
    pockets=load_pockets(); chosen=[r['pocket'] for r in ranked if r['score']>0] or [ranked[0]['pocket']]
    # EnterpriseOS supervises composite missions.
    if len(chosen)>1 and 'enterpriseos' not in chosen: chosen=['enterpriseos']+chosen
    steps=[]
    for i,pid in enumerate(chosen):
        p=pockets[pid]
        steps.append({'order':i+1,'pocket':pid,'objective':p['mission'],'workflow':p['workflow'],'action_mode':'plan','handoffs':p['handoffs']})
    return {'mission_id':str(uuid.uuid4()),'intent':intent,'status':'PLANNED','pockets':chosen,'steps':steps,'events':[],'note':'This is an execution plan. External actions require configured adapters, authority, policy checks, and read-back verification.'}
