cat > ~/ndsp_fix_delivery_ws_final_v2.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail

TASK_NAME="NDSP_FIX_DELIVERY_WS_FINAL_V2"
STAMP="$(date +%Y%m%d_%H%M%S)"

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
APP="$BACKEND/app"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups/${TASK_NAME}_${STAMP}"
REPORT="$REPORT_DIR/${TASK_NAME}_${STAMP}.md"

API_BASE="http://127.0.0.1:9001"

PY="$BACKEND/venv/bin/python"
if [ ! -x "$PY" ]; then
  PY="python3"
fi

mkdir -p "$REPORT_DIR" "$BACKUP_DIR"

log() {
  echo "$@" | tee -a "$REPORT"
}

section() {
  echo "" | tee -a "$REPORT"
  echo "$1" | tee -a "$REPORT"
  echo "------------------------------------------------------------" | tee -a "$REPORT"
}

{
  echo "# $TASK_NAME"
  echo "- STAMP=$STAMP"
  echo "- ROOT=$ROOT"
  echo "- BACKEND=$BACKEND"
  echo "- REPORT=$REPORT"
  echo "- BACKUP_DIR=$BACKUP_DIR"
} | tee "$REPORT"

section "1) Preconditions"

for p in "$ROOT" "$BACKEND" "$APP"; do
  if [ ! -d "$p" ]; then
    log "ERROR: missing path: $p"
    exit 1
  fi
  log "PATH_OK=$p"
done

log "PRECONDITIONS_OK=True"

section "2) Discover systemd environment without leaking secrets"

if systemctl list-unit-files ndsp-api.service >/dev/null 2>&1; then
  systemctl show ndsp-api.service -p Environment -p EnvironmentFiles | sed \
    -e 's/\(TOKEN=\)[^ ]*/\1***REDACTED***/g' \
    -e 's/\(PASS=\)[^ ]*/\1***REDACTED***/g' \
    -e 's/\(KEY=\)[^ ]*/\1***REDACTED***/g' \
    -e 's/\(SECRET=\)[^ ]*/\1***REDACTED***/g' \
    | tee -a "$REPORT"
else
  log "NDSP_API_SERVICE_FOUND=False"
fi

section "3) Telegram token diagnosis"

TELEGRAM_REAL_SEND=SKIPPED
TELEGRAM_GETME=SKIPPED
TELEGRAM_REASON=""

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-${BOT_TOKEN:-}}"
CHAT_ID="${TELEGRAM_CHAT_ID:-${OWNER_TELEGRAM_CHAT_ID:-${CHAT_ID:-}}}"

if [ -z "$BOT_TOKEN" ]; then
  TELEGRAM_REASON="MISSING_BOT_TOKEN_ENV"
elif [ -z "$CHAT_ID" ]; then
  TELEGRAM_REASON="MISSING_CHAT_ID_ENV"
else
  GETME_CODE="$(curl -sS -o /tmp/ndsp_tg_getme.json -w '%{http_code}' --max-time 15 \
    "https://api.telegram.org/bot${BOT_TOKEN}/getMe" || true)"

  log "TELEGRAM_GETME_HTTP_CODE=$GETME_CODE"

  if [ "$GETME_CODE" = "200" ] && grep -q '"ok":true' /tmp/ndsp_tg_getme.json; then
    TELEGRAM_GETME=True

    MSG="NDSP backend closure test ${STAMP}: Telegram delivery OK. decision_support_only."
    SEND_CODE="$(curl -sS -o /tmp/ndsp_tg_send.json -w '%{http_code}' --max-time 20 \
      -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      -d "chat_id=${CHAT_ID}" \
      --data-urlencode "text=${MSG}" || true)"

    log "TELEGRAM_SEND_HTTP_CODE=$SEND_CODE"

    if [ "$SEND_CODE" = "200" ] && grep -q '"ok":true' /tmp/ndsp_tg_send.json; then
      TELEGRAM_REAL_SEND=True
    else
      TELEGRAM_REAL_SEND=False
      TELEGRAM_REASON="SEND_FAILED_CHECK_CHAT_ID_OR_BOT_PERMISSION"
    fi
  else
    TELEGRAM_GETME=False
    TELEGRAM_REAL_SEND=False
    TELEGRAM_REASON="INVALID_BOT_TOKEN_OR_NOT_LOADED"
  fi
