from __future__ import annotations
from typing import Any

def evaluate_data_quality(*, asset_identity, source_identity, contract_status,
                          freshness_status, completeness=True, integrity=True):
    failures=[]
    checks={
        "asset_identity": bool(asset_identity.get("ok")),
        "source_identity": bool(source_identity.get("ok")),
        "contract": bool(contract_status.get("ok")),
        "freshness": freshness_status in {"CURRENT","EXPECTED_NOT_YET_DUE"},
        "completeness": bool(completeness),
        "integrity": bool(integrity),
    }
    failures=[k for k,v in checks.items() if not v]
    return {
        "status":"ACCEPTED" if not failures else "DATA_BLOCKED",
        "decision_use_allowed":not failures,
        "monitoring_use_allowed":True,
        "checks":checks,
        "failures":failures,
    }
