from __future__ import annotations
from typing import Any, Mapping


def personalize_experience(
    payload: Mapping[str, Any],
    *,
    role: str,
    experience_mode: str,
    preferences: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Presentation-only personalization. It never changes the governed decision."""
    preferences = dict(preferences or {})
    allowed_modes = {"beginner", "professional"}
    normalized_mode = experience_mode if experience_mode in allowed_modes else "beginner"
    return {
        "role": role,
        "experience_mode": normalized_mode,
        "language": preferences.get("language", "ar"),
        "density": preferences.get("density", "comfortable"),
        "decision_id": payload.get("decision_id"),
        "single_truth_state": payload.get("single_truth_state"),
        "changes_decision": False,
        "decision_authority": False,
    }
