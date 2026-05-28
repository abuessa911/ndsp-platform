#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
ENV_FILE="$BACKEND/.env"
SERVICE_NAME="ndsp-checkout-api.service"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_APPROVE_PARAM_TYPES_FINAL_$(date +%Y%m%d_%H%M%S).md"
MIGRATION="$ROOT/database/migrations/20260524_004_approve_param_types_final.sql"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  log ""
  log "=== JOURNAL LAST 120 ==="
  sudo journalctl -u "$SERVICE_NAME" -n 120 --no-pager >> "$REPORT" 2>&1 || true
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

log "# NDSP Approve Parameter Types Final Fix"
log "- TIME=$(date -Is)"

[ -d "$BACKEND" ] || fail "Backend not found: $BACKEND"
[ -f "$BACKEND/src/server.js" ] || fail "server.js not found"
[ -f "$ENV_FILE" ] || fail ".env not found: $ENV_FILE"

DB_URL="$(find_database_url || true)"
[ -n "$DB_URL" ] || fail "DATABASE_URL not found"

ADMIN_KEY="$(grep '^NDSP_ADMIN_KEY=' "$ENV_FILE" | tail -1 | cut -d= -f2- || true)"
[ -n "$ADMIN_KEY" ] || fail "NDSP_ADMIN_KEY missing"

log "PRECONDITIONS_OK=True"

cat > "$MIGRATION" <<'SQL'
BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS ndsp_user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_email TEXT NOT NULL,
    plan_code TEXT NOT NULL REFERENCES ndsp_plans(code) ON UPDATE CASCADE,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'pending', 'suspended', 'cancelled', 'expired')),
    source_checkout_ref TEXT,
    activation_mode TEXT NOT NULL DEFAULT 'admin_approved',
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ,
    last_status_check_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ndsp_subscription_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    customer_email TEXT NOT NULL,
    plan_code TEXT,
    action TEXT NOT NULL,
    actor TEXT NOT NULL DEFAULT 'admin',
    before_data JSONB,
    after_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE ndsp_checkout_requests
ADD COLUMN IF NOT EXISTS activated_subscription_id UUID;

UPDATE ndsp_user_subscriptions
SET customer_email = lower(trim(customer_email));

WITH ranked AS (
    SELECT
        id,
        row_number() OVER (
            PARTITION BY customer_email
            ORDER BY updated_at DESC, created_at DESC, id DESC
        ) AS rn
    FROM ndsp_user_subscriptions
)
UPDATE ndsp_checkout_requests
SET activated_subscription_id = NULL
WHERE activated_subscription_id IN (
    SELECT id FROM ranked WHERE rn > 1
);

WITH ranked AS (
    SELECT
        id,
        row_number() OVER (
            PARTITION BY customer_email
            ORDER BY updated_at DESC, created_at DESC, id DESC
        ) AS rn
    FROM ndsp_user_subscriptions
)
DELETE FROM ndsp_user_subscriptions
WHERE id IN (
    SELECT id FROM ranked WHERE rn > 1
);

ALTER TABLE ndsp_user_subscriptions
DROP CONSTRAINT IF EXISTS ndsp_user_subscriptions_source_checkout_ref_key;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ndsp_user_subscriptions_customer_email_key'
    ) THEN
        ALTER TABLE ndsp_user_subscriptions
        ADD CONSTRAINT ndsp_user_subscriptions_customer_email_key
        UNIQUE (customer_email);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_ndsp_checkout_activated_subscription'
    ) THEN
        ALTER TABLE ndsp_checkout_requests
        ADD CONSTRAINT fk_ndsp_checkout_activated_subscription
        FOREIGN KEY (activated_subscription_id)
        REFERENCES ndsp_user_subscriptions(id)
        ON DELETE SET NULL;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_plan_status
ON ndsp_user_subscriptions (plan_code, status);