fi

log "TELEGRAM_GETME=$TELEGRAM_GETME"
log "TELEGRAM_REAL_SEND=$TELEGRAM_REAL_SEND"
log "TELEGRAM_REASON=$TELEGRAM_REASON"

section "4) Email SMTP diagnosis"

EMAIL_REAL_SEND=SKIPPED
EMAIL_REASON=""

SMTP_HOST="${SMTP_HOST:-}"
SMTP_PORT="${SMTP_PORT:-587}"
SMTP_USER="${SMTP_USER:-${EMAIL_USER:-}}"
SMTP_PASS="${SMTP_PASS:-${EMAIL_PASS:-}}"
SMTP_FROM="${SMTP_FROM:-$SMTP_USER}"
SMTP_TO="${SMTP_TO:-${OWNER_EMAIL:-nawaf.barrak.911@gmail.com}}"

if [ -z "$SMTP_HOST" ]; then
  EMAIL_REASON="MISSING_SMTP_HOST"
elif [ -z "$SMTP_USER" ]; then
  EMAIL_REASON="MISSING_SMTP_USER"
elif [ -z "$SMTP_PASS" ]; then
  EMAIL_REASON="MISSING_SMTP_PASS"
else
  set +e
  "$PY" - <<PY > /tmp/ndsp_email_final.out 2>&1
import os, smtplib, ssl
from email.message import EmailMessage

host=os.environ.get("SMTP_HOST")
port=int(os.environ.get("SMTP_PORT","587"))
user=os.environ.get("SMTP_USER") or os.environ.get("EMAIL_USER")
password=os.environ.get("SMTP_PASS") or os.environ.get("EMAIL_PASS")
sender=os.environ.get("SMTP_FROM") or user
to=os.environ.get("SMTP_TO") or os.environ.get("OWNER_EMAIL") or "nawaf.barrak.911@gmail.com"

msg=EmailMessage()
msg["Subject"]="NDSP backend closure email test"
msg["From"]=sender
msg["To"]=to
msg.set_content("NDSP backend closure test: Email delivery OK. decision_support_only.")

if port == 465:
    with smtplib.SMTP_SSL(host, port, timeout=20) as s:
        s.login(user, password)
        s.send_message(msg)
else:
    with smtplib.SMTP(host, port, timeout=20) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(user, password)
        s.send_message(msg)

print("EMAIL_SENT_OK=True")
PY
  EMAIL_RC=$?
  set -e

  sed -e 's/[A-Za-z0-9._%+-]\+@[A-Za-z0-9.-]\+\.[A-Za-z]\{2,\}/***EMAIL_REDACTED***/g' /tmp/ndsp_email_final.out | tee -a "$REPORT" || true

  if [ "$EMAIL_RC" = "0" ] && grep -q "EMAIL_SENT_OK=True" /tmp/ndsp_email_final.out; then
    EMAIL_REAL_SEND=True
  else
    EMAIL_REAL_SEND=False
    EMAIL_REASON="SMTP_SEND_FAILED"
  fi
fi

log "EMAIL_REAL_SEND=$EMAIL_REAL_SEND"
log "EMAIL_REASON=$EMAIL_REASON"

section "5) WebSocket route and auth discovery"

curl -sk -o /tmp/ndsp_openapi.json --max-time 10 "$API_BASE/openapi.json" || true

"$PY" - <<'PY' /tmp/ndsp_openapi.json | tee -a "$REPORT" || true
import json, sys
try:
    data=json.load(open(sys.argv[1]))
except Exception as e:
    print("OPENAPI_PARSE=False", e)
    raise SystemExit(0)

paths=sorted(data.get("paths",{}).keys())
for p in paths:
    if "ws" in p.lower() or "websocket" in p.lower() or "ticker" in p.lower() or "live" in p.lower():
        print("WS_RELATED_PATH=", p)
PY

