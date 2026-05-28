"""
Governance v6 quarantine.

Legacy sniper engine disabled:
- No entry_long / entry_short
- No stop / target trading levels
- No execution signal
"""

def run(*args, **kwargs):
    return {
        "status": "blocked",
        "reason": "legacy_sniper_engine_disabled_by_governance_v6",
    }


def analyze(*args, **kwargs):
    return run(*args, **kwargs)
