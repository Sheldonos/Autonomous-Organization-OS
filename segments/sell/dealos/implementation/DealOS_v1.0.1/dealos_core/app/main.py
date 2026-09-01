from datetime import datetime, timezone
from email.utils import parseaddr
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from .config import settings
from .db import Base, engine, get_db
from .models import Opportunity, Deal, Message, Outbox, Approval, Suppression, ResearchJob, ActionQueue, AuditEvent
from .llm import classify_email, parse_owner_command
from .policy import evaluate_action
from .manus import verify_webhook
from .research import run_research, scan_lane
from .automation import finalize_research
from .hunter import find_email, verify_email
from .stripe_adapter import create_draft_invoice, verify_webhook as verify_stripe_webhook
from .docusign_adapter import send_template_envelope
from .profile import lane_enabled, lanes as lane_config

app=FastAPI(title='DealOS Core',version='1.0.0')
Base.metadata.create_all(bind=engine)

def auth(x_dealos_key:str|None=Header(None)):
    if x_dealos_key != settings.dealos_api_key:
        raise HTTPException(401,'Invalid DealOS key')
    return True

def audit(db, actor, event_type, entity_type=None, entity_id=None, risk_level=None, payload=None):
    db.add(AuditEvent(actor=actor,event_type=event_type,entity_type=entity_type,entity_id=entity_id,risk_level=risk_level,payload=payload or {}))

@app.get('/health')
def health(): return {'ok':True,'service':'dealos-core','version':'1.0.0'}

@app.post('/events/email',dependencies=[Depends(auth)])
def email_event(payload:dict, db:Session=Depends(get_db)):
    raw_sender=(payload.get('from') or payload.get('sender') or '').strip()
    sender=(parseaddr(raw_sender)[1] or raw_sender).strip().lower()
    subject=payload.get('subject') or ''
    body=payload.get('body_text') or payload.get('text') or payload.get('body') or ''
    external_id=payload.get('message_id') or payload.get('id')
    thread_id=payload.get('thread_id')
    if external_id and db.scalar(select(Message).where(Message.external_message_id==external_id)):
        return {'status':'duplicate'}
    if sender==settings.owner_email.lower():
        cmd=parse_owner_command(body)
        if cmd:
            a=db.get(Approval,cmd['approval_id'])
            if not a or a.status!='pending': raise HTTPException(404,'Pending approval not found')
            a.status='approved' if cmd['decision']=='approve' else 'rejected'
            a.decided_at=datetime.now(timezone.utc); a.decided_by=sender
            audit(db,'owner','approval_decided','approval',a.id,a.risk_level,{'decision':a.status})
            db.commit(); return {'status':'owner_command','decision':a.status,'approval_id':a.id}
    prior_outbox=db.scalar(select(Outbox).where(Outbox.to_email==sender,Outbox.deal_id.is_not(None)).order_by(Outbox.created_at.desc())) if sender else None
    linked_deal=db.get(Deal,prior_outbox.deal_id) if prior_outbox and prior_outbox.deal_id else None
    deal_context={}
    if linked_deal:
        deal_context={'id':linked_deal.id,'name':linked_deal.name,'lane':linked_deal.lane,'stage':linked_deal.stage,'expected_value_usd':float(linked_deal.expected_value_usd or 0),'metadata':linked_deal.metadata_json}
    classification=classify_email(sender,subject,body,deal_context=deal_context)
    m=Message(deal_id=linked_deal.id if linked_deal else None,external_message_id=external_id,thread_id=thread_id,direction='inbound',sender=sender,subject=subject,body_text=body,classification=classification)
    db.add(m)
    if classification.get('intent')=='unsubscribe' and sender:
        if not db.scalar(select(Suppression).where(Suppression.email==sender)):
            db.add(Suppression(email=sender,reason='recipient_opt_out',source='gmail'))
        audit(db,'inbox-agent','contact_suppressed','contact',sender,'green',{'reason':'opt_out'})
    elif classification.get('reply_needed') and classification.get('draft_reply'):
        risk=classification.get('risk_level','green')
        if risk in ('green','blue'):
            if sender and not db.scalar(select(Suppression).where(Suppression.email==sender)):
                db.add(Outbox(deal_id=linked_deal.id if linked_deal else None,to_email=sender,subject=subject,body_text=classification['draft_reply'],reply_to_message_id=external_id,risk_level=risk))
        else:
            db.add(Approval(deal_id=linked_deal.id if linked_deal else None,action_type='send_email',summary=f'Review proposed reply to {sender}: {subject}',risk_level='orange' if risk!='red' else 'red',payload={'to':sender,'subject':subject,'body':classification.get('draft_reply')}))
    audit(db,'inbox-agent','email_ingested','message',external_id,classification.get('risk_level'),{'classification':classification})
    db.commit()
    return {'status':'ingested','classification':classification}

