#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new/ndsp_checkout_plans_package"
FRONTEND="$ROOT/checkout-admin-vite"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_PLANS_UI_DEPLOY_$(date +%Y%m%d_%H%M%S).md"
STAMP="$(date +%Y%m%d_%H%M%S)"

MY_PUBLIC_DIR="/var/www/checkout-plans"
ADMIN_PUBLIC_DIR="/var/www/plans-console"

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

mkdir -p "$REPORT_DIR"

log "# NDSP Checkout Plans UI Deploy"
log "- TIME=$(date -Is)"
log "- FRONTEND=$FRONTEND"

[ -d "$FRONTEND" ] || fail "Frontend directory not found"
[ -f "$FRONTEND/package.json" ] || fail "package.json not found"
[ -f "$FRONTEND/src/App.jsx" ] || fail "App.jsx not found"

cd "$FRONTEND"

cat > ".env" <<'ENVEOF'
VITE_NDSP_API_BASE=https://api.ndsp.app/checkout-api
ENVEOF

cat > "vite.config.js" <<'VITEEOF'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()]
});
VITEEOF

log "VITE_ENV_WRITTEN=True"
log "VITE_CONFIG_WRITTEN=True"

npm install
npm run build

[ -d "$FRONTEND/dist" ] || fail "Vite dist not created"

log "FRONTEND_BUILD_OK=True"

sudo mkdir -p "$MY_PUBLIC_DIR" "$ADMIN_PUBLIC_DIR"

sudo rsync -a --delete "$FRONTEND/dist/" "$MY_PUBLIC_DIR/"
sudo rsync -a --delete "$FRONTEND/dist/" "$ADMIN_PUBLIC_DIR/"

sudo chown -R www-data:www-data "$MY_PUBLIC_DIR" "$ADMIN_PUBLIC_DIR"

log "STATIC_FILES_DEPLOYED=True"
log "- MY_PUBLIC_DIR=$MY_PUBLIC_DIR"
log "- ADMIN_PUBLIC_DIR=$ADMIN_PUBLIC_DIR"

find_nginx_file() {
  local domain="$1"
  grep -Rsl "server_name .*${domain}\|server_name ${domain}" /etc/nginx/sites-available /etc/nginx/conf.d 2>/dev/null | head -1 || true
}

MY_NGINX_FILE="$(find_nginx_file "my\.ndsp\.app")"
ADMIN_NGINX_FILE="$(find_nginx_file "admin\.ndsp\.app")"

[ -n "$MY_NGINX_FILE" ] || fail "Could not find nginx config for my.ndsp.app"
[ -n "$ADMIN_NGINX_FILE" ] || fail "Could not find nginx config for admin.ndsp.app"

log "MY_NGINX_FILE=$MY_NGINX_FILE"
log "ADMIN_NGINX_FILE=$ADMIN_NGINX_FILE"

sudo cp "$MY_NGINX_FILE" "${MY_NGINX_FILE}.bak_checkout_ui_${STAMP}"
sudo cp "$ADMIN_NGINX_FILE" "${ADMIN_NGINX_FILE}.bak_admin_plans_ui_${STAMP}"

insert_block() {
  local file="$1"
  local marker="$2"
  local block="$3"

  if sudo grep -q "$marker" "$file"; then
    log "${marker}_ALREADY_EXISTS=True"
    return 0
  fi

  sudo python3 - "$file" "$block" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
block = sys.argv[2]
text = path.read_text()

pos = text.rfind("\n}")
if pos == -1:
    raise SystemExit("Could not find final closing brace in nginx file")

path.write_text(text[:pos] + "\n" + block + "\n" + text[pos:])
PY

  log "${marker}_INSERTED=True"
}

MY_BLOCK='
    # NDSP_CHECKOUT_PLANS_UI_BEGIN
    location ^~ /checkout-plans/ {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /checkout-plans/index.html;
    }
    # NDSP_CHECKOUT_PLANS_UI_END
'

ADMIN_BLOCK='
    # NDSP_ADMIN_PLANS_UI_BEGIN
    location ^~ /plans-console/ {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /plans-console/index.html;
    }
    # NDSP_ADMIN_PLANS_UI_END
'

insert_block "$MY_NGINX_FILE" "NDSP_CHECKOUT_PLANS_UI_BEGIN" "$MY_BLOCK"
insert_block "$ADMIN_NGINX_FILE" "NDSP_ADMIN_PLANS_UI_BEGIN" "$ADMIN_BLOCK"

sudo nginx -t
log "NGINX_CONFIG_OK=True"

sudo systemctl reload nginx
log "NGINX_RELOAD_OK=True"

sleep 2

MY_CODE="$(curl -k -s -o /tmp/ndsp_checkout_ui_my.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_CODE="$(curl -k -s -o /tmp/ndsp_checkout_ui_admin.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"
API_CODE="$(curl -k -s -o /tmp/ndsp_checkout_ui_api.json -w '%{http_code}' https://api.ndsp.app/checkout-api/api/v1/plans || true)"

log "MY_CHECKOUT_UI_HTTP_CODE=$MY_CODE"
log "ADMIN_PLANS_UI_HTTP_CODE=$ADMIN_CODE"
log "API_PLANS_HTTP_CODE=$API_CODE"

[ "$MY_CODE" = "200" ] || fail "my.ndsp.app checkout UI failed"
[ "$ADMIN_CODE" = "200" ] || fail "admin.ndsp.app plans UI failed"
[ "$API_CODE" = "200" ] || fail "api.ndsp.app checkout plans API failed"

if grep -q '<div id="root"></div>' /tmp/ndsp_checkout_ui_my.html; then
  log "MY_UI_ROOT_FOUND=True"
else
  fail "React root not found in my checkout UI"
fi

if grep -q '<div id="root"></div>' /tmp/ndsp_checkout_ui_admin.html; then
  log "ADMIN_UI_ROOT_FOUND=True"
else
  fail "React root not found in admin plans UI"
fi

log "FINAL_STATUS=NDSP_CHECKOUT_PLANS_UI_DEPLOYED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_PLANS_UI_DEPLOYED"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/checkout"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"
