########################################
# 💀 timing_model ENGINE (TEMP VERSION)
########################################

def calculate_tdl(market: dict):

    """
    timing_model = Trend Direction Logic
    (نسخة مؤقتة تعتمد على السعر فقط)
    """

    price = market.get("price", 0)

    if price == 0:
        return {
            "tdl_lm_score": 50,
            "tdl_s_score": 50,
            "dominant": "NEUTRAL"
        }

    ########################################
    # 📊 SIMPLE LOGIC (مؤقت)
    ########################################
    # إذا السعر كبير = سوق قوي (fake logic حالياً)
    if price > 50000:
        lm = 70
        sm = 30
        dominant = "LM"
    else:
        lm = 40
        sm = 60
        dominant = "SM"

    return {
        "tdl_lm_score": lm,
        "tdl_s_score": sm,
        "dominant": dominant
    }
