import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from app.policy import evaluate_action

def test_sign_requires_owner():
    x=evaluate_action('signature',{})
    assert x['requires_approval'] is True

def test_research_is_green():
    x=evaluate_action('research',{})
    assert x['allowed'] is True and x['requires_approval'] is False
