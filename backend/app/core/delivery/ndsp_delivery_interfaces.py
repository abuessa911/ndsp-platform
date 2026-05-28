from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import json
import os
import smtplib
import ssl
import urllib.error
import urllib.request
from email.message import EmailMessage
from app.core.delivery.ndsp_env_compat import (
    telegram_token,
    telegram_chat_id,
    smtp_host,
    smtp_port,
    smtp_user,
    smtp_password,
    smtp_from,
    smtp_to,
)

from typing import Any, Dict, List

from app.core.delivery.ndsp_delivery_settings import get_channel_enabled


MAX_MESSAGE_LENGTH = 1600

FORBIDDEN_TERMS = [
    "BUY NOW",
    "SELL NOW",
    "TP",
    "SL",
    "take profit",
    "stop loss",
    "raw_rsi",
    "raw_macd",
    "cot_raw",
    "DATABASE_URL",
    "JWT_SECRET",
    "API_SECRET",
    "ADMIN_KEY",
    "TELEGRAM_BOT_TOKEN",
    "SMTP_PASSWORD",
    "PUSH_SECRET",
]


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _enabled(name: str) -> bool:
    return _env(name).lower() in {"1", "true", "yes", "on", "enabled"}


def _clean_text(value: Any) -> str:
    text = str(value or "").strip()
    for term in FORBIDDEN_TERMS:
        text = text.replace(term, "[sanitized]")
        text = text.replace(term.lower(), "[sanitized]")
    return text[:MAX_MESSAGE_LENGTH]


def _alert_text(alert: Dict[str, Any]) -> str:
    symbol = _clean_text(alert.get("symbol") or "SYSTEM")
    severity = _clean_text(alert.get("severity") or "info")
    title = _clean_text(alert.get("title") or "NDSP Alert")
    message = _clean_text(alert.get("message") or "Governed alert update.")
    context = _clean_text(alert.get("context") or "Decision Active / Execution Sanitized")
    timestamp = _clean_text(alert.get("timestamp") or "")

    return (
        f"NDSP Alert\\n"
        f"Symbol: {symbol}\\n"
        f"Severity: {severity}\\n"
        f"Title: {title}\\n"
        f"Message: {message}\\n"
        f"Context: {context}\\n"
        f"Mode: Decision Active / Execution Sanitized\\n"
        f"Time: {timestamp}"
    )[:MAX_MESSAGE_LENGTH]


def delivery_status() -> Dict[str, Any]:
    telegram_configured = bool(telegram_token() and telegram_chat_id())
    email_configured = bool(smtp_host() and smtp_user() and smtp_password() and (smtp_to()))
    push_configured = bool(_env("NDSP_PUSH_WEBHOOK_URL") or _env("PUSH_WEBHOOK_URL"))

    return {
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "channels": {
            "portal": {"enabled": True, "configured": True},
            "telegram": {
                "enabled": get_channel_enabled("telegram", "NDSP_TELEGRAM_ENABLED"),
                "configured": telegram_configured,
            },
            "email": {
                "enabled": get_channel_enabled("email", "NDSP_EMAIL_ENABLED"),
                "configured": email_configured,
            },
            "push": {
                "enabled": get_channel_enabled("push", "NDSP_PUSH_ENABLED"),
                "configured": push_configured,
            },
        },
        "delivery_mode": "sanitized",
        "direct_execution": False,
        "secrets_exposed": False,
    }


def _post_json(url: str, payload: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            body = res.read().decode("utf-8", errors="replace")
            return {"ok": 200 <= res.status < 300, "status_code": res.status, "body": body[:500]}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        return {"ok": False, "status_code": e.code, "body": body[:500]}
    except Exception as e:
        return {"ok": False, "status": "error", "message": _clean_text(type(e).__name__)}


def send_telegram(alert: Dict[str, Any]) -> Dict[str, Any]:
    if not get_channel_enabled("telegram", "NDSP_TELEGRAM_ENABLED"):
        return {"ok": False, "status": "disabled"}

    token = telegram_token()
    chat_id = telegram_chat_id()
    if not token or not chat_id:
        return {"ok": False, "status": "not_configured"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": _alert_text(alert),
        "disable_web_page_preview": True,
    }

    result = _post_json(url, payload)
    return {
        "ok": bool(result.get("ok")),
        "status": "sent" if result.get("ok") else "failed",
        "provider": "telegram",
        "status_code": result.get("status_code"),
    }


def send_email(alert: Dict[str, Any]) -> Dict[str, Any]:
    if not get_channel_enabled("email", "NDSP_EMAIL_ENABLED"):
        return {"ok": False, "status": "disabled"}

    host = smtp_host()
    port = int(smtp_port() or "587")
    user = smtp_user()
    password = smtp_password()
    mail_from = smtp_from() or user
    mail_to = smtp_to()

    if not host or not user or not password or not mail_to:
        return {"ok": False, "status": "not_configured"}

    msg = EmailMessage()
    msg["Subject"] = _clean_text(alert.get("title") or "NDSP Alert")
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(_alert_text(alert))

    try:
        context = ssl.create_default_context()
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=15) as server:
                server.starttls(context=context)
                server.login(user, password)
                server.send_message(msg)

        return {"ok": True, "status": "sent", "provider": "email"}
    except Exception as e:
        return {"ok": False, "status": "failed", "provider": "email", "message": _clean_text(type(e).__name__)}


def send_push(alert: Dict[str, Any]) -> Dict[str, Any]:
    if not get_channel_enabled("push", "NDSP_PUSH_ENABLED"):
        return {"ok": False, "status": "disabled"}

    url = _env("NDSP_PUSH_WEBHOOK_URL") or _env("PUSH_WEBHOOK_URL")
    if not url:
        return {"ok": False, "status": "not_configured"}

    payload = {
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "delivery_mode": "sanitized",
        "title": _clean_text(alert.get("title") or "NDSP Alert"),
        "message": _clean_text(alert.get("message") or "Governed alert update."),
        "symbol": _clean_text(alert.get("symbol") or "SYSTEM"),
        "severity": _clean_text(alert.get("severity") or "info"),
        "context": _clean_text(alert.get("context") or "Decision Active / Execution Sanitized"),
        "direct_execution": False,
    }

    result = _post_json(url, payload)
    return {
        "ok": bool(result.get("ok")),
        "status": "sent" if result.get("ok") else "failed",
        "provider": "push",
        "status_code": result.get("status_code"),
    }


def deliver_alert(alert: Dict[str, Any]) -> Dict[str, Any]:
    status = delivery_status()
    channels: List[str] = alert.get("channels") or ["portal"]

    results: Dict[str, Any] = {}

    for channel in channels:
        ch = str(channel).lower().strip()

        if ch == "portal":
            results[ch] = {"ok": True, "status": "available", "provider": "portal"}
        elif ch == "telegram":
            results[ch] = send_telegram(alert)
        elif ch == "email":
            results[ch] = send_email(alert)
        elif ch == "push":
            results[ch] = send_push(alert)
        else:
            results[ch] = {"ok": False, "status": "unsupported"}

    return {
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "delivery_mode": "sanitized",
        "status": status,
        "results": results,
        "secrets_exposed": False,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }
