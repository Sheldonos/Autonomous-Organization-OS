from pathlib import Path
import os, yaml

def load_yaml(name, default=None):
    candidates=[Path(os.getenv('CONFIG_DIR','/app/config'))/name, Path(__file__).resolve().parents[2]/'config'/name]
    for p in candidates:
        if p.exists(): return yaml.safe_load(p.read_text()) or (default or {})
    return default or {}

def business_profile():
    return load_yaml('business_profile.yaml', load_yaml('business_profile.example.yaml',{}))

def lanes(): return load_yaml('lanes.yaml',{})

def lane_offer(lane):
    return business_profile().get('lanes',{}).get(lane,{})

def lane_enabled(lane):
    x=lane_offer(lane)
    return bool(x.get('enabled')) and 'REQUIRED_USER_CONFIG' not in str(x)

def account_registry(): return load_yaml('account_registry.yaml', load_yaml('account_registry.example.yaml',{}))
