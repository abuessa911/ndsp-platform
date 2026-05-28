"""
Governance v6 sanitized brain loader.

Legacy service momentum loader disabled.
"""


def load(*args, **kwargs):
    return {
        "status": "disabled",
        "reason": "legacy_loader_disabled_by_governance_v6",
    }


def run(*args, **kwargs):
    return load(*args, **kwargs)
