#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
FRONTEND="$ROOT/checkout-admin-vite"
MIGRATION="$ROOT/database/migrations/20260524_001_checkout_plans.sql"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_PLANS_RUN_$(date +%Y%m%d_%H%M%S).md"
API_ENV="$BACKEND/.env"
FRONT_ENV="$FRONTEND/.env"
SERVICE_NAME="ndsp-checkout-api.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  exit 1
}

log "# NDSP Checkout Plans Run"
log "- TIME=$(date -Is)"
log "- ROOT=$ROOT"

[ -d "$ROOT" ] || fail "Package root not found: $ROOT"
[ -f "$MIGRATION" ] || fail "Migration not found: $MIGRATION"
[ -f "$BACKEND/package.json" ] || fail "Backend package.json not found"
[ -f "$BACKEND/src/server.js" ] || fail "Backend server.js not found"
[ -f "$FRONTEND/package.json" ] || fail "Frontend package.json not found"
[ -f "$FRONTEND/src/App.jsx" ] || fail "Frontend App.jsx not found"

log "PRECONDITIONS_OK=True"

if ! command -v node >/dev/null 2>&1; then
  fail "node is not installed"
fi

if ! command -v npm >/dev/null 2>&1; then
  fail "npm is not installed"
fi

NODE_MAJOR="$(node -p "Number(process.versions.node.split('.')[0])")"
if [ "$NODE_MAJOR" -lt 18 ]; then
  fail "Node.js 18+ is required. Current: $(node -v)"
fi

if ! command -v psql >/dev/null 2>&1; then
  log "PSQL_NOT_FOUND_INSTALLING=True"
  sudo apt-get update -y
  sudo apt-get install -y postgresql-client
fi

log "TOOLS_OK=True"
log "- NODE=$(node -v)"
log "- NPM=$(npm -v)"
log "- PSQL=$(psql --version | head -1)"

find_database_url() {
  if [ -n "${DATABASE_URL:-}" ]; then
    echo "$DATABASE_URL"
    return 0
  fi

  local files=(
    "$BASE/backend/.env"
    "$BASE/backend/.env.production"
    "$BASE/backend/.env.local"
    "$BASE/.env"
    "$BASE/.env.production"
  )

  for f in "${files[@]}"; do
    if [ -f "$f" ]; then
      local line
      line="$(grep -E '^DATABASE_URL=' "$f" | tail -1 || true)"
      if [ -n "$line" ]; then
        line="${line#DATABASE_URL=}"
        line="${line%\"}"
        line="${line#\"}"
        line="${line%\'}"
        line="${line#\'}"
        echo "$line"
        return 0
      fi
    fi
  done

  local svc
  svc="$(sudo systemctl cat ndsp-api.service 2>/dev/null | grep -E 'DATABASE_URL=' | tail -1 || true)"
  if [ -n "$svc" ]; then
    echo "$svc" | sed -E 's/^.*DATABASE_URL=//' | sed -E 's/[ "]+$//'
    return 0
  fi

  return 1
}

DB_URL="$(find_database_url || true)"

if [ -z "$DB_URL" ]; then
  fail "DATABASE_URL not found. Export it then rerun: DATABASE_URL='postgresql://user:pass@127.0.0.1:5432/db' ./RUN_NDSP_CHECKOUT_PLANS_NOW.sh"
fi

case "$DB_URL" in
  postgres://*|postgresql://*)
    log "DATABASE_URL_FOUND=True"
    ;;
  *)
    fail "DATABASE_URL exists but is not PostgreSQL: $DB_URL"
    ;;
esac

if [ -f "$API_ENV" ]; then
  cp "$API_ENV" "$API_ENV.bak_$(date +%Y%m%d_%H%M%S)"
fi

ADMIN_KEY="$(grep -E '^NDSP_ADMIN_KEY=' "$API_ENV" 2>/dev/null | tail -1 | cut -d= -f2- || true)"
if [ -z "$ADMIN_KEY" ] || [ "$ADMIN_KEY" = "change_this_admin_key" ]; then
  ADMIN_KEY="$(openssl rand -hex 32)"
fi

cat > "$API_ENV" <<ENVEOF
PORT=8088
DATABASE_URL=$DB_URL
NDSP_ADMIN_KEY=$ADMIN_KEY
CORS_ORIGIN=*
ENVEOF

chmod 600 "$API_ENV"
log "BACKEND_ENV_WRITTEN=True"
log "- API_ENV=$API_ENV"
log "- ADMIN_KEY_STORED_IN=$API_ENV"

if [ -f "$FRONT_ENV" ]; then
  cp "$FRONT_ENV" "$FRONT_ENV.bak_$(date +%Y%m%d_%H%M%S)"
fi

cat > "$FRONT_ENV" <<ENVEOF
VITE_NDSP_API_BASE=http://localhost:8088
ENVEOF

log "FRONTEND_ENV_WRITTEN=True"

cd "$BACKEND"
npm install
node --check src/db.js
node --check src/server.js
log "BACKEND_INSTALL_AND_SYNTAX_OK=True"

cd "$ROOT"
DATABASE_URL="$DB_URL" bash scripts/run_migration.sh
log "MIGRATION_OK=True"

cd "$FRONTEND"
npm install
npm run build
log "FRONTEND_BUILD_OK=True"

NPM_BIN="$(command -v npm)"
NODE_BIN="$(command -v node)"

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
ExecStart=$NPM_BIN run start
Restart=always
RestartSec=5
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"
sleep 2

if systemctl is-active --quiet "$SERVICE_NAME"; then
  log "SERVICE_ACTIVE=True"
else
  sudo systemctl status "$SERVICE_NAME" --no-pager -l || true
  fail "Service failed to start: $SERVICE_NAME"
fi

HEALTH_CODE="$(curl -s -o /tmp/ndsp_checkout_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
PLANS_CODE="$(curl -s -o /tmp/ndsp_checkout_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "- HEALTH_HTTP_CODE=$HEALTH_CODE"
log "- PLANS_HTTP_CODE=$PLANS_CODE"

if [ "$HEALTH_CODE" != "200" ]; then
  cat /tmp/ndsp_checkout_health.json || true
  fail "Health endpoint failed"
fi

if [ "$PLANS_CODE" != "200" ]; then
  cat /tmp/ndsp_checkout_plans.json || true
  fail "Plans endpoint failed"
fi

log "SMOKE_TEST_OK=True"
log "FINAL_STATUS=NDSP_CHECKOUT_PLANS_READY"
log "ASSERT_OK=True"
log "- REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "REPORT=$REPORT"
echo ""
echo "Admin key is stored here:"
echo "$API_ENV"
echo ""
echo "To view masked key:"
echo "grep '^NDSP_ADMIN_KEY=' $API_ENV | sed 's/=.*/=********MASKED********/'"
echo ""
echo "API:"
echo "curl http://127.0.0.1:8088/health"
echo "curl http://127.0.0.1:8088/api/v1/plans"
