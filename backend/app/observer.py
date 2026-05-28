import time
import json

from app.core.governed_pipeline import run_governed

LOG = "/home/nawaf511/empire-core-new/backend/logs/observer.log"

SYMBOLS = ["BTCUSDT"]


def log(data):
    with open(LOG, "a") as f:
        f.write(json.dumps(data) + "\n")


def run():
    while True:
        for s in SYMBOLS:
            data = run_governed(s)

            if not isinstance(data, dict):
                continue

            decision = data.get("decision", {})
            risk = data.get("risk", {})
            states = data.get("states", {})

            output = {
                "symbol": s,
                "decision": decision,
                "confidence": decision.get("confidence"),
                "allowed": (decision.get("state") in ("bullish", "bearish")) and (
                    (risk.get("state") or states.get("risk_state")) not in (
                        "blocked",
                        "paused",
                        "drawdown",
                        "safe_mode",
                        "error",
                    )
                ),
                "risk": risk,
                "timestamp": time.time()
            }

            log(output)
            print("OBSERVE:", output)

        time.sleep(60)


if __name__ == "__main__":
    run()
