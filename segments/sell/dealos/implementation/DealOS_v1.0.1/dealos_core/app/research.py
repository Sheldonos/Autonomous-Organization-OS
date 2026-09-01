import json
from .config import settings
from .profile import lanes, lane_enabled
from .usage import assert_openai_budget, record_openai_usage

def _client():
    if not settings.openai_api_key: raise RuntimeError('OPENAI_API_KEY required')
    from openai import OpenAI
    return OpenAI(api_key=settings.openai_api_key)

RESEARCH_SCHEMA={
 'type':'object','properties':{
  'summary':{'type':'string'},'qualification_score':{'type':'number','minimum':0,'maximum':100},
  'organization_name':{'type':['string','null']},'company_domain':{'type':['string','null']},
  'verified_facts':{'type':'array','items':{'type':'object','properties':{'fact':{'type':'string'},'source_url':{'type':'string'}},'required':['fact','source_url'],'additionalProperties':False}},
  'decision_makers':{'type':'array','items':{'type':'object','properties':{'first_name':{'type':['string','null']},'last_name':{'type':['string','null']},'full_name':{'type':['string','null']},'title':{'type':['string','null']},'email':{'type':['string','null']},'source_url':{'type':['string','null']}},'required':['first_name','last_name','full_name','title','email','source_url'],'additionalProperties':False}},
  'needs':{'type':'array','items':{'type':'string'}},'risks':{'type':'array','items':{'type':'string'}},
  'recommended_outreach_angle':{'type':['string','null']},'recommended_next_action':{'type':'string'}},
 'required':['summary','qualification_score','organization_name','company_domain','verified_facts','decision_makers','needs','risks','recommended_outreach_angle','recommended_next_action'],'additionalProperties':False}

SCAN_SCHEMA={
 'type':'object','properties':{'opportunities':{'type':'array','items':{'type':'object','properties':{
  'external_id':{'type':'string'},'title':{'type':'string'},'organization_name':{'type':'string'},'company_domain':{'type':['string','null']},
  'url':{'type':'string'},'why_now':{'type':'string'},'buyer_function':{'type':['string','null']},'score':{'type':'number','minimum':0,'maximum':100}},
  'required':['external_id','title','organization_name','company_domain','url','why_now','buyer_function','score'],'additionalProperties':False}}},
 'required':['opportunities'],'additionalProperties':False}

def run_research(prompt:str):
    assert_openai_budget(0.10)
    r=_client().responses.create(
      model=settings.openai_standard_model,
      tools=[{'type':'web_search'}],
      input=[{'role':'system','content':'Research a business opportunity using current public web evidence. Return only evidence-backed facts. Do not invent names, emails, relationships, budgets, certifications or contract details. Prefer official/primary sources.'},{'role':'user','content':prompt}],
      text={'format':{'type':'json_schema','name':'deal_research','schema':RESEARCH_SCHEMA,'strict':True}}
    )
    record_openai_usage(settings.openai_standard_model,'qualified_research',r,web_search_calls=1)
    return json.loads(r.output_text)

def scan_lane(lane:str):
    cfg=lanes().get('private_market',{}).get(lane)
    if not cfg: raise ValueError('Unknown lane')
    if not lane_enabled(lane): raise ValueError('Lane disabled or business profile unconfigured')
    prompt=cfg.get('scan_prompt')+'\nReturn at most '+str(cfg.get('max_results_per_scan',10))+' opportunities. Use a stable public URL-derived external_id or deterministic organization+signal identifier.'
    assert_openai_budget(0.10)
    r=_client().responses.create(
      model=settings.openai_standard_model, tools=[{'type':'web_search'}],
      input=[{'role':'system','content':'Find recent, public, verifiable B2B buying or need signals. Do not invent opportunities. Primary sources preferred. Exclude vague listicles and generic market commentary.'},{'role':'user','content':prompt}],
      text={'format':{'type':'json_schema','name':'market_scan','schema':SCAN_SCHEMA,'strict':True}}
    )
    record_openai_usage(settings.openai_standard_model,'private_market_scan',r,web_search_calls=1)
    return json.loads(r.output_text)
