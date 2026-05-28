"""
Governance v6 quarantine.

Legacy scanner disabled:
- No BUY/SELL/NONE generation
- No random signal generation
- No bypass around governed_pipeline
"""

from app.core.governed_pipeline import run_governed


def generate_signal(symbol: str = "BTCUSDT"):
    return run_governed(symbol)


def scan_market(symbol: str = "BTCUSDT"):
    return {
        "version": "1.0.0",
        "status": "governed",
        "data": run_governed(symbol),
    }
