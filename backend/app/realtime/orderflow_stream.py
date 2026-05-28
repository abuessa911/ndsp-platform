"""
Governance v6 sanitized realtime orderflow stream.

Context only.
No directional trading pressure is exposed.
"""


def get_liquidity_context(*args, **kwargs):
    return {
        "status": "context_only",
        "liquidity_state": "neutral_pressure",
        "summary": "Realtime orderflow context is neutral or unavailable.",
    }


def run(*args, **kwargs):
    return get_liquidity_context(*args, **kwargs)
