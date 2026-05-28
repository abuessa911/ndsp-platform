import os
import time
import logging
from pathlib import Path
from datetime import datetime, timezone

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
LOG_DIR.mkdir(exist_ok=True)
RUNTIME_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "ndsp_health_monitor.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

API_BASE = os.getenv("NDSP_API_BASE", "http://127.0.0.1:9000").rstrip("/")
SYMBOL = os.getenv("NDSP_HEALTH_SYMBOL", "XAUUSD")
INTERVAL = int(os.getenv("NDSP_HEALTH_INTERVAL_SECONDS", "60"))
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "true").lower() == "true"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_FREE_CHAT_ID = os.getenv("TELEGRAM_FREE_CHAT_ID", "")
TELEGRAM_PRO_CHAT_ID = os.getenv("TELEGRAM_PRO_CHAT_ID", "")
TELEGRAM_VIP_CHAT_ID = os.getenv("TELEGRAM_VIP_CHAT_ID", "")

STATE_FILE = RUNTIME_DIR / "ndsp_health_monitor_state.txt"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def telegram_targets():
    targets = []
    for value in [TELEGRAM_FREE_CHAT_ID, TELEGRAM_PRO_CHAT_ID, TELEGRAM_VIP_CHAT_ID]:
        if value and value not in targets:
            targets.append(value)
    return targets


def send_telegram(text):
    if not TELEGRAM_ENABLED or not TELEGRAM_TOKEN:
        return False, "telegram_not_configured"

    targets = telegram_targets()
    if not targets:
        return False, "no_chat_targets"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    results = []

    for chat_id in targets:
        try:
            r = requests.post(
                url,
                data={"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
                timeout=15,
            )
            if r.status_code >= 400:
                results.append(f"{chat_id}:fail")
            else:
                results.append(f"{chat_id}:ok")
        except Exception:
            results.append(f"{chat_id}:error")

    return True, ",".join(results)


def read_last_state():
    try:
        return STATE_FILE.read_text().strip()
    except Exception:
        return "unknown"


def write_last_state(value):
    STATE_FILE.write_text(value)


def check_api():
    url = f"{API_BASE}/decision"
    r = requests.get(url, params={"symbol": SYMBOL}, timeout=10)
    r.raise_for_status()
    payload = r.json()

    if not isinstance(payload, dict):
        raise RuntimeError("invalid_payload_type")

    decision = payload.get("decision", {})
    states = payload.get("states", {})

    if decision.get("direction") not in ["bullish", "bearish", "neutral"]:
        raise RuntimeError("invalid_decision_direction")

    if states.get("system_state") not in ["live", "blocked", "safe_mode", "error"]:
        raise RuntimeError("invalid_system_state")

    return payload


def main():
    logging.info("NDSP health monitor started api=%s symbol=%s interval=%s", API_BASE, SYMBOL, INTERVAL)

    while True:
        try:
            payload = check_api()
            last = read_last_state()

            if last != "healthy":
                msg = "\n".join([
                    "NDSP Health Restored",
                    "",
                    f"API: {API_BASE}",
                    f"Symbol: {SYMBOL}",
                    f"System State: {payload.get('states', {}).get('system_state')}",
                    f"Decision: {payload.get('decision', {}).get('direction')}",
                    f"Confidence: {payload.get('decision', {}).get('confidence')}%",
                    f"Timestamp: {now_iso()}",
                ])
                sent, reason = send_telegram(msg)
                logging.info("health_restored telegram_sent=%s reason=%s", sent, reason)

            write_last_state("healthy")
            logging.info("healthy symbol=%s", SYMBOL)

        except Exception as e:
            last = read_last_state()
            logging.error("unhealthy error=%s", str(e))

            if last != "unhealthy":
                msg = "\n".join([
                    "NDSP Health Alert",
                    "",
                    "Status: UNHEALTHY",
                    f"API: {API_BASE}",
                    f"Symbol: {SYMBOL}",
                    f"Reason: {str(e)[:250]}",
                    f"Timestamp: {now_iso()}",
                ])
                sent, reason = send_telegram(msg)
                logging.info("health_alert telegram_sent=%s reason=%s", sent, reason)

            write_last_state("unhealthy")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
