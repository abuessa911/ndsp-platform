from __future__ import annotations

"""
Compatibility service for older /signal imports.

Governance v6:
- NDSP is not a signal engine.
- timing_model remains direction authority through governed_pipeline.
- This function returns the governed decision-delivery contract.
"""

from app.core.governed_pipeline import run_governed


def build_signal(symbol: str = "BTCUSDT"):
    return run_governed(symbol)
