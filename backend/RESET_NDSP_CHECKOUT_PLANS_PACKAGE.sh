#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
BROKEN_INSTALLER="$PWD/install_ndsp_checkout_plans_package.sh"
STAMP="$(date +%Y%m%d_%H%M%S)"

echo "=== NDSP CHECKOUT + ADMIN PLANS CLEAN RESET ==="

if [ -f "$BROKEN_INSTALLER" ]; then
  cp "$BROKEN_INSTALLER" "$BROKEN_INSTALLER.broken_$STAMP.bak"
  rm -f "$BROKEN_INSTALLER"
  echo "BROKEN_INSTALLER_BACKUP=$BROKEN_INSTALLER.broken_$STAMP.bak"
fi

mkdir -p \
  "$ROOT/database/migrations" \
  "$ROOT/scripts" \
  "$ROOT/backend-express/src" \
  "$ROOT/checkout-admin-vite/src/pages"

cat > "$ROOT/database/migrations/20260524_001_checkout_plans.sql" <<'SQL_EOF_NDSP'
BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS ndsp_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT NOT NULL UNIQUE,
    name_ar TEXT NOT NULL,
    name_en TEXT NOT NULL,
    description_ar TEXT NOT NULL DEFAULT '',
    description_en TEXT NOT NULL DEFAULT '',
    price_usd NUMERIC(12,2) NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    billing_period TEXT NOT NULL DEFAULT 'monthly'
        CHECK (billing_period IN ('monthly', 'yearly', 'one_time')),
    trial_days INTEGER NOT NULL DEFAULT 0 CHECK (trial_days >= 0),
    sort_order INTEGER NOT NULL DEFAULT 100,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    features JSONB NOT NULL DEFAULT '[]'::jsonb,
    limits JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ndsp_plans_active_public
ON ndsp_plans (is_active, is_public, sort_order);

CREATE TABLE IF NOT EXISTS ndsp_checkout_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    checkout_ref TEXT NOT NULL UNIQUE DEFAULT (
        'NDSP-' || upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 12))
    ),
    plan_code TEXT NOT NULL REFERENCES ndsp_plans(code) ON UPDATE CASCADE,
    customer_email TEXT NOT NULL,
    telegram_id TEXT,
    amount_usd NUMERIC(12,2) NOT NULL,
    payment_currency TEXT NOT NULL DEFAULT 'USDT',
    payment_network TEXT NOT NULL DEFAULT 'TRC20'
        CHECK (payment_network IN ('TRC20', 'BEP20')),
    provider TEXT NOT NULL DEFAULT 'manual_or_nowpayments',
    provider_payment_id TEXT,
    provider_invoice_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending_review'
        CHECK (
            status IN (
                'pending_review',
                'manual_review_required',
                'waiting_payment',
                'paid_pending_activation',
                'activated',
                'rejected',
                'expired',
                'cancelled'
            )
        ),
    admin_note TEXT,
    public_note TEXT,
    request_ip INET,
    user_agent TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (now() + interval '24 hours'),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ndsp_checkout_email_created
