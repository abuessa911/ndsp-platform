def generate_explanation(result):

    engines = result.get("engines", [])
    confidence = result.get("confidence", 0)

    bullish = 0
    bearish = 0
    neutral = 0

    for e in engines:
        if e["state"] == "bullish":
            bullish += 1
        elif e["state"] == "bearish":
            bearish += 1
        else:
            neutral += 1

    explanation_en = []
    explanation_ar = []

    # 🎯 Dominance logic
    if bullish > bearish:
        explanation_en.append("Bullish pressure slightly dominates")
        explanation_ar.append("الضغط الشرائي مسيطر بشكل طفيف")
    elif bearish > bullish:
        explanation_en.append("Bearish pressure slightly dominates")
        explanation_ar.append("الضغط البيعي مسيطر بشكل طفيف")
    else:
        explanation_en.append("Balanced market with conflicting signals")
        explanation_ar.append("السوق متوازن مع تضارب في الإشارات")

    # 🧠 Neutral context
    if neutral >= 2:
        explanation_en.append("Lack of strong directional conviction")
        explanation_ar.append("لا يوجد اتجاه قوي واضح")

    # 🧠 Confidence layer
    if confidence >= 0.85:
        strength = "strong"
        strength_ar = "قوي"
    elif confidence >= 0.6:
        strength = "moderate"
        strength_ar = "متوسط"
    else:
        strength = "weak"
        strength_ar = "ضعيف"

    return {
        "narrative_en": " | ".join(explanation_en),
        "narrative_ar": " | ".join(explanation_ar),
        "confidence_level": strength,
        "confidence_level_ar": strength_ar
    }
