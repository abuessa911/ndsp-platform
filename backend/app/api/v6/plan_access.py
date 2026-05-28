from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/api/v6/access", tags=["NDSP Plan Access"])

SYSTEM_NAME = "NDSP"
API_VERSION = "1.0.0"
GOVERNANCE_VERSION = "6.1.0"

ALLOWED_PLANS = {"free", "pro", "elite", "saas"}

PLAN_FEATURES: Dict[str, Dict[str, Any]] = {
    "free": {
        "label": "Free",
        "level": 0,
        "markets": ["AUDUSD"],
        "features": {
            "market_state": True,
            "limited_confidence": True,
            "full_confidence": False,
            "scenario_panel": False,
            "advanced_scenario": False,
            "alerts": False,
            "history": False,
            "api_access": False,
            "nmp_context": False,
            "momentum_context": False,
            "advanced_dashboard": False,
            "priority_updates": False,
            "organization_console": False,
            "white_label": False,
        },
        "limits": {
            "refresh_mode": "delayed",
            "api_rate": "none",
            "history_days": 0,
        },
    },
    "pro": {
        "label": "Pro",
        "level": 1,
        "markets": ["BTCUSDT", "ETHUSDT", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD"],
        "features": {
            "market_state": True,
            "limited_confidence": False,
            "full_confidence": True,
            "scenario_panel": True,
            "advanced_scenario": False,
            "alerts": True,
            "history": True,
            "api_access": True,
            "nmp_context": False,
            "momentum_context": False,
            "advanced_dashboard": False,
            "priority_updates": False,
            "organization_console": False,
            "white_label": False,
        },
        "limits": {
            "refresh_mode": "standard",
            "api_rate": "standard",
            "history_days": 14,
        },
    },
    "elite": {
        "label": "Elite",
        "level": 2,
        "markets": [
            "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT",
            "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
            "XAUUSD", "XAGUSD", "USOIL", "UKOIL",
            "US30", "US100", "US500", "GER40", "UK100", "FRA40", "JP225"
        ],
        "features": {
            "market_state": True,
            "limited_confidence": False,
            "full_confidence": True,
            "scenario_panel": True,
            "advanced_scenario": True,
            "alerts": True,
            "history": True,
            "api_access": True,
            "nmp_context": True,
            "momentum_context": True,
            "advanced_dashboard": True,
            "priority_updates": True,
            "organization_console": False,
            "white_label": False,
        },
        "limits": {
            "refresh_mode": "priority",
            "api_rate": "high",
            "history_days": 90,
        },
    },
    "saas": {
        "label": "SaaS",
        "level": 3,
        "markets": ["ALL_GOVERNED_MARKETS"],
        "features": {
            "market_state": True,
            "limited_confidence": False,
            "full_confidence": True,
            "scenario_panel": True,
            "advanced_scenario": True,
            "alerts": True,
            "history": True,
            "api_access": True,
            "nmp_context": True,
            "momentum_context": True,
            "advanced_dashboard": True,
            "priority_updates": True,
            "organization_console": True,
            "white_label": True,
        },
        "limits": {
            "refresh_mode": "enterprise",
            "api_rate": "enterprise",
            "history_days": 365,
        },
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_plan(plan: Optional[str]) -> str:
    value = (plan or "free").strip().lower()
    if value not in ALLOWED_PLANS:
        return "free"
    return value


def jsonl_paths() -> list[Path]:
    candidates = [
        os.getenv("NDSP_NOWPAYMENTS_JSONL", ""),
        os.getenv("NOWPAYMENTS_JSONL", ""),
        "/var/lib/ndsp/nowpayments/payments.jsonl",
        "/var/lib/ndsp/payments.jsonl",
        str(Path.home() / "empire-core-new/backend/data/nowpayments_payments.jsonl"),
        str(Path.home() / "empire-core-new/backend/nowpayments_payments.jsonl"),
        str(Path.home() / "ndsp_nowpayments_payments.jsonl"),
    ]
    out = []
    for item in candidates:
        if item:
            p = Path(item).expanduser()
            if p.exists() and p.is_file():
                out.append(p)
    return out


def read_latest_confirmed_payment(email: str) -> Optional[Dict[str, Any]]:
    target = email.strip().lower()
    if not target:
        return None

    latest: Optional[Dict[str, Any]] = None

    for path in jsonl_paths():
        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except Exception:
                        continue

                    row_email = str(row.get("email") or row.get("customer_email") or "").strip().lower()
                    if row_email != target:
                        continue

                    review_status = str(row.get("review_status") or row.get("status") or "").lower()
                    subscription_status = str(row.get("subscription_status") or "").lower()
                    activation = str(row.get("activation") or "").lower()

                    is_confirmed = (
                        review_status == "confirmed"
                        or subscription_status == "active"
                        or activation == "manual_admin_confirmed"
                    )

                    if not is_confirmed:
                        continue

                    latest = row
        except Exception:
            continue

    return latest


def plan_from_payment(row: Optional[Dict[str, Any]]) -> str:
    if not row:
        return "free"

    plan = normalize_plan(str(row.get("plan") or row.get("package") or row.get("tier") or "free"))

    subscription_status = str(row.get("subscription_status") or "").lower()
    review_status = str(row.get("review_status") or row.get("status") or "").lower()

    if subscription_status == "active" or review_status == "confirmed":
        return plan

    return "free"


def build_access_response(email: str, source: str, payment: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    plan = plan_from_payment(payment)
    access = PLAN_FEATURES[plan]

    subscription = {
        "status": "active" if plan != "free" else "free",
        "plan": access["label"],
        "review_status": payment.get("review_status") if payment else None,
        "activation": payment.get("activation") if payment else None,
        "payment_id": payment.get("payment_id") if payment else None,
        "expires_at": payment.get("expires_at") or payment.get("expires") if payment else None,
    }

    return {
        "version": API_VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "system": SYSTEM_NAME,
        "timestamp": utc_now(),
        "email": email,
        "source": source,
        "subscription": subscription,
        "access": {
            "plan": plan,
            "label": access["label"],
            "level": access["level"],
            "features": access["features"],
            "markets": access["markets"],
            "limits": access["limits"],
        },
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
        },
    }


@router.get("/plans")
def get_plan_matrix() -> Dict[str, Any]:
    return {
        "version": API_VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "system": SYSTEM_NAME,
        "timestamp": utc_now(),
        "allowed_plans": ["Free", "Pro", "Elite", "SaaS"],
        "plans": PLAN_FEATURES,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
        },
    }


@router.get("/me")
def get_my_access(
    request: Request,
    email: str = Query("", description="User email. Temporary until JWT is finalized."),
) -> JSONResponse:
    clean_email = email.strip().lower()

    if not clean_email:
        return JSONResponse(
            status_code=200,
            content=build_access_response(email="", source="default_free_no_email", payment=None),
        )

    payment = read_latest_confirmed_payment(clean_email)
    payload = build_access_response(
        email=clean_email,
        source="nowpayments_jsonl_temporary" if payment else "default_free_no_active_subscription",
        payment=payment,
    )
    return JSONResponse(status_code=200, content=payload)


@router.get("/feature")
def check_feature(
    email: str = Query("", description="User email. Temporary until JWT is finalized."),
    feature: str = Query(..., description="Feature key to check."),
) -> Dict[str, Any]:
    clean_email = email.strip().lower()
    payment = read_latest_confirmed_payment(clean_email) if clean_email else None
    plan = plan_from_payment(payment)
    access = PLAN_FEATURES[plan]
    allowed = bool(access["features"].get(feature, False))

    return {
        "version": API_VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "system": SYSTEM_NAME,
        "timestamp": utc_now(),
        "email": clean_email,
        "plan": access["label"],
        "feature": feature,
        "allowed": allowed,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
        },
    }
