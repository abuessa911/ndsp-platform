from __future__ import annotations

FORBIDDEN_INTERNAL_FIELDS={"raw_payload","secrets","internal_stacktrace","private_equations"}

def prepare_external_payload(payload):
    clean={k:v for k,v in payload.items() if k not in FORBIDDEN_INTERNAL_FIELDS}
    clean["external_contract_enforced"]=True
    clean["decision_logic_executed_in_gateway"]=False
    return clean
