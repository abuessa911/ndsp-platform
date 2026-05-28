# ============================================
# KILL SWITCH MODULE
# ============================================

from typing import Dict


def check_kill_switch(state: Dict) -> Dict:
    """
    Kill switch system to stop execution under critical conditions

    INPUT:
        state: dict (system_state + risk_state + meta)

    OUTPUT:
        modified state if kill switch triggered
    """

    if not isinstance(state, dict):
        return {
            "system_state": "error",
            "reason": "invalid_state_format"
        }

    system_state = state.get("system_state", "live")
    risk_state = state.get("risk_state", "normal")
    alerts = state.get("alerts", [])

    # ==============================
    # RULE 1: Critical alert trigger
    # ==============================
    for alert in alerts:
        if alert.get("type") == "critical":
            return {
                **state,
                "system_state": "blocked",
                "reason": "critical_alert_triggered"
            }

    # ==============================
    # RULE 2: Risk pause trigger
    # ==============================
    if risk_state == "paused":
        return {
            **state,
            "system_state": "blocked",
            "reason": "risk_paused"
        }

    # ==============================
    # RULE 3: System already in error
    # ==============================
    if system_state == "error":
        return {
            **state,
            "system_state": "safe_mode",
            "reason": "system_error_kill_switch"
        }

    # ==============================
    # DEFAULT
    # ==============================
    return state
