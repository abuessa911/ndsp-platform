#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
API_ENV="$BACKEND/.env"
SERVICE_NAME="ndsp-checkout-api.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_8088_FIX_$(date +%Y%m%d_%H%M%S).md"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  log ""
  log "=== SYSTEMD STATUS ==="
  sudo systemctl status "$SERVICE_NAME" --no-pager -l >> "$REPORT" 2>&1 || true
  log ""
  log "=== JOURNAL LAST 80 ==="
  sudo journalctl -u "$SERVICE_NAME" -n 80 --no-pager >> "$REPORT" 2>&1 || true
  echo ""
  echo "FAILED=True"
  echo "REPORT=$REPORT"
  exit 1
}

log "# NDSP Checkout API 8088 Service Fix"
log "- TIME=$(date -Is)"
log "- ROOT=$ROOT"
log "- BACKEND=$BACKEND"

[ -d "$BACKEND" ] || fail "Backend directory not found: $BACKEND"
[ -f "$BACKEND/src/server.js" ] || fail "server.js not found"
[ -f "$BACKEND/package.json" ] || fail "package.json not found"
[ -f "$API_ENV" ] || fail ".env not found: $API_ENV"

NODE_BIN="$(command -v node || true)"
NPM_BIN="$(command -v npm || true)"

[ -n "$NODE_BIN" ] || fail "node not found in current shell"
[ -n "$NPM_BIN" ] || fail "npm not found in current shell"

NODE_DIR="$(dirname "$NODE_BIN")"

log "NODE_BIN=$NODE_BIN"
log "NPM_BIN=$NPM_BIN"
log "NODE_VERSION=$(node -v)"
log "NPM_VERSION=$(npm -v)"

cd "$BACKEND"

npm install
node --check src/db.js
node --check src/server.js

log "BACKEND_SYNTAX_OK=True"

if ss -lptn '( sport = :8088 )' | grep -q ':8088'; then
  log "PORT_8088_ALREADY_LISTENING_BEFORE_RESTART=True"
  ss -lptn '( sport = :8088 )' >> "$REPORT" 2>&1 || true
else
  log "PORT_8088_FREE_BEFORE_RESTART=True"
fi

sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
sudo systemctl reset-failed "$SERVICE_NAME" 2>/dev/null || true

sudo tee "$SERVICE_FILE" >/dev/null <<SERVICEEOF
[Unit]
Description=NDSP Checkout Plans Express API
After=network.target

[Service]
Type=simple
User=nawaf511
Group=nawaf511
WorkingDirectory=$BACKEND
EnvironmentFile=$API_ENV
Environment=NODE_ENV=production
Environment=PATH=$NODE_DIR:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin
ExecStart=$NODE_BIN $BACKEND/src/server.js
Restart=always
RestartSec=5
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
SERVICEEOF

log "SERVICE_FILE_REWRITTEN=True"

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

sleep 4

log ""
log "=== SERVICE STATE ==="
sudo systemctl show "$SERVICE_NAME" \
  -p ActiveState \
  -p SubState \
  -p MainPID \
  -p ExecMainStatus \
  -p NRestarts \
  --no-pager >> "$REPORT" 2>&1 || true

if systemctl is-active --quiet "$SERVICE_NAME"; then
  log "SERVICE_ACTIVE=True"
else
  fail "Service is not active after restart"
fi

log ""
log "=== PORT CHECK ==="
ss -lptn '( sport = :8088 )' >> "$REPORT" 2>&1 || true

if ss -lptn '( sport = :8088 )' | grep -q ':8088'; then
  log "PORT_8088_LISTENING=True"
else
  log "PORT_8088_LISTENING=False"
  sudo journalctl -u "$SERVICE_NAME" -n 120 --no-pager >> "$REPORT" 2>&1 || true
  fail "Service active but port 8088 is not listening"
fi

HEALTH_CODE="$(curl -4 -sS -o /tmp/ndsp_checkout_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
PLANS_CODE="$(curl -4 -sS -o /tmp/ndsp_checkout_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "HEALTH_HTTP_CODE=$HEALTH_CODE"
log "PLANS_HTTP_CODE=$PLANS_CODE"

log ""
log "=== HEALTH BODY ==="
cat /tmp/ndsp_checkout_health.json >> "$REPORT" 2>&1 || true

log ""
log "=== PLANS BODY HEAD ==="
head -c 1000 /tmp/ndsp_checkout_plans.json >> "$REPORT" 2>&1 || true
echo "" >> "$REPORT"

if [ "$HEALTH_CODE" != "200" ]; then
  fail "Health endpoint still failed"
fi

if [ "$PLANS_CODE" != "200" ]; then
  fail "Plans endpoint still failed"
fi

log "SMOKE_TEST_OK=True"
log "FINAL_STATUS=NDSP_CHECKOUT_API_8088_READY"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_API_8088_READY"
echo "REPORT=$REPORT"
echo ""
echo "Test:"
echo "curl http://127.0.0.1:8088/health"
echo "curl http://127.0.0.1:8088/api/v1/plans"
