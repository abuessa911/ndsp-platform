"""
Governance v6 quarantine.

Legacy module disabled: app.services.sniper_engine

Reason:
- NDSP must not expose trading commands.
- No parallel direction or execution logic is allowed.
- governed_pipeline.py is the only decision-delivery authority.
"""

def disabled(*args, **kwargs):
    return {
        "status": "blocked",
        "reason": "legacy_module_disabled_by_governance_v6",
        "module": "app.services.sniper_engine",
    }


def run(*args, **kwargs):
    return disabled(*args, **kwargs)


def analyze(*args, **kwargs):
    return disabled(*args, **kwargs)


def evaluate(*args, **kwargs):
    return disabled(*args, **kwargs)


def process(*args, **kwargs):
    return disabled(*args, **kwargs)
