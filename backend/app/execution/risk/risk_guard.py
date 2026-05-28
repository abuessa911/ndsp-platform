from app.execution.risk.behavioral_lock import is_locked

def check_trading_allowed():
    if is_locked():
        return {
            "allowed": False,
            "reason": "Behavioral lock active"
        }
    return {
        "allowed": True
    }
