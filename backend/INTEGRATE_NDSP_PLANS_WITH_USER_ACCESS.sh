#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
FRONTEND="$ROOT/checkout-admin-vite"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_PLANS_USER_ACCESS_INTEGRATION_$(date +%Y%m%d_%H%M%S).md"

MY_DIR="/var/www/checkout-plans"
ADMIN_DIR="/var/www/plans-console"
MIGRATION="$ROOT/database/migrations/20260524_002_subscription_activation.sql"
ENV_FILE="$BACKEND/.env"
SERVICE_NAME="ndsp-checkout-api.service"

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

  local files=(
    "$BACKEND/.env"
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

  return 1
}

log "# NDSP Plans User Access Integration"
log "- TIME=$(date -Is)"
log "- ROOT=$ROOT"
log "- BACKEND=$BACKEND"
log "- FRONTEND=$FRONTEND"

[ -d "$ROOT" ] || fail "Package root missing: $ROOT"
[ -d "$BACKEND" ] || fail "Backend missing: $BACKEND"
[ -d "$FRONTEND" ] || fail "Frontend missing: $FRONTEND"
[ -f "$ENV_FILE" ] || fail "Backend .env missing: $ENV_FILE"

DB_URL="$(find_database_url || true)"
[ -n "$DB_URL" ] || fail "DATABASE_URL not found"

ADMIN_KEY="$(grep '^NDSP_ADMIN_KEY=' "$ENV_FILE" | tail -1 | cut -d= -f2- || true)"
[ -n "$ADMIN_KEY" ] || fail "NDSP_ADMIN_KEY missing in $ENV_FILE"

log "PRECONDITIONS_OK=True"
log "DATABASE_URL_FOUND=True"
log "ADMIN_KEY_FOUND=True"

cat > "$MIGRATION" <<'SQL'
BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS ndsp_user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_email TEXT NOT NULL,
    plan_code TEXT NOT NULL REFERENCES ndsp_plans(code) ON UPDATE CASCADE,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'pending', 'suspended', 'cancelled', 'expired')),
    source_checkout_ref TEXT UNIQUE,
    activation_mode TEXT NOT NULL DEFAULT 'admin_approved',
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ,
    last_status_check_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_email_unique
ON ndsp_user_subscriptions (lower(customer_email));

CREATE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_plan_status
ON ndsp_user_subscriptions (plan_code, status);

CREATE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_source_checkout
ON ndsp_user_subscriptions (source_checkout_ref);

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

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_ndsp_checkout_activated_subscription'
    ) THEN
        ALTER TABLE ndsp_checkout_requests
        ADD CONSTRAINT fk_ndsp_checkout_activated_subscription
        FOREIGN KEY (activated_subscription_id)
        REFERENCES ndsp_user_subscriptions(id)
        ON DELETE SET NULL;
    END IF;
END $$;

CREATE OR REPLACE FUNCTION ndsp_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_ndsp_user_subscriptions_updated_at ON ndsp_user_subscriptions;
CREATE TRIGGER trg_ndsp_user_subscriptions_updated_at
BEFORE UPDATE ON ndsp_user_subscriptions
FOR EACH ROW EXECUTE FUNCTION ndsp_set_updated_at();

COMMIT;
SQL

DATABASE_URL="$DB_URL" psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"
log "SUBSCRIPTION_MIGRATION_OK=True"

python3 - "$BACKEND/src/server.js" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text()

begin = "// NDSP_SUBSCRIPTION_ACTIVATION_ENDPOINTS_BEGIN"
end = "// NDSP_SUBSCRIPTION_ACTIVATION_ENDPOINTS_END"

