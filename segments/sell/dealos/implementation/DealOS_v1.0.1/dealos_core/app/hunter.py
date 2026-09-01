import httpx
from .config import settings

def find_email(domain:str, first_name:str, last_name:str):
    if not settings.hunter_enabled or not settings.hunter_api_key:
        return None
    params={'domain':domain,'first_name':first_name,'last_name':last_name,'api_key':settings.hunter_api_key}
    r=httpx.get('https://api.hunter.io/v2/email-finder',params=params,timeout=30)
    r.raise_for_status(); data=r.json().get('data') or {}
    email=data.get('email')
    if not email: return None
    return {
      'email':email,'score':data.get('score'),'position':data.get('position'),
      'first_name':data.get('first_name') or first_name,'last_name':data.get('last_name') or last_name,
      'sources':data.get('sources') or [],'verification':data.get('verification')
    }

def verify_email(email:str):
    if not settings.hunter_enabled or not settings.hunter_api_key: return None
    r=httpx.get('https://api.hunter.io/v2/email-verifier',params={'email':email,'api_key':settings.hunter_api_key},timeout=30)
    r.raise_for_status(); return r.json().get('data') or {}
