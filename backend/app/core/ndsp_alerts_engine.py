from datetime import datetime, timezone
import os
import json
import urllib.request

ALERTS_LOG = "/home/nawaf511/ndsp_ops/logs/alerts.log"

def now():
    return datetime.now(timezone.utc).isoformat()

def sanitize_decision(payload: dict) -> dict:
    return {
        "system": "NDSP",
        "symbol": payload.get("symbol", "UNKNOWN"),
        "direction": (payload.get("decision") or {}).get("direction", "neutral"),
        "confidence": (payload.get("decision") or {}).get("confidence", 0),
        "system_state": (payload.get("states") or {}).get("system_state", "unknown"),
        "risk_state": (payload.get("states") or {}).get("risk_state", "unknown"),
        "nmp_signal": (payload.get("market_alignment") or {}).get("signal", "NO_SIGNAL"),
        "timestamp": now(),
        "safe": True,
        "raw_logic_exposed": False,
        "direct_execution": False,
    }

def build_alert_message(payload: dict) -> str:
    safe = sanitize_decision(payload)
    return (
        f"NDSP Alert\\n"
        f"Symbol: {safe['symbol']}\\n"
        f"Context: {safe['direction']}\\n"
        f"Confidence: {safe['confidence']}\\n"
        f"System: {safe['system_state']}\\n"
        f"Risk: {safe['risk_state']}\\n"
        f"market_alignment: {safe['nmp_signal']}\\n"
        f"Note: Decision-support context only. No execution instruction."
    )

def log_alert(channel: str, payload: dict, status: str):
    os.makedirs(os.path.dirname(ALERTS_LOG), exist_ok=True)
    row = {
        "timestamp": now(),
        "channel": channel,
        "status": status,
        "payload": sanitize_decision(payload),
    }
    with open(ALERTS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\\n")

def send_telegram(payload: dict) -> dict:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        log_alert("telegram", payload, "not_configured")
        return {"ok": False, "channel": "telegram", "status": "not_configured"}

    msg = build_alert_message(payload)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": msg}).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as res:
            ok = 200 <= res.status < 300
        log_alert("telegram", payload, "sent" if ok else "failed")
        return {"ok": ok, "channel": "telegram", "status": "sent" if ok else "failed"}
    except Exception:
        log_alert("telegram", payload, "failed")
        return {"ok": False, "channel": "telegram", "status": "failed"}

def send_email(payload: dict) -> dict:
    # V1 foundation only. SMTP keys must be configured later.
    log_alert("email", payload, "queued_placeholder")
    return {"ok": True, "channel": "email", "status": "queued_placeholder"}

def send_push(payload: dict) -> dict:
    # V1 foundation only. Web Push/Firebase keys must be configured later.
    log_alert("push", payload, "queued_placeholder")
    return {"ok": True, "channel": "push", "status": "queued_placeholder"}

def dispatch_alert(payload: dict, channels=None) -> dict:
    channels = channels or ["telegram", "email", "push"]
    results = []
    for ch in channels:
        if ch == "telegram":
            results.append(send_telegram(payload))
        elif ch == "email":
            results.append(send_email(payload))
        elif ch == "push":
            results.append(send_push(payload))
    return {"ok": True, "system": "NDSP", "results": results, "safe": True}
