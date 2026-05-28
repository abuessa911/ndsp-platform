def evaluate_confidence(score: float):

    if score < 0:
        score = 0

    if score > 1:
        score = 1

    return {
        "score": score,
        "confidence": score,
        "confidence_type": "normal"
    }
