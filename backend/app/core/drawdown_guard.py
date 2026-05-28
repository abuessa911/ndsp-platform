########################################
# 💀 DRAWDOWN GUARD LAYER
########################################

def apply_drawdown_guard(decision: dict):

    """
    Prevent trading when drawdown exceeds safe threshold.
    يمنع التداول إذا تجاوز التراجع الحد الآمن.
    """

    drawdown = decision.get("drawdown", 0)

    if drawdown and drawdown < -0.2:
        decision["blocked"] = True
        decision["reason"] = "drawdown_limit_exceeded"

    decision.setdefault("meta", {})
    decision["meta"]["drawdown_guard"] = "ok"

    return decision
