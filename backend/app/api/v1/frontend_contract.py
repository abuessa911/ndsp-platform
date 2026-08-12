from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["NDSP Frontend Contract"])


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def data(payload: Any) -> Dict[str, Any]:
    return {"data": payload}


def err(code: str, ar: str, en: str, http_status: int = 400):
    return {
        "error": {
            "code": code,
            "message_ar": ar,
            "message_en": en,
        }
    }


class RegisterPayload(BaseModel):
    email: str
    name: Optional[str] = None
    type: Optional[str] = "ordinary"
    locale: Optional[str] = "ar"
    _client_signals: Optional[Dict[str, Any]] = None


class LoginPayload(BaseModel):
    email: str
    password: str


class CodePayload(BaseModel):
    code: str


class EmailPayload(BaseModel):
    email: str


class ResetPayload(BaseModel):
    token: str
    new_password: str


class CheckoutPayload(BaseModel):
    plan: str
    cycle: str = "monthly"
    method: str = "crypto"


class WatchlistPayload(BaseModel):
    asset_id: str


class AlertPrefsPayload(BaseModel):
    events: Dict[str, bool] = {}
    dq_threshold: int = 70
    brief_time: str = "08:00"
    digest: bool = True
    quiet_from: str = "22:00"
    quiet_to: str = "07:00"


@router.get("/contract/status")
def contract_status():
    return data({
        "ok": True,
        "contract": "NDSP_FRONTEND_API_V1_BRIDGE",
        "mode": "safe_bridge",
        "backend_authority": True,
        "frontend_display_only": True,
        "raw_logic_exposed": False,
        "timestamp": now_iso(),
    })


@router.post("/auth/register")
async def auth_register(payload: RegisterPayload):
    return data({
        "decision": "PENDING_REVIEW",
        "ref": "NDSP-REG-SAFE-BRIDGE",
        "message_ar": "تم استلام طلب التسجيل. تبدأ التجربة بعد التفعيل فقط.",
        "message_en": "Registration received. Trial starts only after activation.",
    })


@router.post("/auth/login")
async def auth_login(payload: LoginPayload):
    return data({
        "challenge": "2fa",
        "method": "email",
        "message_ar": "تم تفعيل التحقق الثنائي التجريبي.",
        "message_en": "Two-factor verification challenge issued.",
    })


@router.post("/auth/2fa/verify")
async def auth_2fa_verify(payload: CodePayload):
    return data({
        "session": {
            "state": "verified_demo",
            "issued_at": now_iso(),
        }
    })


@router.post("/auth/magic-link")
async def auth_magic_link(payload: EmailPayload):
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get("/auth/magic-link/verify")
async def auth_magic_link_verify(token: str = ""):
    return data({
        "session": {
            "state": "magic_link_verified_demo",
            "issued_at": now_iso(),
        }
    })


@router.post("/auth/forgot")
async def auth_forgot(payload: EmailPayload):
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/auth/reset")
async def auth_reset(payload: ResetPayload):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/account/activate")
async def account_activate():
    started = datetime.now(timezone.utc)
    ends = started + timedelta(days=16)
    return data({
        "trial_day": 1,
        "total": 16,
        "started_at": started.isoformat(),
        "ends_at": ends.isoformat(),
        "expired": False,
        "phase": 1,
        "governance_note": "Trial clock is server-side and per-user.",
    })


@router.get("/account/trial")
async def account_trial():
    started = datetime.now(timezone.utc) - timedelta(days=0)
    ends = started + timedelta(days=16)
    return data({
        "trial_day": 1,
        "total": 16,
        "started_at": started.isoformat(),
        "ends_at": ends.isoformat(),
        "expired": False,
        "phase": 1,
    })


@router.get("/packages")
async def packages():
    return data([
        {
            "plan": "free",
            "markets": 1,
            "assets": 3,
            "analyses": "5/week",
            "named_layers": [],
            "brief": "limited",
            "alerts": "one",
        },
        {
            "plan": "pro",
            "markets": 2,
            "assets": 20,
            "analyses": "15/day",
            "named_layers": ["TDL", "NMP"],
            "alerts": "basic_limited",
        },
        {
            "plan": "elite",
            "markets": "all_supported",
            "assets": 100,
            "analyses": "250/day",
            "named_layers": ["TDL", "NMP", "Devil's Advocate", "Nawaf Golden Alignment"],
            "alerts": "advanced_telegram",
        },
        {
            "plan": "institutional_suite",
            "markets": "all_supported",
            "assets": "250+ or contract",
            "analyses": "contract",
            "named_layers": ["TDL", "NMP", "Devil's Advocate", "Nawaf Golden Alignment"],
            "api": True,
            "webhooks": True,
        },
    ])