block = r'''
// NDSP_SUBSCRIPTION_ACTIVATION_ENDPOINTS_BEGIN

function publicPlanPayload(plan) {
  if (!plan) return null;

  return {
    code: plan.code,
    name_ar: plan.name_ar,
    name_en: plan.name_en,
    description_ar: plan.description_ar,
    description_en: plan.description_en,
    price_usd: plan.price_usd,
    currency: plan.currency,
    billing_period: plan.billing_period,
    trial_days: plan.trial_days,
    features: plan.features || [],
    limits: plan.limits || {},
    metadata: {
      public_label: plan.metadata?.public_label || plan.name_en || plan.code,
      payment_currency: plan.metadata?.payment_currency || "USDT",
      supported_networks: plan.metadata?.supported_networks || ["TRC20", "BEP20"]
    }
  };
}

function publicSubscriptionPayload(subscription, plan) {
  if (!subscription) {
    return {
      active: false,
      status: "none",
      plan_code: null,
      plan: null,
      features: [],
      limits: {}
    };
  }

  const expired = subscription.expires_at
    ? new Date(subscription.expires_at).getTime() <= Date.now()
    : false;

  const active = subscription.status === "active" && !expired;

  return {
    active,
    status: expired ? "expired" : subscription.status,
    plan_code: subscription.plan_code,
    customer_email: subscription.customer_email,
    started_at: subscription.started_at,
    expires_at: subscription.expires_at,
    source_checkout_ref: subscription.source_checkout_ref,
    plan: active ? publicPlanPayload(plan) : null,
    features: active ? (plan?.features || []) : [],
    limits: active ? (plan?.limits || {}) : {}
  };
}

/**
 * User endpoint:
 * Check current subscription and plan entitlements by email.
 */
app.get("/api/v1/subscription/status", async (req, res) => {
  const email = normalizeEmail(req.query?.email);

  if (!isValidEmail(email)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_email"
    });
  }

  try {
    const result = await query(
      `
      SELECT
        s.*,
        p.code AS plan_code_joined,
        p.name_ar,
        p.name_en,
        p.description_ar,
        p.description_en,
        p.price_usd,
        p.currency,
        p.billing_period,
        p.trial_days,
        p.features,
        p.limits,
        p.metadata AS plan_metadata
      FROM ndsp_user_subscriptions s
      JOIN ndsp_plans p ON p.code = s.plan_code
      WHERE lower(s.customer_email) = lower($1)
      ORDER BY s.updated_at DESC
      LIMIT 1
      `,
      [email]
    );

    if (result.rowCount === 0) {
      return res.json({
        ok: true,
        subscription: publicSubscriptionPayload(null, null)
      });
    }

    const row = result.rows[0];

    await query(
      `
      UPDATE ndsp_user_subscriptions
      SET last_status_check_at = now()
      WHERE id = $1
      `,
      [row.id]
    );

    const subscription = {
      id: row.id,
      customer_email: row.customer_email,
      plan_code: row.plan_code,
      status: row.status,
      source_checkout_ref: row.source_checkout_ref,
      started_at: row.started_at,
      expires_at: row.expires_at,
      metadata: row.metadata
    };

    const plan = {
      code: row.plan_code_joined,
      name_ar: row.name_ar,
      name_en: row.name_en,
      description_ar: row.description_ar,
      description_en: row.description_en,
      price_usd: row.price_usd,
      currency: row.currency,
      billing_period: row.billing_period,
      trial_days: row.trial_days,
      features: row.features,
      limits: row.limits,
      metadata: row.plan_metadata
    };

    return res.json({
      ok: true,
      subscription: publicSubscriptionPayload(subscription, plan)
    });
  } catch (error) {
    console.error("SUBSCRIPTION_STATUS_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_load_subscription_status"
    });
  }
});

/**
 * Admin endpoint:
 * List checkout requests for approval workflow.
 */
app.get("/api/v1/admin/checkout/requests", requireAdmin, async (req, res) => {
  const status = String(req.query?.status || "").trim();
  const limit = Math.min(Number(req.query?.limit || 50) || 50, 200);

  const allowedStatuses = [
    "pending_review",
    "manual_review_required",
    "waiting_payment",
    "paid_pending_activation",
    "activated",
    "rejected",
    "expired",
    "cancelled"
  ];

  if (status && !allowedStatuses.includes(status)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_status"
    });
  }

  try {
    const params = [];
    let where = "";

    if (status) {
      params.push(status);
      where = `WHERE c.status = $${params.length}`;
    }

    params.push(limit);

    const result = await query(
      `
      SELECT
        c.id,
        c.checkout_ref,
        c.plan_code,
        c.customer_email,
        c.telegram_id,
        c.amount_usd,
        c.payment_currency,
        c.payment_network,
        c.provider,
        c.provider_payment_id,
        c.provider_invoice_url,
        c.status,
        c.admin_note,
        c.public_note,
        c.expires_at,
        c.reviewed_at,
        c.created_at,
        c.updated_at,
        c.activated_subscription_id,
        p.name_ar,
        p.name_en,
        p.features,
        p.limits
      FROM ndsp_checkout_requests c
      JOIN ndsp_plans p ON p.code = c.plan_code
      ${where}
      ORDER BY c.created_at DESC
      LIMIT $${params.length}
      `,
      params
    );

    return res.json({
      ok: true,
      requests: result.rows
    });
  } catch (error) {
    console.error("ADMIN_CHECKOUT_REQUESTS_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_load_checkout_requests"
    });
  }
});

/**
 * Admin endpoint:
 * Approve checkout request and activate user subscription.
 */
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
      SELECT c.*, p.features, p.limits, p.metadata AS plan_metadata
      FROM ndsp_checkout_requests c
      JOIN ndsp_plans p ON p.code = c.plan_code
      WHERE c.checkout_ref = $1
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

    if (["rejected", "cancelled", "expired"].includes(checkout.status)) {
      await client.query("ROLLBACK");
      return res.status(409).json({
        ok: false,
        error: "checkout_request_not_approvable",
        status: checkout.status
      });
    }

    if (checkout.status === "activated" && checkout.activated_subscription_id) {
      const existingSub = await client.query(
        "SELECT * FROM ndsp_user_subscriptions WHERE id = $1 LIMIT 1",
        [checkout.activated_subscription_id]
      );

      await client.query("COMMIT");

      return res.json({
        ok: true,
        already_activated: true,
        checkout,
        subscription: existingSub.rows[0] || null
      });
    }

    const beforeSub = await client.query(
      "SELECT * FROM ndsp_user_subscriptions WHERE lower(customer_email) = lower($1) LIMIT 1",
      [checkout.customer_email]
    );

    let subResult = await client.query(
      `
      UPDATE ndsp_user_subscriptions
      SET
        plan_code = $1,
        status = 'active',
        source_checkout_ref = $2,
        activation_mode = 'admin_approved',
        started_at = now(),
        expires_at = $3::timestamptz,
        metadata = jsonb_build_object(
          'approved_from_checkout_ref', $2,
          'payment_currency', $4,
          'payment_network', $5,
          'amount_usd', $6,
          'admin_note', $7,
          'governance', jsonb_build_object(
            'mode', 'decision_active',
            'execution_policy', 'execution_sanitized'
          )
        )
      WHERE lower(customer_email) = lower($8)
      RETURNING *
      `,
      [
        checkout.plan_code,
        checkout.checkout_ref,
        expiresAt,
        checkout.payment_currency,
        checkout.payment_network,
        checkout.amount_usd,
        adminNote,
        checkout.customer_email
      ]
    );

    if (subResult.rowCount === 0) {
      subResult = await client.query(
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
          $1,
          $2,
          'active',
          $3,
          'admin_approved',
          now(),
          $4::timestamptz,
          jsonb_build_object(
            'approved_from_checkout_ref', $3,
            'payment_currency', $5,
            'payment_network', $6,
            'amount_usd', $7,
            'admin_note', $8,
            'governance', jsonb_build_object(
              'mode', 'decision_active',
              'execution_policy', 'execution_sanitized'
            )
          )
        )
        RETURNING *
        `,
        [
          checkout.customer_email,
          checkout.plan_code,
          checkout.checkout_ref,
          expiresAt,
          checkout.payment_currency,
          checkout.payment_network,
          checkout.amount_usd,
          adminNote
        ]
      );
    }

    const subscription = subResult.rows[0];

    const updatedCheckout = await client.query(
      `
      UPDATE ndsp_checkout_requests
      SET
        status = 'activated',
        reviewed_at = now(),
        admin_note = $1,
        public_note = 'Subscription activated after admin review.',
        activated_subscription_id = $2
      WHERE checkout_ref = $3
      RETURNING *
      `,
      [adminNote, subscription.id, checkout.checkout_ref]
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
      VALUES ($1, $2, 'approve_checkout_activate_subscription', 'admin', $3::jsonb, $4::jsonb)
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
    console.error("ADMIN_APPROVE_CHECKOUT_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_approve_checkout"
    });
  } finally {
    client.release();
  }
});

/**
 * Admin endpoint:
 * Reject checkout request.
 */
app.post("/api/v1/admin/checkout/:checkout_ref/reject", requireAdmin, async (req, res) => {
  const checkoutRef = String(req.params.checkout_ref || "").trim();
  const adminNote = String(req.body?.admin_note || "Rejected by admin").trim();

  if (!/^NDSP-[A-Z0-9]{8,32}$/.test(checkoutRef)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_checkout_ref"
    });
  }

  try {
    const result = await query(
      `
      UPDATE ndsp_checkout_requests
      SET
        status = 'rejected',
        reviewed_at = now(),
        admin_note = $1,
        public_note = 'Subscription request rejected after review.'
      WHERE checkout_ref = $2
        AND status <> 'activated'
      RETURNING *
      `,
      [adminNote, checkoutRef]
    );

    if (result.rowCount === 0) {
      return res.status(404).json({
        ok: false,
        error: "checkout_request_not_found_or_already_activated"
      });
    }

    await query(
      `
      INSERT INTO ndsp_subscription_audit_logs (
        customer_email,
        plan_code,
        action,
        actor,
        before_data,
        after_data
      )
      VALUES ($1, $2, 'reject_checkout_request', 'admin', NULL, $3::jsonb)
      `,
      [
        result.rows[0].customer_email,
        result.rows[0].plan_code,
        JSON.stringify(result.rows[0])
      ]
    );

    return res.json({
      ok: true,
      checkout: result.rows[0]
    });
  } catch (error) {
    console.error("ADMIN_REJECT_CHECKOUT_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_reject_checkout"
    });
  }
});

// NDSP_SUBSCRIPTION_ACTIVATION_ENDPOINTS_END
'''