ON ndsp_checkout_requests (customer_email, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ndsp_checkout_status_created
ON ndsp_checkout_requests (status, created_at DESC);

CREATE TABLE IF NOT EXISTS ndsp_plan_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    plan_code TEXT NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL DEFAULT 'admin',
    before_data JSONB,
    after_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION ndsp_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_ndsp_plans_updated_at ON ndsp_plans;
CREATE TRIGGER trg_ndsp_plans_updated_at
BEFORE UPDATE ON ndsp_plans
FOR EACH ROW EXECUTE FUNCTION ndsp_set_updated_at();

DROP TRIGGER IF EXISTS trg_ndsp_checkout_updated_at ON ndsp_checkout_requests;
CREATE TRIGGER trg_ndsp_checkout_updated_at
BEFORE UPDATE ON ndsp_checkout_requests
FOR EACH ROW EXECUTE FUNCTION ndsp_set_updated_at();

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
VALUES
(
    'pro',
    'Pro',
    'Pro',
    'وصول احترافي لبيئة دعم القرار مع عرض مؤسسي مبسط.',
    'Professional access to the decision-support environment with simplified institutional output.',
    49.00,
    'USD',
    'monthly',
    0,
    10,
    TRUE,
    TRUE,
    '["Market context overview","Decision-support dashboard","Public sanitized output","Core assets coverage"]'::jsonb,
    '{"max_assets":25,"decision_depth":"standard","admin_review_required":true}'::jsonb,
    '{"public_label":"Pro","payment_currency":"USDT","supported_networks":["TRC20","BEP20"]}'::jsonb
),
(
    'elite',
    'Elite',
    'Elite',
    'وصول موسع لطبقات التحليل المؤسسية مع شرح أعمق للحالة.',
    'Expanded access to institutional analytical layers with deeper scenario explanation.',
    149.00,
    'USD',
    'monthly',
    16,
    20,
    TRUE,
    TRUE,
    '["Advanced market interpretation","Expanded asset coverage","Elite decision surface","Scenario explanation","Sanitized multi-layer output"]'::jsonb,
    '{"max_assets":100,"decision_depth":"advanced","trial_days":16,"admin_review_required":true}'::jsonb,
    '{"public_label":"Elite","payment_currency":"USDT","supported_networks":["TRC20","BEP20"],"manual_activation":true}'::jsonb
),
(
    'saas',
    'SaaS',
    'SaaS',
    'حزمة مؤسسية مخصصة للفرق والجهات التي تحتاج بيئة تشغيل أوسع.',
    'Institutional package for teams and organizations requiring broader operating access.',
    499.00,
    'USD',
    'monthly',
    0,
    30,
    TRUE,
    TRUE,
    '["Institutional workspace","Team-oriented access","Extended reporting","Priority review","Governance-safe output"]'::jsonb,
    '{"max_assets":500,"decision_depth":"institutional","team_access":true,"admin_review_required":true}'::jsonb,
    '{"public_label":"SaaS","payment_currency":"USDT","supported_networks":["TRC20","BEP20"],"manual_activation":true}'::jsonb
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

COMMIT;
SQL_EOF_NDSP

cat > "$ROOT/scripts/run_migration.sh" <<'RUN_MIGRATION_EOF_NDSP'
#!/usr/bin/env bash
set -Eeuo pipefail

if [ -z "${DATABASE_URL:-}" ]; then
  echo "ERROR: DATABASE_URL is required"
  echo "Example:"
  echo "DATABASE_URL='postgresql://user:pass@127.0.0.1:5432/ndsp' bash scripts/run_migration.sh"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATION="$ROOT_DIR/database/migrations/20260524_001_checkout_plans.sql"

psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"

echo "MIGRATION_OK=True"
RUN_MIGRATION_EOF_NDSP

chmod +x "$ROOT/scripts/run_migration.sh"

cat > "$ROOT/backend-express/package.json" <<'BACKEND_PACKAGE_EOF_NDSP'
{
  "name": "ndsp-checkout-plans-express",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.7",
    "express": "^4.19.2",
    "helmet": "^7.1.0",
    "pg": "^8.12.0"
  }
}
BACKEND_PACKAGE_EOF_NDSP

cat > "$ROOT/backend-express/.env.example" <<'BACKEND_ENV_EOF_NDSP'
PORT=8088
DATABASE_URL=postgresql://ndsp_user:change_me@127.0.0.1:5432/ndsp
NDSP_ADMIN_KEY=change_this_admin_key
CORS_ORIGIN=http://localhost:5173
BACKEND_ENV_EOF_NDSP

cat > "$ROOT/backend-express/src/db.js" <<'BACKEND_DB_EOF_NDSP'
import pg from "pg";

const { Pool } = pg;

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is required");
}

export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 8000
});

export async function query(text, params = []) {
  return pool.query(text, params);
}
BACKEND_DB_EOF_NDSP

cat > "$ROOT/backend-express/src/server.js" <<'BACKEND_SERVER_EOF_NDSP'
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

app.get("/health", (req, res) => {
  res.json({
    ok: true,
    service: "ndsp-checkout-plans-express",
    version: "1.0.0"
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

app.use((req, res) => {
  res.status(404).json({
    ok: false,
    error: "not_found"
  });
});

app.listen(PORT, () => {
  console.log(`NDSP checkout/plans Express API listening on port ${PORT}`);
});
BACKEND_SERVER_EOF_NDSP

cat > "$ROOT/checkout-admin-vite/package.json" <<'FRONTEND_PACKAGE_EOF_NDSP'
{
  "name": "ndsp-checkout-admin-vite",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 5173",
    "build": "vite build",
    "preview": "vite preview --host 0.0.0.0 --port 5173"
  },
  "dependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }
}
FRONTEND_PACKAGE_EOF_NDSP

cat > "$ROOT/checkout-admin-vite/index.html" <<'FRONTEND_HTML_EOF_NDSP'
<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>NDSP Checkout & Admin Plans</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/App.jsx"></script>
  </body>
</html>
FRONTEND_HTML_EOF_NDSP

cat > "$ROOT/checkout-admin-vite/.env.example" <<'FRONTEND_ENV_EOF_NDSP'
VITE_NDSP_API_BASE=http://localhost:8088
FRONTEND_ENV_EOF_NDSP

cat > "$ROOT/checkout-admin-vite/src/api.js" <<'FRONTEND_API_EOF_NDSP'
const API_BASE = import.meta.env.VITE_NDSP_API_BASE || "http://localhost:8088";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "request_failed");
  }

  return data;
}

