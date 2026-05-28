"""
Governance v6 sanitized compute engine.

Legacy dynamic engine loading is disabled.
Use governed_pipeline.run_governed for runtime decisions.
"""


def run(*args, **kwargs):
    return {
        "status": "disabled",
        "reason": "legacy_compute_engine_disabled_by_governance_v6",
    }


def compute(*args, **kwargs):
    return run(*args, **kwargs)