pattern = re.compile(
    r"\n// NDSP_SUBSCRIPTION_ACTIVATION_ENDPOINTS_BEGIN.*?// NDSP_SUBSCRIPTION_ACTIVATION_ENDPOINTS_END\n",
    re.S,
)
text = pattern.sub("\n", text)

needle = "app.use((req, res) => {"
if needle not in text:
    raise SystemExit("Could not find 404 app.use marker")

text = text.replace(needle, block + "\n\n" + needle, 1)
path.write_text(text)
PY

log "BACKEND_ENDPOINTS_PATCHED=True"

cd "$BACKEND"
node --check src/server.js
log "BACKEND_SYNTAX_OK=True"

sudo systemctl restart "$SERVICE_NAME"
sleep 3

if systemctl is-active --quiet "$SERVICE_NAME"; then
  log "SERVICE_ACTIVE=True"
else
  sudo systemctl status "$SERVICE_NAME" --no-pager -l || true
  fail "$SERVICE_NAME failed after backend patch"
fi

cat > "$FRONTEND/.env" <<'ENV'
VITE_NDSP_API_BASE=/checkout-api
ENV

cat > "$FRONTEND/vite.config.js" <<'VITE'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()]
});
VITE

cat > "$FRONTEND/src/App.jsx" <<'JSX'
import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { apiGet, apiPost, apiPatch } from "./api.js";
import "./styles.css";

