from pathlib import Path
import time, httpx, jwt
from .config import settings

def _token():
    required=[settings.docusign_integration_key,settings.docusign_user_id]
    if not settings.docusign_enabled or not all(required): raise RuntimeError('DocuSign disabled or incomplete')
    key=Path(settings.docusign_private_key_path).read_text()
    aud=settings.docusign_oauth_base_url.replace('https://','').rstrip('/')
    now=int(time.time())
    assertion=jwt.encode({'iss':settings.docusign_integration_key,'sub':settings.docusign_user_id,'aud':aud,'iat':now,'exp':now+3600,'scope':'signature impersonation'},key,algorithm='RS256')
    r=httpx.post(f'{settings.docusign_oauth_base_url}/oauth/token',data={'grant_type':'urn:ietf:params:oauth:grant-type:jwt-bearer','assertion':assertion},timeout=30)
    r.raise_for_status(); return r.json()['access_token']

def send_template_envelope(template_id:str, roles:list[dict], email_subject:str, status:str='sent'):
    if status not in {'created','sent'}: raise ValueError('status must be created or sent')
    if not settings.docusign_account_id: raise RuntimeError('DOCUSIGN_ACCOUNT_ID missing')
    body={'templateId':template_id,'templateRoles':roles,'emailSubject':email_subject,'status':status}
    r=httpx.post(f"{settings.docusign_base_url}/v2.1/accounts/{settings.docusign_account_id}/envelopes",headers={'Authorization':f'Bearer {_token()}','Content-Type':'application/json'},json=body,timeout=45)
    r.raise_for_status(); return r.json()
