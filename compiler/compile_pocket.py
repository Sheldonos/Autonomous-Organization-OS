#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
TOK=re.compile(r"[a-z0-9+#.-]+")
def norm(s): return ' '.join(TOK.findall((s or '').lower()))
def main():
 p=argparse.ArgumentParser(); p.add_argument('id'); p.add_argument('--mission',required=True); p.add_argument('--keywords',required=True); p.add_argument('--segment',default='extensions'); p.add_argument('--max-skills',type=int,default=120); a=p.parse_args()
 skills=json.load(open(ROOT/'substrate/registry/skills.json')); terms=[x.strip() for x in a.keywords.split(',') if x.strip()]
 scored=[]
 for s in skills:
  txt=norm(' '.join([s.get('slug',''),s.get('domain',''),s.get('description','')]))
  score=sum(8 if norm(t) in norm(s.get('slug','')) else 3 if norm(t) in txt else 0 for t in terms)
  if score: scored.append((score,s['slug'],s.get('domain'),s.get('description','')))
 scored.sort(key=lambda x:(-x[0],x[1])); scored=scored[:a.max_skills]
 out=ROOT/'extensions'/a.id; out.mkdir(parents=True,exist_ok=True)
 (out/'manifest.json').write_text(json.dumps({'id':a.id,'segment':a.segment,'mission':a.mission,'keywords':terms,'substrate':'2.0.0-rc1','skill_routes_file':'skill_routes.json'},indent=2)+'\n')
 (out/'skill_routes.json').write_text(json.dumps({'count':len(scored),'skills':[{'slug':x[1],'score':x[0],'domain':x[2],'description':x[3]} for x in scored]},indent=2)+'\n')
 print(out)
if __name__=='__main__': main()