CREATE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_source_checkout
ON ndsp_user_subscriptions (source_checkout_ref);

COMMIT;
SQL

psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"
log "DB_PARAM_TYPES_MIGRATION_OK=True"

cp "$BACKEND/src/server.js" "$BACKEND/src/server.js.bak_param_types_$(date +%Y%m%d_%H%M%S)"

python3 - "$BACKEND/src/server.js" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text()

new_approve = r'''
app.post("/api/v1/admin/checkout/:checkout_ref/approve", requireAdmin, async (req, res) => {
  const checkoutRef = String(req.params.checkout_ref || "").trim();
  const adminNote = String(req.body?.admin_note || "Approved by admin").trim();
  const expiresAt = req.body?.expires_at ? String(req.body.expires_at) : null;

  if (!/^NDSP-[A-Z0-9]{8,32}$/.test(checkoutRef)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_checkout_ref"
    });
  }

  const client = await pool.connect();

  try {
    await client.query("BEGIN");

    const checkoutResult = await client.query(
      `
      SELECT
        c.*,
        p.features,
        p.limits,
        p.metadata AS plan_metadata
      FROM ndsp_checkout_requests c
      JOIN ndsp_plans p ON p.code = c.plan_code
      WHERE c.checkout_ref = $1::text
      FOR UPDATE
      `,
      [checkoutRef]
    );

    if (checkoutResult.rowCount === 0) {
      await client.query("ROLLBACK");
      return res.status(404).json({
        ok: false,
        error: "checkout_request_not_found"
      });
    }

    const checkout = checkoutResult.rows[0];
    const normalizedEmail = normalizeEmail(checkout.customer_email);

    if (["rejected", "cancelled", "expired"].includes(checkout.status)) {
      await client.query("ROLLBACK");
      return res.status(409).json({
        ok: false,
        error: "checkout_request_not_approvable",
        status: checkout.status
      });
    }

    const beforeSub = await client.query(
      `
      SELECT *
      FROM ndsp_user_subscriptions
      WHERE customer_email = $1::text
      LIMIT 1
      `,
      [normalizedEmail]
    );

    const subscriptionMetadata = {
      approved_from_checkout_ref: checkout.checkout_ref,
      payment_currency: checkout.payment_currency,
      payment_network: checkout.payment_network,
      amount_usd: checkout.amount_usd,
      admin_note: adminNote,
      governance: {
        mode: "decision_active",
        execution_policy: "execution_sanitized"
      }
    };

    const subscriptionResult = await client.query(
      `
      INSERT INTO ndsp_user_subscriptions (
        customer_email,
        plan_code,
        status,
        source_checkout_ref,
        activation_mode,
        started_at,
        expires_at,
        metadata
      )
      VALUES (
        $1::text,
        $2::text,
        'active',
        $3::text,
        'admin_approved',
        now(),
        $4::timestamptz,
        $5::jsonb
      )
      ON CONFLICT (customer_email)
      DO UPDATE SET
        plan_code = EXCLUDED.plan_code,
        status = 'active',
        source_checkout_ref = EXCLUDED.source_checkout_ref,
        activation_mode = 'admin_approved',
        started_at = now(),
        expires_at = EXCLUDED.expires_at,
        metadata = EXCLUDED.metadata,
        updated_at = now()
      RETURNING *
      `,
      [
        normalizedEmail,
        String(checkout.plan_code),
        String(checkout.checkout_ref),
        expiresAt,
        JSON.stringify(subscriptionMetadata)
      ]
    );

    const subscription = subscriptionResult.rows[0];

    const updatedCheckout = await client.query(
      `
      UPDATE ndsp_checkout_requests
      SET
        customer_email = $1::text,
        status = 'activated',
        reviewed_at = now(),
        admin_note = $2::text,
        public_note = 'Subscription activated after admin review.',
        activated_subscription_id = $3::uuid
      WHERE checkout_ref = $4::text
      RETURNING *
      `,
      [
        normalizedEmail,
        adminNote,
        subscription.id,
        checkout.checkout_ref
      ]
    );

    await client.query(
      `
      INSERT INTO ndsp_subscription_audit_logs (
        customer_email,
        plan_code,
        action,
        actor,
        before_data,
        after_data
      )
      VALUES (
        $1::text,
        $2::text,
        'approve_checkout_activate_subscription',
        'admin',
        $3::jsonb,
        $4::jsonb
      )
      `,
      [
        subscription.customer_email,
        subscription.plan_code,
        beforeSub.rowCount ? JSON.stringify(beforeSub.rows[0]) : null,
        JSON.stringify(subscription)
      ]
    );

    await client.query("COMMIT");

    return res.json({
      ok: true,
      checkout: updatedCheckout.rows[0],
      subscription
    });
  } catch (error) {
    await client.query("ROLLBACK");

    console.error("ADMIN_APPROVE_CHECKOUT_ERROR", {
      message: error.message,
      code: error.code,
      detail: error.detail,
      hint: error.hint,
      position: error.position,
      constraint: error.constraint,
      checkout_ref: checkoutRef
    });

    return res.status(500).json({
      ok: false,
      error: "failed_to_approve_checkout",
      detail: process.env.NODE_ENV === "production" ? undefined : error.message
    });
  } finally {
    client.release();
  }
});
'''

