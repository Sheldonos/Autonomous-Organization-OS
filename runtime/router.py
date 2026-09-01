from __future__ import annotations
import json,re,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
TOK=re.compile(r"[a-z0-9+#.-]+")
STOP={'a','an','and','or','the','to','of','in','on','for','with','from','then','it','this','that','my','our','we','i','be','is','are','as','by','at','into','all','new'}
def words(s): return {w for w in TOK.findall((s or '').lower()) if w not in STOP and len(w)>1}
def load_pockets(): return json.load(open(ROOT/'registry/pockets.json'))
def rank(intent, limit=5):
    q=words(intent); pockets=load_pockets(); out=[]
    low=intent.lower(); compact=re.sub(r'[^a-z0-9]','',low)
    for pid,p in pockets.items():
        text=' '.join([pid,p.get('title',''),p.get('mission',''),' '.join(p.get('keywords',[])),' '.join(p.get('workflow',[]))])
        w=words(text); overlap=q&w
        score=len(overlap)*4; phrase_hits=[]
        for k in p.get('keywords',[]):
            kl=k.lower()
            if len(kl)>=3 and kl in low:
                score+=6; phrase_hits.append(k)
        for a in p.get('aliases',[]):
            if a.lower() in low: score+=10; phrase_hits.append(a)
        stem=pid[:-2] if pid.endswith('os') else pid
        if stem and stem in compact: score+=12
        out.append({'pocket':pid,'title':p['title'],'segment':p['segment'],'score':score,'matched_tokens':sorted(overlap),'matched_phrases':sorted(set(phrase_hits))})
    out.sort(key=lambda x:(-x['score'],x['pocket']))
    return out[:limit]
