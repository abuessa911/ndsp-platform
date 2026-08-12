#!/usr/bin/env bash
set -Eeuo pipefail

TELEGRAM_ENV="/etc/ndsp/ndsp-telegram.env"
STATE_DIR="/var/lib/ndsp"
STATE_FILE="$STATE_DIR/telegram_health_state"
LOCK_FILE="/tmp/ndsp_telegram_health_alert.lock"

mkdir -p "$STATE_DIR"

exec 9>"$LOCK_FILE"
flock -n 9 || exit 0

if [[ ! -f "$TELEGRAM_ENV" ]]; then
  exit 0
fi

set +u
source "$TELEGRAM_ENV"
set -u

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-${BOT_TOKEN:-${TG_BOT_TOKEN:-${NDSP_TELEGRAM_BOT_TOKEN:-}}}}}"
CHAT_ID="${TELEGRAM_CHAT_ID:-${TG_CHAT_ID:-${NDSP_TELEGRAM_CHAT_ID:-${TELEGRAM_ADMIN_CHAT_ID:-}}}}"

[[ -n "${BOT_TOKEN:-}" && -n "${CHAT_ID:-}" ]] || exit 0

send_msg(){
  local msg="$1"
  curl -sS --max-time 20 \
    -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${msg}" >/dev/null || true
}

check_code(){
  local url="$1"
  curl -k -sS -L --max-time 15 -o /tmp/ndsp_auto_alert_probe.out -w "%{http_code}" "$url" || true
}

API_CODE="$(check_code "http://127.0.0.1:9001/api/runtime/health")"
SEATS_CODE="$(check_code "https://my.ndsp.app/api/seats/status")"
POLICY_CODE="$(check_code "https://my.ndsp.app/api/trial/activation-policy")"
V7_CODE="$(check_code "https://my.ndsp.app/api/v7/trial/activation-policy")"

API_SERVICE_STATE="$(systemctl is-active ndsp-api.service 2>/dev/null || true)"
NGINX_STATE="$(systemctl is-active nginx 2>/dev/null || true)"
PG_STATE="$(systemctl is-active postgresql.service 2>/dev/null || true)"
PORT9001_OWNER="$(lsof -nP -iTCP:9001 -sTCP:LISTEN 2>/dev/null | awk 'NR==2{print $1}' || true)"

STATUS="OK"

[[ "$API_SERVICE_STATE" == "active" ]] || STATUS="BAD"
[[ "$NGINX_STATE" == "active" ]] || STATUS="BAD"
[[ "$PG_STATE" == "active" ]] || STATUS="BAD"
[[ "$API_CODE" == "200" ]] || STATUS="BAD"
[[ "$SEATS_CODE" == "200" ]] || STATUS="BAD"
[[ "$POLICY_CODE" == "200" ]] || STATUS="BAD"
[[ "$V7_CODE" == "404" ]] || STATUS="BAD"
[[ "$PORT9001_OWNER" == "gunicorn" || "$PORT9001_OWNER" == "python" ]] || STATUS="BAD"

PREV_STATUS=""
[[ -f "$STATE_FILE" ]] && PREV_STATUS="$(cat "$STATE_FILE" 2>/dev/null || true)"

# أرسل فقط عند تغير الحالة، أو أول تشغيل
if [[ "$STATUS" != "$PREV_STATUS" ]]; then
  if [[ "$STATUS" == "OK" ]]; then
    send_msg "NDSP health restored ✅
Time: $(date -Is)
API: $API_CODE
Seats: $SEATS_CODE
Policy: $POLICY_CODE
Legacy /api/v7: $V7_CODE
9001 owner: ${PORT9001_OWNER:-NONE}
Services: api=$API_SERVICE_STATE nginx=$NGINX_STATE postgres=$PG_STATE"
  else
    send_msg "NDSP health alert ❌
Time: $(date -Is)
API: $API_CODE
Seats: $SEATS_CODE
Policy: $POLICY_CODE
Legacy /api/v7 expected 404, got: $V7_CODE
9001 owner: ${PORT9001_OWNER:-NONE}
Services: api=$API_SERVICE_STATE nginx=$NGINX_STATE postgres=$PG_STATE"
  fi
fi

echo "$STATUS" > "$STATE_FILE"
