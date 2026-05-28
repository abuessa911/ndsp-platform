"""
Governance v6 quarantine.

Execution/trading path disabled:
- NDSP is not a broker execution system
- No BUY/SELL orders
- No TP/SL
- No direct trade routing
"""

def disabled(*args, **kwargs):
    return {
        "status": "blocked",
        "reason": "legacy_execution_path_disabled_by_governance_v6",
    }