@app.post('/events/opportunity',dependencies=[Depends(auth)])
def opportunity_event(payload:dict, db:Session=Depends(get_db)):
    source=payload.get('source','unknown'); external_id=str(payload.get('external_id') or '')
    if not external_id: raise HTTPException(422,'external_id required')
    existing=db.scalar(select(Opportunity).where(Opportunity.source==source,Opportunity.external_id==external_id))
    if existing: return {'status':'duplicate','id':existing.id}
    raw=payload.get('raw') or payload
    title=payload.get('title') or raw.get('title') or 'Untitled opportunity'
    score=payload.get('score')
    if score is None:
        text=(title+' '+str(payload.get('description') or '')).lower()
        score=50 + (15 if any(x in text for x in ['ai','automation','modernization','software','cyber','data']) else 0)
    o=Opportunity(source=source,external_id=external_id,title=title,url=payload.get('url'),description=payload.get('description'),estimated_value_usd=payload.get('estimated_value_usd'),score=score,raw=raw)
    db.add(o); db.flush()
    if float(score)>=65:
        ev=float(payload.get('estimated_value_usd') or 0)
        provider='manus' if settings.manus_enabled and ev>=settings.manus_min_expected_value_usd else 'openai'
        db.add(ResearchJob(opportunity_id=o.id,provider=provider,prompt=f'Research and qualify opportunity {title}. Verify buyer, requirements, likely incumbents/partners, deadlines, constraints, evidence and next actions.',expected_value_usd=ev or None))
    audit(db,'opportunity-hunter','opportunity_ingested','opportunity',o.id,'green',{'score':score})
    db.commit(); return {'status':'ingested','id':o.id,'score':score}

@app.get('/outbox/next',dependencies=[Depends(auth)])
def outbox_next(limit:int=10, db:Session=Depends(get_db)):
    rows=db.scalars(select(Outbox).where(Outbox.status=='queued',Outbox.scheduled_at<=datetime.now(timezone.utc)).order_by(Outbox.scheduled_at).limit(min(limit,50))).all()
    return {'items':[{'id':r.id,'deal_id':r.deal_id,'to_email':r.to_email,'subject':r.subject,'body_text':r.body_text,'reply_to_message_id':r.reply_to_message_id,'risk_level':r.risk_level} for r in rows]}

@app.post('/outbox/{item_id}/sent',dependencies=[Depends(auth)])
def outbox_sent(item_id:str,payload:dict,db:Session=Depends(get_db)):
    r=db.get(Outbox,item_id)
    if not r: raise HTTPException(404)
    r.status='sent'; r.sent_at=datetime.now(timezone.utc)
    audit(db,'n8n','email_sent','outbox',r.id,r.risk_level,payload); db.commit(); return {'ok':True}

@app.get('/actions/next',dependencies=[Depends(auth)])
def actions_next(limit:int=10, action_type:str|None=None, db:Session=Depends(get_db)):
    q=select(ActionQueue).where(ActionQueue.status=='queued',ActionQueue.scheduled_at<=datetime.now(timezone.utc))
    if action_type: q=q.where(ActionQueue.action_type==action_type)
    rows=db.scalars(q.order_by(ActionQueue.scheduled_at).limit(min(limit,50))).all()
    items=[]
    for r in rows:
        if r.requires_approval:
            a=db.get(Approval,r.approval_id) if r.approval_id else None
            if not a or a.status!='approved': continue
        items.append({'id':r.id,'action_type':r.action_type,'payload':r.payload,'risk_level':r.risk_level})
    return {'items':items}

@app.post('/actions/{item_id}/complete',dependencies=[Depends(auth)])
def action_complete(item_id:str,payload:dict,db:Session=Depends(get_db)):
    r=db.get(ActionQueue,item_id)
    if not r: raise HTTPException(404)
    r.status='completed'; r.result=payload; r.completed_at=datetime.now(timezone.utc)
    audit(db,'n8n','action_completed','action',r.id,r.risk_level,payload); db.commit(); return {'ok':True}

