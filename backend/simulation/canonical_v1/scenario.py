from __future__ import annotations

def run_scenario(*, base_decision_id, assumptions, computed_outputs):
    return {
        "base_decision_id":base_decision_id,
        "assumptions":dict(assumptions),
        "outputs":dict(computed_outputs),
        "state":"SIMULATION_ONLY",
        "decision_publish_allowed":False,
        "alert_publish_allowed":False,
    }
