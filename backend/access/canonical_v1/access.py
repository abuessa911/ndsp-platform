from __future__ import annotations

ROLE_ORDER={"beginner":1,"professional":2,"admin":3,"owner":4}

def can_view(*, role, minimum_role):
    return ROLE_ORDER.get(role,0)>=ROLE_ORDER.get(minimum_role,999)

def filter_experience(payload, *, role, experience_mode):
    return {
        "role":role,
        "experience_mode":experience_mode,
        "decision_id":payload.get("decision_id"),
        "single_truth_state":payload.get("single_truth_state"),
        "advanced_evidence_visible":can_view(role=role,minimum_role="professional"),
        "labs_visible":can_view(role=role,minimum_role="admin"),
        "owner_override_visible":role=="owner",
        "changes_decision":False,
    }
