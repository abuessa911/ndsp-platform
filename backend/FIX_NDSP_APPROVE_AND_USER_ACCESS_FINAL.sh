#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BACKEND="$ROOT/backend-express"
ENV_FILE="$BACKEND/.env"
SERVICE_NAME="ndsp-checkout-api.service"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_APPROVE_USER_ACCESS_FINAL_FIX_$(date +%Y%m%d_%H%M%S).md"
MIGRATION="$ROOT/database/migrations/20260524_003_fix_subscription_approve_upsert.sql"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  log ""
  log "=== SERVICE STATUS ==="
  sudo systemctl status "$SERVICE_NAME" --no-pager -l >> "$REPORT" 2>&1 || true
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

log "# NDSP Approve + User Access Final Fix"
log "- TIME=$(date -Is)"
log "- BACKEND=$BACKEND"

[ -d "$BACKEND" ] || fail "Backend not found: $BACKEND"
[ -f "$ENV_FILE" ] || fail "Env file not found: $ENV_FILE"
[ -f "$BACKEND/src/server.js" ] || fail "server.js not found"

DB_URL="$(find_database_url || true)"
[ -n "$DB_URL" ] || fail "DATABASE_URL not found"

ADMIN_KEY="$(grep '^NDSP_ADMIN_KEY=' "$ENV_FILE" | tail -1 | cut -d= -f2- || true)"
[ -n "$ADMIN_KEY" ] || fail "NDSP_ADMIN_KEY missing"

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

UPDATE ndsp_user_subscriptions
SET customer_email = lower(trim(customer_email))
WHERE customer_email <> lower(trim(customer_email));

WITH ranked AS (
    SELECT
        id,
        row_number() OVER (
            PARTITION BY lower(customer_email)
            ORDER BY updated_at DESC, created_at DESC, id DESC
        ) AS rn
    FROM ndsp_user_subscriptions
),
dupes AS (
    SELECT id FROM ranked WHERE rn > 1
)
UPDATE ndsp_checkout_requests
SET activated_subscription_id = NULL
WHERE activated_subscription_id IN (SELECT id FROM dupes);

WITH ranked AS (
    SELECT
        id,
        row_number() OVER (
            PARTITION BY lower(customer_email)
            ORDER BY updated_at DESC, created_at DESC, id DESC
        ) AS rn
    FROM ndsp_user_subscriptions
)
DELETE FROM ndsp_user_subscriptions
WHERE id IN (SELECT id FROM ranked WHERE rn > 1);

ALTER TABLE ndsp_user_subscriptions
DROP CONSTRAINT IF EXISTS ndsp_user_subscriptions_source_checkout_ref_key;

DROP INDEX IF EXISTS idx_ndsp_user_subscriptions_email_unique;
DROP INDEX IF EXISTS idx_ndsp_user_subscriptions_source_checkout;

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

CREATE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_plan_status
ON ndsp_user_subscriptions (plan_code, status);

CREATE INDEX IF NOT EXISTS idx_ndsp_user_subscriptions_source_checkout
ON ndsp_user_subscriptions (source_checkout_ref);

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

psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"
log "DB_APPROVE_FIX_MIGRATION_OK=True"

cp "$BACKEND/src/server.js" "$BACKEND/src/server.js.bak_approve_fix_$(date +%Y%m%d_%H%M%S)"

cat > "$BACKEND/src/server.js" <<'JS'
import "dotenv/config";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { pool, query } from "./db.js";

const app = express();

const PORT = Number(process.env.PORT || 8088);
const CORS_ORIGIN = process.env.CORS_ORIGIN || "*";
const ADMIN_KEY = process.env.NDSP_ADMIN_KEY || "";

app.use(helmet());
app.use(cors({ origin: CORS_ORIGIN === "*" ? true : CORS_ORIGIN }));
app.use(express.json({ limit: "1mb" }));

