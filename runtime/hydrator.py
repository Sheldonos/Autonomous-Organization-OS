from __future__ import annotations
import json, pathlib, zipfile, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'substrate/source_archives/IBM_Enterprise_Autonomous_Operations_OS_v2.0.0-rc1.zip'
PREFIX='IBM_Enterprise_Autonomous_Operations_OS_v2.0.0-rc1/'
def locate_pocket(pid):
    for p in (ROOT/'segments').glob(f'*/*'):
        if p.is_dir() and p.name==pid and (p/'manifest.json').exists(): return p
    raise KeyError(pid)
def _team_slugs(pid,team):
    for p in (ROOT/'skills/os_factory').glob(f'*/{pid}/factory-{pid}-{team}/ROUTES.json'):
        return json.load(open(p)).get('canonical_children',[])
    raise KeyError(f'unknown team {pid}/{team}')
def _extract_slugs(slugs,dest):
    dest=pathlib.Path(dest);(dest/'.bob/skills').mkdir(parents=True,exist_ok=True);extracted=[]
    with zipfile.ZipFile(ARCHIVE) as z:
        names=set(z.namelist())
        for slug in sorted(set(slugs)):
            pref=PREFIX+f'.bob/skills/{slug}/';hits=[n for n in names if n.startswith(pref) and not n.endswith('/')]
            if not hits: continue
            for n in hits:
                target=dest/n[len(PREFIX):];target.parent.mkdir(parents=True,exist_ok=True)
                with z.open(n) as src,open(target,'wb') as out:shutil.copyfileobj(src,out)
            extracted.append(slug)
        for rel in ['AGENTS.md','manifest.yaml','registry/skills.json','registry/agents.json','registry/roles.json','registry/modes.json']:
            n=PREFIX+rel
            if n in names:
                target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
                with z.open(n) as src,open(target,'wb') as out:shutil.copyfileobj(src,out)
    return extracted
def hydrate(pid,dest,max_skills=None,team=None):
    pocket=locate_pocket(pid)
    if team: slugs=_team_slugs(pid,team)
    else: slugs=[x['slug'] for x in json.load(open(pocket/'skill_routes.json'))['skills']]
    if max_skills: slugs=slugs[:max_skills]
    dest=pathlib.Path(dest); extracted=_extract_slugs(slugs,dest)
    (dest/'federation').mkdir(parents=True,exist_ok=True)
    for fn in ['manifest.json','teams.json','workflow.json','skill_routes.json','connectors.json']:
        shutil.copy2(pocket/fn,dest/'federation'/fn)
    # Include relevant first-party wrapper(s).
    for base in (ROOT/'skills/os_factory').glob(f'*/{pid}'):
        target=dest/'federation/wrappers';shutil.copytree(base,target,dirs_exist_ok=True)
    if pid=='dealos': shutil.copytree(pocket/'implementation'/'DealOS_v1.0.1',dest/'dealos',dirs_exist_ok=True)
    result={'pocket':pid,'team':team,'destination':str(dest),'skills_requested':len(slugs),'skills_extracted':len(extracted),'slugs':extracted}
    (dest/'federation/HYDRATION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');return result
def hydrate_skill(slug,dest):
    acc=json.load(open(ROOT/'registry/skill_accountability.json'))['skills']; row=next((x for x in acc if x['slug']==slug),None)
    if not row: raise KeyError(slug)
    extracted=_extract_slugs([slug],dest);return {'skill':slug,'accountability':row,'skills_extracted':len(extracted),'destination':str(dest)}
