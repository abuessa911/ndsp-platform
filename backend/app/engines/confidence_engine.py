# /opt/empire-core/backend/app/core/confidence_engine.py

########################################
# 💀 CONFIDENCE ENGINE (REAL)
########################################

def evaluate_confidence(score: float):

    ########################################
    # 🎯 NORMALIZE
    ########################################
    if score > 1:
        score = score / 100

    if score < 0:
        score = 0

    if score > 1:
        score = 1

    ########################################
    # 🧠 CLASSIFY
    ########################################
    confidence_type = classify_confidence(score)

    ########################################
    # 📦 OUTPUT
    ########################################
    return {
        "score": score,                # 0 → 1
        "confidence": score,
        "confidence_type": confidence_type
    }


########################################
# 📊 TYPE CLASSIFICATION
########################################

def classify_confidence(conf):

    if conf >= 0.8:
        return "strong"

    elif conf >= 0.65:
        return "medium"

    elif conf >= 0.45:
        return "weak"

    else:
        return "very_weak"


########################################
# 🔁 BACKWARD SUPPORT
########################################

def classify(conf):
    return classify_confidence(conf)
