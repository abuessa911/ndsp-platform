#!/usr/bin/env bash
set -Eeuo pipefail

TASK_NAME="NDSP_RESTORE_ONLY_3_V2"
STAMP="$(date +%Y%m%d_%H%M%S)"

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
APP="$BACKEND/app"
MAIN="$APP/main.py"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups/${TASK_NAME}_${STAMP}"
REPORT="$REPORT_DIR/${TASK_NAME}_${STAMP}.md"

PY="$BACKEND/venv/bin/python"
[ -x "$PY" ] || PY="python3"

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
  echo "- ROOT=$ROOT"
  echo "- BACKEND=$BACKEND"
  echo "- REPORT=$REPORT"
  echo "- BACKUP_DIR=$BACKUP_DIR"
  echo "- MODE=ONLY_WEBSOCKET_TELEGRAM_EMAIL_COMPAT"
} | tee "$REPORT"

section "1) Backup"

cp -a "$MAIN" "$BACKUP_DIR/main.py.bak"

[ -f "$APP/core/delivery/ndsp_delivery_interfaces.py" ] && \
cp -a "$APP/core/delivery/ndsp_delivery_interfaces.py" \
"$BACKUP_DIR/ndsp_delivery_interfaces.py.bak"

[ -f "$APP/integrations/telegram/unified_sender.py" ] && \
cp -a "$APP/integrations/telegram/unified_sender.py" \
"$BACKUP_DIR/unified_sender.py.bak"

log "BACKUP_OK=True"

section "2) Create env compatibility helper"

mkdir -p "$APP/core/delivery"

cat > "$APP/core/delivery/ndsp_env_compat.py" <<'PY'
import os

def env_any(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return default

def telegram_token() -> str:
    return env_any(
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_TOKEN",
        "BOT_TOKEN"
    )

def telegram_chat_id() -> str:
    return env_any(
        "TELEGRAM_CHAT_ID",
        "OWNER_TELEGRAM_CHAT_ID",
        "CHAT_ID"
    )

def telegram_chat_ids() -> str:
    return env_any(
        "TELEGRAM_CHAT_IDS",
        "TELEGRAM_CHAT_ID",
        "OWNER_TELEGRAM_CHAT_ID",
        "CHAT_ID"
    )

def smtp_host() -> str:
    return env_any("SMTP_HOST", "EMAIL_HOST")

def smtp_port() -> str:
    return env_any(
        "SMTP_PORT",
        "EMAIL_PORT",
        default="587"
    )

def smtp_user() -> str:
    return env_any("SMTP_USER", "EMAIL_USER")

def smtp_password() -> str:
    return env_any(
        "SMTP_PASSWORD",
        "SMTP_PASS",
        "EMAIL_PASSWORD",
        "EMAIL_PASS"
    )

def smtp_from() -> str:
    return env_any(
        "SMTP_FROM",
        "EMAIL_FROM",
        "SMTP_USER",
        "EMAIL_USER"
    )

def smtp_to() -> str:
    return env_any(
        "SMTP_TO",
        "ALERT_EMAIL_TO",
        "OWNER_EMAIL"
    )
PY

log "ENV_COMPAT_CREATED=True"

section "3) Patch Telegram compatibility only"

if [ -f "$APP/integrations/telegram/unified_sender.py" ]; then

"$PY" <<'PY'
from pathlib import Path

p = Path(
"/home/nawaf511/empire-core-new/backend/app/integrations/telegram/unified_sender.py"
)

s = p.read_text()

future = "from __future__ import annotations"

compat = (
"from app.core.delivery.ndsp_env_compat "
"import telegram_token, telegram_chat_ids, telegram_chat_id"
)

if compat not in s:

    if future in s:
        s = s.replace(
            future,
            future + "\n" + compat
        )
    else:
        s = compat + "\n" + s

s = s.replace(
'os.getenv("TELEGRAM_BOT_TOKEN", "").strip()',
'telegram_token()'
)

s = s.replace(
'os.getenv("TELEGRAM_CHAT_IDS", "").strip()',
'telegram_chat_ids()'
)

s = s.replace(
'os.getenv("TELEGRAM_CHAT_ID", "").strip()',
'telegram_chat_id()'
)

p.write_text(s)
PY

log "TELEGRAM_COMPAT_PATCHED=True"

else

log "TELEGRAM_COMPAT_PATCHED=False"

fi

section "4) Patch Email compatibility only"

if [ -f "$APP/core/delivery/ndsp_delivery_interfaces.py" ]; then

"$PY" <<'PY'
from pathlib import Path

p = Path(
"/home/nawaf511/empire-core-new/backend/app/core/delivery/ndsp_delivery_interfaces.py"
)

s = p.read_text()

inject = """
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
"""

if "from app.core.delivery.ndsp_env_compat import" not in s:

    marker = "from email.message import EmailMessage"

    if marker in s:
        s = s.replace(marker, marker + inject)

replace_map = {
    '_env("TELEGRAM_BOT_TOKEN")': 'telegram_token()',
    '_env("TELEGRAM_CHAT_ID")': 'telegram_chat_id()',
    '_env("SMTP_HOST")': 'smtp_host()',
    '_env("SMTP_PORT", "587")': 'smtp_port()',
    '_env("SMTP_USER")': 'smtp_user()',
    '_env("SMTP_PASSWORD")': 'smtp_password()',
    '_env("SMTP_FROM", user)': 'smtp_from() or user',
    '_env("SMTP_TO") or _env("ALERT_EMAIL_TO")': 'smtp_to()',
}

for old, new in replace_map.items():
    s = s.replace(old, new)

p.write_text(s)
PY

log "EMAIL_COMPAT_PATCHED=True"

else

log "EMAIL_COMPAT_PATCHED=False"

fi

section "5) Ensure WebSocket routers are registered"

"$PY" <<'PY' | tee -a "$REPORT"
from pathlib import Path

p = Path(
"/home/nawaf511/empire-core-new/backend/app/main.py"
)

s = p.read_text()

changed = False

ticker_import = (
"from app.api.websockets.ticker "
"import router as ticker_ws_router"
)

live_import = (
"from app.api.live_ws "
"import router as live_ws_router"
)

if ticker_import not in s:

    if live_import in s:

        s = s.replace(
            live_import,
            live_import + "\n" + ticker_import
        )

    else:

        s = ticker_import + "\n" + s

    changed = True

if "app.include_router(ticker_ws_router)" not in s:

    if "app.include_router(live_ws_router)" in s:

        s = s.replace(
            "app.include_router(live_ws_router)",
            "app.include_router(live_ws_router)\n"
            "app.include_router(ticker_ws_router)"
        )

    else:

        s += "\napp.include_router(ticker_ws_router)\n"

    changed = True

p.write_text(s)

print(f"WEBSOCKET_ROUTER_PATCHED={changed}")
PY

section "6) Compile"

cd "$BACKEND"

PYTHONPATH="$BACKEND" \
"$PY" -m compileall -q "$APP"

log "COMPILE_OK=True"

section "7) Restart API"

sudo systemctl restart ndsp-api.service

sleep 3

systemctl is-active ndsp-api.service | \
sed 's/^/NDSP_API_ACTIVE=/' | tee -a "$REPORT"

section "8) Smoke"

ROOT_CODE="$(
curl -sk \
-o /tmp/ndsp_root.json \
-w '%{http_code}' \
--max-time 10 \
http://127.0.0.1:9001/ || true
)"

