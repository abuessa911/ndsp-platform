import time

def apply_feature_gate(data: dict, user: dict):

    plan = user.get("plan", "free")

    ########################################
    # 💰 FREE PLAN LIMITATIONS
    ########################################
    if plan == "free":

        if "decision" in data:

            confidence = data["decision"].get("confidence", 0)

            # 🔥 apply reduction
            confidence *= 0.7

            # 💀 FIX: round بعد التعديل
            confidence = round(confidence, 2)

            data["decision"]["confidence"] = confidence

        time.sleep(2)

    ########################################
    # 💰 PRO PLAN
    ########################################
    elif plan == "pro":
        time.sleep(0.5)

    ########################################
    # 💰 ELITE PLAN
    ########################################
    else:
        pass

    return data
