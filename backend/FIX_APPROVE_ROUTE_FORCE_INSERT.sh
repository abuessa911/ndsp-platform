#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
SERVER="$BACKEND/src/server.js"
ENV_FILE="$BACKEND/.env"
SERVICE_NAME="ndsp-checkout-api.service"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_APPROVE_FORCE_INSERT_$(date +%Y%m%d_%H%M%S).md"

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

log "# NDSP Approve Route Force Insert"
log "- TIME=$(date -Is)"

[ -f "$SERVER" ] || fail "server.js not found: $SERVER"
[ -f "$ENV_FILE" ] || fail ".env not found: $ENV_FILE"

DB_URL="$(find_database_url || true)"
[ -n "$DB_URL" ] || fail "DATABASE_URL not found"

ADMIN_KEY="$(grep '^NDSP_ADMIN_KEY=' "$ENV_FILE" | tail -1 | cut -d= -f2- || true)"
[ -n "$ADMIN_KEY" ] || fail "NDSP_ADMIN_KEY missing"

log "PRECONDITIONS_OK=True"

python3 - "$SERVER" <<'PY'
from pathlib import Path
import sys
import time

path = Path(sys.argv[1])
text = path.read_text()
backup = path.with_name(f"server.js.bak_force_approve_{int(time.time())}")
backup.write_text(text)

new_approve = r'''
// NDSP_APPROVE_ROUTE_FORCE_BEGIN
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
      detail: error.message
    });
  } finally {
    client.release();
  }
});
// NDSP_APPROVE_ROUTE_FORCE_END
'''

def remove_marker_blocks(s: str) -> str:
    while True:
      start = s.find("// NDSP_APPROVE_ROUTE_FORCE_BEGIN")
      if start == -1:
        return s
      end = s.find("// NDSP_APPROVE_ROUTE_FORCE_END", start)
      if end == -1:
        return s[:start]
      end = s.find("\n", end)
      if end == -1:
        end = len(s)
      s = s[:start] + "\n" + s[end:]

def remove_route_by_start(s: str, marker: str) -> str:
    while True:
        start = s.find(marker)
        if start == -1:
            return s

        app_start = s.rfind("app.post", 0, start)
        if app_start == -1:
            app_start = start

        # امسح حتى بداية reject أو 404 أو نهاية route المعتادة
        candidates = []
        for next_marker in [
            'app.post("/api/v1/admin/checkout/:checkout_ref/reject"',
            "app.post('/api/v1/admin/checkout/:checkout_ref/reject'",
            "app.use((req, res)",
            "app.listen("
        ]:
            p = s.find(next_marker, start + 1)
            if p != -1:
                candidates.append(p)

        if candidates:
            end = min(candidates)
        else:
            end = s.find("\n});", start)
            if end == -1:
                end = len(s)
            else:
                end += len("\n});")

        s = s[:app_start] + "\n" + s[end:]

text = remove_marker_blocks(text)

for marker in [
    '"/api/v1/admin/checkout/:checkout_ref/approve"',
    "'/api/v1/admin/checkout/:checkout_ref/approve'"
]:
    text = remove_route_by_start(text, marker)

insert_points = [
    'app.post("/api/v1/admin/checkout/:checkout_ref/reject"',
    "app.post('/api/v1/admin/checkout/:checkout_ref/reject'",
    "app.use((req, res)",
    "app.listen("
]

insert_at = -1
for marker in insert_points:
    insert_at = text.find(marker)
    if insert_at != -1:
        break

if insert_at == -1:
    raise SystemExit("No safe insertion point found")

text = text[:insert_at] + new_approve + "\n\n" + text[insert_at:]

path.write_text(text)
print(f"BACKUP={backup}")
print("APPROVE_ROUTE_FORCE_INSERTED=True")
PY

cd "$BACKEND"
node --check src/server.js
log "APPROVE_ROUTE_FORCE_INSERTED=True"
log "SERVER_SYNTAX_OK=True"

sudo systemctl restart "$SERVICE_NAME"
sleep 3

if systemctl is-active --quiet "$SERVICE_NAME"; then
  log "SERVICE_ACTIVE=True"
else
  fail "$SERVICE_NAME failed after approve route insert"
fi