@router.get("/me/entitlements")
async def me_entitlements():
    return data({
        "plan": "trial",
        "limits": {
            "markets": "all_supported_during_trial",
            "assets": 100,
            "analyses_per_day": 250,
            "named_layers": ["TDL", "NMP", "Devil's Advocate", "Nawaf Golden Alignment"],
            "alerts": True,
        },
    })


@router.post("/payments/checkout")
async def payments_checkout(payload: CheckoutPayload):
    return data({
        "subscription_id": "sub_safe_bridge",
        "state": "manual_review_required" if payload.method == "bank" else "pending",
        "ref": "NDSP-PAY-SAFE-BRIDGE",
        "instructions": {
            "message_ar": "لا يوجد تفعيل تلقائي. يتم الاعتماد بعد المراجعة.",
            "message_en": "No auto activation. Approval is completed after review.",
        },
    })


@router.post("/payments/webhook")
async def payments_webhook(request: Request):
    return data({
        "received": True,
        "state": "pending_review",
        "note": "Safe bridge accepted webhook envelope only.",
    })


@router.get("/me/subscription")
async def me_subscription():
    return data({
        "plan": "trial",
        "state": "active",
        "ref": "NDSP-TRIAL",
    })


@router.get("/markets")
async def markets():
    return data([
        {"id": "fx", "name_ar": "العملات", "name_en": "FX", "state": "active", "assets_count": 3},
        {"id": "commodities", "name_ar": "السلع", "name_en": "Commodities", "state": "active", "assets_count": 3},
        {"id": "indices", "name_ar": "المؤشرات", "name_en": "Indices", "state": "active", "assets_count": 3},
        {"id": "crypto", "name_ar": "الرقمية", "name_en": "Crypto", "state": "active", "assets_count": 3},
    ])


@router.get("/assets")
async def assets(market: Optional[str] = None):
    rows = [
        {"id": "XAU", "symbol": "XAU/USD", "market": "commodities", "name_ar": "الذهب", "name_en": "Gold"},
        {"id": "WTI", "symbol": "WTI/USD", "market": "commodities", "name_ar": "النفط", "name_en": "Oil"},
        {"id": "EURUSD", "symbol": "EUR/USD", "market": "fx", "name_ar": "اليورو/دولار", "name_en": "EUR/USD"},
        {"id": "BTC", "symbol": "BTC/USD", "market": "crypto", "name_ar": "بيتكوين", "name_en": "Bitcoin"},
        {"id": "SPX", "symbol": "SPX", "market": "indices", "name_ar": "إس آند بي", "name_en": "S&P 500"},
    ]
    if market:
        rows = [r for r in rows if r["market"] == market]
    return data(rows)


@router.get("/assets/{asset_id}/decision")
async def asset_decision(asset_id: str):
    return data({
        "asset_id": asset_id,
        "symbol": asset_id,
        "bias": "flat",
        "horizon": "short",
        "horizon_strength": 61,
        "decision_quality": 64,
        "market_state": "ranging",
        "liquidity": "moderate",
        "risk": "moderate",
        "volatility": "moderate",
        "sentiment": "neutral",
        "scenario_refs": [
            {"type": "activation", "level": 100.0, "note_ar": "مستوى تفعيل سياقي", "note_en": "Contextual activation level"},
            {"type": "arrival", "level": 104.0, "note_ar": "نطاق وصول سياقي", "note_en": "Contextual arrival zone"},
            {"type": "review", "level": 106.0, "note_ar": "منطقة مراجعة", "note_en": "Review zone"},
            {"type": "invalidation", "level": 97.0, "note_ar": "مستوى إلغاء السيناريو", "note_en": "Scenario invalidation level"},
        ],
        "golden_alignment": {
            "active": False,
            "note_ar": "معزز سياقي للجودة فقط — وليس ضمانًا.",
            "note_en": "Contextual quality enhancer only — not a guarantee.",
        },
        "devil_advocate": [
            {"reason_ar": "الحالة تحتاج متابعة إضافية.", "reason_en": "The condition requires additional monitoring."}
        ],
        "summary_ar": "ملخص منقح آمن لدعم القرار فقط.",
        "summary_en": "Safe sanitized decision-support summary only.",
    })


