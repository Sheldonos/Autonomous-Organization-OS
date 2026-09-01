from .config import settings
from .profile import business_profile, lane_offer, lane_enabled
from .usage import assert_openai_budget, record_openai_usage

def draft_first_touch(lane:str, contact:dict, research:dict):
    if not settings.outreach_autonomous_enabled or not lane_enabled(lane): return None
    profile=business_profile(); offer=lane_offer(lane)
    if not settings.openai_api_key: return None
    from openai import OpenAI
    assert_openai_budget(0.02)
    client=OpenAI(api_key=settings.openai_api_key)
    facts=research.get('verified_facts') or []
    facts='\n'.join(f"- {x.get('fact')} ({x.get('source_url')})" for x in facts[:5])
    prompt=(f"Write a <=90-word first-touch B2B email.\\n"
            f"Sender: {profile.get('business',{}).get('sender_name')} / {profile.get('business',{}).get('brand_name')}\\n"
            f"Recipient: {contact.get('name')} | {contact.get('title')}\\n"
            f"Approved offer: {offer.get('offer_name')} — {offer.get('one_sentence_value')}\\n"
            f"CTA: {offer.get('call_to_action')}\\nVerified context:\n{facts}\\n"
            f"Research angle: {research.get('recommended_outreach_angle')}\\n"
            "Rules: factual, low-pressure, no fake familiarity, no unsupported metrics, no invented customers/certifications, one CTA, no tracking gimmicks.")
    r=client.responses.create(model=settings.openai_fast_model,input=prompt)
    record_openai_usage(settings.openai_fast_model,'outreach_draft',r)
    org=research.get('organization_name') or 'your team'
    return {'subject':f'Quick question about {org}'[:120], 'body':r.output_text.strip()}