@app.post('/actions/queue',dependencies=[Depends(auth)])
def action_queue(payload:dict,db:Session=Depends(get_db)):
    action_type=payload.get('action_type')
    if not action_type: raise HTTPException(422,'action_type required')
    ev=evaluate_action(action_type,payload.get('payload'))
    if not ev['allowed']:
        audit(db,'policy','action_blocked','action',None,ev['risk_level'],{'action_type':action_type,'reason':ev['reason']}); db.commit()
        raise HTTPException(403,ev['reason'])
    approval_id=None
    if ev['requires_approval']:
        a=Approval(action_type=action_type,summary=payload.get('summary') or f'Approve {action_type}',risk_level=ev['risk_level'],payload=payload.get('payload') or {})
        db.add(a); db.flush(); approval_id=a.id
    q=ActionQueue(deal_id=payload.get('deal_id'),action_type=action_type,payload=payload.get('payload') or {},risk_level=ev['risk_level'],requires_approval=ev['requires_approval'],approval_id=approval_id)
    db.add(q); db.commit(); return {'id':q.id,'approval_id':approval_id,**ev}

@app.get('/owner/approvals',dependencies=[Depends(auth)])
def approvals(db:Session=Depends(get_db)):
    rows=db.scalars(select(Approval).where(Approval.status=='pending').order_by(Approval.requested_at)).all()
    return {'items':[{'id':r.id,'deal_id':r.deal_id,'action_type':r.action_type,'summary':r.summary,'risk_level':r.risk_level,'requested_at':r.requested_at.isoformat()} for r in rows]}

@app.post('/owner/approvals/{approval_id}/decision',dependencies=[Depends(auth)])
def decision(approval_id:str,payload:dict,db:Session=Depends(get_db)):
    d=str(payload.get('decision','')).lower()
    if d not in ('approve','reject'): raise HTTPException(422,'decision must be approve or reject')
    a=db.get(Approval,approval_id)
    if not a or a.status!='pending': raise HTTPException(404,'Pending approval not found')
    a.status='approved' if d=='approve' else 'rejected'; a.decided_at=datetime.now(timezone.utc); a.decided_by='owner_console'
    audit(db,'owner','approval_decided','approval',a.id,a.risk_level,{'decision':a.status}); db.commit(); return {'ok':True,'status':a.status}

@app.get('/owner/weekly-digest',dependencies=[Depends(auth)])
def weekly_digest(db:Session=Depends(get_db)):
    pending=db.scalars(select(Approval).where(Approval.status=='pending').order_by(Approval.requested_at).limit(15)).all()
    deals=db.scalars(select(Deal).order_by(Deal.updated_at.desc()).limit(15)).all()
    lines=['DealOS Weekly Owner Digest','','PENDING APPROVALS']
    if not pending: lines.append('- None')
    for a in pending: lines.append(f'- {a.id} [{a.risk_level.upper()}] {a.summary}')
    lines += ['','ACTIVE / RECENT DEALS']
    if not deals: lines.append('- None yet')
    for d in deals: lines.append(f'- {d.name} | {d.stage} | expected ${float(d.expected_value_usd or 0):,.0f} | risk {d.risk_level}')
    lines += ['','Reply from the authorized owner email with exactly:','APPROVE <approval-id>','or','REJECT <approval-id>']
    return {'subject':'DealOS weekly owner digest','body_text':'\n'.join(lines),'pending_count':len(pending)}

@app.get('/deals',dependencies=[Depends(auth)])
def list_deals(limit:int=50,db:Session=Depends(get_db)):
    rows=db.scalars(select(Deal).order_by(Deal.updated_at.desc()).limit(min(limit,100))).all()
    return {'items':[{'id':d.id,'name':d.name,'lane':d.lane,'stage':d.stage,'expected_value_usd':float(d.expected_value_usd or 0),'recurring_monthly_usd':float(d.recurring_monthly_usd or 0),'probability':float(d.probability or 0),'risk_level':d.risk_level,'next_action':d.next_action} for d in rows]}

