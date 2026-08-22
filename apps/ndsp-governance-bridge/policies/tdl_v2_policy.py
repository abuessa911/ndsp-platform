from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

POLICY_PATH = Path(__file__).resolve().parents[2] / "config" / "tdl_v2_policy.json"

DEFAULT_POLICY: Dict[str, Any] = {
    "tdl_v2_enabled": True,
    "timing_layer_enabled": True,
    "timing_mode": "control_days",
    "mon_wed_controller": "S",
    "thu_fri_controller": "L&M",
    "sunday_mode": "neutral_review",
    "output_policy": "tdl_v2_only",
    "updated_at": None,
    "updated_by": "system",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_tdl_v2_policy() -> Dict[str, Any]:
    try:
        if POLICY_PATH.exists():
            data = json.loads(POLICY_PATH.read_text())
            if isinstance(data, dict):
                merged = dict(DEFAULT_POLICY)
                merged.update(data)
                return merged
    except Exception:
        pass
    return dict(DEFAULT_POLICY)


def write_tdl_v2_policy(updates: Dict[str, Any], updated_by: str = "admin") -> Dict[str, Any]:
    policy = read_tdl_v2_policy()
    allowed = {
        "tdl_v2_enabled",
        "timing_layer_enabled",
        "timing_mode",
        "mon_wed_controller",
        "thu_fri_controller",
        "sunday_mode",
        "output_policy",
    }

    for key, value in (updates or {}).items():
        if key in allowed:
            policy[key] = value

    policy["updated_at"] = _utc_now()
    policy["updated_by"] = updated_by or "admin"

    POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)
    POLICY_PATH.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n")
    return policy