@router.get("/assets/{asset_id}/chart")
async def asset_chart(asset_id: str, timeframe: str = "1h"):
    base = datetime.now(timezone.utc) - timedelta(hours=24)
    series = []
    for i in range(24):
        ts = base + timedelta(hours=i)
        val = 100 + (i % 7)
        series.append({"ts": ts.isoformat(), "o": val, "h": val + 1, "l": val - 1, "c": val + 0.3})
    return data({
        "series": series,
        "reference_zones": [
            {"type": "activation", "level": 100},
            {"type": "arrival", "level": 104},
            {"type": "review", "level": 106},
            {"type": "invalidation", "level": 97},
        ],
        "horizon_cone": {"upper": 108, "lower": 96},
    })


@router.get("/brief/today")
async def brief_today():
    return data({
        "market_weather": {
            "title_ar": "صافٍ مع تقلب متوسط",
            "title_en": "Clear with moderate volatility",
            "bias": "flat",
            "risk": "moderate",
            "liquidity": "moderate",
            "desc_ar": "موجز منقح للسوق.",
            "desc_en": "Sanitized market brief.",
        },
        "glance": [
            {"key": "decision_quality", "value": 64},
            {"key": "risk", "value": "moderate"},
        ],
        "top_reads": [],
        "golden_spotlight": None,
        "devil_today": [],
    })


@router.get("/me/watchlist")
async def get_watchlist():
    return data(["XAU", "BTC", "EURUSD"])


@router.post("/me/watchlist")
async def add_watchlist(payload: WatchlistPayload):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/me/watchlist/{asset_id}")
async def delete_watchlist(asset_id: str):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me/dashboard")
async def me_dashboard():
    return data({
        "hero_asset": "XAU",
        "watchlist": ["XAU", "BTC", "EURUSD"],
        "global_states": {
            "risk": "moderate",
            "liquidity": "moderate",
            "volatility": "moderate",
        },
        "ticker": [
            {"symbol": "XAU/USD", "price": 100.1},
            {"symbol": "BTC/USD", "price": 100.2},
        ],
    })


@router.get("/me/alert-prefs")
async def get_alert_prefs():
    return data({
        "events": {"bias": True, "golden": True, "scenario": True, "caution": True, "horizon": True},
        "dq_threshold": 70,
        "brief_time": "08:00",
        "digest": True,
        "quiet_from": "22:00",
        "quiet_to": "07:00",
    })


@router.put("/me/alert-prefs")
async def put_alert_prefs(payload: AlertPrefsPayload):
    return data(payload.model_dump())


@router.post("/me/channels/telegram/link")
async def telegram_link():
    return data({
        "code": "NDSP-LINK-DEMO",
        "expires_in": 600,
    })


@router.post("/me/channels/telegram/verify")
async def telegram_verify():
    return data({
        "state": "linked",
        "last_test_at": now_iso(),
    })


@router.post("/me/channels/email/test")
async def email_test():
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get("/admin/registrations")
async def admin_registrations(status: Optional[str] = None):
    return data([])


@router.post("/admin/registrations/{registration_id}/decision")
async def admin_registration_decision(registration_id: str, request: Request):
    return data({
        "registration_id": registration_id,
        "state": "recorded",
    })


@router.get("/admin/trials")
async def admin_trials():
    return data([])


@router.get("/admin/payments")
async def admin_payments():
    return data([])


@router.post("/admin/payments/{payment_id}/approve")
async def admin_payment_approve(payment_id: str):
    return data({"payment_id": payment_id, "state": "confirmed"})


@router.post("/admin/payments/{payment_id}/reject")
async def admin_payment_reject(payment_id: str):
    return data({"payment_id": payment_id, "state": "rejected"})


@router.get("/admin/layers")
async def admin_layers():
    return data({
        "visible": ["TDL", "NMP", "Devil's Advocate", "Nawaf Golden Alignment"],
        "hidden_count": 12,
        "raw_logic_exposed": False,
    })


@router.get("/admin/health")
async def admin_health():
    return data({
        "ok": True,
        "service": "ndsp-api-v1-safe-bridge",
        "timestamp": now_iso(),
    })
