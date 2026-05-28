# ============================================
# CIRCUIT BREAKER MODULE
# ============================================

from typing import Dict


def apply_circuit_breaker(state: Dict) -> Dict:
    """
    Circuit breaker to protect system from unsafe conditions

    INPUT:
        state: dict containing system_state + risk_state + metrics

    OUTPUT:
        modified state (safe_mode / blocked if needed)
    """

    if not isinstance(state, dict):
        return {
            "system_state": "error",
            "reason": "invalid_state_format"
        }

    risk = state.get("risk_state", "normal")
    confidence = state.get("confidence", 0)
    system = state.get("system_state", "live")

    # ==============================
    # RULE 1: Drawdown protection
    # ==============================
    if risk == "drawdown":
        return {
            **state,
            "system_state": "safe_mode",
            "reason": "drawdown_protection_triggered"
        }

    # ==============================
    # RULE 2: Low confidence protection
    # ==============================
    if confidence < 20:
        return {
            **state,
            "system_state": "blocked",
            "reason": "low_confidence"
        }

    # ==============================
    # RULE 3: System error fallback
    # ==============================
    if system == "error":
        return {
            **state,
            "system_state": "safe_mode",
            "reason": "system_error_fallback"
        }

    # ==============================
    # DEFAULT (PASS)
    # ==============================
    return state