@app.get('/deals/{deal_id}',dependencies=[Depends(auth)])
def get_deal(deal_id:str,db:Session=Depends(get_db)):
    d=db.get(Deal,deal_id)
    if not d: raise HTTPException(404)
    return {'id':d.id,'name':d.name,'lane':d.lane,'stage':d.stage,'expected_value_usd':float(d.expected_value_usd or 0),'recurring_monthly_usd':float(d.recurring_monthly_usd or 0),'probability':float(d.probability or 0),'risk_level':d.risk_level,'next_action':d.next_action,'metadata':d.metadata_json}

@app.post('/research/queue',dependencies=[Depends(auth)])
def queue_research(payload:dict,db:Session=Depends(get_db)):
    ev=float(payload.get('expected_value_usd') or 0)
    provider=payload.get('provider') or ('manus' if settings.manus_enabled and ev>=settings.manus_min_expected_value_usd else 'openai')
    r=ResearchJob(deal_id=payload.get('deal_id'),opportunity_id=payload.get('opportunity_id'),provider=provider,prompt=payload.get('prompt') or 'Research this deal and return evidence-backed findings.',structured_schema=payload.get('structured_schema'),expected_value_usd=ev or None)
    db.add(r); db.commit(); return {'id':r.id,'provider':provider}

@app.get('/research/jobs/next',dependencies=[Depends(auth)])
def research_next(provider:str='manus',limit:int=3,db:Session=Depends(get_db)):
    rows=db.scalars(select(ResearchJob).where(ResearchJob.provider==provider,ResearchJob.status=='queued').order_by(ResearchJob.created_at).limit(min(limit,10))).all()
    return {'items':[{'id':r.id,'prompt':r.prompt,'structured_schema':r.structured_schema,'expected_value_usd':float(r.expected_value_usd or 0)} for r in rows]}

@app.post('/research/jobs/{job_id}/submitted',dependencies=[Depends(auth)])
def research_submitted(job_id:str,payload:dict,db:Session=Depends(get_db)):
    r=db.get(ResearchJob,job_id)
    if not r: raise HTTPException(404)
    r.status='submitted'; r.external_task_id=str(payload.get('external_task_id') or payload.get('task_id') or ''); r.submitted_at=datetime.now(timezone.utc)
    db.commit(); return {'ok':True}

@app.post('/research/jobs/{job_id}/complete',dependencies=[Depends(auth)])
def research_complete(job_id:str,payload:dict,db:Session=Depends(get_db)):
    r=db.get(ResearchJob,job_id)
    if not r: raise HTTPException(404)
    r.status='completed'; r.result=payload; r.completed_at=datetime.now(timezone.utc)
    downstream=finalize_research(db,r,payload)
    db.commit(); return {'ok':True,'downstream':downstream}


@app.post('/research/jobs/{job_id}/run-openai',dependencies=[Depends(auth)])
def research_run_openai(job_id:str,db:Session=Depends(get_db)):
    r=db.get(ResearchJob,job_id)
    if not r or r.status!='queued' or r.provider!='openai': raise HTTPException(404,'Queued OpenAI job not found')
    try:
        result=run_research(r.prompt)
    except Exception as e:
        audit(db,'research-worker','research_error','research_job',r.id,'yellow',{'error':str(e)[:500]}); db.commit(); raise HTTPException(502,'Research provider failed')
    r.status='completed'; r.result=result; r.completed_at=datetime.now(timezone.utc)
    downstream=finalize_research(db,r,result)
    audit(db,'research-worker','research_completed','research_job',r.id,'green',{'downstream':downstream}); db.commit()
    return {'ok':True,'result':result,'downstream':downstream}

@app.post('/market/scan/{lane}',dependencies=[Depends(auth)])
def market_scan(lane:str,db:Session=Depends(get_db)):
    if not settings.private_market_scans_enabled: raise HTTPException(403,'PRIVATE_MARKET_SCANS_ENABLED=false')
    if not lane_enabled(lane): return {'lane':lane,'created':0,'opportunity_ids':[],'status':'lane_disabled_or_unconfigured'}
    lane_cfg=lane_config().get('private_market',{}).get(lane,{})
    min_score=float(lane_cfg.get('min_score',70))
    data=scan_lane(lane); created=[]
    for x in data.get('opportunities') or []:
        ext=str(x.get('external_id') or x.get('url') or '')
        if not ext: continue
        if db.scalar(select(Opportunity).where(Opportunity.source=='web_scan',Opportunity.external_id==ext)): continue
        raw={**x,'lane':lane}
        o=Opportunity(source='web_scan',external_id=ext,title=x.get('title') or 'Web opportunity',url=x.get('url'),description=x.get('why_now'),score=x.get('score'),raw=raw)
        db.add(o); db.flush(); created.append(o.id)
        if float(x.get('score') or 0)>=min_score:
            db.add(ResearchJob(opportunity_id=o.id,provider='openai',prompt=f"Research and qualify this {lane} opportunity: {x.get('title')} at {x.get('organization_name')}. Evidence: {x.get('url')}. Signal: {x.get('why_now')}. Identify verified decision makers and the best next action."))
    audit(db,'opportunity-hunter','private_market_scan','lane',lane,'green',{'created':len(created)}); db.commit()
    return {'lane':lane,'created':len(created),'opportunity_ids':created}

