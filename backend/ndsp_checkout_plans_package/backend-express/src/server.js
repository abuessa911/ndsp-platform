import "dotenv/config";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { query } from "./db.js";

const app = express();

const PORT = Number(process.env.PORT || 8088);
const CORS_ORIGIN = process.env.CORS_ORIGIN || "*";
const ADMIN_KEY = process.env.NDSP_ADMIN_KEY || process.env.ADMIN_API_KEY || "";

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

function clientIp(req) {
  const forwarded = req.headers["x-forwarded-for"];
  if (typeof forwarded === "string" && forwarded.length > 0) {
    return forwarded.split(",")[0].trim();
  }
  return req.socket.remoteAddress || null;
}

app.get("/health", (req, res) => {
  res.json({
    ok: true,
    service: "ndsp-checkout-plans-express",
    version: "1.0.0"
  });
});

/**
 * Endpoint 1:
 * Public plans for checkout page.
 */
app.get("/api/v1/plans", async (req, res) => {
  try {
    const result = await query(
      `
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
      `
    );

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

/**
 * Endpoint 2:
 * Create checkout request.
 * No automatic activation.
 * Output remains manual-review / sanitized.
 */
app.post("/api/v1/checkout", async (req, res) => {
  const planCode = String(req.body?.plan_code || "").trim().toLowerCase();
  const email = normalizeEmail(req.body?.email);
  const telegramId = String(req.body?.telegram_id || "").trim() || null;
  const network = String(req.body?.network || "TRC20").trim().toUpperCase();

  if (!isValidPlanCode(planCode)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_plan_code"
    });
  }

  if (!isValidEmail(email)) {
    return res.status(400).json({
      ok: false,
      error: "invalid_email"
    });
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
        "Your checkout request has been received and is pending manual review.",
        clientIp(req),
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

/**
 * Endpoint 3:
 * Admin plans list.
 */
app.get("/api/v1/admin/plans", requireAdmin, async (req, res) => {
  try {
    const result = await query(
      `
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
      `
    );

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

/**
 * Endpoint 4:
 * Admin update plan.
 */
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

  const client = await query("SELECT 1").then(() => null).catch(() => null);

  try {
    const beforeResult = await query(
      "SELECT * FROM ndsp_plans WHERE code = $1 LIMIT 1",
      [code]
    );

    if (beforeResult.rowCount === 0) {
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

    const updateResult = await query(updateSql, values);
    const updated = updateResult.rows[0];

    await query(
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

    return res.json({
      ok: true,
      plan: updated
    });
  } catch (error) {
    console.error("ADMIN_UPDATE_PLAN_ERROR", error);
    return res.status(500).json({
      ok: false,
      error: "failed_to_update_plan"
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
