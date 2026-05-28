cat > ~/ndsp_clean_lock_env_and_test_delivery.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail

TASK_NAME="NDSP_CLEAN_LOCK_ENV_AND_TEST_DELIVERY"
STAMP="$(date +%Y%m%d_%H%M%S)"

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
ENV_FILE="$BACKEND/.env"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups/${TASK_NAME}_${STAMP}"
REPORT="$REPORT_DIR/${TASK_NAME}_${STAMP}.md"

PY="$BACKEND/venv/bin/python"
[ -x "$PY" ] || PY="python3"

mkdir -p "$REPORT_DIR" "$BACKUP_DIR"

log(){ echo "$@" | tee -a "$REPORT"; }
section(){ echo "" | tee -a "$REPORT"; echo "$1" | tee -a "$REPORT"; echo "------------------------------------------------------------" | tee -a "$REPORT"; }

redact_file() {
  sed -E \
    -e 's/(TOKEN|KEY|SECRET|PASS|PASSWORD|DATABASE_URL)=.*/\1=***REDACTED***/g' \
    -e 's/[0-9]{8,12}:[A-Za-z0-9_-]{20,}/***TELEGRAM_TOKEN_REDACTED***/g'
}

{
  echo "# $TASK_NAME"
  echo "- ROOT=$ROOT"
  echo "- BACKEND=$BACKEND"
  echo "- ENV_FILE=$ENV_FILE"
  echo "- REPORT=$REPORT"
  echo "- BACKUP_DIR=$BACKUP_DIR"
  echo "- MODE=ENV_CLEAN_LOCK_TEST_ONLY"
} | tee "$REPORT"

section "1) Backup current env and related files"

if [ -f "$ENV_FILE" ]; then
  cp -a "$ENV_FILE" "$BACKUP_DIR/.env.before_clean.bak"
  log "BACKUP_ENV_OK=True"
else
  log "CURRENT_ENV_MISSING=True"
  touch "$ENV_FILE"
fi

for f in \
  "$BACKEND/.env.backup_unify_admin_keys_20260511_204528" \
  "$BACKEND/.env.bak_admin_key_20260508_110835" \
  "$BACKEND/.env.backup_admin_api_key_20260502_002536" \
  "$BACKEND/.telegram_env" \
  "/etc/ndsp/ndsp-api-admin.env"
do
  if [ -f "$f" ]; then
    cp -a "$f" "$BACKUP_DIR/$(echo "$f" | sed 's#/#_#g').bak"
    log "BACKUP_SOURCE_OK=$f"
  fi
done

section "2) Build clean unified .env without printing secrets"

"$PY" <<'PY'
from pathlib import Path
import os
import re

backend = Path("/home/nawaf511/empire-core-new/backend")
env_file = backend / ".env"

sources = [
    backend / ".env",
    backend / ".env.backup_unify_admin_keys_20260511_204528",
    backend / ".env.bak_admin_key_20260508_110835",
    backend / ".env.backup_admin_api_key_20260502_002536",
    backend / ".telegram_env",
    Path("/etc/ndsp/ndsp-api-admin.env"),
]

allowed_keys = [
    "ENV",
    "PYTHONUNBUFFERED",

    "ADMIN_KEY",
    "NDSP_ADMIN_KEY",
    "ADMIN_UI_KEY",

    "DATABASE_URL",

    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_TOKEN",
    "BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "TELEGRAM_CHAT_IDS",
    "OWNER_TELEGRAM_CHAT_ID",
    "TELEGRAM_FREE_CHAT_ID",
    "TELEGRAM_PRO_CHAT_ID",
    "TELEGRAM_VIP_CHAT_ID",
    "TELEGRAM_PRO_CHANNEL",
    "TELEGRAM_ELITE_CHANNEL",

    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASS",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "SMTP_TO",
    "SMTP_ADMIN_TO",
    "ALERT_EMAIL_TO",
    "OWNER_EMAIL",

    "NOWPAYMENTS_API_KEY",
    "NOWPAYMENTS_IPN_SECRET",

    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",

    "MT4_CSV_DIR",
    "MT4_DATA_DIR",

    "CORS_ORIGINS",
    "APP_ENV",
    "LOG_LEVEL",
]

aliases = {
    "TELEGRAM_TOKEN": "TELEGRAM_BOT_TOKEN",
    "BOT_TOKEN": "TELEGRAM_BOT_TOKEN",
    "OWNER_TELEGRAM_CHAT_ID": "TELEGRAM_CHAT_ID",
    "SMTP_PASS": "SMTP_PASSWORD",
    "EMAIL_PASS": "SMTP_PASSWORD",
    "EMAIL_PASSWORD": "SMTP_PASSWORD",
    "EMAIL_USER": "SMTP_USER",
    "EMAIL_HOST": "SMTP_HOST",
    "EMAIL_FROM": "SMTP_FROM",
    "EMAIL_PORT": "SMTP_PORT",
}

