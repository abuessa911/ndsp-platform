#!/usr/bin/env bash
set -Eeuo pipefail

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_API_NGINX_LINK_$(date +%Y%m%d_%H%M%S).md"
STAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  echo "FAILED=True"
  echo "REPORT=$REPORT"
  exit 1
}

log "# NDSP Checkout API Nginx Link"
log "- TIME=$(date -Is)"

if ! systemctl is-active --quiet ndsp-checkout-api.service; then
  fail "ndsp-checkout-api.service is not active"
fi

LOCAL_HEALTH="$(curl -s -o /tmp/ndsp_checkout_local_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
LOCAL_PLANS="$(curl -s -o /tmp/ndsp_checkout_local_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "LOCAL_HEALTH_HTTP_CODE=$LOCAL_HEALTH"
log "LOCAL_PLANS_HTTP_CODE=$LOCAL_PLANS"

[ "$LOCAL_HEALTH" = "200" ] || fail "Local checkout health failed"
[ "$LOCAL_PLANS" = "200" ] || fail "Local checkout plans failed"

log "LOCAL_API_OK=True"

NGINX_FILES="$(grep -Rsl 'server_name .*api\.ndsp\.app\|server_name api\.ndsp\.app' /etc/nginx/sites-available /etc/nginx/conf.d 2>/dev/null || true)"

if [ -z "$NGINX_FILES" ]; then
  fail "Could not find nginx config for api.ndsp.app"
fi

TARGET_FILE="$(echo "$NGINX_FILES" | head -1)"
BACKUP_FILE="${TARGET_FILE}.bak_checkout_api_${STAMP}"

sudo cp "$TARGET_FILE" "$BACKUP_FILE"

log "NGINX_TARGET_FILE=$TARGET_FILE"
log "NGINX_BACKUP_FILE=$BACKUP_FILE"

if sudo grep -q 'NDSP_CHECKOUT_API_PROXY_BEGIN' "$TARGET_FILE"; then
  log "NGINX_BLOCK_ALREADY_EXISTS=True"
else
  sudo python3 - "$TARGET_FILE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()

block = r'''

    # NDSP_CHECKOUT_API_PROXY_BEGIN
    location /checkout-api/ {
        proxy_pass http://127.0.0.1:8088/;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 15s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    # NDSP_CHECKOUT_API_PROXY_END
'''

insert_pos = text.rfind("\n}")
if insert_pos == -1:
    raise SystemExit("Could not find closing server brace")

text = text[:insert_pos] + block + text[insert_pos:]
path.write_text(text)
PY
  log "NGINX_BLOCK_INSERTED=True"
fi

sudo nginx -t
log "NGINX_CONFIG_OK=True"

sudo systemctl reload nginx
log "NGINX_RELOAD_OK=True"

sleep 2

REMOTE_HEALTH="$(curl -k -s -o /tmp/ndsp_checkout_remote_health.json -w '%{http_code}' https://api.ndsp.app/checkout-api/health || true)"
REMOTE_PLANS="$(curl -k -s -o /tmp/ndsp_checkout_remote_plans.json -w '%{http_code}' https://api.ndsp.app/checkout-api/api/v1/plans || true)"

log "REMOTE_HEALTH_HTTP_CODE=$REMOTE_HEALTH"
log "REMOTE_PLANS_HTTP_CODE=$REMOTE_PLANS"

if [ "$REMOTE_HEALTH" != "200" ]; then
  log "REMOTE_HEALTH_BODY=$(cat /tmp/ndsp_checkout_remote_health.json 2>/dev/null || true)"
  fail "Remote checkout health failed"
fi

if [ "$REMOTE_PLANS" != "200" ]; then
  log "REMOTE_PLANS_BODY=$(cat /tmp/ndsp_checkout_remote_plans.json 2>/dev/null || true)"
  fail "Remote checkout plans failed"
fi

log "REMOTE_API_OK=True"
log "FINAL_STATUS=NDSP_CHECKOUT_API_NGINX_LINKED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_API_NGINX_LINKED"
echo "REPORT=$REPORT"
echo ""
echo "Test:"
echo "curl https://api.ndsp.app/checkout-api/health"
echo "curl https://api.ndsp.app/checkout-api/api/v1/plans"