grep -RInE "WebSocket|websocket|Depends|admin|token|origin|403|ticker" "$APP/api" "$APP/core" "$APP/services" 2>/dev/null \
  | head -120 \
  | sed -e 's/token=[^ ,)]*/token=***REDACTED***/g' \
  | tee -a "$REPORT" || true

section "6) WebSocket connection attempts with trusted headers"

WEBSOCKET_REAL_TEST=False

set +e
"$PY" - <<'PY' > /tmp/ndsp_ws_final.out 2>&1
import asyncio, json

candidates = [
    "ws://127.0.0.1:9001/ws/ticker",
    "ws://127.0.0.1:9001/ws/ticker?symbol=BTCUSDT",
    "ws://127.0.0.1:9001/ws",
    "ws://127.0.0.1:9001/ws?symbol=BTCUSDT",
    "ws://127.0.0.1:9001/api/ws/ticker",
    "ws://127.0.0.1:9001/api/ws/ticker?symbol=BTCUSDT",
    "ws://127.0.0.1:9001/api/v6/ws/ticker",
    "ws://127.0.0.1:9001/api/v6/ws/ticker?symbol=BTCUSDT",
    "ws://127.0.0.1:9001/live",
    "ws://127.0.0.1:9001/live?symbol=BTCUSDT",
]

headers = [
    ("Origin", "https://my.ndsp.app"),
    ("User-Agent", "NDSP-Backend-Closure-Test"),
    ("X-NDSP-Internal", "true"),
]

async def main():
    try:
        import websockets
    except Exception as e:
        print("WEBSOCKET_IMPORT_OK=False", e)
        return 2

    print("WEBSOCKET_IMPORT_OK=True")

    for url in candidates:
        try:
            async with websockets.connect(
                url,
                additional_headers=headers,
                open_timeout=6,
                close_timeout=2,
            ) as ws:
                print(f"WEBSOCKET_CONNECTED={url}")
                for payload in [
                    {"type":"ping"},
                    {"symbol":"BTCUSDT"},
                    {"type":"subscribe","symbol":"BTCUSDT"},
                    {"action":"subscribe","symbol":"BTCUSDT"},
                ]:
                    try:
                        await ws.send(json.dumps(payload))
                    except Exception:
                        pass
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=5)
                        print("WEBSOCKET_MESSAGE_RECEIVED=True")
                        print("WEBSOCKET_MESSAGE_PREVIEW=", str(msg)[:300])
                        return 0
                    except Exception:
                        continue
                print("WEBSOCKET_CONNECTED_NO_MESSAGE=True")
                return 0
        except Exception as e:
            print(f"WEBSOCKET_CONNECT_FAILED={url} error={e}")

    return 1

raise SystemExit(asyncio.run(main()))
PY
WS_RC=$?
set -e

cat /tmp/ndsp_ws_final.out | tee -a "$REPORT" || true

if [ "$WS_RC" = "0" ] && grep -q "WEBSOCKET_CONNECTED=" /tmp/ndsp_ws_final.out; then
  WEBSOCKET_REAL_TEST=True
fi

log "WEBSOCKET_REAL_TEST=$WEBSOCKET_REAL_TEST"
log "WEBSOCKET_RC=$WS_RC"

section "7) Final status"

if [ "$WEBSOCKET_REAL_TEST" = "True" ]; then
  log "ASSERT_OK=True"
  if [ "$TELEGRAM_REAL_SEND" = "True" ] && [ "$EMAIL_REAL_SEND" = "True" ]; then
    log "FINAL_STATUS=DELIVERY_AND_WEBSOCKET_FULLY_CLOSED"
  else
    log "FINAL_STATUS=WEBSOCKET_CLOSED_TELEGRAM_OR_EMAIL_NEEDS_ENV_FIX"
  fi
else
  log "ASSERT_OK=False"
  log "FINAL_STATUS=WEBSOCKET_STILL_BLOCKED_REVIEW_ROUTE_OR_AUTH"
  exit 1
fi

log "REPORT=$REPORT"
log "BACKUP_DIR=$BACKUP_DIR"
log "DONE"
SH

chmod +x ~/ndsp_fix_delivery_ws_final_v2.sh
bash ~/ndsp_fix_delivery_ws_final_v2.sh