pattern = re.compile(
    r'app\.post\("/api/v1/admin/checkout/:checkout_ref/approve", requireAdmin, async \(req, res\) => \{.*?\n\}\);\n\napp\.post\("/api/v1/admin/checkout/:checkout_ref/reject"',
    re.S
)

match = pattern.search(text)
if not match:
    raise SystemExit("approve endpoint block not found")

replacement = new_approve + '\n\napp.post("/api/v1/admin/checkout/:checkout_ref/reject"'
text = pattern.sub(replacement, text, count=1)

path.write_text(text)
PY

cd "$BACKEND"
node --check src/server.js
log "APPROVE_ENDPOINT_PATCHED=True"
log "SERVER_SYNTAX_OK=True"

sudo systemctl restart "$SERVICE_NAME"
sleep 3

if systemctl is-active --quiet "$SERVICE_NAME"; then
  log "SERVICE_ACTIVE=True"
else
  fail "$SERVICE_NAME failed after patch"
fi

LOCAL_HEALTH="$(curl -s -o /tmp/ndsp_pt_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
LOCAL_PLANS="$(curl -s -o /tmp/ndsp_pt_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "LOCAL_HEALTH_CODE=$LOCAL_HEALTH"
log "LOCAL_PLANS_CODE=$LOCAL_PLANS"

[ "$LOCAL_HEALTH" = "200" ] || fail "Local health failed"
[ "$LOCAL_PLANS" = "200" ] || fail "Local plans failed"

TEST_EMAIL="ndsp.paramtypes.$(date +%s)@example.com"

CHECKOUT_CODE="$(curl -s \
  -X POST http://127.0.0.1:8088/api/v1/checkout \
  -H 'Content-Type: application/json' \
  -d "{\"plan_code\":\"elite\",\"email\":\"$TEST_EMAIL\",\"telegram_id\":\"@ndsp_paramtypes\",\"network\":\"TRC20\"}" \
  -o /tmp/ndsp_pt_checkout.json \
  -w '%{http_code}' || true)"

log "CHECKOUT_CREATE_CODE=$CHECKOUT_CODE"
[ "$CHECKOUT_CODE" = "201" ] || fail "Checkout create failed"

CHECKOUT_REF="$(python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/ndsp_pt_checkout.json").read_text())
print(data["checkout"]["checkout_ref"])
PY
)"

log "CHECKOUT_REF_CREATED=$CHECKOUT_REF"

