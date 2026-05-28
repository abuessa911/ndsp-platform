#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
ENV_FILE="$BACKEND/.env"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_DEMO_TEST_EMAILS_$(date +%Y%m%d_%H%M%S).md"
MIGRATION="$ROOT/database/migrations/20260524_007_free_plan_and_demo_emails.sql"

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

find_database_url() {
  if [ -n "${DATABASE_URL:-}" ]; then
    echo "$DATABASE_URL"
    return 0
  fi

  for f in "$ENV_FILE" "$BASE/backend/.env" "$BASE/backend/.env.production" "$BASE/.env" "$BASE/.env.production"; do
    if [ -f "$f" ]; then
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

  return 1
}

create_and_approve() {
  local plan="$1"
  local email="$2"
  local telegram="$3"

  log ""
  log "CREATE_CHECKOUT_PLAN=$plan"
  log "CREATE_CHECKOUT_EMAIL=$email"

  local checkout_file="/tmp/ndsp_demo_${plan}_checkout.json"
  local approve_file="/tmp/ndsp_demo_${plan}_approve.json"
  local status_file="/tmp/ndsp_demo_${plan}_status.json"

  local checkout_code
  checkout_code="$(curl -sS \
    -X POST http://127.0.0.1:8088/api/v1/checkout \
    -H 'Content-Type: application/json' \
    -d "{\"plan_code\":\"$plan\",\"email\":\"$email\",\"telegram_id\":\"$telegram\",\"network\":\"TRC20\"}" \
    -o "$checkout_file" \
    -w '%{http_code}' || true)"

  log "${plan^^}_CHECKOUT_CODE=$checkout_code"

  [ "$checkout_code" = "201" ] || {
    log "${plan^^}_CHECKOUT_RESPONSE_BEGIN"
    cat "$checkout_file" >> "$REPORT" 2>&1 || true
    log "${plan^^}_CHECKOUT_RESPONSE_END"
    fail "$plan checkout create failed"
  }

  local checkout_ref
  checkout_ref="$(python3 - "$checkout_file" <<'PY'
import json, sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text())
print(data["checkout"]["checkout_ref"])
PY
)"

  log "${plan^^}_CHECKOUT_REF=$checkout_ref"

  local approve_code
  approve_code="$(curl -sS \
    -X POST "http://127.0.0.1:8088/api/v1/admin/checkout/$checkout_ref/approve" \
    -H 'Content-Type: application/json' \
    -H "x-admin-key: $ADMIN_KEY" \
    -d "{\"admin_note\":\"Demo $plan account activation\"}" \
    -o "$approve_file" \
    -w '%{http_code}' || true)"

  log "${plan^^}_APPROVE_CODE=$approve_code"

  [ "$approve_code" = "200" ] || {
    log "${plan^^}_APPROVE_RESPONSE_BEGIN"
    cat "$approve_file" >> "$REPORT" 2>&1 || true
    log "${plan^^}_APPROVE_RESPONSE_END"
    fail "$plan approve failed"
  }

  local status_code
  status_code="$(curl -sS -G \
    --data-urlencode "email=$email" \
    -o "$status_file" \
    -w '%{http_code}' \
    http://127.0.0.1:8088/api/v1/subscription/status || true)"

  log "${plan^^}_STATUS_CODE=$status_code"

  [ "$status_code" = "200" ] || fail "$plan subscription status failed"

  python3 - "$status_file" "$plan" <<'PY'
import json, sys
from pathlib import Path

status_file = sys.argv[1]
expected_plan = sys.argv[2]

data = json.loads(Path(status_file).read_text())
sub = data.get("subscription") or {}

if not sub.get("active"):
    raise SystemExit(f"{expected_plan.upper()}_SUBSCRIPTION_NOT_ACTIVE")

if sub.get("plan_code") != expected_plan:
    raise SystemExit(f"{expected_plan.upper()}_PLAN_MISMATCH={sub.get('plan_code')}")
PY

  log "${plan^^}_ACTIVE_OK=True"
}

log "# NDSP Demo Test Emails"
log "- TIME=$(date -Is)"

[ -d "$ROOT" ] || fail "Package root not found: $ROOT"
[ -f "$ENV_FILE" ] || fail "Env file not found: $ENV_FILE"

DB_URL="$(find_database_url || true)"
[ -n "$DB_URL" ] || fail "DATABASE_URL not found"

ADMIN_KEY="$(grep '^NDSP_ADMIN_KEY=' "$ENV_FILE" | tail -1 | cut -d= -f2- || true)"
[ -n "$ADMIN_KEY" ] || fail "NDSP_ADMIN_KEY missing"

if ! systemctl is-active --quiet ndsp-checkout-api.service; then
  fail "ndsp-checkout-api.service is not active"
fi

log "PRECONDITIONS_OK=True"
log "DATABASE_URL_FOUND=True"
log "ADMIN_KEY_FOUND=True"
log "SERVICE_ACTIVE=True"

cat > "$MIGRATION" <<'SQL'
BEGIN;

