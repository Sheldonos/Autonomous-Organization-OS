from sqlalchemy import select
from .models import ResearchJob, Opportunity, Deal, Organization, Contact, Outbox, Suppression, AuditEvent
from .config import settings
from .hunter import find_email
from .outreach import draft_first_touch

def finalize_research(db, job:ResearchJob, result:dict):
    score=float(result.get('qualification_score') or 0)
    if score < 65: return {'qualified':False,'score':score}
    opp=db.get(Opportunity,job.opportunity_id) if job.opportunity_id else None
    lane=(opp.raw or {}).get('lane') if opp else None
    if not lane: lane='federal' if opp and opp.source=='sam' else 'ai_transformation'
    name=result.get('organization_name') or (opp.title if opp else 'Qualified opportunity')
    domain=(result.get('company_domain') or '').lower().strip() or None
    org=db.scalar(select(Organization).where(Organization.domain==domain)) if domain else None
    if not org:
        org=Organization(name=name,domain=domain,type='prospect')
        db.add(org); db.flush()
    deal=Deal(opportunity_id=opp.id if opp else None,name=f'{name} — {lane}',lane=lane,stage='qualified',expected_value_usd=job.expected_value_usd,probability=min(score/100,0.95),risk_level='green',next_action='identify and contact best-fit decision maker',metadata_json={'research':result})
    db.add(deal); db.flush()
    selected=None
    for dm in result.get('decision_makers') or []:
        email=(dm.get('email') or '').lower().strip() or None
        if not email and settings.hunter_enabled and domain and dm.get('first_name') and dm.get('last_name') and score>=settings.hunter_min_opportunity_score:
            try:
                found=find_email(domain,dm['first_name'],dm['last_name']); email=(found or {}).get('email')
            except Exception:
                email=None
        if email:
            if db.scalar(select(Suppression).where(Suppression.email==email.lower())): continue
            c=db.scalar(select(Contact).where(Contact.email==email.lower()))
            if not c:
                c=Contact(organization_id=org.id,email=email.lower(),name=dm.get('full_name') or f"{dm.get('first_name') or ''} {dm.get('last_name') or ''}".strip(),title=dm.get('title'),source='research/hunter',metadata_json={'source_url':dm.get('source_url')})
                db.add(c); db.flush()
            selected={'email':c.email,'name':c.name,'title':c.title}; break
    if selected:
        draft=draft_first_touch(lane,selected,result)
        if draft:
            db.add(Outbox(deal_id=deal.id,to_email=selected['email'],subject=draft['subject'],body_text=draft['body'],risk_level='green',metadata_json={'purpose':'first_touch','lane':lane}))
            deal.stage='outreach_queued'; deal.next_action='await response'
    db.add(AuditEvent(actor='intelligence-agent',event_type='research_finalized',entity_type='deal',entity_id=deal.id,risk_level='green',payload={'score':score,'contact_found':bool(selected),'outreach_queued':deal.stage=='outreach_queued'}))
    return {'qualified':True,'score':score,'deal_id':deal.id,'contact_found':bool(selected),'outreach_queued':deal.stage=='outreach_queued'}
