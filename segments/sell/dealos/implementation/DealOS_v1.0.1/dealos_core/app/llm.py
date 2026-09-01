import json, re
from .config import settings
from .profile import business_profile, account_registry
from .policy import load_policy
from .usage import assert_openai_budget, record_openai_usage

OPT_OUT=re.compile(r'\b(unsubscribe|remove me|stop emailing|do not contact|opt[ -]?out)\b',re.I)
OWNER_CMD=re.compile(r'^\s*(APPROVE|REJECT)\s+([0-9a-fA-F-]{8,})\s*$',re.I)

def cheap_local_classification(sender:str, subject:str|None, body:str|None):
    text=f'{subject or ""}\n{body or ""}'
    if OPT_OUT.search(text):
        return {'category':'opt_out','intent':'unsubscribe','reply_needed':False,'risk_level':'green','needs_research':False,'deal_signal':False}
    return {'category':'business_message','intent':'unknown','reply_needed':False,'risk_level':'green','needs_research':False,'deal_signal':False}

def parse_owner_command(body:str|None):
    m=OWNER_CMD.match((body or '').strip())
    return None if not m else {'decision':m.group(1).lower(),'approval_id':m.group(2)}

def classify_email(sender, subject, body, deal_context=None):
    base=cheap_local_classification(sender,subject,body)
    if base['category']=='opt_out' or not settings.openai_api_key:
        return base
    try:
        from openai import OpenAI
        assert_openai_budget(0.02)
        client=OpenAI(api_key=settings.openai_api_key)
        schema={
          'type':'object','properties':{
            'category':{'type':'string'},'intent':{'type':'string'},'reply_needed':{'type':'boolean'},
            'risk_level':{'type':'string','enum':['green','blue','yellow','orange','red']},
            'needs_research':{'type':'boolean'},'deal_signal':{'type':'boolean'},
            'draft_reply':{'type':['string','null']},'reason':{'type':'string'}},
          'required':['category','intent','reply_needed','risk_level','needs_research','deal_signal','draft_reply','reason'],
          'additionalProperties':False}
        profile=business_profile()
        registry=account_registry()
        negotiation=load_policy('negotiation')
        safe_context={
            'business': profile.get('business',{}),
            'approved_capabilities': profile.get('approved_capabilities',[]),
            'approved_evidence': profile.get('approved_evidence',[]),
            'lane_offers': profile.get('lanes',{}),
            'commercial_authority': registry.get('commercial_authority',{}),
            'negotiation_policy': negotiation,
            'deal_context': deal_context or {},
        }
        system=(
            'Classify this business email and, when appropriate, draft a concise reply using ONLY the approved context supplied. '
            'Never invent capabilities, customers, relationships, certifications, prices, deadlines, or authority. '
            'Routine replies and non-binding commercial discussion inside configured negotiation floors/terms may be green/blue. '
            'When discussing price or terms, make clear the discussion is non-binding and subject to a definitive signed agreement. '
            'Escalate signatures, binding acceptance, exclusivity, IP assignment, uncapped liability, unusual indemnity, bank/payment-destination changes, '
            'credentials, fraud/sanctions concerns, federal contingent-fee/kickback concerns, or terms outside the configured envelope. '
            'Do not promise an attachment or completed work that has not actually been generated.'
        )
        response=client.responses.create(
            model=settings.openai_fast_model,
            input=[{'role':'system','content':system},
                   {'role':'user','content':f'Approved context: {json.dumps(safe_context, default=str)}\n\nSender: {sender}\nSubject: {subject}\nBody:\n{body}'}],
            text={'format':{'type':'json_schema','name':'email_classification','schema':schema,'strict':True}}
        )
        record_openai_usage(settings.openai_fast_model,'email_classification',response)
        return json.loads(response.output_text)
    except Exception as e:
        base['classifier_error']=str(e)[:300]
        return base