function useHashRoute() {
  const [route, setRoute] = useState(window.location.hash || "#/checkout");

  useEffect(() => {
    const handler = () => setRoute(window.location.hash || "#/checkout");
    window.addEventListener("hashchange", handler);
    return () => window.removeEventListener("hashchange", handler);
  }, []);

  return route;
}

function Notice({ type = "", children }) {
  if (!children) return null;
  return <div className={`notice ${type}`}>{children}</div>;
}

function Checkout() {
  const [plans, setPlans] = useState([]);
  const [selectedCode, setSelectedCode] = useState("");
  const [email, setEmail] = useState("");
  const [telegramId, setTelegramId] = useState("");
  const [network, setNetwork] = useState("TRC20");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");
  const [checkout, setCheckout] = useState(null);

  useEffect(() => {
    async function loadPlans() {
      try {
        setLoading(true);
        setError("");
        const data = await apiGet("/api/v1/plans");
        const loadedPlans = data.plans || [];
        setPlans(loadedPlans);
        setSelectedCode(loadedPlans[0]?.code || "");
      } catch (err) {
        setError(err.message || "failed_to_load_plans");
      } finally {
        setLoading(false);
      }
    }

    loadPlans();
  }, []);

  const selectedPlan = useMemo(() => {
    return plans.find((plan) => plan.code === selectedCode) || null;
  }, [plans, selectedCode]);

  async function submitCheckout(event) {
    event.preventDefault();

    try {
      setCreating(true);
      setError("");
      setCheckout(null);

      const data = await apiPost("/api/v1/checkout", {
        plan_code: selectedCode,
        email,
        telegram_id: telegramId,
        network
      });

      setCheckout(data.checkout);
    } catch (err) {
      setError(err.message || "failed_to_create_checkout");
    } finally {
      setCreating(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">NDSP Checkout</p>
          <h1>اختيار الباقة وطلب التفعيل</h1>
          <p className="hero-text">
            اختر الباقة المناسبة. التفعيل لا يتم تلقائيًا، وكل طلب يخضع لمراجعة إدارية قبل فتح الوصول.
          </p>
        </div>
        <div className="hero-badge">Decision Active / Execution Sanitized</div>
      </section>

      <Notice>{loading ? "جاري تحميل الباقات..." : ""}</Notice>
      <Notice type="error">{error ? `خطأ: ${error}` : ""}</Notice>

      {!loading && plans.length > 0 && (
        <section className="checkout-grid">
          <div className="plans-grid">
            {plans.map((plan) => (
              <button
                key={plan.code}
                className={`plan-card ${selectedCode === plan.code ? "selected" : ""}`}
                onClick={() => setSelectedCode(plan.code)}
                type="button"
              >
                <span className="plan-code">{plan.name_en}</span>
                <strong>${Number(plan.price_usd).toFixed(2)}</strong>
                <small>{plan.billing_period}</small>
                <p>{plan.description_ar}</p>
                <ul>
                  {(plan.features || []).slice(0, 6).map((feature) => (
                    <li key={feature}>{feature}</li>
                  ))}
                </ul>
                {plan.trial_days > 0 && (
                  <span className="trial-badge">{plan.trial_days} يوم تجربة</span>
                )}
              </button>
            ))}
          </div>

          <form className="checkout-form" onSubmit={submitCheckout}>
            <h2>بيانات الطلب</h2>

            <label>
              الباقة
              <input value={selectedPlan?.name_en || ""} readOnly />
            </label>

            <label>
              البريد الإلكتروني
              <input
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </label>

            <label>
              Telegram ID اختياري
              <input
                placeholder="@username أو ID"
                value={telegramId}
                onChange={(event) => setTelegramId(event.target.value)}
              />
            </label>

            <label>
              شبكة الدفع
              <select value={network} onChange={(event) => setNetwork(event.target.value)}>
                <option value="TRC20">USDT TRC20</option>
                <option value="BEP20">USDT BEP20</option>
              </select>
            </label>

            <div className="summary-box">
              <span>المبلغ</span>
              <strong>
                ${selectedPlan ? Number(selectedPlan.price_usd).toFixed(2) : "0.00"} / USDT
              </strong>
            </div>

            <button className="primary-btn" disabled={creating || !selectedCode}>
              {creating ? "جاري إنشاء الطلب..." : "إنشاء طلب الاشتراك"}
            </button>

            <p className="safe-note">
              لا يتم عرض أي منطق داخلي حساس. الواجهة تعرض نتيجة مؤسسية مبسطة فقط.
            </p>
          </form>
        </section>
      )}

      {checkout && (
        <section className="result-card">
          <h2>تم إنشاء الطلب</h2>
          <p>رقم الطلب: <strong>{checkout.checkout_ref}</strong></p>
          <p>الحالة: <strong>{checkout.status}</strong></p>
          <p>الباقة: <strong>{checkout.plan_code}</strong></p>
          <p>المبلغ: <strong>{checkout.amount_usd} {checkout.payment_currency}</strong></p>
          <p>الشبكة: <strong>{checkout.payment_network}</strong></p>
          <p className="safe-note">
            بعد الموافقة الإدارية ستظهر مزايا الباقة في صفحة My Access.
          </p>
        </section>
      )}
    </main>
  );
}

function MyAccess() {
  const [email, setEmail] = useState("");
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function checkAccess(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setSubscription(null);

      const data = await apiGet(`/api/v1/subscription/status?email=${encodeURIComponent(email)}`);
      setSubscription(data.subscription);
    } catch (err) {
      setError(err.message || "failed_to_load_subscription");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">NDSP Access</p>
          <h1>مزايا الباقة الحالية</h1>
          <p className="hero-text">
            أدخل بريدك لمعرفة حالة تفعيلك والمزايا المتاحة لك بعد الموافقة الإدارية.
          </p>
        </div>
        <div className="hero-badge">User Entitlements</div>
      </section>

      <form className="admin-key-card" onSubmit={checkAccess}>
        <label>
          البريد الإلكتروني
          <input
            type="email"
            value={email}
            placeholder="name@example.com"
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <button className="primary-btn" disabled={loading}>
          {loading ? "جاري الفحص..." : "فحص الوصول"}
        </button>
      </form>

      <Notice type="error">{error ? `خطأ: ${error}` : ""}</Notice>

      {subscription && (
        <section className="access-card">
          <h2>{subscription.active ? "الاشتراك مفعل" : "لا يوجد اشتراك مفعل"}</h2>
          <div className="status-pills">
            <span>{subscription.status}</span>
            {subscription.plan_code && <span>{subscription.plan_code}</span>}
          </div>

          {subscription.active && subscription.plan && (
            <>
              <p className="safe-note">
                الباقة الحالية: <strong>{subscription.plan.name_en}</strong>
              </p>

              <h3>المزايا المتاحة</h3>
              <ul className="feature-list">
                {(subscription.features || []).map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>

              <h3>حدود الباقة</h3>
              <pre className="json-box">{JSON.stringify(subscription.limits || {}, null, 2)}</pre>
            </>
          )}
        </section>
      )}
    </main>
  );
}

function AdminConsole() {
  const [adminKey, setAdminKey] = useState(() => localStorage.getItem("NDSP_ADMIN_KEY") || "");
  const [plans, setPlans] = useState([]);
  const [requests, setRequests] = useState([]);
  const [editing, setEditing] = useState({});
  const [loading, setLoading] = useState(false);
  const [savingCode, setSavingCode] = useState("");
  const [actionRef, setActionRef] = useState("");
  const [error, setError] = useState("");
  const [okMessage, setOkMessage] = useState("");

  const adminHeaders = useMemo(() => ({ "x-admin-key": adminKey }), [adminKey]);

  async function loadAll() {
    try {
      setLoading(true);
      setError("");
      setOkMessage("");

      const [plansData, requestsData] = await Promise.all([
        apiGet("/api/v1/admin/plans", { headers: adminHeaders }),
        apiGet("/api/v1/admin/checkout/requests?limit=50", { headers: adminHeaders })
      ]);

      const loadedPlans = plansData.plans || [];
      setPlans(loadedPlans);
      setRequests(requestsData.requests || []);

      const nextEditing = {};
      for (const plan of loadedPlans) {
        nextEditing[plan.code] = {
          name_ar: plan.name_ar || "",
          name_en: plan.name_en || "",
          description_ar: plan.description_ar || "",
          description_en: plan.description_en || "",
          price_usd: plan.price_usd || 0,
          billing_period: plan.billing_period || "monthly",
          trial_days: plan.trial_days || 0,
          sort_order: plan.sort_order || 100,
          is_active: Boolean(plan.is_active),
          is_public: Boolean(plan.is_public),
          features: JSON.stringify(plan.features || [], null, 2),
          limits: JSON.stringify(plan.limits || {}, null, 2),
          metadata: JSON.stringify(plan.metadata || {}, null, 2)
        };
      }

      setEditing(nextEditing);
      localStorage.setItem("NDSP_ADMIN_KEY", adminKey);
    } catch (err) {
      setError(err.message || "failed_to_load_admin_data");
    } finally {
      setLoading(false);
    }
  }

  function updateField(code, field, value) {
    setEditing((current) => ({
      ...current,
      [code]: {
        ...(current[code] || {}),
        [field]: value
      }
    }));
  }

  function safeJson(value, fallback) {
    try {
      return JSON.parse(value);
    } catch {
      return fallback;
    }
  }

  async function savePlan(code) {
    const draft = editing[code];
    if (!draft) return;

    try {
      setSavingCode(code);
      setError("");
      setOkMessage("");

      await apiPatch(`/api/v1/admin/plans/${code}`, {
        name_ar: draft.name_ar,
        name_en: draft.name_en,
        description_ar: draft.description_ar,
        description_en: draft.description_en,
        price_usd: Number(draft.price_usd),
        billing_period: draft.billing_period,
        trial_days: Number(draft.trial_days),
        sort_order: Number(draft.sort_order),
        is_active: Boolean(draft.is_active),
        is_public: Boolean(draft.is_public),
        features: safeJson(draft.features, []),
        limits: safeJson(draft.limits, {}),
        metadata: safeJson(draft.metadata, {})
      }, {
        headers: adminHeaders
      });

      setOkMessage(`تم تحديث الباقة: ${code}`);
      await loadAll();
    } catch (err) {
      setError(err.message || "failed_to_save_plan");
    } finally {
      setSavingCode("");
    }
  }

  async function approveRequest(checkoutRef) {
    try {
      setActionRef(checkoutRef);
      setError("");
      setOkMessage("");

      await apiPost(`/api/v1/admin/checkout/${checkoutRef}/approve`, {
        admin_note: "Approved from NDSP Admin Plans console"
      }, {
        headers: adminHeaders
      });

      setOkMessage(`تم تفعيل الطلب: ${checkoutRef}`);
      await loadAll();
    } catch (err) {
      setError(err.message || "failed_to_approve_request");
    } finally {
      setActionRef("");
    }
  }

  async function rejectRequest(checkoutRef) {
    try {
      setActionRef(checkoutRef);
      setError("");
      setOkMessage("");

      await apiPost(`/api/v1/admin/checkout/${checkoutRef}/reject`, {
        admin_note: "Rejected from NDSP Admin Plans console"
      }, {
        headers: adminHeaders
      });

      setOkMessage(`تم رفض الطلب: ${checkoutRef}`);
      await loadAll();
    } catch (err) {
      setError(err.message || "failed_to_reject_request");
    } finally {
      setActionRef("");
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">NDSP Admin</p>
          <h1>إدارة الباقات والتفعيلات</h1>
          <p className="hero-text">
            تعديل الباقات، مراجعة طلبات الاشتراك، وتفعيل وصول المستخدمين بعد الموافقة الإدارية.
          </p>
        </div>
        <div className="hero-badge">Admin Protected</div>
      </section>

      <section className="admin-key-card">
        <label>
          Admin Key
          <input
            dir="ltr"
            type="password"
            value={adminKey}
            onChange={(event) => setAdminKey(event.target.value)}
            placeholder="x-admin-key"
          />
        </label>
        <button className="primary-btn" onClick={loadAll} disabled={!adminKey || loading}>
          {loading ? "جاري التحميل..." : "تحميل البيانات"}
        </button>
      </section>

      <Notice type="error">{error ? `خطأ: ${error}` : ""}</Notice>
      <Notice type="success">{okMessage}</Notice>

      <section className="admin-plan-card">
        <header>
          <div>
            <p className="eyebrow">Activation Queue</p>
            <h2>طلبات التفعيل</h2>
          </div>
          <div className="status-pills">
            <span>{requests.length} requests</span>
          </div>
        </header>

        <div className="requests-grid">
          {requests.map((request) => (
            <article className="mini-card" key={request.checkout_ref}>
              <span className="plan-code">{request.checkout_ref}</span>
              <h3>{request.plan_code} — {request.status}</h3>
              <p>{request.customer_email}</p>
              <p>{request.amount_usd} {request.payment_currency} / {request.payment_network}</p>
              <div className="row-actions">
                <button
                  className="primary-btn"
                  disabled={actionRef === request.checkout_ref || request.status === "activated"}
                  onClick={() => approveRequest(request.checkout_ref)}
                >
                  {request.status === "activated" ? "مفعل" : "Approve"}
                </button>
                <button
                  className="danger-btn"
                  disabled={actionRef === request.checkout_ref || request.status === "activated"}
                  onClick={() => rejectRequest(request.checkout_ref)}
                >
                  Reject
                </button>
              </div>
            </article>
          ))}
          {requests.length === 0 && <p className="safe-note">لا توجد طلبات حالية.</p>}
        </div>
      </section>

      <section className="admin-plans-list">
        {plans.map((plan) => {
          const draft = editing[plan.code] || {};

          return (
            <article className="admin-plan-card" key={plan.code}>
              <header>
                <div>
                  <span className="plan-code">{plan.code}</span>
                  <h2>{plan.name_en}</h2>
                </div>
                <div className="status-pills">
                  <span>{plan.is_active ? "Active" : "Inactive"}</span>
                  <span>{plan.is_public ? "Public" : "Hidden"}</span>
                </div>
              </header>

              <div className="admin-form-grid">
                <label>
                  الاسم عربي
                  <input value={draft.name_ar || ""} onChange={(event) => updateField(plan.code, "name_ar", event.target.value)} />
                </label>

                <label>
                  الاسم English
                  <input dir="ltr" value={draft.name_en || ""} onChange={(event) => updateField(plan.code, "name_en", event.target.value)} />
                </label>

                <label>
                  السعر USD
                  <input type="number" step="0.01" value={draft.price_usd} onChange={(event) => updateField(plan.code, "price_usd", event.target.value)} />
                </label>

                <label>
                  Billing Period
                  <select value={draft.billing_period || "monthly"} onChange={(event) => updateField(plan.code, "billing_period", event.target.value)}>
                    <option value="monthly">monthly</option>
                    <option value="yearly">yearly</option>
                    <option value="one_time">one_time</option>
                  </select>
                </label>

                <label>
                  Trial Days
                  <input type="number" value={draft.trial_days} onChange={(event) => updateField(plan.code, "trial_days", event.target.value)} />
                </label>

                <label>
                  Sort Order
                  <input type="number" value={draft.sort_order} onChange={(event) => updateField(plan.code, "sort_order", event.target.value)} />
                </label>

                <label className="check-row">
                  <input type="checkbox" checked={Boolean(draft.is_active)} onChange={(event) => updateField(plan.code, "is_active", event.target.checked)} />
                  Active
                </label>

                <label className="check-row">
                  <input type="checkbox" checked={Boolean(draft.is_public)} onChange={(event) => updateField(plan.code, "is_public", event.target.checked)} />
                  Public
                </label>
              </div>

              <label>
                الوصف عربي
                <textarea value={draft.description_ar || ""} onChange={(event) => updateField(plan.code, "description_ar", event.target.value)} />
              </label>

              <label>
                Description English
                <textarea dir="ltr" value={draft.description_en || ""} onChange={(event) => updateField(plan.code, "description_en", event.target.value)} />
              </label>

              <div className="json-grid">
                <label>
                  features JSON
                  <textarea dir="ltr" value={draft.features || "[]"} onChange={(event) => updateField(plan.code, "features", event.target.value)} />
                </label>

                <label>
                  limits JSON
                  <textarea dir="ltr" value={draft.limits || "{}"} onChange={(event) => updateField(plan.code, "limits", event.target.value)} />
                </label>

                <label>
                  metadata JSON
                  <textarea dir="ltr" value={draft.metadata || "{}"} onChange={(event) => updateField(plan.code, "metadata", event.target.value)} />
                </label>
              </div>

              <button className="primary-btn" onClick={() => savePlan(plan.code)} disabled={savingCode === plan.code}>
                {savingCode === plan.code ? "جاري الحفظ..." : "حفظ التعديل"}
              </button>
            </article>
          );
        })}
      </section>
    </main>
  );
}

function App() {
  const route = useHashRoute();

  return (
    <>
      <nav className="top-nav">
        <a href="#/checkout">Checkout</a>
        <a href="#/access">My Access</a>
        <a href="#/admin/plans">Admin Plans</a>
      </nav>

      {route === "#/admin/plans" ? (
        <AdminConsole />
      ) : route === "#/access" ? (
        <MyAccess />
      ) : (
        <Checkout />
      )}
    </>
  );
}

createRoot(document.getElementById("root")).render(<App />);
JSX

cat >> "$FRONTEND/src/styles.css" <<'CSS'

/* NDSP subscription activation extension */
.requests-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.mini-card,
.access-card {
  border: 1px solid var(--border);
  background: rgba(2, 6, 23, 0.45);
  border-radius: 22px;
  padding: 18px;
}

.mini-card h3,
.access-card h3 {
  margin: 10px 0;
}

.mini-card p {
  color: var(--muted);
  margin: 8px 0;
  overflow-wrap: anywhere;
}

.row-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 14px;
}

.danger-btn {
  width: 100%;
  border: 1px solid rgba(251, 113, 133, 0.35);
  border-radius: 16px;
  padding: 14px 18px;
  background: rgba(251, 113, 133, 0.12);
  color: #fecdd3;
  font-weight: 900;
}

.danger-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.access-card {
  margin-top: 24px;
}

.feature-list {
  line-height: 2;
}

.json-box {
  direction: ltr;
  text-align: left;
  white-space: pre-wrap;
  border: 1px solid var(--border);
  background: rgba(2, 6, 23, 0.72);
  border-radius: 16px;
  padding: 16px;
  overflow: auto;
}

@media (max-width: 980px) {
  .requests-grid {
    grid-template-columns: 1fr;
  }
}
CSS

log "FRONTEND_PATCHED=True"

cd "$FRONTEND"
npm install
npm run build

[ -f "$FRONTEND/dist/index.html" ] || fail "Frontend dist missing"

python3 - <<'PY'
from pathlib import Path

p = Path("/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite/dist/index.html")
text = p.read_text()
marker = "<!-- NDSP_PLANS_USER_ACCESS_INTEGRATED -->"
if marker not in text:
    text = text.replace("<head>", "<head>\n  " + marker, 1)
p.write_text(text)
PY

sudo mkdir -p "$MY_DIR" "$ADMIN_DIR"
sudo rsync -a --delete "$FRONTEND/dist/" "$MY_DIR/"
sudo rsync -a --delete "$FRONTEND/dist/" "$ADMIN_DIR/"
sudo chown -R www-data:www-data "$MY_DIR" "$ADMIN_DIR"

log "FRONTEND_BUILD_AND_DEPLOY_OK=True"

LOCAL_HEALTH="$(curl -s -o /tmp/ndsp_int_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
LOCAL_PLANS="$(curl -s -o /tmp/ndsp_int_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "LOCAL_HEALTH_CODE=$LOCAL_HEALTH"
log "LOCAL_PLANS_CODE=$LOCAL_PLANS"

[ "$LOCAL_HEALTH" = "200" ] || fail "Local health failed"
[ "$LOCAL_PLANS" = "200" ] || fail "Local plans failed"

TEST_EMAIL="ndsp.activation.$(date +%s)@example.com"

CHECKOUT_CODE="$(curl -s \
  -X POST http://127.0.0.1:8088/api/v1/checkout \
  -H 'Content-Type: application/json' \
  -d "{\"plan_code\":\"elite\",\"email\":\"$TEST_EMAIL\",\"telegram_id\":\"@ndsp_activation_test\",\"network\":\"TRC20\"}" \
  -o /tmp/ndsp_int_checkout.json \
  -w '%{http_code}' || true)"

log "CHECKOUT_CREATE_CODE=$CHECKOUT_CODE"
[ "$CHECKOUT_CODE" = "201" ] || fail "Checkout create failed"

CHECKOUT_REF="$(python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/ndsp_int_checkout.json").read_text())
print(data["checkout"]["checkout_ref"])
PY
)"

