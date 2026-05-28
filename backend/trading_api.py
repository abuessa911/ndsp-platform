"""
Governance v6 quarantine.

Legacy trading API disabled.
Use app.core.governed_pipeline.run_governed only.
"""

from app.core.governed_pipeline import run_governed


def get_signal(symbol: str = "BTCUSDT"):
    return run_governed(symbol)
