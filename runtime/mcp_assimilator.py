from __future__ import annotations
import json, pathlib, re, hashlib
from .capability_registry import CapabilityRegistry, stable_hash
from .router import load_pockets, words

ROOT=pathlib.Path(__file__).resolve().parents[1]
WRITE={'create','update','edit','delete','remove','send','post','publish','deploy','merge','approve','reject','purchase','pay','refund','transfer','invite','schedule','cancel','sign','execute','run','write','upload','move','rename','archive','close','open','assign','label'}
HIGH={'delete','remove','transfer','refund','payment','pay','purchase','signature','sign','deploy','production','credential','secret','permission','role','access','employment','terminate','legal','filing'}
READ={'get','read','list','search','find','fetch','query','inspect','status','health','lookup','view','download'}
SAFE_SLUG=re.compile(r'[^a-z0-9]+')

def slugify(s): return SAFE_SLUG.sub('-',s.lower()).strip('-')[:90]
def cap_text(cap): return ' '.join([str(cap.get('name','')),str(cap.get('title','')),str(cap.get('description',''))])
def classify(cap_type,cap):
    toks=words(cap_text(cap));
    if cap_type!='tool': return ('low','read_only')
    high=toks & HIGH; write=toks & WRITE; read=toks & READ
    if high: return ('high','consequential_write')
    if write: return ('medium','write')
    if read and not write: return ('low','read_only')
    return ('medium','unknown_effect')

def pocket_routes(cap,limit=5):
    q=words(cap_text(cap)); out=[]
    for pid,p in load_pockets().items():
        pt=words(' '.join([pid,p['title'],p['mission'],' '.join(p.get('keywords',[])),' '.join(p.get('workflow',[]))]))
        score=4*len(q&pt)
        for kw in p.get('keywords',[]):
            kt=words(kw)
            if kt and kt.issubset(q): score+=8
        if score: out.append((score,pid))
    out.sort(key=lambda x:(-x[0],x[1])); return [p for _,p in out[:limit]] or ['enterpriseos']

def normalize_snapshot(s):
    return {
      'connector_id':s['connector_id'],'discovery_source':s.get('discovery_source',{}),'protocol_version':s.get('protocol_version','unknown'),'server_info':s.get('server_info',{}),'server_capabilities':s.get('server_capabilities',{}),
      'tools':s.get('tools',[]) or [],'resources':s.get('resources',[]) or [],'resource_templates':s.get('resource_templates',[]) or [],'prompts':s.get('prompts',[]) or []
    }

def generate_skill(dynamic_dir,connector_id,cap_type,cap,risk,side_effect,routes):
    name=cap.get('name') or cap.get('uri') or cap.get('uriTemplate') or cap.get('title') or 'capability'
    slug=f'dynamic-{slugify(connector_id)}-{cap_type}-{slugify(str(name))}'
    d=pathlib.Path(dynamic_dir)/slug; d.mkdir(parents=True,exist_ok=True)
    desc=(cap.get('description') or cap.get('title') or f'{cap_type} {name}').replace('\n',' ')
    body=f'''---\nname: {slug}\ndescription: "Assimilated {cap_type} from connected capability provider {connector_id}: {desc[:500].replace(chr(34), chr(39))}"\n---\n\n# Assimilated capability: {name}\n\n## Source\n- Connector: `{connector_id}`\n- Capability type: `{cap_type}`\n- Risk class: `{risk}`\n- Side-effect class: `{side_effect}`\n- Initial trust state: `QUARANTINED`\n\n## Contract\nThis wrapper was generated from the provider's advertised schema. It is metadata learning, not model-weight training. Tool availability does not grant authority. Re-read the live schema before consequential execution when freshness may matter.\n\n## Activation\nUse only when the objective requires this exact provider capability and the adaptive registry maps it to the active pocket/team.\n\n## Authorization\n- Read-only operations may be enabled after profiling.\n- Writes require policy approval or a narrowly pre-authorized path.\n- High-risk writes require connector certification, explicit decision rights, and read-back evidence.\n- Never expose credentials or bypass provider authorization.\n\n## Input/output schema\nSee `CAPABILITY.json`, which preserves the provider-advertised schema and metadata.\n\n## Pocket routes\n{', '.join('`'+x+'`' for x in routes)}\n\n## Validation\nTreat discovery as structural evidence only. A capability is not production-write-certified until environment-specific tests verify permission scope, idempotency/retry behavior, failure semantics, and read-back.\n'''
    (d/'SKILL.md').write_text(body)
    (d/'CAPABILITY.json').write_text(json.dumps(cap,indent=2)+'\n')
    return slug,str(d/'SKILL.md')

