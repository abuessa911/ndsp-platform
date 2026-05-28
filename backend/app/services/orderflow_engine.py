"""
Governance v6 sanitized orderflow context.

This module may provide contextual pressure only.
It must not define direction, side, entry, or execution.
"""


def get_orderflow_context(*args, **kwargs):
    return {
        "status": "context_only",
        "pressure": "neutral",
        "summary": "Orderflow context is neutral or unavailable.",
    }


def run(*args, **kwargs):
    return get_orderflow_context(*args, **kwargs)