function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPlanCode(code) {
  return /^[a-z0-9_-]{2,40}$/.test(String(code || ""));
}

function getClientIp(req) {
  const forwarded = req.headers["x-forwarded-for"];
  if (typeof forwarded === "string" && forwarded.length > 0) {
    return forwarded.split(",")[0].trim();
  }
  return req.socket.remoteAddress || null;
}

function requireAdmin(req, res, next) {
  const incoming = req.header("x-admin-key") || "";

  if (!ADMIN_KEY) {
    return res.status(500).json({
      ok: false,
      error: "admin_key_not_configured"
    });
  }

  if (incoming !== ADMIN_KEY) {
    return res.status(401).json({
      ok: false,
      error: "unauthorized"
    });
  }

  return next();
}

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
      supported_networks: plan.metadata?.supported_networks || ["TRC20", "BEP20"],
      manual_activation: true
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

app.get("/health", (req, res) => {
  res.json({
    ok: true,
    service: "ndsp-checkout-plans-express",
    version: "1.1.0",
    subscriptions: true
  });
});

app.get("/api/v1/plans", async (req, res) => {
  try {
    const result = await query(`
      SELECT
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
        features,
        limits,
        metadata
      FROM ndsp_plans
      WHERE is_active = TRUE
        AND is_public = TRUE
      ORDER BY sort_order ASC, price_usd ASC
    `);

    return res.json({
      ok: true,
      plans: result.rows
    });
  } catch (error) {
    console.error("GET_PLANS_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_load_plans"
    });
  }
});

app.post("/api/v1/checkout", async (req, res) => {
  const planCode = String(req.body?.plan_code || "").trim().toLowerCase();
  const email = normalizeEmail(req.body?.email);
  const telegramId = String(req.body?.telegram_id || "").trim() || null;
  const network = String(req.body?.network || "TRC20").trim().toUpperCase();

  if (!isValidPlanCode(planCode)) {
    return res.status(400).json({ ok: false, error: "invalid_plan_code" });
  }

  if (!isValidEmail(email)) {
    return res.status(400).json({ ok: false, error: "invalid_email" });
  }

  if (!["TRC20", "BEP20"].includes(network)) {
    return res.status(400).json({
      ok: false,
      error: "unsupported_network",
      supported_networks: ["TRC20", "BEP20"]
    });
  }

  try {
    const planResult = await query(
      `
      SELECT
        code,
        name_ar,
        name_en,
        price_usd,
        currency,
        billing_period,
        trial_days,
        features,
        limits,
        metadata
      FROM ndsp_plans
      WHERE code = $1
        AND is_active = TRUE
        AND is_public = TRUE
      LIMIT 1
      `,
      [planCode]
    );

    if (planResult.rowCount === 0) {
      return res.status(404).json({
        ok: false,
        error: "plan_not_available"
      });
    }

    const plan = planResult.rows[0];

    const insertResult = await query(
      `
      INSERT INTO ndsp_checkout_requests (
        plan_code,
        customer_email,
        telegram_id,
        amount_usd,
        payment_currency,
        payment_network,
        status,
        public_note,
        request_ip,
        user_agent,
        metadata
      )
      VALUES (
        $1,
        $2,
        $3,
        $4,
        'USDT',
        $5,
        'pending_review',
        $6,
        $7::inet,
        $8,
        $9::jsonb
      )
      RETURNING
        id,
        checkout_ref,
        plan_code,
        customer_email,
        amount_usd,
        payment_currency,
        payment_network,
        status,
        expires_at,
        created_at
      `,
      [
        plan.code,
        email,
        telegramId,
        plan.price_usd,
        network,
        "Checkout request received and pending manual review.",
        getClientIp(req),
        req.header("user-agent") || null,
        JSON.stringify({
          source: "vite_checkout",
          plan_snapshot: plan,
          manual_activation: true,
          governance: {
            mode: "decision_active",
            execution_policy: "execution_sanitized"
          }
        })
      ]
    );

    return res.status(201).json({
      ok: true,
      checkout: insertResult.rows[0],
      message_ar: "تم إنشاء طلب الاشتراك. التفعيل لا يتم تلقائيًا وسيخضع للمراجعة.",
      message_en: "Checkout request created. Activation is not automatic and requires review."
    });
  } catch (error) {
    console.error("CREATE_CHECKOUT_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_create_checkout"
    });
  }
});

