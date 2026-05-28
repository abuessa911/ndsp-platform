# ================================
# COMPLIANCE LAYER (FIXED)
# ================================

def enforce(decision: dict):

    if not decision:
        return {
            "status": "error",
            "message": "invalid decision"
        }

    state = decision.get("decision", {}).get("state", "neutral")
    confidence = decision.get("decision", {}).get("confidence", 0)

    # 🚨 Fail-safe rules
    if confidence < 0.2:
        decision["decision"]["state"] = "neutral"

    # 🔐 Compliance rules
    if state not in ["bullish", "bearish", "neutral"]:
        decision["decision"]["state"] = "neutral"

    decision["compliance"] = {
        "status": "approved"
    }

    return decision
