from __future__ import annotations

from fastapi import APIRouter, Request

from app.saas.subscriptions_db import (
    upsert_telegram_user,
    list_telegram_users,
    upsert_subscription_lead,
)
from app.alerts.telegram_sender import send_telegram_to_chat

router = APIRouter(prefix="/api/v6/telegram", tags=["telegram-webhook"])


def _extract_start_plan(text: str | None) -> str:
    raw = (text or "").strip().lower()

    if not raw.startswith("/start"):
        return "free"

    parts = raw.split(maxsplit=1)
    if len(parts) < 2:
        return "free"

    plan = parts[1].strip().lower()
    if plan in ("free", "pro", "elite"):
        return plan

    return "free"


def _welcome_message(plan: str, first_name: str | None = None) -> str:
    name = first_name or "صديقنا"

    if plan == "pro":
        return f"""
مرحبًا {name} 👋

اخترت خطة NDSP Pro.

مزايا Pro:
- تنبيهات قناة Pro
- قرارات وسيناريوهات منظمة
- اشتراك شهري

السعر الحالي: 99$
للتفعيل، تواصل مع الإدارة وأرسل إثبات الدفع.
بعد التأكيد سيتم إرسال رابط الدخول الخاص بك.
""".strip()

    if plan == "elite":
        return f"""
مرحبًا {name} 👑

اخترت خطة NDSP Elite.

مزايا Elite:
- قناة VIP فقط
- أولوية في التنبيهات
- مزايا market_alignment عند توفرها
- تجربة أعلى من Pro

السعر الحالي: 199$
للتفعيل، تواصل مع الإدارة وأرسل إثبات الدفع.
بعد التأكيد سيتم إرسال رابط VIP الخاص بك.
""".strip()

    return f"""
مرحبًا {name} 👋

أهلًا بك في NDSP Intelligence.

يمكنك متابعة الباقات من الموقع:
https://ndsp.app

الباقات المتاحة:
- Free
- Pro
- Elite

للاشتراك اختر الخطة من الموقع أو أرسل:
 /start pro
 /start elite
""".strip()


@router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    message = data.get("message") or data.get("edited_message") or {}
    chat = message.get("chat") or {}
    user = message.get("from") or {}
    text = message.get("text") or ""

    if not user:
        return {
            "status": "ignored",
            "reason": "missing_user",
        }

    telegram_user_id = str(user.get("id"))
    chat_id = str(chat.get("id") or telegram_user_id)

    saved = upsert_telegram_user(
        telegram_user_id=telegram_user_id,
        username=user.get("username"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        chat_id=chat_id,
    )

    plan = _extract_start_plan(text)

    lead = None
    if text.strip().lower().startswith("/start") and plan in ("pro", "elite"):
        lead = upsert_subscription_lead(
            telegram_user_id=telegram_user_id,
            username=user.get("username"),
            first_name=user.get("first_name"),
            plan=plan,
            status="pending",
            source="telegram_start",
        )

    reply = None
    if text.strip().lower().startswith("/start"):
        reply = send_telegram_to_chat(
            chat_id=chat_id,
            message=_welcome_message(plan, user.get("first_name")),
        )

    return {
        "status": "ok",
        "telegram_user": saved,
        "start_plan": plan,
        "lead": lead,
        "reply": reply,
    }


@router.get("/users")
def telegram_users():
    return {
        "status": "ok",
        "users": list_telegram_users(),
    }