log "CHECKOUT_REF_CREATED=$CHECKOUT_REF"

APPROVE_CODE="$(curl -s \
  -X POST "http://127.0.0.1:8088/api/v1/admin/checkout/$CHECKOUT_REF/approve" \
  -H 'Content-Type: application/json' \
  -H "x-admin-key: $ADMIN_KEY" \
  -d '{"admin_note":"Final integration automatic approval test"}' \
  -o /tmp/ndsp_int_approve.json \
  -w '%{http_code}' || true)"

log "APPROVE_CODE=$APPROVE_CODE"
[ "$APPROVE_CODE" = "200" ] || fail "Approve checkout failed"

STATUS_CODE="$(curl -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_int_status.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/subscription/status || true)"

log "SUBSCRIPTION_STATUS_CODE=$STATUS_CODE"
[ "$STATUS_CODE" = "200" ] || fail "Subscription status failed"

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/tmp/ndsp_int_status.json").read_text())
sub = data.get("subscription") or {}

if not sub.get("active"):
    raise SystemExit("SUBSCRIPTION_NOT_ACTIVE")

if sub.get("plan_code") != "elite":
    raise SystemExit("SUBSCRIPTION_PLAN_NOT_ELITE")
PY

log "SUBSCRIPTION_ACTIVE_OK=True"

