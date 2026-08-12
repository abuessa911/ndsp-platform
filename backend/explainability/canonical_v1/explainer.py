from __future__ import annotations

def explain_decision(decision, *, audience="beginner"):
    allowed={"beginner","professional","admin","share"}
    if audience not in allowed:
        raise ValueError("unsupported audience")
    readiness=decision.get("decision_readiness") or {}
    direction=(decision.get("investment_direction") or {}).get("direction") or               (decision.get("weekly_tdl") or {}).get("direction") or "unknown"
    return {
        "audience":audience,
        "direction":direction,
        "state":decision.get("single_truth_state"),
        "reason_code":readiness.get("reason_code"),
        "evidence_reference_required":True,
        "changes_decision":False,
    }
