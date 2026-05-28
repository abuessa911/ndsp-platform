def apply_failsafe(data: dict):

    decision = data.get("decision", {})
    confidence = decision.get("confidence", 0)

    # لو الثقة ضعيفة جدًا → no_trade
    if confidence < 0.2:
        data["decision"]["state"] = "no_trade"
        data["risk"]["state"] = "blocked"
        data["risk"]["reason"] = "low_confidence"

    return data
