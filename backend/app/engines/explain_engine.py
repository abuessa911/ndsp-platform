def build_explanation(decision_data):

    direction = decision_data.get("decision", {}).get("direction", "neutral")
    confidence = decision_data.get("confidence", 0)
    momentum = decision_data.get("states", {}).get("momentum", {})

    signal = momentum.get("signal", "neutral")
    state = momentum.get("state", "unknown")

    ########################################
    # 💀 CORE LOGIC
    ########################################

    if direction == "bullish":
        summary = "السوق يظهر قوة شرائية واضحة"
        reason = "الزخم إيجابي"
    elif direction == "bearish":
        summary = "السوق يظهر ضعف وضغط بيعي"
        reason = "الزخم سلبي"
    else:
        summary = "السوق في حالة توازن"
        reason = "لا يوجد زخم واضح"

    ########################################
    # 💀 STRENGTH
    ########################################
    if confidence >= 0.8:
        strength = "قوية"
    elif confidence >= 0.6:
        strength = "متوسطة"
    else:
        strength = "ضعيفة"

    ########################################
    # 💀 FINAL OUTPUT
    ########################################
    return {
        "summary": summary,
        "reason": reason,
        "strength": strength,
        "confidence": confidence,
        "momentum_state": state,
        "signal": signal
    }
