import base64, hashlib, httpx
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from .config import settings

_public_key_cache=None

def create_task(message:str, structured_schema:dict|None=None):
    if not settings.manus_enabled or not settings.manus_api_key:
        raise RuntimeError('Manus is disabled or missing API key')
    body={
      'message':{'content':message},
      'agent_profile':settings.manus_profile,
      'interactive_mode':False,
      'hide_in_task_list':True,
      'share_visibility':'private'
    }
    if structured_schema: body['structured_output_schema']=structured_schema
    r=httpx.post(f'{settings.manus_base_url}/v2/task.create',headers={'x-manus-api-key':settings.manus_api_key},json=body,timeout=60)
    r.raise_for_status(); return r.json()

def get_public_key():
    global _public_key_cache
    if _public_key_cache: return _public_key_cache
    headers={'x-manus-api-key':settings.manus_api_key} if settings.manus_api_key else {}
    r=httpx.get(f'{settings.manus_base_url}/v2/webhook.publicKey',headers=headers,timeout=30)
    r.raise_for_status(); data=r.json()
    pem=data.get('public_key') or data.get('publicKey') or data.get('data',{}).get('public_key')
    if not pem: raise RuntimeError('Manus public key missing from response')
    _public_key_cache=serialization.load_pem_public_key(pem.encode())
    return _public_key_cache

def verify_webhook(url:str, body:bytes, signature_b64:str, timestamp:str):
    import time
    if abs(time.time()-float(timestamp)) > 300: return False
    digest=hashlib.sha256(body).hexdigest()
    signed=f'{timestamp}.{url}.{digest}'.encode()
    try:
        get_public_key().verify(base64.b64decode(signature_b64),signed,padding.PKCS1v15(),hashes.SHA256())
        return True
    except Exception:
        return False