LOCAL_HEALTH="$(curl -s -o /tmp/ndsp_force_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
LOCAL_PLANS="$(curl -s -o /tmp/ndsp_force_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "LOCAL_HEALTH_CODE=$LOCAL_HEALTH"
log "LOCAL_PLANS_CODE=$LOCAL_PLANS"

[ "$LOCAL_HEALTH" = "200" ] || fail "Local health failed"
[ "$LOCAL_PLANS" = "200" ] || fail "Local plans failed"

TEST_EMAIL="ndsp.force.approve.$(date +%s)@example.com"

CHECKOUT_CODE="$(curl -s \
  -X POST http://127.0.0.1:8088/api/v1/checkout \
  -H 'Content-Type: application/json' \
  -d "{\"plan_code\":\"elite\",\"email\":\"$TEST_EMAIL\",\"telegram_id\":\"@ndsp_force_approve\",\"network\":\"TRC20\"}" \
  -o /tmp/ndsp_force_checkout.json \
  -w '%{http_code}' || true)"

log "CHECKOUT_CREATE_CODE=$CHECKOUT_CODE"
[ "$CHECKOUT_CODE" = "201" ] || fail "Checkout create failed"

CHECKOUT_REF="$(python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/ndsp_force_checkout.json").read_text())
print(data["checkout"]["checkout_ref"])
PY
)"

log "CHECKOUT_REF_CREATED=$CHECKOUT_REF"

APPROVE_CODE="$(curl -s \
  -X POST "http://127.0.0.1:8088/api/v1/admin/checkout/$CHECKOUT_REF/approve" \
  -H 'Content-Type: application/json' \
  -H "x-admin-key: $ADMIN_KEY" \
  -d '{"admin_note":"Force approve route final verification"}' \
  -o /tmp/ndsp_force_approve.json \
  -w '%{http_code}' || true)"

log "APPROVE_CODE=$APPROVE_CODE"

if [ "$APPROVE_CODE" != "200" ]; then
  log "APPROVE_RESPONSE_BEGIN"
  cat /tmp/ndsp_force_approve.json >> "$REPORT" 2>&1 || true
  log "APPROVE_RESPONSE_END"
  fail "Approve endpoint failed after force insert"
fi

STATUS_CODE="$(curl -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_force_status.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/subscription/status || true)"

log "SUBSCRIPTION_STATUS_CODE=$STATUS_CODE"
[ "$STATUS_CODE" = "200" ] || fail "Subscription status failed"

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/tmp/ndsp_force_status.json").read_text())
sub = data.get("subscription") or {}

if not sub.get("active"):
    raise SystemExit("SUBSCRIPTION_NOT_ACTIVE")

if sub.get("plan_code") != "elite":
    raise SystemExit("SUBSCRIPTION_NOT_ELITE")
PY

log "SUBSCRIPTION_ACTIVE_OK=True"

MY_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_force_my_access.json \
  -w '%{http_code}' \
  https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"

ADMIN_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_force_admin_access.json \
  -w '%{http_code}' \
  https://admin.ndsp.app/checkout-api/api/v1/subscription/status || true)"

ADMIN_REQUESTS_CODE="$(curl -s \
  -H "x-admin-key: $ADMIN_KEY" \
  -o /tmp/ndsp_force_admin_requests.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/admin/checkout/requests || true)"

MY_UI_CODE="$(curl -k -s -o /tmp/ndsp_force_my_ui.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -s -o /tmp/ndsp_force_admin_ui.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

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

for f in ["/tmp/ndsp_force_my_access.json", "/tmp/ndsp_force_admin_access.json"]:
    data = json.loads(Path(f).read_text())
    sub = data.get("subscription") or {}
    if not sub.get("active"):
        raise SystemExit(f"REMOTE_SUBSCRIPTION_NOT_ACTIVE={f}")
    if sub.get("plan_code") != "elite":
        raise SystemExit(f"REMOTE_SUBSCRIPTION_NOT_ELITE={f}")
PY

log "REMOTE_SUBSCRIPTION_ACTIVE_OK=True"
log "TEST_EMAIL=$TEST_EMAIL"
log "FINAL_STATUS=NDSP_APPROVE_FORCE_INSERT_FIXED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_APPROVE_FORCE_INSERT_FIXED"
echo "TEST_EMAIL=$TEST_EMAIL"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/access"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"
