from __future__ import annotations
from fastapi import APIRouter, Depends, Body
from app.governance.admin_only import require_admin_role
from app.integrations.telegram.unified_sender import telegram_status, send_telegram_message

router = APIRouter(prefix="/api/admin/telegram", tags=["telegram-admin"])

@router.get("/status", dependencies=[Depends(require_admin_role)])
def get_telegram_status():
    return telegram_status()

@router.post("/test", dependencies=[Depends(require_admin_role)])
def send_test_message(payload: dict = Body(default={})):
    text = payload.get("message") or "NDSP v6 test notification"
    return send_telegram_message(text)
