from __future__ import annotations
import pathlib, json, datetime, uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]

def propose(title,rationale,changes,evidence=None):
    pid=str(uuid.uuid4()); d=ROOT/'proposals'/pid; d.mkdir(parents=True,exist_ok=True)
    record={'proposal_id':pid,'title':title,'rationale':rationale,'changes':changes,'evidence':evidence or [],'state':'QUARANTINED','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'promotion_rule':'tests + policy + authorized review; production core is never silently self-rewritten'}
    (d/'proposal.json').write_text(json.dumps(record,indent=2)+'\n'); return record