def assimilate(snapshot,db_path,dynamic_dir=None):
    s=normalize_snapshot(snapshot); reg=CapabilityRegistry(db_path); dynamic_dir=dynamic_dir or str(ROOT/'dynamic_skills')
    # Hash advertised functional surface, not volatile discovery timestamps.
    h=stable_hash({k:s[k] for k in ['protocol_version','server_info','server_capabilities','tools','resources','resource_templates','prompts']})
    old=reg.connector(s['connector_id']); changed=bool(old and old['capability_hash']!=h)
    reg.upsert_connector(s['connector_id'],'mcp',s['protocol_version'],s['server_info'],h,'PROFILED',{'server_capabilities':s['server_capabilities'],'discovery_source':s.get('discovery_source',{})})
    generated=[]; counts={}
    for cap_type,key in [('tool','tools'),('resource','resources'),('resource_template','resource_templates'),('prompt','prompts')]:
        counts[cap_type]=len(s[key])
        for cap in s[key]:
            name=cap.get('name') or cap.get('uri') or cap.get('uriTemplate') or cap.get('title') or hashlib.sha256(json.dumps(cap,sort_keys=True).encode()).hexdigest()[:12]
            risk,side=classify(cap_type,cap); routes=pocket_routes(cap)
            cid=reg.upsert_capability(s['connector_id'],cap_type,str(name),cap.get('description',''),cap.get('inputSchema') or cap.get('input_schema'),cap.get('outputSchema') or cap.get('output_schema'),risk,side,'QUARANTINED',cap)
            slug,path=generate_skill(dynamic_dir,s['connector_id'],cap_type,cap,risk,side,routes)
            reg.register_dynamic_skill(slug,s['connector_id'],cid,'QUARANTINED',path,routes)
            generated.append({'slug':slug,'capability_id':cid,'type':cap_type,'name':name,'risk_class':risk,'side_effect_class':side,'pocket_routes':routes})
    reg.event('CAPABILITY_ASSIMILATED',s['connector_id'],{'changed':changed,'counts':counts,'generated_skills':len(generated),'capability_hash':h}); reg.emit('CAPABILITY_CHANGED',s['connector_id'],{'changed':changed,'counts':counts,'capability_hash':h})
    # A capability change can make blocked goals worth re-evaluating. Do not execute them here.
    resume_candidates=[]
    available_words=words(' '.join(x['name'] for x in generated)+ ' '+ ' '.join(cap_text(x) for x in s['tools']))
    for g in reg.goals(None):
        blocked=json.loads(g['blocked_by_json'])
        if g['status']=='BLOCKED' or blocked:
            bwords=words(' '.join(map(str,blocked)))
            if not bwords or bwords & available_words: resume_candidates.append(g['goal_id'])
    if resume_candidates:
        reg.event('GOALS_POTENTIALLY_UNBLOCKED',s['connector_id'],{'goal_ids':resume_candidates})
        reg.emit('GOALS_POTENTIALLY_UNBLOCKED',s['connector_id'],{'goal_ids':resume_candidates})
    return {'status':'ASSIMILATED','connector_id':s['connector_id'],'changed':changed,'capability_hash':h,'counts':counts,'dynamic_skills_generated':len(generated),'resume_candidates':resume_candidates,'generated':generated}