app.get("/api/v1/admin/plans", requireAdmin, async (req, res) => {
  try {
    const result = await query(`
      SELECT
        id,
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
        metadata,
        created_at,
        updated_at
      FROM ndsp_plans
      ORDER BY sort_order ASC, price_usd ASC
    `);

    return res.json({
      ok: true,
      plans: result.rows
    });
  } catch (error) {
    console.error("ADMIN_GET_PLANS_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_load_admin_plans"
    });
  }
});

app.patch("/api/v1/admin/plans/:code", requireAdmin, async (req, res) => {
  const code = String(req.params.code || "").trim().toLowerCase();

  if (!isValidPlanCode(code)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_plan_code"
    });
  }

  const allowedFields = {
    name_ar: "name_ar",
    name_en: "name_en",
    description_ar: "description_ar",
    description_en: "description_en",
    price_usd: "price_usd",
    currency: "currency",
    billing_period: "billing_period",
    trial_days: "trial_days",
    sort_order: "sort_order",
    is_active: "is_active",
    is_public: "is_public",
    features: "features",
    limits: "limits",
    metadata: "metadata"
  };

  const body = req.body || {};
  const entries = Object.entries(body).filter(([key]) => allowedFields[key]);

  if (entries.length === 0) {
    return res.status(400).json({
      ok: false,
      error: "no_allowed_fields_to_update"
    });
  }

  if (body.billing_period && !["monthly", "yearly", "one_time"].includes(body.billing_period)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_billing_period"
    });
  }

  if (body.price_usd !== undefined && Number(body.price_usd) < 0) {
    return res.status(400).json({
      ok: false,
      error: "invalid_price_usd"
    });
  }

  if (body.trial_days !== undefined && Number(body.trial_days) < 0) {
    return res.status(400).json({
      ok: false,
      error: "invalid_trial_days"
    });
  }

  const client = await pool.connect();

  try {
    await client.query("BEGIN");

    const beforeResult = await client.query(
      "SELECT * FROM ndsp_plans WHERE code = $1 LIMIT 1",
      [code]
    );

    if (beforeResult.rowCount === 0) {
      await client.query("ROLLBACK");
      return res.status(404).json({
        ok: false,
        error: "plan_not_found"
      });
    }

    const setParts = [];
    const values = [];
    let index = 1;

    for (const [key, rawValue] of entries) {
      const column = allowedFields[key];

      if (["features", "limits", "metadata"].includes(key)) {
        setParts.push(`${column} = $${index}::jsonb`);
        values.push(JSON.stringify(rawValue));
      } else {
        setParts.push(`${column} = $${index}`);
        values.push(rawValue);
      }

      index += 1;
    }

    values.push(code);

    const updateSql = `
      UPDATE ndsp_plans
      SET ${setParts.join(", ")}
      WHERE code = $${index}
      RETURNING *
    `;

    const updateResult = await client.query(updateSql, values);
    const updated = updateResult.rows[0];

    await client.query(
      `
      INSERT INTO ndsp_plan_audit_logs (
        plan_code,
        action,
        actor,
        before_data,
        after_data
      )
      VALUES ($1, 'update_plan', 'admin', $2::jsonb, $3::jsonb)
      `,
      [
        code,
        JSON.stringify(beforeResult.rows[0]),
        JSON.stringify(updated)
      ]
    );

    await client.query("COMMIT");

    return res.json({
      ok: true,
      plan: updated
    });
  } catch (error) {
    await client.query("ROLLBACK");
    console.error("ADMIN_UPDATE_PLAN_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_update_plan"
    });
  } finally {
    client.release();
  }
});

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
      WHERE s.customer_email = $1
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
      "SELECT * FROM ndsp_user_subscriptions WHERE customer_email = $1 LIMIT 1",
      [normalizedEmail]
    );

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
        checkout.plan_code,
        checkout.checkout_ref,
        expiresAt,
        checkout.payment_currency,
        checkout.payment_network,
        checkout.amount_usd,
        adminNote
      ]
    );

    const subscription = subscriptionResult.rows[0];

    const updatedCheckout = await client.query(
      `
      UPDATE ndsp_checkout_requests
      SET
        customer_email = $1,
        status = 'activated',
        reviewed_at = now(),
        admin_note = $2,
        public_note = 'Subscription activated after admin review.',
        activated_subscription_id = $3
      WHERE checkout_ref = $4
      RETURNING *
      `,
      [normalizedEmail, adminNote, subscription.id, checkout.checkout_ref]
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
    console.error("ADMIN_APPROVE_CHECKOUT_ERROR", {
      message: error.message,
      code: error.code,
      detail: error.detail,
      constraint: error.constraint
    });

    return res.status(500).json({
      ok: false,
      error: "failed_to_approve_checkout"
    });
  } finally {
    client.release();
  }
});

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

