#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
FRONTEND="$ROOT/checkout-admin-vite"
ENV_FILE="$BACKEND/.env"
APP_FILE="$FRONTEND/src/App.jsx"
CSS_FILE="$FRONTEND/src/styles.css"
MY_DIR="/var/www/checkout-plans"
ADMIN_DIR="/var/www/plans-console"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_TELEGRAM_ALERT_LIMITS_$(date +%Y%m%d_%H%M%S).md"
MIGRATION="$ROOT/database/migrations/20260524_006_telegram_alert_limits.sql"

# عدّل الأرقام هنا إذا تبي
PRO_TELEGRAM_ALERTS_PER_DAY=25
ELITE_TELEGRAM_ALERTS_PER_DAY=150
SAAS_TELEGRAM_ALERTS_PER_DAY=1000

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

log "# NDSP Telegram Alert Limits"
log "- TIME=$(date -Is)"
log "- ROOT=$ROOT"
log "- PRO_TELEGRAM_ALERTS_PER_DAY=$PRO_TELEGRAM_ALERTS_PER_DAY"
log "- ELITE_TELEGRAM_ALERTS_PER_DAY=$ELITE_TELEGRAM_ALERTS_PER_DAY"
log "- SAAS_TELEGRAM_ALERTS_PER_DAY=$SAAS_TELEGRAM_ALERTS_PER_DAY"

[ -d "$ROOT" ] || fail "Package root not found"
[ -d "$BACKEND" ] || fail "Backend not found"
[ -d "$FRONTEND" ] || fail "Frontend not found"
[ -f "$APP_FILE" ] || fail "App.jsx not found"
[ -f "$CSS_FILE" ] || fail "styles.css not found"

DB_URL="$(find_database_url || true)"
[ -n "$DB_URL" ] || fail "DATABASE_URL not found"

log "PRECONDITIONS_OK=True"
log "DATABASE_URL_FOUND=True"

cat > "$MIGRATION" <<SQL
BEGIN;

UPDATE ndsp_plans
SET
  limits = jsonb_set(
    jsonb_set(
      jsonb_set(
        COALESCE(limits, '{}'::jsonb),
        '{telegram_alerts_per_day}',
        to_jsonb($PRO_TELEGRAM_ALERTS_PER_DAY),
        true
      ),
      '{telegram_alerts_per_month}',
      to_jsonb($((PRO_TELEGRAM_ALERTS_PER_DAY * 30))),
      true
    ),
    '{telegram_alerts_enabled}',
    'true'::jsonb,
    true
  ),
  metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{telegram_alert_policy}',
    to_jsonb('Standard Telegram alert delivery with daily quota.'::text),
    true
  ),
  updated_at = now()
WHERE code = 'pro';

UPDATE ndsp_plans
SET
  limits = jsonb_set(
    jsonb_set(
      jsonb_set(
        COALESCE(limits, '{}'::jsonb),
        '{telegram_alerts_per_day}',
        to_jsonb($ELITE_TELEGRAM_ALERTS_PER_DAY),
        true
      ),
      '{telegram_alerts_per_month}',
      to_jsonb($((ELITE_TELEGRAM_ALERTS_PER_DAY * 30))),
      true
    ),
    '{telegram_alerts_enabled}',
    'true'::jsonb,
    true
  ),
  metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{telegram_alert_policy}',
    to_jsonb('Expanded Telegram alert delivery for Elite users.'::text),
    true
  ),
  updated_at = now()
WHERE code = 'elite';

UPDATE ndsp_plans
SET
  limits = jsonb_set(
    jsonb_set(
      jsonb_set(
        COALESCE(limits, '{}'::jsonb),
        '{telegram_alerts_per_day}',
        to_jsonb($SAAS_TELEGRAM_ALERTS_PER_DAY),
        true
      ),
      '{telegram_alerts_per_month}',
      to_jsonb($((SAAS_TELEGRAM_ALERTS_PER_DAY * 30))),
      true
    ),
    '{telegram_alerts_enabled}',
    'true'::jsonb,
    true
  ),
  metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{telegram_alert_policy}',
    to_jsonb('Institutional Telegram alert delivery with high-volume quota.'::text),
    true
  ),
  updated_at = now()
WHERE code = 'saas';

COMMIT;
SQL

psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"

log "DB_TELEGRAM_LIMITS_OK=True"

cp "$APP_FILE" "$APP_FILE.bak_telegram_limits_$(date +%Y%m%d_%H%M%S)"

python3 - "$APP_FILE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()

old = '''  const items = [
    {
      label: "عدد الأصول المتاحة",
      value: safeLimits.max_assets ? `حتى ${safeLimits.max_assets} أصل` : "حسب الباقة"
    },
    {
      label: "عمق التحليل",
      value: readableDecisionDepth(safeLimits.decision_depth)
    }
  ];

  if (safeLimits.trial_days) {
    items.push({
      label: "مدة التجربة",
      value: `${safeLimits.trial_days} يوم`
    });
  }

  if (safeLimits.team_access) {
    items.push({
      label: "وصول الفرق",
      value: "متاح"
    });
  }'''

