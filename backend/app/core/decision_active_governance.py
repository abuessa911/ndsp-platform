from __future__ import annotations

from typing import Any, Dict

from app.core.decision_active_sanitizer import apply_decision_active_governance


def enforce_decision_active_governance(payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_decision_active_governance(payload)