app.use((req, res) => {
  res.status(404).json({
    ok: false,
    error: "not_found"
  });
});

app.listen(PORT, () => {
  console.log(`NDSP checkout/plans Express API listening on port ${PORT}`);
});
JS

cd "$BACKEND"
node --check src/server.js
log "SERVER_REWRITE_SYNTAX_OK=True"

sudo systemctl restart "$SERVICE_NAME"
sleep 3

if systemctl is-active --quiet "$SERVICE_NAME"; then
  log "SERVICE_ACTIVE=True"
else
  fail "$SERVICE_NAME failed after server rewrite"
fi

LOCAL_HEALTH="$(curl -s -o /tmp/ndsp_fix_health.json -w '%{http_code}' http://127.0.0.1:8088/health || true)"
LOCAL_PLANS="$(curl -s -o /tmp/ndsp_fix_plans.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"

log "LOCAL_HEALTH_CODE=$LOCAL_HEALTH"
log "LOCAL_PLANS_CODE=$LOCAL_PLANS"

[ "$LOCAL_HEALTH" = "200" ] || fail "Local health failed"
[ "$LOCAL_PLANS" = "200" ] || fail "Local plans failed"

TEST_EMAIL="ndsp.approve.fix.$(date +%s)@example.com"

CHECKOUT_CODE="$(curl -s \
  -X POST http://127.0.0.1:8088/api/v1/checkout \
  -H 'Content-Type: application/json' \
  -d "{\"plan_code\":\"elite\",\"email\":\"$TEST_EMAIL\",\"telegram_id\":\"@ndsp_approve_fix\",\"network\":\"TRC20\"}" \
  -o /tmp/ndsp_fix_checkout.json \
  -w '%{http_code}' || true)"

log "CHECKOUT_CREATE_CODE=$CHECKOUT_CODE"
[ "$CHECKOUT_CODE" = "201" ] || fail "Checkout create failed"

CHECKOUT_REF="$(python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/ndsp_fix_checkout.json").read_text())
print(data["checkout"]["checkout_ref"])
PY
)"

log "CHECKOUT_REF_CREATED=$CHECKOUT_REF"

APPROVE_CODE="$(curl -s \
  -X POST "http://127.0.0.1:8088/api/v1/admin/checkout/$CHECKOUT_REF/approve" \
  -H 'Content-Type: application/json' \
  -H "x-admin-key: $ADMIN_KEY" \
  -d '{"admin_note":"Approve endpoint final fix verification"}' \
  -o /tmp/ndsp_fix_approve.json \
  -w '%{http_code}' || true)"

