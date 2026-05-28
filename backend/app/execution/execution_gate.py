from app.execution.mode_config import get_mode

def allow_trade(decision, entry, conflict, black):

    mode = get_mode()

    ########################################
    # 💀 SAFE MODE (STRICT)
    ########################################
    if mode == "SAFE":

        if decision.get("confidence_type") not in ["medium", "strong"]:
            return False, "low_confidence"

        if entry.get("entry_score", 0) < 2:
            return False, "weak_entry"

        if conflict.get("score", 0) > 0:
            return False, "conflict_detected"

        if black.get("trap"):
            return False, "blacklayer_block"

    ########################################
    # ⚡ AGGRESSIVE MODE
    ########################################
    if mode == "AGGRESSIVE":

        if decision.get("confidence_type") == "low":
            return False, "too_weak"

        if entry.get("entry_score", 0) < 1:
            return False, "very_weak_entry"

        if black.get("trap"):
            return False, "blacklayer_block"

    ########################################
    # 🚫 INVALID
    ########################################
    if decision.get("direction") in ["wait", "no_trade"]:
        return False, "invalid_direction"

    return True, "approved"