export function apiGet(path, options = {}) {
  return request(path, {
    method: "GET",
    headers: options.headers || {}
  });
}

export function apiPost(path, body, options = {}) {
  return request(path, {
    method: "POST",
    headers: options.headers || {},
    body: JSON.stringify(body)
  });
}

export function apiPatch(path, body, options = {}) {
  return request(path, {
    method: "PATCH",
    headers: options.headers || {},
    body: JSON.stringify(body)
  });
}
FRONTEND_API_EOF_NDSP

cat > "$ROOT/checkout-admin-vite/src/App.jsx" <<'FRONTEND_APP_EOF_NDSP'
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

      {loading && <div className="notice">جاري تحميل الباقات...</div>}
      {error && <div className="notice error">خطأ: {error}</div>}

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
                  {(plan.features || []).slice(0, 5).map((feature) => (
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
            احتفظ برقم الطلب. سيتم التفعيل بعد المراجعة الإدارية.
          </p>
        </section>
      )}
    </main>
  );
}

function AdminPlans() {
  const [adminKey, setAdminKey] = useState(() => localStorage.getItem("NDSP_ADMIN_KEY") || "");
  const [plans, setPlans] = useState([]);
  const [editing, setEditing] = useState({});
  const [loading, setLoading] = useState(false);
  const [savingCode, setSavingCode] = useState("");
  const [error, setError] = useState("");
  const [okMessage, setOkMessage] = useState("");

  async function loadPlans() {
    try {
      setLoading(true);
      setError("");
      setOkMessage("");

      const data = await apiGet("/api/v1/admin/plans", {
        headers: {
          "x-admin-key": adminKey
        }
      });

      const loadedPlans = data.plans || [];
      setPlans(loadedPlans);

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
      setError(err.message || "failed_to_load_admin_plans");
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
        headers: {
          "x-admin-key": adminKey
        }
      });

      setOkMessage(`تم تحديث الباقة: ${code}`);
      await loadPlans();
    } catch (err) {
      setError(err.message || "failed_to_save_plan");
    } finally {
      setSavingCode("");
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">NDSP Admin</p>
          <h1>إدارة الباقات</h1>
          <p className="hero-text">
            تعديل الأسعار، حالة الظهور، مدة التجربة، والخصائص العامة بدون كشف أي منطق داخلي حساس.
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
        <button className="primary-btn" onClick={loadPlans} disabled={!adminKey || loading}>
          {loading ? "جاري التحميل..." : "تحميل الباقات"}
        </button>
      </section>

      {error && <div className="notice error">خطأ: {error}</div>}
      {okMessage && <div className="notice success">{okMessage}</div>}

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
        <a href="#/admin/plans">Admin Plans</a>
      </nav>

      {route === "#/admin/plans" ? <AdminPlans /> : <Checkout />}
    </>
  );
}

createRoot(document.getElementById("root")).render(<App />);
FRONTEND_APP_EOF_NDSP

cat > "$ROOT/checkout-admin-vite/src/styles.css" <<'FRONTEND_CSS_EOF_NDSP'
:root {
  color-scheme: dark;
  --bg: #050816;
  --panel: rgba(15, 23, 42, 0.78);
  --border: rgba(148, 163, 184, 0.18);
  --text: #e5edf7;
  --muted: #94a3b8;
  --gold: #f5c451;
  --cyan: #45d5ff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background:
    radial-gradient(circle at top left, rgba(69, 213, 255, 0.16), transparent 32rem),
    radial-gradient(circle at top right, rgba(245, 196, 81, 0.14), transparent 30rem),
    linear-gradient(180deg, #050816, #08111f 55%, #050816);
  color: var(--text);
}

button,
input,
select,
textarea {
  font: inherit;
}

button {
  cursor: pointer;
}

.top-nav {
  width: min(1180px, calc(100% - 32px));
  margin: 20px auto 0;
  display: flex;
  gap: 12px;
}

.top-nav a {
  color: var(--text);
  text-decoration: none;
  border: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.72);
  padding: 10px 14px;
  border-radius: 999px;
}

.page-shell {
  width: min(1180px, calc(100% - 32px));
  margin: 26px auto 80px;
}

