import os
from dataclasses import dataclass

def env(name, default=None, required=False):
    v=os.getenv(name, default)
    if required and (v is None or str(v).startswith('REQUIRED')):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return v

def b(name, default=False):
    return str(os.getenv(name, str(default))).lower() in {'1','true','yes','on'}

def i(name, default):
    return int(os.getenv(name, default))

def f(name, default):
    return float(os.getenv(name, default))

@dataclass(frozen=True)
class Settings:
    owner_email: str = env('OWNER_EMAIL','owner@example.invalid')
    dealos_api_key: str = env('DEALOS_API_KEY','dev-only-change-me')
    database_url: str = env('DATABASE_URL','sqlite:///./dealos.db')
    openai_api_key: str|None = env('OPENAI_API_KEY')
    openai_fast_model: str = env('OPENAI_FAST_MODEL','gpt-5.6-luna')
    openai_standard_model: str = env('OPENAI_STANDARD_MODEL','gpt-5.6-terra')
    openai_high_model: str = env('OPENAI_HIGH_MODEL','gpt-5.6-sol')
    openai_daily_budget_usd: float = f('OPENAI_DAILY_BUDGET_USD',15)
    openai_monthly_budget_usd: float = f('OPENAI_MONTHLY_BUDGET_USD',300)
    openai_web_search_cost_per_call_usd: float = f('OPENAI_WEB_SEARCH_COST_PER_CALL_USD',0.01)
    manus_enabled: bool = b('MANUS_ENABLED',False)
    manus_api_key: str|None = env('MANUS_API_KEY')
    manus_base_url: str = env('MANUS_BASE_URL','https://api.manus.ai')
    manus_profile: str = env('MANUS_PROFILE','manus-1.6-lite')
    manus_min_expected_value_usd: float = f('MANUS_MIN_EXPECTED_VALUE_USD',25000)
    hunter_enabled: bool = b('HUNTER_ENABLED',False)
    hunter_api_key: str|None = env('HUNTER_API_KEY')
    hunter_min_opportunity_score: float = f('HUNTER_MIN_OPPORTUNITY_SCORE',70)
    outreach_autonomous_enabled: bool = b('OUTREACH_AUTONOMOUS_ENABLED',False)
    private_market_scans_enabled: bool = b('PRIVATE_MARKET_SCANS_ENABLED',False)
    federal_contingent_fee_enabled: bool = b('FEDERAL_CONTINGENT_FEE_ENABLED',False)
    stripe_enabled: bool = b('STRIPE_ENABLED',False)
    stripe_secret_key: str|None = env('STRIPE_SECRET_KEY')
    stripe_webhook_secret: str|None = env('STRIPE_WEBHOOK_SECRET')
    stripe_default_currency: str = env('STRIPE_DEFAULT_CURRENCY','usd')
    docusign_enabled: bool = b('DOCUSIGN_ENABLED',False)
    docusign_base_url: str = env('DOCUSIGN_BASE_URL','https://demo.docusign.net/restapi')
    docusign_oauth_base_url: str = env('DOCUSIGN_OAUTH_BASE_URL','https://account-d.docusign.com')
    docusign_integration_key: str|None = env('DOCUSIGN_INTEGRATION_KEY')
    docusign_user_id: str|None = env('DOCUSIGN_USER_ID')
    docusign_account_id: str|None = env('DOCUSIGN_ACCOUNT_ID')
    docusign_private_key_path: str = env('DOCUSIGN_PRIVATE_KEY_PATH','/run/secrets/docusign_private_key.pem')


settings=Settings()
