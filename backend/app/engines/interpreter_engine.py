"""
Governance v6 sanitized interpreter.

Converts abstract state into display context only.
Does not produce long/short or execution intent.
"""


def interpret(state: str):
    state = str(state or "neutral").lower().strip()

    if state == "favorable":
        return "constructive_context"

    if state == "unfavorable":
        return "caution_context"

    return "neutral_context"
