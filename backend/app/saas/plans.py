from __future__ import annotations

PLANS = {
    "guest": {
        "name": "Guest",
        "dashboard": "market_state_only",
        "confidence": "limited",
        "scenario": False,
        "alerts": False,
        "history": "none",
        "telegram_channel": None,
    },
    "free": {
        "name": "Free",
        "dashboard": "limited",
        "confidence": "limited",
        "scenario": False,
        "alerts": True,
        "history": "limited",
        "telegram_channel": "free",
    },
    "pro": {
        "name": "Pro",
        "dashboard": "full_core",
        "confidence": "full",
        "scenario": True,
        "alerts": True,
        "history": "full",
        "telegram_channel": "pro",
    },
    "elite": {
        "name": "Elite",
        "dashboard": "enhanced",
        "confidence": "full",
        "scenario": True,
        "alerts": True,
        "history": "rich",
        "market_alignment": True,
        "telegram_channel": "vip",
    },
    "admin": {
        "name": "Admin",
        "dashboard": "operational",
        "confidence": "full",
        "scenario": True,
        "alerts": True,
        "history": "full",
        "admin": True,
        "telegram_channel": None,
    },
}


def get_plan(plan: str | None) -> dict:
    key = (plan or "guest").lower()
    return PLANS.get(key, PLANS["guest"])


def can_receive_alerts(plan: str | None) -> bool:
    return bool(get_plan(plan).get("alerts"))


def get_plan_channel(plan: str | None) -> str | None:
    return get_plan(plan).get("telegram_channel")
