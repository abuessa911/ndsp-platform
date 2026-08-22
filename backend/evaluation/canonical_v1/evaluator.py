from __future__ import annotations

def evaluate_completed_decision(*, decision_id, decision_created_at,
                                outcome_observed_at, metrics):
    return {
        "decision_id":decision_id,
        "decision_created_at":decision_created_at,
        "outcome_observed_at":outcome_observed_at,
        "metrics":dict(metrics),
        "post_decision_only":True,
        "historical_decision_mutated":False,
    }
