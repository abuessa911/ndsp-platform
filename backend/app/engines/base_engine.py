def engine_output(name, state, score, confidence, meta=None):
    return {
        "name": name,
        "state": state,
        "score": score,
        "confidence": confidence,
        "meta": meta or {}
    }
