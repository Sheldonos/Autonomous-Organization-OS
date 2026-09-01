from __future__ import annotations
DENY={'unrestricted_money_movement','binding_signature_without_authority','credential_exfiltration','bypass_access_control','fabricate_claims','delete_authoritative_records_without_recovery'}
APPROVAL={'external_message','public_publish','calendar_commitment','production_deploy','contract_transmission','purchase','spend','permission_change','security_control_change','employment_decision','legal_filing','signature','money_movement'}
ALLOW={'research','analysis','draft','classify','simulate','local_test','workspace_write','read_authorized_data','generate_internal_artifact'}
def evaluate(action_type, preauthorized=False, adapter_verified=False, readback_supported=False):
    a=action_type.strip().lower()
    if a in DENY: return {'decision':'DENY','reason':'Globally prohibited as an unrestricted action.'}
    if a in ALLOW: return {'decision':'ALLOW','reason':'Low-risk internal action within authorized scope.'}
    if a in APPROVAL:
        if preauthorized and adapter_verified and readback_supported and a not in {'signature','money_movement','employment_decision','legal_filing'}:
            return {'decision':'ALLOW_WITH_GUARDRAILS','reason':'Narrowly pre-authorized action with verified adapter and read-back.'}
        return {'decision':'REQUIRE_APPROVAL','reason':'Consequential action requires explicit authority/approval.'}
    return {'decision':'REQUIRE_POLICY_REVIEW','reason':'Action type is not classified; fail closed.'}
