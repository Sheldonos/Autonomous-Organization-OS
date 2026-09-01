from pathlib import Path
import yaml, os

POLICY_DIR=Path(os.getenv('POLICY_DIR','/app/policies'))

def load_policy(name):
    p=POLICY_DIR/f'{name}.yaml'
    if not p.exists():
        p=Path(__file__).resolve().parents[2]/'policies'/f'{name}.yaml'
    if not p.exists(): return {}
    return yaml.safe_load(p.read_text()) or {}

def evaluate_action(action_type:str, payload:dict|None=None):
    payload=payload or {}
    autonomy=load_policy('autonomy')
    compliance=load_policy('compliance')
    lower=action_type.lower()
    red=set(autonomy.get('levels',{}).get('red',{}).get('triggers',[]))
    orange=set(autonomy.get('levels',{}).get('orange',{}).get('triggers',[]))
    if lower in red:
        return {'risk_level':'red','allowed':False,'requires_approval':False,'reason':'red_stop'}
    if lower in orange or any(k in lower for k in ['sign','binding','bank_change','payout','refund']):
        return {'risk_level':'orange','allowed':True,'requires_approval':True,'reason':'owner_gate'}
    if lower=='federal_contingent_fee' and not compliance.get('federal',{}).get('contingent_fee_enabled',False):
        return {'risk_level':'red','allowed':False,'requires_approval':False,'reason':'federal_contingent_fee_disabled'}
    return {'risk_level':'green','allowed':True,'requires_approval':False,'reason':'within_policy'}
