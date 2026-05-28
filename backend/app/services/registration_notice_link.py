from __future__ import annotations

from typing import Any, Dict
from app.core.elite_trial_capacity import enforce_elite_trial_capacity


def attach_registration_notice(response: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(response, dict):
        return response

    category = str(response.get("category") or "ordinary").strip() or "ordinary"

    if category.lower() in {"analyst", "professional_user", "specialist", "professional"}:
        category = "professional"
    elif category.lower() in {"private", "private_invite", "invite"}:
        category = "private_invite"
    else:
        category = "ordinary"

    response["next_url"] = f"https://app.ndsp.app/trial-notice?category={category}"
    response["registration_notice"] = {
        "type": "registration_notice_only",
        "ask_feedback_now": False,
        "show_feedback_form_now": False,
        "final_day_feedback_required": True,
        "url": response["next_url"],
    }

    return response
