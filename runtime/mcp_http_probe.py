from __future__ import annotations
import urllib.request, json, os, datetime
PROTOCOL='2026-07-28'

def _post(url,method,params=None,token=None,request_id=1):
    body={'jsonrpc':'2.0','id':request_id,'method':method,'params':params or {},'_meta':{'io.modelcontextprotocol/clientInfo':{'name':'faos-capability-assimilator','version':'1.2.0'}}}
    headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream','MCP-Protocol-Version':PROTOCOL,'Mcp-Method':method}
    if token: headers['Authorization']='Bearer '+token
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(req,timeout=30) as r:
        data=r.read().decode(); ctype=(r.headers.get('Content-Type') or '').lower()
        if 'text/event-stream' in ctype or data.lstrip().startswith('event:') or data.lstrip().startswith('data:'):
            payloads=[]
            for line in data.splitlines():
                if line.startswith('data:'):
                    raw=line[5:].strip()
                    if raw and raw!='[DONE]': payloads.append(json.loads(raw))
            if not payloads: raise RuntimeError('empty MCP event-stream response')
            # For request/response RPCs use the last JSON-RPC response event.
            return payloads[-1]
        return json.loads(data)

def _result(x):
    if 'error' in x: raise RuntimeError(x['error'])
    return x.get('result',{})

def _pages(url,method,key,token,max_pages=50):
    out=[]; cursor=None
    for i in range(max_pages):
        params={} if cursor is None else {'cursor':cursor}; res=_result(_post(url,method,params,token,i+10)); out.extend(res.get(key,[]) or []); cursor=res.get('nextCursor')
        if not cursor: break
    return out

def discover(url,connector_id,token_env=None):
    token=os.getenv(token_env) if token_env else None
    try: disc=_result(_post(url,'server/discover',{},token,1))
    except Exception: disc={}
    return {'connector_id':connector_id,'discovery_source':{'transport':'http','url':url,'token_env':token_env},'protocol_version':PROTOCOL,'server_info':disc.get('serverInfo',{}),'server_capabilities':disc.get('capabilities',{}),'tools':_pages(url,'tools/list','tools',token),'resources':_pages(url,'resources/list','resources',token),'resource_templates':_pages(url,'resources/templates/list','resourceTemplates',token),'prompts':_pages(url,'prompts/list','prompts',token),'discovered_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
