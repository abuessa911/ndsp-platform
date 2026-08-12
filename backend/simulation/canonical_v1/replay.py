from __future__ import annotations
from datetime import datetime

def validate_as_of_inputs(*, as_of, evidence_timestamps):
    boundary=datetime.fromisoformat(as_of.replace("Z","+00:00"))
    future=[x for x in evidence_timestamps if datetime.fromisoformat(x.replace("Z","+00:00"))>boundary]
    return {
        "status":"REPLAY_READY" if not future else "LOOK_AHEAD_BIAS_BLOCKED",
        "simulation_only":True,
        "decision_publish_allowed":False,
        "future_evidence":future,
    }