new = '''  const items = [
    {
      label: "عدد الأصول المتاحة",
      value: safeLimits.max_assets ? `حتى ${safeLimits.max_assets} أصل` : "حسب الباقة"
    },
    {
      label: "عمق التحليل",
      value: readableDecisionDepth(safeLimits.decision_depth)
    }
  ];

  if (safeLimits.telegram_alerts_enabled && safeLimits.telegram_alerts_per_day) {
    items.push({
      label: "تنبيهات تيليجرام",
      value: `حتى ${safeLimits.telegram_alerts_per_day} تنبيه يوميًا`
    });
  }

  if (safeLimits.telegram_alerts_per_month) {
    items.push({
      label: "حد التنبيهات الشهري",
      value: `حتى ${safeLimits.telegram_alerts_per_month} تنبيه شهريًا`
    });
  }

  if (safeLimits.trial_days) {
    items.push({
      label: "مدة التجربة",
      value: `${safeLimits.trial_days} يوم`
    });
  }

  if (safeLimits.team_access) {
    items.push({
      label: "وصول الفرق",
      value: "متاح"
    });
  }'''

if old not in text:
    raise SystemExit("AccessLimitCards target block not found")

text = text.replace(old, new, 1)
path.write_text(text)
PY

log "FRONTEND_TELEGRAM_LIMITS_PATCHED=True"

cd "$FRONTEND"

cat > ".env" <<'ENV'
VITE_NDSP_API_BASE=/checkout-api
ENV

cat > "vite.config.js" <<'VITE'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()]
});
VITE

npm install
npm run build

[ -f "$FRONTEND/dist/index.html" ] || fail "Vite dist missing"

python3 - <<'PY'
from pathlib import Path

p = Path("/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite/dist/index.html")
text = p.read_text()
marker = "<!-- NDSP_TELEGRAM_ALERT_LIMITS_ENABLED -->"

if marker not in text:
    text = text.replace("<head>", "<head>\n  " + marker, 1)

p.write_text(text)
PY

sudo mkdir -p "$MY_DIR" "$ADMIN_DIR"
sudo rsync -a --delete "$FRONTEND/dist/" "$MY_DIR/"
sudo rsync -a --delete "$FRONTEND/dist/" "$ADMIN_DIR/"
sudo chown -R www-data:www-data "$MY_DIR" "$ADMIN_DIR"

log "FRONTEND_BUILD_AND_DEPLOY_OK=True"

TEST_EMAIL="ndsp.clean.rebuild.1779648774@example.com"

STATUS_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_telegram_limits_status.json \
  -w '%{http_code}' \
  https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"

MY_UI_CODE="$(curl -k -sS -o /tmp/ndsp_telegram_limits_my.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -sS -o /tmp/ndsp_telegram_limits_admin.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

log "STATUS_CODE=$STATUS_CODE"
log "MY_UI_CODE=$MY_UI_CODE"
log "ADMIN_UI_CODE=$ADMIN_UI_CODE"

[ "$STATUS_CODE" = "200" ] || fail "Subscription status failed"
[ "$MY_UI_CODE" = "200" ] || fail "my UI failed"
[ "$ADMIN_UI_CODE" = "200" ] || fail "admin UI failed"

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/tmp/ndsp_telegram_limits_status.json").read_text())
sub = data.get("subscription") or {}
limits = sub.get("limits") or {}

if not sub.get("active"):
    raise SystemExit("SUBSCRIPTION_NOT_ACTIVE")

if "telegram_alerts_per_day" not in limits:
    raise SystemExit("TELEGRAM_ALERTS_PER_DAY_MISSING")

if "telegram_alerts_per_month" not in limits:
    raise SystemExit("TELEGRAM_ALERTS_PER_MONTH_MISSING")

print("telegram_alerts_per_day=", limits.get("telegram_alerts_per_day"))
print("telegram_alerts_per_month=", limits.get("telegram_alerts_per_month"))
PY

grep -q "NDSP_TELEGRAM_ALERT_LIMITS_ENABLED" /tmp/ndsp_telegram_limits_my.html || fail "Telegram marker missing in my UI"
grep -q "NDSP_TELEGRAM_ALERT_LIMITS_ENABLED" /tmp/ndsp_telegram_limits_admin.html || fail "Telegram marker missing in admin UI"

log "TELEGRAM_LIMITS_STATUS_OK=True"
log "UI_MARKER_OK=True"
log "FINAL_STATUS=NDSP_TELEGRAM_ALERT_LIMITS_ADDED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_TELEGRAM_ALERT_LIMITS_ADDED"
echo "REPORT=$REPORT"
echo ""
echo "Hard refresh:"
echo "https://my.ndsp.app/checkout-plans/#/access"
