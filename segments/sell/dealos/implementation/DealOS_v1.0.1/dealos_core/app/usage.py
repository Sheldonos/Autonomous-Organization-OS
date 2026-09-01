from datetime import datetime, timezone
from sqlalchemy import select, func
from .db import SessionLocal
from .models import ModelUsage
from .config import settings

# Conservative short-context estimates per 1M tokens. Keep these at or above the
# current rate you actually pay; over-estimating is safer than runaway spend.
MODEL_PRICES = {
    'gpt-5.6-luna': (1.00, 6.00),
    'gpt-5.6-terra': (2.50, 15.00),
    'gpt-5.6-sol': (5.00, 30.00),
}

def _period_totals(db):
    now=datetime.now(timezone.utc)
    day=now.replace(hour=0,minute=0,second=0,microsecond=0)
    month=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    daily=float(db.scalar(select(func.coalesce(func.sum(ModelUsage.estimated_cost_usd),0)).where(ModelUsage.created_at>=day)) or 0)
    monthly=float(db.scalar(select(func.coalesce(func.sum(ModelUsage.estimated_cost_usd),0)).where(ModelUsage.created_at>=month)) or 0)
    return daily,monthly

def assert_openai_budget(reserve_usd:float=0.05):
    with SessionLocal() as db:
        daily,monthly=_period_totals(db)
    if daily + reserve_usd > settings.openai_daily_budget_usd:
        raise RuntimeError(f'OpenAI daily budget reached: ${daily:.2f}/${settings.openai_daily_budget_usd:.2f}')
    if monthly + reserve_usd > settings.openai_monthly_budget_usd:
        raise RuntimeError(f'OpenAI monthly budget reached: ${monthly:.2f}/${settings.openai_monthly_budget_usd:.2f}')

def _tokens(response, key):
    usage=getattr(response,'usage',None)
    if usage is None: return 0
    v=getattr(usage,key,None)
    if v is None and isinstance(usage,dict): v=usage.get(key)
    return int(v or 0)

def record_openai_usage(model:str, task_type:str, response, web_search_calls:int=0):
    it=_tokens(response,'input_tokens')
    ot=_tokens(response,'output_tokens')
    pin,pout=MODEL_PRICES.get(model, MODEL_PRICES['gpt-5.6-sol'])
    est=(it/1_000_000)*pin + (ot/1_000_000)*pout + web_search_calls*settings.openai_web_search_cost_per_call_usd
    with SessionLocal() as db:
        db.add(ModelUsage(provider='openai',model=model,task_type=task_type,input_tokens=it,output_tokens=ot,estimated_cost_usd=est))
        db.commit()
    return est
