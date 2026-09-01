from __future__ import annotations
import json,pathlib
from .hydrator import hydrate,locate_pocket
ROOT=pathlib.Path(__file__).resolve().parents[1]

def team_routes(pid,team_id):
    base=ROOT/'skills/os_factory'
    for p in base.glob(f'*/{pid}/factory-{pid}-{team_id}/ROUTES.json'):
        return json.load(open(p)).get('canonical_children',[])
    raise KeyError((pid,team_id))

def context_plan(pid,team_id=None,max_skills=20):
    if team_id:
        slugs=team_routes(pid,team_id)[:max_skills]
    else:
        d=json.load(open(locate_pocket(pid)/'skill_routes.json')); slugs=[x['slug'] for x in d['skills'][:max_skills]]
    return {'pocket':pid,'team':team_id,'max_skills':max_skills,'canonical_skill_slugs':slugs,'principle':'hydrate only what the next bounded job needs; durable state stays outside model context'}