ADMIN_REQUESTS_CODE="$(curl -s \
  -H "x-admin-key: $ADMIN_KEY" \
  -o /tmp/ndsp_int_admin_requests.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/admin/checkout/requests || true)"

log "ADMIN_REQUESTS_CODE=$ADMIN_REQUESTS_CODE"
[ "$ADMIN_REQUESTS_CODE" = "200" ] || fail "Admin checkout requests failed"

MY_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_int_my_access.json \
  -w '%{http_code}' \
  https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"

ADMIN_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_int_admin_access.json \
  -w '%{http_code}' \
  https://admin.ndsp.app/checkout-api/api/v1/subscription/status || true)"

MY_UI_CODE="$(curl -k -s -o /tmp/ndsp_int_my_ui.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -s -o /tmp/ndsp_int_admin_ui.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

log "MY_ACCESS_API_CODE=$MY_ACCESS_API_CODE"
log "ADMIN_ACCESS_API_CODE=$ADMIN_ACCESS_API_CODE"
log "MY_UI_CODE=$MY_UI_CODE"
log "ADMIN_UI_CODE=$ADMIN_UI_CODE"

[ "$MY_ACCESS_API_CODE" = "200" ] || fail "my.ndsp.app subscription status failed"
[ "$ADMIN_ACCESS_API_CODE" = "200" ] || fail "admin.ndsp.app subscription status failed"
[ "$MY_UI_CODE" = "200" ] || fail "my.ndsp.app UI failed"
[ "$ADMIN_UI_CODE" = "200" ] || fail "admin.ndsp.app UI failed"

grep -q "NDSP_PLANS_USER_ACCESS_INTEGRATED" /tmp/ndsp_int_my_ui.html || fail "My UI integration marker missing"
grep -q "NDSP_PLANS_USER_ACCESS_INTEGRATED" /tmp/ndsp_int_admin_ui.html || fail "Admin UI integration marker missing"

log "REMOTE_UI_AND_API_OK=True"
log "TEST_EMAIL=$TEST_EMAIL"
log "FINAL_STATUS=NDSP_PLANS_USER_ACCESS_INTEGRATED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_PLANS_USER_ACCESS_INTEGRATED"
echo "TEST_EMAIL=$TEST_EMAIL"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/access"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"
