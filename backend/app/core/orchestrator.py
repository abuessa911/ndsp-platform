"""
Governance v6 sanitized orchestrator.

Legacy multi-engine orchestration is disabled.
The only governed decision path is app.core.governed_pipeline.run_governed.
"""


def run(*args, **kwargs):
    from app.core.governed_pipeline import run_governed

    symbol = kwargs.get("symbol")
    if not symbol and args:
        symbol = args[0]
    return run_governed(symbol or "XAUUSD")


def orchestrate(*args, **kwargs):
    return run(*args, **kwargs)