log "APPROVE_CODE=$APPROVE_CODE"

if [ "$APPROVE_CODE" != "200" ]; then
  log "APPROVE_RESPONSE_BEGIN"
  cat /tmp/ndsp_fix_approve.json >> "$REPORT" 2>&1 || true
  log "APPROVE_RESPONSE_END"
  fail "Approve endpoint still failed"
fi

STATUS_CODE="$(curl -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_fix_status.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/subscription/status || true)"

log "SUBSCRIPTION_STATUS_CODE=$STATUS_CODE"
[ "$STATUS_CODE" = "200" ] || fail "Subscription status failed"

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/tmp/ndsp_fix_status.json").read_text())
sub = data.get("subscription") or {}

if not sub.get("active"):
    raise SystemExit("SUBSCRIPTION_NOT_ACTIVE")

if sub.get("plan_code") != "elite":
    raise SystemExit("SUBSCRIPTION_NOT_ELITE")
PY

log "SUBSCRIPTION_ACTIVE_OK=True"

ADMIN_REQUESTS_CODE="$(curl -s \
  -H "x-admin-key: $ADMIN_KEY" \
  -o /tmp/ndsp_fix_admin_requests.json \
  -w '%{http_code}' \
  http://127.0.0.1:8088/api/v1/admin/checkout/requests || true)"

log "ADMIN_REQUESTS_CODE=$ADMIN_REQUESTS_CODE"
[ "$ADMIN_REQUESTS_CODE" = "200" ] || fail "Admin requests endpoint failed"

MY_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_fix_my_access.json \
  -w '%{http_code}' \
  https://my.ndsp.app/checkout-api/api/v1/subscription/status || true)"

ADMIN_ACCESS_API_CODE="$(curl -k -sG \
  --data-urlencode "email=$TEST_EMAIL" \
  -o /tmp/ndsp_fix_admin_access.json \
  -w '%{http_code}' \
  https://admin.ndsp.app/checkout-api/api/v1/subscription/status || true)"

log "MY_ACCESS_API_CODE=$MY_ACCESS_API_CODE"
log "ADMIN_ACCESS_API_CODE=$ADMIN_ACCESS_API_CODE"

[ "$MY_ACCESS_API_CODE" = "200" ] || fail "my.ndsp.app subscription API failed"
[ "$ADMIN_ACCESS_API_CODE" = "200" ] || fail "admin.ndsp.app subscription API failed"

python3 - <<'PY'
import json
from pathlib import Path

for f in ["/tmp/ndsp_fix_my_access.json", "/tmp/ndsp_fix_admin_access.json"]:
    data = json.loads(Path(f).read_text())
    sub = data.get("subscription") or {}
    if not sub.get("active"):
        raise SystemExit(f"REMOTE_SUBSCRIPTION_NOT_ACTIVE={f}")
    if sub.get("plan_code") != "elite":
        raise SystemExit(f"REMOTE_SUBSCRIPTION_NOT_ELITE={f}")
PY

log "REMOTE_SUBSCRIPTION_ACTIVE_OK=True"

MY_UI_CODE="$(curl -k -s -o /tmp/ndsp_fix_my_ui.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -s -o /tmp/ndsp_fix_admin_ui.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

log "MY_UI_CODE=$MY_UI_CODE"
log "ADMIN_UI_CODE=$ADMIN_UI_CODE"

[ "$MY_UI_CODE" = "200" ] || fail "my UI failed"
[ "$ADMIN_UI_CODE" = "200" ] || fail "admin UI failed"

log "TEST_EMAIL=$TEST_EMAIL"
log "FINAL_STATUS=NDSP_APPROVE_USER_ACCESS_FIXED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_APPROVE_USER_ACCESS_FIXED"
echo "TEST_EMAIL=$TEST_EMAIL"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/access"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"
