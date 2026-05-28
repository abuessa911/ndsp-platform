import os
import time
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = PROJECT_ROOT / "runtime" / "telegram_decision_state.json"
LOG_FILE = PROJECT_ROOT / "logs" / "telegram_decision_worker.log"

logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

API_BASE = os.getenv("NDSP_API_BASE", "http://127.0.0.1:9001").rstrip("/")
SYMBOLS = [x.strip().upper() for x in os.getenv("NDSP_TELEGRAM_SYMBOLS", "BTCUSDT,ETHUSDT,SOLUSDT").split(",") if x.strip()]
INTERVAL = int(os.getenv("NDSP_TELEGRAM_INTERVAL_SECONDS", "60"))
DUP_WINDOW = int(os.getenv("NDSP_TELEGRAM_DUPLICATE_WINDOW_SECONDS", "600"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_FREE_CHAT_ID = os.getenv("TELEGRAM_FREE_CHAT_ID", "")
TELEGRAM_PRO_CHAT_ID = os.getenv("TELEGRAM_PRO_CHAT_ID", "")
TELEGRAM_VIP_CHAT_ID = os.getenv("TELEGRAM_VIP_CHAT_ID", "")
TELEGRAM_CHAT_IDS = [x.strip() for x in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if x.strip()]
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "true").lower() == "true"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    try:
        return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    except Exception:
        return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def fetch_decision(symbol):
    r = requests.get(f"{API_BASE}/decision", params={"symbol": symbol}, timeout=15)
    r.raise_for_status()
    return r.json()


def valid_payload(p):
    if not isinstance(p, dict):
        return False, "payload_not_dict"

    if p.get("error") is True:
        return False, f"backend_error:{p.get('code', 'unknown')}"

    if p.get("version") != "1.0.0":
        return False, "invalid_version"

    if p.get("governance_version") != "6.0.0":
        return False, "invalid_governance_version"

    symbol = p.get("symbol")
    if not symbol:
        return False, "missing_symbol"

    d = p.get("decision", {})
    if d.get("direction") not in ["bullish", "bearish", "neutral"]:
        return False, "invalid_or_missing_direction"

    try:
        c = float(d.get("confidence", -1))
        if c < 0 or c > 100:
            return False, "confidence_out_of_range"
    except Exception:
        return False, "invalid_confidence"

    forbidden_words = ["BUY NOW", "SELL NOW", "ENTER NOW", "CLOSE NOW", "TAKE PROFIT", "STOP LOSS"]
    raw = str(p).upper()
    for w in forbidden_words:
        if w in raw:
            return False, f"forbidden_word:{w}"

    comp = p.get("compliance")
    if isinstance(comp, dict) and comp.get("logic_leak") is True:
        return False, "logic_leak_true"

    return True, "telegram_delivery_compliance_passed"

def make_hash(p):
    compact = {
        "symbol": p.get("symbol"),
        "decision": p.get("decision"),
        "states": p.get("states"),
        "execution": p.get("execution"),
        "risk": p.get("risk"),
        "market_alignment": p.get("market_alignment"),
    }
    return hashlib.sha256(json.dumps(compact, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def clean(v):
    if v is None:
        return "-"
    return str(v).replace("BUY NOW", "").replace("SELL NOW", "").replace("TP", "").replace("SL", "").strip() or "-"


def build_message(p, tier="pro"):
    d = p.get("decision", {})
    st = p.get("states", {})
    e = p.get("execution", {})
    n = p.get("market_alignment", {})
    r = p.get("risk", {})
    m = p.get("meta", {})
    x = p.get("explainability", {})
    md = p.get("intelligence", {}).get("momentum_dual", {})

    symbol = clean(p.get("symbol"))
    direction = clean(d.get("direction")).upper()
    confidence = clean(d.get("confidence"))
    timestamp = clean(m.get("timestamp", now_iso()))

    if tier == "free":
        return "\n".join([
            "NDSP Free Update",
            "",
            f"Symbol: {symbol}",
            f"Market State: {direction}",
            f"Confidence: Limited",
            f"System: {clean(st.get('system_state'))}",
            "",
            "Upgrade required for scenario, market_alignment, and intelligence context.",
            "",
            f"Timestamp: {timestamp}",
        ])

    if tier == "vip":
        return "\n".join([
            "NDSP VIP Intelligence Update",
            "",
            f"Symbol: {symbol}",
            f"Market State: {direction}",
            f"Confidence: {confidence}%",
            "",
            "System Stack:",
            f"- System State: {clean(st.get('system_state'))}",
            f"- Risk State: {clean(st.get('risk_state'))}",
            f"- Position State: {clean(st.get('position_state'))}",
            f"- Lifecycle: {clean(e.get('lifecycle'))}",
            "",
            "market_alignment Context:",
            f"- Signal: {clean(n.get('signal'))}",
            f"- Position: {clean(n.get('position'))}",
            "",
            "Momentum Context:",
            f"- Signal: {clean(md.get('signal'))}",
            f"- Confidence Effect: {clean(md.get('confidence_effect'))}",
            f"- Context: {clean(md.get('context'))}",
            "",
            "Risk Context:",
            f"- State: {clean(r.get('state'))}",
            f"- Reason: {clean(r.get('reason'))}",
            "",
            "Scenario:",
            f"- Interest: {clean(p.get('scenario', {}).get('interest'))}",
            f"- Invalidation: {clean(p.get('scenario', {}).get('invalidation'))}",
            f"- Target: {clean(p.get('scenario', {}).get('target'))}",
            "",
            "Explanation:",
            f"- Reason: {clean(x.get('reason'))}",
            f"- Context: {clean(x.get('context_explanation'))}",
            f"- Confidence: {clean(x.get('confidence_explanation'))}",
            f"- Risk: {clean(x.get('risk_explanation'))}",
            "",
            f"Timestamp: {timestamp}",
        ])

    return "\n".join([
        "NDSP PRO Decision Update",
        "",
        f"Symbol: {symbol}",
        f"Market State: {direction}",
        f"Confidence: {confidence}%",
        "",
        "System:",
        f"- State: {clean(st.get('system_state'))}",
        f"- Risk: {clean(st.get('risk_state'))}",
        f"- Position: {clean(st.get('position_state'))}",
        f"- Lifecycle: {clean(e.get('lifecycle'))}",
        "",
        "market_alignment Context:",
        f"- Signal: {clean(n.get('signal'))}",
        f"- Position: {clean(n.get('position'))}",
        "",
        "Momentum Context:",
        f"- Signal: {clean(md.get('signal'))}",
        f"- Effect: {clean(md.get('confidence_effect'))}",
        "",
        "Risk Context:",
        f"- State: {clean(r.get('state'))}",
        f"- Reason: {clean(r.get('reason'))}",
        "",
        "Explanation:",
        f"- {clean(x.get('reason'))}",
        "",
        f"Timestamp: {timestamp}",
    ])

def send_telegram(text, chat_id=None):
    if not TELEGRAM_ENABLED:
        return False, "disabled"

    if not TELEGRAM_TOKEN:
        return False, "missing_token"

    targets = []
    if chat_id:
        targets = [chat_id]
    elif TELEGRAM_CHAT_IDS:
        targets = TELEGRAM_CHAT_IDS

    if not targets:
        return False, "missing_chat_ids"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    results = []
    for target in targets:
        try:
            rr = requests.post(url, data={"chat_id": target, "text": text}, timeout=20)
            if rr.status_code >= 400:
                results.append(f"{target}:fail")
            else:
                results.append(f"{target}:ok")
        except Exception:
            results.append(f"{target}:error")

    return True, ",".join(results)


def send_tiered_telegram(payload):
    results = []

    if TELEGRAM_FREE_CHAT_ID:
        ok, reason = send_telegram(build_message(payload, "free"), TELEGRAM_FREE_CHAT_ID)
        results.append(f"free={ok}:{reason}")

    if TELEGRAM_PRO_CHAT_ID:
        ok, reason = send_telegram(build_message(payload, "pro"), TELEGRAM_PRO_CHAT_ID)
        results.append(f"pro={ok}:{reason}")

    if TELEGRAM_VIP_CHAT_ID:
        ok, reason = send_telegram(build_message(payload, "vip"), TELEGRAM_VIP_CHAT_ID)
        results.append(f"vip={ok}:{reason}")

    if not results:
        ok, reason = send_telegram(build_message(payload, "pro"))
        results.append(f"legacy={ok}:{reason}")

    return True, " | ".join(results)

def loop():
    logging.info("worker started")
    while True:
        state = load_state()
        for symbol in SYMBOLS:
            try:
                p = fetch_decision(symbol)
                ok_payload, payload_reason = valid_payload(p)
                if not ok_payload:
                    logging.warning("invalid payload symbol=%s reason=%s payload=%s", symbol, payload_reason, str(p)[:500])
                    continue

                h = make_hash(p)
                old = state.get(symbol, {})
                last = float(old.get("last_sent", 0))

                if old.get("hash") == h and time.time() - last < DUP_WINDOW:
                    logging.info("duplicate skipped symbol=%s", symbol)
                    continue

                ok, reason = send_tiered_telegram(p)
                state[symbol] = {"hash": h, "last_sent": time.time(), "sent": ok, "reason": reason, "updated_at": now_iso()}
                save_state(state)
                logging.info("telegram symbol=%s sent=%s reason=%s", symbol, ok, reason)

            except Exception as ex:
                logging.exception("error symbol=%s %s", symbol, ex)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    loop()
