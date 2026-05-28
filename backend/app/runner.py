import time

from app.core.governed_pipeline import run_governed
from app.execution.paper_executor import execute
from app.services.price_feed import get_price
from app.core.auto_stop import check

SYMBOLS = ["BTCUSDT"]


def _can_execute(data: dict) -> bool:
    decision = data.get("decision", {})
    state = decision.get("state") or decision.get("direction")
    risk = data.get("risk", {})
    risk_state = risk.get("state") or data.get("states", {}).get("risk_state")

    if state not in ("bullish", "bearish"):
        return False

    if risk_state in ("blocked", "paused", "drawdown", "safe_mode", "error"):
        return False

    return True


def _build_execution_decision(data: dict) -> dict:
    decision = data.get("decision", {})
    state = decision.get("state") or decision.get("direction") or "no_trade"

    return {
        "direction": state,
        "confidence": decision.get("confidence", 0),
        "score": decision.get("score", 0),
    }


def run():
    while True:
        if not check():
            print("💀 STOPPED (LOSS LIMIT)")
            break

        for s in SYMBOLS:
            data = run_governed(s)

            if not isinstance(data, dict):
                continue

            if not _can_execute(data):
                continue

            price = get_price(s)

            trade = execute(
                s,
                _build_execution_decision(data),
                price
            )

            print("TRADE:", trade)

        time.sleep(60)


if __name__ == "__main__":
    run()
