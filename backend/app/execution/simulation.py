from app.execution.risk.risk_guard import check_trading_allowed
from app.execution.risk.behavioral_lock import update_loss
import random
from datetime import datetime
import os

TRADES = []

# 🧪 TEST MODE (controlled)
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

def simulate_trade(signal):

    # 🔒 Check lock
    guard = check_trading_allowed()
    if not guard["allowed"]:
        return {
            "status": "blocked",
            "reason": guard["reason"]
        }

    # 🧪 Controlled override
    if not TEST_MODE:
        if signal.get("grade") not in ["A+", "A"]:
            return {"status": "skipped"}
    else:
        signal["grade"] = "A"

    outcome = random.choice(["win", "loss"])

    pnl = 0.02 if outcome == "win" else -0.03

    update_loss(pnl)

    trade = {
        "time": str(datetime.utcnow()),
        "signal": signal,
        "result": outcome,
        "pnl": pnl,
        "mode": "test" if TEST_MODE else "live"
    }

    TRADES.append(trade)

    return trade


def get_journal():
    return TRADES