APPROVE_CODE="$(curl -s \
  -X POST "http://127.0.0.1:8088/api/v1/admin/checkout/$CHECKOUT_REF/approve" \
  -H 'Content-Type: application/json' \
  -H "x-admin-key: $ADMIN_KEY" \
  -d '{"admin_note":"Approve param types final verification"}' \
  -o /tmp/ndsp_pt_approve.json \
  -w '%{http_code}' || true)"

log "APPROVE_CODE=$APPROVE_CODE"

if [ "$APPROVE_CODE" != "200" ]; then
  log "APPROVE_RESPONSE_BEGIN"
  cat /tmp/ndsp_pt_approve.json >> "$REPORT" 2>&1 || true
  log "APPROVE_RESPONSE_END"
  fail "Approve endpoint failed after param type patch"
fi

STATUS_CODE="$(curl -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_pt_status.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/subscription/status || true)"

log "SUBSCRIPTION_STATUS_CODE=$STATUS_CODE"
[ "$STATUS_CODE" = "200" ] || fail "Subscription status failed"

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/tmp/ndsp_pt_status.json").read_text())
sub = data.get("subscription") or {}

if not sub.get("active"):
    raise SystemExit("SUBSCRIPTION_NOT_ACTIVE")

if sub.get("plan_code") != "elite":
    raise SystemExit("SUBSCRIPTION_NOT_ELITE")
PY

log "SUBSCRIPTION_ACTIVE_OK=True"

MY_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_pt_my_access.json \
  -w '%{http_code}' \
  https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"

ADMIN_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_pt_admin_access.json \
  -w '%{http_code}' \
  https://admin.ndsp.app/checkout-api/api/v1/subscription/status || true)"

ADMIN_REQUESTS_CODE="$(curl -s \
  -H "x-admin-key: $ADMIN_KEY" \
  -o /tmp/ndsp_pt_admin_requests.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/admin/checkout/requests || true)"

MY_UI_CODE="$(curl -k -s -o /tmp/ndsp_pt_my_ui.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -s -o /tmp/ndsp_pt_admin_ui.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

log "MY_ACCESS_API_CODE=$MY_ACCESS_API_CODE"
log "ADMIN_ACCESS_API_CODE=$ADMIN_ACCESS_API_CODE"
log "ADMIN_REQUESTS_CODE=$ADMIN_REQUESTS_CODE"
log "MY_UI_CODE=$MY_UI_CODE"
log "ADMIN_UI_CODE=$ADMIN_UI_CODE"

[ "$MY_ACCESS_API_CODE" = "200" ] || fail "my.ndsp.app subscription API failed"
[ "$ADMIN_ACCESS_API_CODE" = "200" ] || fail "admin.ndsp.app subscription API failed"
[ "$ADMIN_REQUESTS_CODE" = "200" ] || fail "Admin requests failed"
[ "$MY_UI_CODE" = "200" ] || fail "my UI failed"
[ "$ADMIN_UI_CODE" = "200" ] || fail "admin UI failed"

python3 - <<'PY'
import json
from pathlib import Path

for f in ["/tmp/ndsp_pt_my_access.json", "/tmp/ndsp_pt_admin_access.json"]:
    data = json.loads(Path(f).read_text())
    sub = data.get("subscription") or {}
    if not sub.get("active"):
        raise SystemExit(f"REMOTE_SUBSCRIPTION_NOT_ACTIVE={f}")
    if sub.get("plan_code") != "elite":
        raise SystemExit(f"REMOTE_SUBSCRIPTION_NOT_ELITE={f}")
PY

log "REMOTE_SUBSCRIPTION_ACTIVE_OK=True"
log "TEST_EMAIL=$TEST_EMAIL"
log "FINAL_STATUS=NDSP_APPROVE_PARAM_TYPES_FIXED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_APPROVE_PARAM_TYPES_FIXED"
echo "TEST_EMAIL=$TEST_EMAIL"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/access"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"