env = {}

line_re = re.compile(r'^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)\s*$')

def clean_value(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        v = v[1:-1]
    return v.strip()

for src in sources:
    if not src.exists():
        continue
    for line in src.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = line_re.match(line)
        if not m:
            continue
        k, v = m.group(1), clean_value(m.group(2))
        k = aliases.get(k, k)
        if k not in allowed_keys:
            continue
        if not v:
            continue
        if "REVOKED_TOKEN_DO_NOT_USE" in v or "REPLACE_WITH" in v:
            continue
        env.setdefault(k, v)

env.setdefault("ENV", "production")
env.setdefault("PYTHONUNBUFFERED", "1")
env.setdefault("SMTP_PORT", "587")

if "ADMIN_KEY" in env:
    env.setdefault("NDSP_ADMIN_KEY", env["ADMIN_KEY"])
    env.setdefault("ADMIN_UI_KEY", env["ADMIN_KEY"])
elif "NDSP_ADMIN_KEY" in env:
    env.setdefault("ADMIN_KEY", env["NDSP_ADMIN_KEY"])
    env.setdefault("ADMIN_UI_KEY", env["NDSP_ADMIN_KEY"])

if "TELEGRAM_BOT_TOKEN" in env:
    env.setdefault("TELEGRAM_TOKEN", env["TELEGRAM_BOT_TOKEN"])

if "TELEGRAM_CHAT_ID" in env:
    env.setdefault("TELEGRAM_CHAT_IDS", env["TELEGRAM_CHAT_ID"])

if "SMTP_PASSWORD" in env:
    env.setdefault("SMTP_PASS", env["SMTP_PASSWORD"])

order = [
    "ENV",
    "PYTHONUNBUFFERED",
    "DATABASE_URL",
    "ADMIN_KEY",
    "NDSP_ADMIN_KEY",
    "ADMIN_UI_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_TOKEN",
    "TELEGRAM_CHAT_ID",
    "TELEGRAM_CHAT_IDS",
    "TELEGRAM_FREE_CHAT_ID",
    "TELEGRAM_PRO_CHAT_ID",
    "TELEGRAM_VIP_CHAT_ID",
    "TELEGRAM_PRO_CHANNEL",
    "TELEGRAM_ELITE_CHANNEL",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "SMTP_PASS",
    "SMTP_FROM",
    "SMTP_TO",
    "SMTP_ADMIN_TO",
    "ALERT_EMAIL_TO",
    "OWNER_EMAIL",
    "NOWPAYMENTS_API_KEY",
    "NOWPAYMENTS_IPN_SECRET",
    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",
    "MT4_CSV_DIR",
    "MT4_DATA_DIR",
    "CORS_ORIGINS",
    "APP_ENV",
    "LOG_LEVEL",
]

out = []
out.append("# NDSP Production Environment")
out.append(f"# Cleaned and locked by {os.getenv('USER','ndsp')} at runtime")
out.append("# Do not commit this file.")
out.append("")

for k in order:
    if k in env:
        v = env[k].replace("\n", "").replace("\r", "")
        out.append(f'{k}="{v}"')

for k in sorted(env):
    if k not in order:
        v = env[k].replace("\n", "").replace("\r", "")
        out.append(f'{k}="{v}"')

env_file.write_text("\n".join(out) + "\n")
print("CLEAN_ENV_WRITTEN=True")
print("CLEAN_ENV_KEY_COUNT=", len(env))
print("HAS_TELEGRAM_BOT_TOKEN=", bool(env.get("TELEGRAM_BOT_TOKEN")))
print("HAS_TELEGRAM_CHAT_ID=", bool(env.get("TELEGRAM_CHAT_ID") or env.get("TELEGRAM_CHAT_IDS")))
print("HAS_SMTP_HOST=", bool(env.get("SMTP_HOST")))
print("HAS_SMTP_USER=", bool(env.get("SMTP_USER")))
print("HAS_SMTP_PASSWORD=", bool(env.get("SMTP_PASSWORD") or env.get("SMTP_PASS")))
print("HAS_DATABASE_URL=", bool(env.get("DATABASE_URL")))
PY
log "CLEAN_ENV_BUILD_DONE=True"

section "3) Show clean env keys only"

cut -d= -f1 "$ENV_FILE" | sed 's/^/ENV_KEY=/' | tee -a "$REPORT"

section "4) Lock .env permissions"

sudo chown nawaf511:www-data "$ENV_FILE"
sudo chmod 640 "$ENV_FILE"

log "ENV_OWNER=$(stat -c '%U:%G' "$ENV_FILE")"
log "ENV_PERMS=$(stat -c '%a' "$ENV_FILE")"

section "5) Protect old env backups permissions"

find "$BACKEND" -maxdepth 1 -type f \( -name ".env.*" -o -name ".telegram_env" \) -print0 \
| while IFS= read -r -d '' f; do
    sudo chown nawaf511:www-data "$f" || true
    sudo chmod 600 "$f" || true
    log "OLD_ENV_LOCKED=$f"
  done

section "6) Restart API with clean env"

sudo systemctl daemon-reload
sudo systemctl restart ndsp-api.service
sleep 4

systemctl is-active ndsp-api.service | sed 's/^/NDSP_API_ACTIVE=/' | tee -a "$REPORT"

ROOT_CODE="$(curl -sk -o /tmp/ndsp_env_root.json -w '%{http_code}' --max-time 10 http://127.0.0.1:9001/ || true)"
HEALTH_CODE="$(curl -sk -o /tmp/ndsp_env_health.json -w '%{http_code}' --max-time 10 http://127.0.0.1:9001/health || true)"
DECISION_CODE="$(curl -sk -o /tmp/ndsp_env_decision.json -w '%{http_code}' --max-time 15 'http://127.0.0.1:9001/decision?symbol=BTCUSDT' || true)"
DELIVERY_CODE="$(curl -sk -o /tmp/ndsp_env_delivery.json -w '%{http_code}' --max-time 10 http://127.0.0.1:9001/api/v6/live/delivery/status || true)"

log "ROOT_HTTP_CODE=$ROOT_CODE"
log "HEALTH_HTTP_CODE=$HEALTH_CODE"
log "DECISION_HTTP_CODE=$DECISION_CODE"
log "DELIVERY_HTTP_CODE=$DELIVERY_CODE"

section "7) Telegram real send test"

set +e
"$PY" <<'PY' > /tmp/ndsp_env_telegram_test.out 2>&1
import os
import urllib.parse
import urllib.request
import json

token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN")
chat = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("OWNER_TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID")

print("TELEGRAM_TOKEN_PRESENT=", bool(token))
print("TELEGRAM_CHAT_PRESENT=", bool(chat))

if not token:
    print("TELEGRAM_REAL_SEND=SKIPPED_NO_TOKEN")
    raise SystemExit(0)

getme_url = f"https://api.telegram.org/bot{token}/getMe"
try:
    with urllib.request.urlopen(getme_url, timeout=15) as r:
        body = r.read().decode()
        print("TELEGRAM_GETME_HTTP_CODE=", r.status)
        ok = '"ok":true' in body
        print("TELEGRAM_GETME_OK=", ok)
except Exception as e:
    print("TELEGRAM_GETME_OK=False")
    print("TELEGRAM_REASON=GETME_FAILED_OR_INVALID_TOKEN")
    raise SystemExit(0)

if not chat:
    print("TELEGRAM_REAL_SEND=SKIPPED_NO_CHAT_ID")
    raise SystemExit(0)

data = urllib.parse.urlencode({
    "chat_id": chat,
    "text": "NDSP production env locked: Telegram delivery test OK. decision_support_only."
}).encode()

try:
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        body = r.read().decode()
        print("TELEGRAM_SEND_HTTP_CODE=", r.status)
        print("TELEGRAM_REAL_SEND=", '"ok":true' in body)
except Exception as e:
    print("TELEGRAM_REAL_SEND=False")
    print("TELEGRAM_REASON=SEND_FAILED")
PY
TG_RC=$?
set -e

cat /tmp/ndsp_env_telegram_test.out | redact_file | tee -a "$REPORT"
log "TELEGRAM_TEST_RC=$TG_RC"

section "8) SMTP real send test"

set +e
"$PY" <<'PY' > /tmp/ndsp_env_smtp_test.out 2>&1
import os
import smtplib
import ssl
from email.message import EmailMessage

host = os.getenv("SMTP_HOST") or os.getenv("EMAIL_HOST")
port = int(os.getenv("SMTP_PORT") or os.getenv("EMAIL_PORT") or "587")
user = os.getenv("SMTP_USER") or os.getenv("EMAIL_USER")
password = os.getenv("SMTP_PASSWORD") or os.getenv("SMTP_PASS") or os.getenv("EMAIL_PASS") or os.getenv("EMAIL_PASSWORD")
sender = os.getenv("SMTP_FROM") or os.getenv("EMAIL_FROM") or user
to = os.getenv("SMTP_TO") or os.getenv("ALERT_EMAIL_TO") or os.getenv("OWNER_EMAIL")

print("SMTP_HOST_PRESENT=", bool(host))
print("SMTP_USER_PRESENT=", bool(user))
print("SMTP_PASSWORD_PRESENT=", bool(password))
print("SMTP_TO_PRESENT=", bool(to))

if not all([host, user, password, sender, to]):
    print("SMTP_REAL_SEND=SKIPPED_MISSING_ENV")
    raise SystemExit(0)

msg = EmailMessage()
msg["Subject"] = "NDSP production env locked"
msg["From"] = sender
msg["To"] = to
msg.set_content("NDSP production env locked: SMTP delivery test OK. decision_support_only.")

try:
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context(), timeout=20) as server:
            server.login(user, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(user, password)
            server.send_message(msg)

    print("SMTP_REAL_SEND=True")
except Exception as e:
    print("SMTP_REAL_SEND=False")
    print("SMTP_REASON=", type(e).__name__)
PY
SMTP_RC=$?
set -e

cat /tmp/ndsp_env_smtp_test.out | redact_file | tee -a "$REPORT"
log "SMTP_TEST_RC=$SMTP_RC"

section "9) WebSocket quick verification"

set +e
"$PY" <<'PY' > /tmp/ndsp_env_ws_test.out 2>&1
import asyncio

async def main():
    import websockets
    urls = [
        "ws://127.0.0.1:9001/ws/decision?symbol=BTCUSDT",
        "ws://127.0.0.1:9001/ws/live?symbol=BTCUSDT",
        "ws://127.0.0.1:9001/ws/ticker",
    ]
    ok = 0
    for url in urls:
        try:
            async with websockets.connect(url, origin="https://my.ndsp.app", open_timeout=8, close_timeout=2) as ws:
                print(f"WEBSOCKET_CONNECTED={url}")
                ok += 1
        except Exception as e:
            print(f"WEBSOCKET_FAILED={url} error={e}")
    print("WEBSOCKET_OK=", ok > 0)
    return 0 if ok else 1

raise SystemExit(asyncio.run(main()))
PY
WS_RC=$?
set -e

cat /tmp/ndsp_env_ws_test.out | tee -a "$REPORT"
log "WEBSOCKET_TEST_RC=$WS_RC"

section "10) Final assertions"

TG_OK=False
SMTP_OK=False
WS_OK=False

grep -q "TELEGRAM_REAL_SEND= True" /tmp/ndsp_env_telegram_test.out || grep -q "TELEGRAM_REAL_SEND= True" /tmp/ndsp_env_telegram_test.out && TG_OK=True
if grep -q "TELEGRAM_REAL_SEND= True" /tmp/ndsp_env_telegram_test.out || grep -q "TELEGRAM_REAL_SEND= True" /tmp/ndsp_env_telegram_test.out || grep -q "TELEGRAM_REAL_SEND= True" /tmp/ndsp_env_telegram_test.out; then
  TG_OK=True
fi
if grep -q "TELEGRAM_REAL_SEND= True" /tmp/ndsp_env_telegram_test.out || grep -q "TELEGRAM_REAL_SEND=True" /tmp/ndsp_env_telegram_test.out; then
  TG_OK=True
fi

if grep -q "SMTP_REAL_SEND=True" /tmp/ndsp_env_smtp_test.out; then
  SMTP_OK=True
fi

if grep -q "WEBSOCKET_OK= True" /tmp/ndsp_env_ws_test.out || grep -q "WEBSOCKET_OK=True" /tmp/ndsp_env_ws_test.out; then
  WS_OK=True
fi

log "TELEGRAM_REAL_SEND_OK=$TG_OK"
log "SMTP_REAL_SEND_OK=$SMTP_OK"
log "WEBSOCKET_OK=$WS_OK"

if [ "$ROOT_CODE" = "200" ] && [ "$DECISION_CODE" = "200" ] && [ "$DELIVERY_CODE" = "200" ] && [ "$WS_OK" = "True" ]; then
  log "ASSERT_OK=True"

  if [ "$TG_OK" = "True" ] && [ "$SMTP_OK" = "True" ]; then
    log "FINAL_STATUS=ENV_CLEANED_LOCKED_AND_DELIVERY_FULLY_VERIFIED"
  else
    log "FINAL_STATUS=ENV_CLEANED_LOCKED_CORE_OK_DELIVERY_ENV_NEEDS_SECRET_ROTATION_OR_SMTP_FIX"
  fi
else
  log "ASSERT_OK=False"
  log "FINAL_STATUS=ENV_LOCK_FAILED_CORE_OR_WS_BROKEN"
  exit 1
fi

log "REPORT=$REPORT"
log "BACKUP_DIR=$BACKUP_DIR"
log "DONE"
SH

chmod +x ~/ndsp_clean_lock_env_and_test_delivery.sh
bash ~/ndsp_clean_lock_env_and_test_delivery.sh
