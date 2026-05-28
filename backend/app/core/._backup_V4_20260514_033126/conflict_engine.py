"""
Governance v6 sanitized conflict engine.

Conflict may reduce confidence or add caution.
It must not determine direction or execution.
"""


def evaluate_conflict(layers=None):
    layers = layers or {}

    return {
        "status": "context_only",
        "level": "none",
        "score": 0,
        "summary": "No governed conflict context is active.",
    }


def run(*args, **kwargs):
    return evaluate_conflict(*args, **kwargs)
