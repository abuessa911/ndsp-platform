# /opt/empire-core/backend/app/core/black_layer.py

def evaluate_black_layer(momentum, liquidity, volatility, zones):
    """
    💀 NDSP LAYER 12: risk shield (Risk Escalation Authority)
    [GOVERNANCE V4.1 ENFORCED]
    - لا يحق لهذه الطبقة اختيار أو تغيير الاتجاه بأي شكل.
    - وظيفتها الحصرية: خفض الثقة (Confidence Penalty) أو رفع حالة الخطر (Risk State).
    """

    ########################################
    # 🧠 INPUT NORMALIZATION
    ########################################

    m_strength = float(momentum.get("strength", 0.0))  # 0 → 1
    m_context = momentum.get("context", "weak")

    liq_state = liquidity.get("state", "neutral")
    vol_state = volatility.get("state", "normal")
    zone_state = zones.get("state", "undefined")

    ########################################
    # 💣 SCORING SYSTEM (ABSTRACTED)
    ########################################

    continuation = 0.0
    risk = 0.0
    reasons = []

    ########################################
    # 💣 MOMENTUM CONTRIBUTION
    ########################################

    if m_strength > 0.6:
        continuation += 0.4
        reasons.append("strong_momentum_alignment")
    elif m_strength > 0.3:
        continuation += 0.2
        reasons.append("moderate_momentum")
    else:
        risk += 0.3
        reasons.append("weak_structure")

    ########################################
    # 💣 LIQUIDITY & VOLATILITY
    ########################################

    if liq_state in ["sweep_up", "sweep_down"]:
        continuation += 0.2
        reasons.append("liquidity_event_detected")

    if vol_state == "high" and m_strength < 0.4:
        risk += 0.3
        reasons.append("unstable_volatility")

    if zone_state in ["resistance", "support"]:
        risk += 0.2
        reasons.append("zone_pressure")

    ########################################
    # 💣 FINAL SCORE
    ########################################

    raw_score = continuation - risk
    raw_score = max(0.0, min(raw_score, 1.0))

    ########################################
    # 💣 V4.1 STATE & PENALTY DERIVATION
    ########################################

    # تحديد حالة الطبقة السوداء والعقوبات بناءً على المعمارية الجديدة
    confidence_penalty = 0
    
    if raw_score > 0.65:
        state = "clear"
    elif raw_score > 0.45:
        state = "caution"
        confidence_penalty = 10 # عقوبة طفيفة على الثقة
    else:
        state = "protective_block"
        confidence_penalty = 25 # عقوبة قاسية يتم سحبها من Layer 13

    regime = "trending" if m_strength > 0.5 else "ranging"

    ########################################
    # 💀 OUTPUT (V4.1 CONTRACT COMPLIANT)
    ########################################

    return {
        "layer_metadata": {
            "layer_name": "Layer 12: risk shield",
            "authority": "Risk Escalation Authority",
            "version": "4.1"
        },
        # Legacy fields for backward compatibility
        "state": state,
        "score": round(raw_score, 2),
        "context": "computed_fusion",
        "regime": regime,
        "reason": reasons,
        
        # V4.1 Strict Output Fields
        "black_layer_state": state,
        "black_layer_penalty": confidence_penalty, # Consumed by Layer 13 (Decision Quality Stack)
        "risk_effect": "high" if state == "protective_block" else "normal"
    }
