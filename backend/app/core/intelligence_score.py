from app.services.trap_probability_engine import trap_probability
from app.services.intent_strength_engine import intent_strength
from app.services.hidden_pressure_engine import hidden_pressure


def amplify(data):
    # 💀 تضخيم الإشارات الضعيفة
    if data.get("rsi", 50) > 65:
        data["divergence"] = "hidden"
        data["zone"] = "supply"

    elif data.get("rsi", 50) < 35:
        data["divergence"] = "hidden"
        data["zone"] = "demand"

    if data.get("momentum") == "weak":
        data["momentum"] = "strong"

    return data


def compute_intelligence(data):

    data = amplify(data)

    trap = trap_probability(data)
    intent = intent_strength(data)
    hidden = hidden_pressure(data)

    total_score = (
        trap["trap_probability"] * 0.3 +
        intent["intent_score"] * 0.4 +
        hidden["hidden_score"] * 0.3
    )

    return {
        "trap": trap,
        "intent": intent,
        "hidden": hidden,
        "intelligence_score": round(total_score, 2)
    }