INSERT INTO ndsp_plans (
    code,
    name_ar,
    name_en,
    description_ar,
    description_en,
    price_usd,
    currency,
    billing_period,
    trial_days,
    sort_order,
    is_active,
    is_public,
    features,
    limits,
    metadata
)
VALUES (
    'free',
    'Free',
    'Free',
    'وصول تجريبي مجاني محدود للتعرف على بيئة دعم القرار.',
    'Limited free access to explore the decision-support environment.',
    0.00,
    'USD',
    'monthly',
    0,
    1,
    TRUE,
    TRUE,
    '[
      "Basic market context overview",
      "Limited decision-support access",
      "Public sanitized output"
    ]'::jsonb,
    '{
      "max_assets": 3,
      "decision_depth": "basic",
      "telegram_alerts_enabled": true,
      "telegram_alerts_per_day": 3,
      "telegram_alerts_per_month": 90,
      "admin_review_required": true
    }'::jsonb,
    '{
      "public_label": "Free",
      "payment_currency": "USDT",
      "supported_networks": ["TRC20", "BEP20"],
      "manual_activation": true,
      "telegram_alert_policy": "Limited free Telegram alert delivery."
    }'::jsonb
)
ON CONFLICT (code) DO UPDATE SET
    name_ar = EXCLUDED.name_ar,
    name_en = EXCLUDED.name_en,
    description_ar = EXCLUDED.description_ar,
    description_en = EXCLUDED.description_en,
    price_usd = EXCLUDED.price_usd,
    currency = EXCLUDED.currency,
    billing_period = EXCLUDED.billing_period,
    trial_days = EXCLUDED.trial_days,
    sort_order = EXCLUDED.sort_order,
    is_active = EXCLUDED.is_active,
    is_public = EXCLUDED.is_public,
    features = EXCLUDED.features,
    limits = EXCLUDED.limits,
    metadata = EXCLUDED.metadata,
    updated_at = now();

UPDATE ndsp_plans
SET limits = jsonb_set(
      jsonb_set(
        jsonb_set(COALESCE(limits, '{}'::jsonb), '{telegram_alerts_enabled}', 'true'::jsonb, true),
        '{telegram_alerts_per_day}', '25'::jsonb, true
      ),
      '{telegram_alerts_per_month}', '750'::jsonb, true
    ),
    updated_at = now()
WHERE code = 'pro';

UPDATE ndsp_plans
SET limits = jsonb_set(
      jsonb_set(
        jsonb_set(COALESCE(limits, '{}'::jsonb), '{telegram_alerts_enabled}', 'true'::jsonb, true),
        '{telegram_alerts_per_day}', '150'::jsonb, true
      ),
      '{telegram_alerts_per_month}', '4500'::jsonb, true
    ),
    updated_at = now()
WHERE code = 'elite';

UPDATE ndsp_plans
SET limits = jsonb_set(
      jsonb_set(
        jsonb_set(COALESCE(limits, '{}'::jsonb), '{telegram_alerts_enabled}', 'true'::jsonb, true),
        '{telegram_alerts_per_day}', '1000'::jsonb, true
      ),
      '{telegram_alerts_per_month}', '30000'::jsonb, true
    ),
    updated_at = now()
WHERE code = 'saas';

COMMIT;
SQL

psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"
log "FREE_PLAN_AND_LIMITS_OK=True"

STAMP="$(date +%s)"

PRO_EMAIL="ndsp.demo.pro.$STAMP@example.com"
SAAS_EMAIL="ndsp.demo.saas.$STAMP@example.com"
FREE_EMAIL="ndsp.demo.free.$STAMP@example.com"

create_and_approve "pro" "$PRO_EMAIL" "@ndsp_demo_pro"
create_and_approve "saas" "$SAAS_EMAIL" "@ndsp_demo_saas"
create_and_approve "free" "$FREE_EMAIL" "@ndsp_demo_free"

REMOTE_PRO_CODE="$(curl -k -sS -G --data-urlencode "email=$PRO_EMAIL" -o /tmp/ndsp_demo_remote_pro.json -w '%{http_code}' https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"
REMOTE_SAAS_CODE="$(curl -k -sS -G --data-urlencode "email=$SAAS_EMAIL" -o /tmp/ndsp_demo_remote_saas.json -w '%{http_code}' https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"
REMOTE_FREE_CODE="$(curl -k -sS -G --data-urlencode "email=$FREE_EMAIL" -o /tmp/ndsp_demo_remote_free.json -w '%{http_code}' https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"

log "REMOTE_PRO_CODE=$REMOTE_PRO_CODE"
log "REMOTE_SAAS_CODE=$REMOTE_SAAS_CODE"
log "REMOTE_FREE_CODE=$REMOTE_FREE_CODE"

[ "$REMOTE_PRO_CODE" = "200" ] || fail "Remote pro status failed"
[ "$REMOTE_SAAS_CODE" = "200" ] || fail "Remote saas status failed"
[ "$REMOTE_FREE_CODE" = "200" ] || fail "Remote free status failed"

python3 - <<'PY'
import json
from pathlib import Path

checks = [
    ("/tmp/ndsp_demo_remote_pro.json", "pro"),
    ("/tmp/ndsp_demo_remote_saas.json", "saas"),
    ("/tmp/ndsp_demo_remote_free.json", "free"),
]

for file_path, expected_plan in checks:
    data = json.loads(Path(file_path).read_text())
    sub = data.get("subscription") or {}
    if not sub.get("active"):
        raise SystemExit(f"{expected_plan.upper()}_REMOTE_NOT_ACTIVE")
    if sub.get("plan_code") != expected_plan:
        raise SystemExit(f"{expected_plan.upper()}_REMOTE_PLAN_MISMATCH={sub.get('plan_code')}")
PY

log "REMOTE_STATUS_OK=True"

log ""
log "DEMO_EMAILS_BEGIN"
log "PRO_EMAIL=$PRO_EMAIL"
log "SAAS_EMAIL=$SAAS_EMAIL"
log "FREE_EMAIL=$FREE_EMAIL"
log "DEMO_EMAILS_END"

log "FINAL_STATUS=NDSP_DEMO_TEST_EMAILS_READY"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DEMO EMAILS READY ==="
echo "PRO_EMAIL=$PRO_EMAIL"
echo "SAAS_EMAIL=$SAAS_EMAIL"
echo "FREE_EMAIL=$FREE_EMAIL"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/access"
echo ""
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_DEMO_TEST_EMAILS_READY"
echo "REPORT=$REPORT"
