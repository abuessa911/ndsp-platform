"""
Governance v6 quarantine.

Legacy root main.py disabled as trading-brain entrypoint.
The active FastAPI application must use app/main.py.
"""

from app.core.governed_pipeline import run_governed


def build_governed_output(symbol: str = "BTCUSDT"):
    return run_governed(symbol)


if __name__ == "__main__":
    print(build_governed_output("BTCUSDT"))