def derive_timing_context(policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
    policy = policy or read_tdl_v2_policy()

    enabled = bool(policy.get("timing_layer_enabled", True))
    if not enabled:
        return {
            "enabled": False,
            "effect": "bypassed",
            "timing_mode": policy.get("timing_mode", "bypassed"),
            "public_note": "Timing Control Layer is disabled by admin policy."
        }

    now = datetime.now(timezone.utc)
    weekday = now.weekday()  # Monday=0 ... Sunday=6

    if weekday in (0, 1, 2):
        return {
            "enabled": True,
            "effect": "applied",
            "active": "timing_model-S",
            "day_group": "MON_WED",
            "timing_state": "MANIPULATION_BUILD_PULLBACK",
            "control_window": "short_term_speculative",
            "dominant_participant": policy.get("mon_wed_controller", "S"),
            "timing_mode": policy.get("timing_mode", "control_days"),
            "public_note": "Short-term speculative control window."
        }

    if weekday in (3, 4):
        return {
            "enabled": True,
            "effect": "applied",
            "active": "timing_model-L&M",
            "day_group": "THU_FRI",
            "timing_state": "EXPANSION_CONFIRMATION_INSTITUTIONAL_CONTROL",
            "control_window": "long_medium_structural",
            "dominant_participant": policy.get("thu_fri_controller", "L&M"),
            "timing_mode": policy.get("timing_mode", "control_days"),
            "public_note": "Long and medium-term structural control window."
        }

    return {
        "enabled": True,
        "effect": "applied",
        "active": "timing_model-NEUTRAL",
        "day_group": "SUNDAY_OR_LOW_LIQUIDITY",
        "timing_state": "NEUTRAL_LOW_CONFIDENCE_REVIEW",
        "control_window": "neutral_review",
        "dominant_participant": "NEUTRAL",
        "timing_mode": policy.get("timing_mode", "control_days"),
        "public_note": "Neutral or low-confidence timing window."
    }


def derive_timing_authority(policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Timing Authority Layer.

    Final custom day-controller law:
    - Monday: L&M controls direction.
    - Tuesday: S controls direction.
    - Wednesday: S controls direction.
    - Thursday: S controls direction.
    - Friday: L&M controls direction.
    - Saturday: S controls direction.
    - Sunday: S controls direction.

    L&M primary categories:
    - institutional direction
    - market activity

    L&M fallback category:
    - institutional_positioning

    S primary categories:
    - market momentum
    - market structure

    S fallback category:
    - Non-institutional_positioning

    This layer determines directional authority only.
    timing_model v2 calculates the actual L&M/S directions from available market_positioning mapping.
    """
    policy = policy or read_tdl_v2_policy()

    enabled = bool(policy.get("timing_layer_enabled", True))
    if not enabled:
        return {
            "enabled": False,
            "authority_mode": "bypassed",
            "controller": "NONE",
            "controller_label": "No timed controller",
            "direction_source": None,
            "day_group": "BYPASSED",
            "weekday": None,
            "weekday_name": None,
            "decision_authority": "tdl_general",
            "effect": "bypassed",
            "lm_primary_categories": ["institutional direction", "market activity"],
            "lm_fallback_categories": ["institutional_positioning"],
            "s_primary_categories": ["market momentum", "market structure"],
            "s_fallback_categories": ["Non-institutional_positioning"],
            "public_note": "Timing authority is disabled by admin policy."
        }

    now = datetime.now(timezone.utc)
    weekday = now.weekday()  # Monday=0 ... Sunday=6

    weekday_names = {
        0: "MONDAY",
        1: "TUESDAY",
        2: "WEDNESDAY",
        3: "THURSDAY",
        4: "FRIDAY",
        5: "SATURDAY",
        6: "SUNDAY",
    }

    lm_payload = {
        "enabled": True,
        "authority_mode": "timed_controller",
        "controller": "L&M",
        "controller_label": "Long and medium-term investors direction",
        "direction_source": "weekly.lm_direction",
        "day_group": "MON_FRI_LM",
        "weekday": weekday,
        "weekday_name": weekday_names.get(weekday),
        "decision_authority": "timing_controller",
        "effect": "active",
        "lm_primary_categories": ["institutional direction", "market activity"],
        "lm_fallback_categories": ["institutional_positioning"],
        "s_primary_categories": ["market momentum", "market structure"],
        "s_fallback_categories": ["Non-institutional_positioning"],
        "public_note": "Timing authority gives directional control to L&M on Monday and Friday."
    }

    s_payload = {
        "enabled": True,
        "authority_mode": "timed_controller",
        "controller": "S",
        "controller_label": "Short-term speculative direction",
        "direction_source": "weekly.s_direction",
        "day_group": "TUE_WED_THU_SAT_SUN_S",
        "weekday": weekday,
        "weekday_name": weekday_names.get(weekday),
        "decision_authority": "timing_controller",
        "effect": "active",
        "lm_primary_categories": ["institutional direction", "market activity"],
        "lm_fallback_categories": ["institutional_positioning"],
        "s_primary_categories": ["market momentum", "market structure"],
        "s_fallback_categories": ["Non-institutional_positioning"],
        "public_note": "Timing authority gives directional control to S on Tuesday, Wednesday, Thursday, Saturday, and Sunday."
    }

    # Monday and Friday: L&M controls.
    if weekday in (0, 4):
        return lm_payload

    # Tuesday, Wednesday, Thursday, Saturday, Sunday: S controls.
    if weekday in (1, 2, 3, 5, 6):
        return s_payload

    return {
        "enabled": True,
        "authority_mode": "neutral_review",
        "controller": "NEUTRAL",
        "controller_label": "Neutral timing review",
        "direction_source": None,
        "day_group": "UNKNOWN",
        "weekday": weekday,
        "weekday_name": weekday_names.get(weekday),
        "decision_authority": "tdl_general",
        "effect": "neutral_review",
        "lm_primary_categories": ["institutional direction", "market activity"],
        "lm_fallback_categories": ["institutional_positioning"],
        "s_primary_categories": ["market momentum", "market structure"],
        "s_fallback_categories": ["Non-institutional_positioning"],
        "public_note": "Timing authority is neutral because the weekday could not be classified."
    }