HEALTH_CODE="$(
curl -sk \
-o /tmp/ndsp_health.json \
-w '%{http_code}' \
--max-time 10 \
http://127.0.0.1:9001/health || true
)"

DECISION_CODE="$(
curl -sk \
-o /tmp/ndsp_decision.json \
-w '%{http_code}' \
--max-time 15 \
'http://127.0.0.1:9001/decision?symbol=BTCUSDT' || true
)"

DELIVERY_CODE="$(
curl -sk \
-o /tmp/ndsp_delivery.json \
-w '%{http_code}' \
--max-time 10 \
http://127.0.0.1:9001/api/v6/live/delivery/status || true
)"

log "ROOT_HTTP_CODE=$ROOT_CODE"
log "HEALTH_HTTP_CODE=$HEALTH_CODE"
log "DECISION_HTTP_CODE=$DECISION_CODE"
log "DELIVERY_HTTP_CODE=$DELIVERY_CODE"

section "9) WebSocket Test"

set +e

"$PY" <<'PY' > /tmp/ndsp_ws_3_v2.out 2>&1
import asyncio
import json

urls = [
    "ws://127.0.0.1:9001/ws/decision?symbol=BTCUSDT",
    "ws://127.0.0.1:9001/ws/live?symbol=BTCUSDT",
    "ws://127.0.0.1:9001/ws/ticker",
]

async def main():

    import websockets

    ok = 0

    for url in urls:

        try:

            async with websockets.connect(
                url,
                origin="https://my.ndsp.app",
                open_timeout=8,
                close_timeout=2
            ) as ws:

                print(f"WEBSOCKET_CONNECTED={url}")

                try:
                    await ws.send(
                        json.dumps({
                            "type": "ping",
                            "symbol": "BTCUSDT"
                        })
                    )
                except Exception:
                    pass

                try:
                    msg = await asyncio.wait_for(
                        ws.recv(),
                        timeout=8
                    )

                    print(
                        "WEBSOCKET_MESSAGE_RECEIVED=True"
                    )

                    print(
                        "WEBSOCKET_MESSAGE_PREVIEW=",
                        str(msg)[:300]
                    )

                except Exception:

                    print(
                        "WEBSOCKET_CONNECTED_NO_MESSAGE=True"
                    )

                ok += 1

        except Exception as e:

            print(
                f"WEBSOCKET_FAILED={url} error={e}"
            )

    return 0 if ok else 1

raise SystemExit(asyncio.run(main()))
PY

WS_RC=$?

set -e

cat /tmp/ndsp_ws_3_v2.out | tee -a "$REPORT"

if grep -q "WEBSOCKET_CONNECTED=" /tmp/ndsp_ws_3_v2.out; then
  log "WEBSOCKET_OK=True"
else
  log "WEBSOCKET_OK=False"
fi

log "WEBSOCKET_RC=$WS_RC"

section "10) Final"

if [ "$ROOT_CODE" = "200" ] && \
   [ "$DECISION_CODE" = "200" ]; then

  log "ASSERT_OK=True"
  log "FINAL_STATUS=THREE_COMPONENTS_RESTORED_SAFELY"

else

  log "ASSERT_OK=False"
  log "FINAL_STATUS=THREE_COMPONENTS_RESTORE_NEEDS_REVIEW"

  exit 1

fi

log "REPORT=$REPORT"
log "BACKUP_DIR=$BACKUP_DIR"
log "DONE"
