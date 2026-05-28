"""
Governance v6 sanitized orderflow engine.

Context only:
- no buy/sell bias
- no side
- no execution intent
- no direction authority
"""


def run(*args, **kwargs):
    return {
        "status": "context_only",
        "pressure": "neutral",
        "summary": "Orderflow context is neutral or unavailable.",
    }


def analyze(*args, **kwargs):
    return run(*args, **kwargs)