.hero-card,
.admin-key-card,
.result-card,
.notice,
.checkout-form,
.admin-plan-card,
.plan-card {
  border: 1px solid var(--border);
  background: var(--panel);
  backdrop-filter: blur(18px);
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.28);
}

.hero-card {
  min-height: 230px;
  border-radius: 32px;
  padding: 34px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.eyebrow {
  margin: 0 0 12px;
  color: var(--gold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-weight: 700;
}

h1 {
  margin: 0;
  font-size: clamp(34px, 5vw, 62px);
  line-height: 1.05;
}

.hero-text {
  max-width: 720px;
  color: var(--muted);
  font-size: 18px;
  line-height: 1.9;
}

.hero-badge,
.trial-badge,
.status-pills span {
  border: 1px solid rgba(245, 196, 81, 0.24);
  color: var(--gold);
  background: rgba(245, 196, 81, 0.08);
  border-radius: 999px;
  padding: 10px 14px;
  white-space: nowrap;
}

.notice {
  margin: 20px 0;
  border-radius: 18px;
  padding: 16px 18px;
  color: var(--muted);
}

.notice.error {
  border-color: rgba(251, 113, 133, 0.35);
  color: #fecdd3;
}

.notice.success {
  border-color: rgba(52, 211, 153, 0.35);
  color: #bbf7d0;
}

.checkout-grid {
  display: grid;
  grid-template-columns: 1.45fr 0.75fr;
  gap: 22px;
  margin-top: 24px;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.plan-card {
  text-align: start;
  color: var(--text);
  border-radius: 26px;
  padding: 24px;
  transition: 0.2s ease;
}

.plan-card:hover,
.plan-card.selected {
  border-color: rgba(69, 213, 255, 0.42);
  transform: translateY(-3px);
}

.plan-card.selected {
  background: linear-gradient(180deg, rgba(69, 213, 255, 0.13), rgba(15, 23, 42, 0.86));
}

.plan-code {
  color: var(--cyan);
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.plan-card strong {
  display: block;
  margin: 16px 0 4px;
  font-size: 38px;
}

.plan-card small,
.safe-note {
  color: var(--muted);
}

.plan-card p {
  color: var(--muted);
  line-height: 1.8;
}

.plan-card ul {
  padding-inline-start: 20px;
  color: var(--text);
  line-height: 1.9;
}

.checkout-form,
.admin-key-card,
.result-card {
  border-radius: 26px;
  padding: 24px;
}

.checkout-form {
  position: sticky;
  top: 20px;
  align-self: start;
}

label {
  display: grid;
  gap: 8px;
  color: var(--muted);
  margin-bottom: 14px;
}

input,
select,
textarea {
  width: 100%;
  border: 1px solid var(--border);
  background: rgba(2, 6, 23, 0.72);
  color: var(--text);
  border-radius: 14px;
  padding: 12px 13px;
  outline: none;
}

textarea {
  min-height: 110px;
  resize: vertical;
}

.summary-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  border: 1px solid var(--border);
  background: rgba(2, 6, 23, 0.42);
  border-radius: 18px;
  padding: 16px;
  margin: 16px 0;
}

.summary-box span {
  color: var(--muted);
}

.summary-box strong {
  color: var(--gold);
}

.primary-btn {
  width: 100%;
  border: 0;
  border-radius: 16px;
  padding: 14px 18px;
  background: linear-gradient(135deg, var(--gold), var(--cyan));
  color: #020617;
  font-weight: 900;
}

.primary-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.result-card {
  margin-top: 24px;
}

.admin-key-card {
  margin-top: 24px;
  display: grid;
  grid-template-columns: 1fr 240px;
  gap: 14px;
  align-items: end;
}

.admin-plans-list {
  display: grid;
  gap: 22px;
  margin-top: 24px;
}

.admin-plan-card {
  border-radius: 28px;
  padding: 24px;
}

.admin-plan-card header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 18px;
}

.status-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.admin-form-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.json-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.check-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 29px;
}

.check-row input {
  width: auto;
}

@media (max-width: 980px) {
  .checkout-grid,
  .plans-grid,
  .admin-key-card,
  .admin-form-grid,
  .json-grid {
    grid-template-columns: 1fr;
  }

  .checkout-form {
    position: static;
  }

  .hero-card {
    align-items: flex-start;
    flex-direction: column;
  }
}
FRONTEND_CSS_EOF_NDSP

cat > "$ROOT/README_RUN.md" <<'README_EOF_NDSP'
# NDSP Checkout + Admin Plans Package

## Run Migration

```sh
cd /home/nawaf511/empire-core-new/ndsp_checkout_plans_package
DATABASE_URL='postgresql://user:password@127.0.0.1:5432/ndsp' bash scripts/run_migration.sh