@app.post('/enrichment/hunter',dependencies=[Depends(auth)])
def hunter_enrich(payload:dict):
    if not settings.hunter_enabled: raise HTTPException(403,'HUNTER_ENABLED=false')
    domain=payload.get('domain'); first=payload.get('first_name'); last=payload.get('last_name')
    if not all([domain,first,last]): raise HTTPException(422,'domain, first_name and last_name required')
    return {'result':find_email(domain,first,last)}

@app.post('/hooks/manus')
async def manus_hook(request:Request,db:Session=Depends(get_db)):
    body=await request.body(); sig=request.headers.get('X-Webhook-Signature'); ts=request.headers.get('X-Webhook-Timestamp')
    if not sig or not ts: raise HTTPException(401,'Missing Manus signature')
    if not verify_webhook(str(request.url),body,sig,ts): raise HTTPException(401,'Invalid Manus signature')
    payload=await request.json(); task_id=str(payload.get('task_id') or payload.get('taskId') or payload.get('data',{}).get('task_id') or '')
    r=db.scalar(select(ResearchJob).where(ResearchJob.external_task_id==task_id)) if task_id else None
    if r:
        r.status='completed'; r.result=payload; r.completed_at=datetime.now(timezone.utc)
    audit(db,'manus','research_webhook','research_job',r.id if r else None,'green',{'task_id':task_id}); db.commit()
    return {'ok':True}

@app.post('/integrations/stripe/draft-invoice',dependencies=[Depends(auth)])
def stripe_draft_invoice(payload:dict,db:Session=Depends(get_db)):
    if not settings.stripe_enabled: raise HTTPException(403,'STRIPE_ENABLED=false')
    required=['customer_email','amount_usd','description']
    if any(not payload.get(x) for x in required): raise HTTPException(422,'customer_email, amount_usd, description required')
    result=create_draft_invoice(payload['customer_email'],float(payload['amount_usd']),payload['description'],int(payload.get('days_until_due',15)),payload.get('metadata'))
    audit(db,'stripe-adapter','draft_invoice_created','invoice',result.get('invoice_id'),'blue',{'amount_usd':payload['amount_usd'],'customer_email':payload['customer_email']}); db.commit()
    return result

@app.post('/integrations/docusign/template-envelope',dependencies=[Depends(auth)])
def docusign_template_envelope(payload:dict,db:Session=Depends(get_db)):
    if not settings.docusign_enabled: raise HTTPException(403,'DOCUSIGN_ENABLED=false')
    if not payload.get('template_id') or not payload.get('roles'): raise HTTPException(422,'template_id and roles required')
    # This endpoint is an actuator. It should be reached only through an approved DealOS action when status=sent.
    status=payload.get('status','created')
    result=send_template_envelope(payload['template_id'],payload['roles'],payload.get('email_subject','Document for review'),status=status)
    audit(db,'docusign-adapter','envelope_'+status,'envelope',result.get('envelopeId'),'orange' if status=='sent' else 'blue',{'template_id':payload['template_id']}); db.commit()
    return result

@app.post('/hooks/stripe')
async def stripe_hook(request:Request,db:Session=Depends(get_db)):
    if not settings.stripe_enabled: raise HTTPException(403,'STRIPE_ENABLED=false')
    body=await request.body(); sig=request.headers.get('Stripe-Signature')
    if not sig: raise HTTPException(401,'Missing Stripe signature')
    try: event=verify_stripe_webhook(body,sig)
    except Exception: raise HTTPException(401,'Invalid Stripe signature')
    audit(db,'stripe','stripe_webhook','stripe_event',event.get('id'),'green',{'type':event.get('type')}); db.commit()
    return {'ok':True}
