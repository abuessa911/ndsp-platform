def apply_quality_logic(base_confidence: float, effects: dict, direction: str):
    score = base_confidence
    applied = []
    if effects.get('golden_alignment'):
        score += 15
        applied.append("Golden_Alignment_Boost")
    if effects.get('high_volatility_anomaly'):
        score -= 25
        applied.append("Black_Layer_Penalty")
    
    final_score = max(0, min(score, 100))
    grade = "A" if final_score >= 85 else "B" if final_score >= 70 else "C" if final_score >= 50 else "D"
    return final_score, applied, grade
