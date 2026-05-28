#!/usr/bin/env bash
set -Eeuo pipefail

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_PLANS_FINAL_VERIFY_$(date +%Y%m%d_%H%M%S).md"
ENV_FILE="/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env"

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

log "# NDSP Checkout Plans Final Verify"
log "- TIME=$(date -Is)"

[ -f "$ENV_FILE" ] || fail "Missing env file: $ENV_FILE"

ADMIN_KEY="$(grep '^NDSP_ADMIN_KEY=' "$ENV_FILE" | tail -1 | cut -d= -f2-)"
[ -n "$ADMIN_KEY" ] || fail "NDSP_ADMIN_KEY missing"

LOCAL_HEALTH="$(curl -s -o /tmp/ndsp_final_local_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
LOCAL_PLANS="$(curl -s -o /tmp/ndsp_final_local_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

MY_UI="$(curl -k -s -o /tmp/ndsp_final_my_ui.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI="$(curl -k -s -o /tmp/ndsp_final_admin_ui.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

MY_API="$(curl -k -s -o /tmp/ndsp_final_my_api.json -w '%{http_code}' https://my.ndsp.app/checkout-api/api/v1/plans || true)"
ADMIN_API="$(curl -k -s -o /tmp/ndsp_final_admin_api.json -w '%{http_code}' https://admin.ndsp.app/checkout-api/api/v1/plans || true)"
DIRECT_API="$(curl -k -s -o /tmp/ndsp_final_direct_api.json -w '%{http_code}' https://api.ndsp.app/checkout-api/api/v1/plans || true)"

ADMIN_PLANS="$(curl -k -s \
  -H "x-admin-key: $ADMIN_KEY" \
  -o /tmp/ndsp_final_admin_plans.json \
  -w '%{http_code}' \
  https://admin.ndsp.app/checkout-api/api/v1/admin/plans || true)"

CHECKOUT_CREATE="$(curl -k -s \
  -X POST https://my.ndsp.app/checkout-api/api/v1/checkout \
  -H 'Content-Type: application/json' \
  -d "{\"plan_code\":\"elite\",\"email\":\"ndsp.test.$(date +%s)@example.com\",\"telegram_id\":\"@ndsp_test\",\"network\":\"TRC20\"}" \
  -o /tmp/ndsp_final_checkout_create.json \
  -w '%{http_code}' || true)"

log "LOCAL_HEALTH_CODE=$LOCAL_HEALTH"
log "LOCAL_PLANS_CODE=$LOCAL_PLANS"
log "MY_UI_CODE=$MY_UI"
log "ADMIN_UI_CODE=$ADMIN_UI"
log "MY_API_CODE=$MY_API"
log "ADMIN_API_CODE=$ADMIN_API"
log "DIRECT_API_CODE=$DIRECT_API"
log "ADMIN_PLANS_CODE=$ADMIN_PLANS"
log "CHECKOUT_CREATE_CODE=$CHECKOUT_CREATE"

[ "$LOCAL_HEALTH" = "200" ] || fail "Local health failed"
[ "$LOCAL_PLANS" = "200" ] || fail "Local plans failed"
[ "$MY_UI" = "200" ] || fail "my.ndsp.app UI failed"
[ "$ADMIN_UI" = "200" ] || fail "admin.ndsp.app UI failed"
[ "$MY_API" = "200" ] || fail "my same-origin API failed"
[ "$ADMIN_API" = "200" ] || fail "admin same-origin API failed"
[ "$DIRECT_API" = "200" ] || fail "direct api.ndsp.app API failed"
[ "$ADMIN_PLANS" = "200" ] || fail "admin plans endpoint failed"
[ "$CHECKOUT_CREATE" = "201" ] || fail "checkout create failed"

grep -q "NDSP_CHECKOUT_ADMIN_VITE_MARKER" /tmp/ndsp_final_my_ui.html || fail "my UI marker missing"
grep -q "NDSP_CHECKOUT_ADMIN_VITE_MARKER" /tmp/ndsp_final_admin_ui.html || fail "admin UI marker missing"

if grep -q '"checkout_ref"' /tmp/ndsp_final_checkout_create.json; then
  log "CHECKOUT_REF_CREATED=True"
else
  fail "checkout_ref not found in checkout response"
fi

log "FINAL_STATUS=NDSP_CHECKOUT_PLANS_FULLY_OPERATIONAL"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_PLANS_FULLY_OPERATIONAL"
echo "REPORT=$REPORT"
