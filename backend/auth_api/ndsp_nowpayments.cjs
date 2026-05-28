const express = require('express');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.POSTGRES_URI ||
    process.env.PG_CONNECTION_STRING ||
    'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
});

const NOWPAYMENTS_API_KEY = process.env.NOWPAYMENTS_API_KEY;
const NOWPAYMENTS_IPN_SECRET = process.env.NOWPAYMENTS_IPN_SECRET;
const NOWPAYMENTS_PRICE_CURRENCY = (process.env.NOWPAYMENTS_PRICE_CURRENCY || 'usd').toLowerCase();
const PUBLIC_URL = (process.env.NDSP_PUBLIC_URL || 'https://ndsp.app').replace(/\/$/, '');

const jwtSecrets = [
  process.env.JWT_SECRET,
  process.env.AUTH_JWT_SECRET,
  process.env.ACCESS_TOKEN_SECRET,
  process.env.SECRET_KEY,
  process.env.TOKEN_SECRET,
  'ndsp-secret'
].filter(Boolean);

function bearerToken(req) {
  const h = req.headers.authorization || '';
  if (h.toLowerCase().startsWith('bearer ')) return h.slice(7).trim();
  return null;
}

function verifyAnyJwt(token) {
  for (const secret of jwtSecrets) {
    try {
      return jwt.verify(token, secret);
    } catch (_) {}
  }
  return jwt.decode(token);
}

async function getAuthUser(req) {
  const token = bearerToken(req);
  if (!token) return null;

  const payload = verifyAnyJwt(token);
  if (!payload) return null;

  const id = payload.id || payload.userId || payload.user_id || payload.sub;
  const email = payload.email || payload.mail || payload.username;

  if (id) {
    const r = await pool.query(`SELECT * FROM public.users WHERE id::text=$1 LIMIT 1`, [String(id)]);
    if (r.rows[0]) return r.rows[0];
  }

  if (email) {
    const r = await pool.query(`SELECT * FROM public.users WHERE lower(email)=lower($1) LIMIT 1`, [String(email)]);
    if (r.rows[0]) return r.rows[0];
  }

  return null;
}

function sortObject(obj) {
  if (Array.isArray(obj)) return obj.map(sortObject);
  if (obj && typeof obj === 'object') {
    return Object.keys(obj).sort().reduce((acc, key) => {
      acc[key] = sortObject(obj[key]);
      return acc;
    }, {});
  }
  return obj;
}

function verifyIpnSignature(req, body) {
  const sig = req.headers['x-nowpayments-sig'];
  if (!sig || !NOWPAYMENTS_IPN_SECRET) return false;

  const sorted = sortObject(body);
  const payload = JSON.stringify(sorted);

  const hmac = crypto
    .createHmac('sha512', NOWPAYMENTS_IPN_SECRET)
    .update(payload)
    .digest('hex');

  try {
    return crypto.timingSafeEqual(Buffer.from(String(sig)), Buffer.from(hmac));
  } catch {
    return false;
  }
}

async function getUserPlanColumn() {
  const r = await pool.query(`
    SELECT column_name, udt_name
    FROM information_schema.columns
    WHERE table_schema='public' AND table_name='users'
  `);

  const cols = new Map(r.rows.map(x => [x.column_name, x.udt_name]));

  if (cols.has('ndsp_plan_id')) return 'ndsp_plan_id';
  if (cols.has('plan_id') && ['int4', 'int8'].includes(cols.get('plan_id'))) return 'plan_id';

  return null;
}

async function activateSubscription(payment) {
  if (!payment || !payment.user_id || !payment.plan_id) return;

  await pool.query(`
    INSERT INTO public.ndsp_subscriptions
      (user_id, user_email, plan_id, plan_code, status, provider, provider_order_id, provider_payment_id, billing_cycle)
    VALUES
      ($1,$2,$3,$4,'active','nowpayments',$5,$6,$7)
  `, [
    payment.user_id,
    payment.user_email,
    payment.plan_id,
    payment.plan_code,
    payment.order_id,
    payment.provider_payment_id,
    payment.billing_cycle || 'monthly'
  ]);

  const planCol = await getUserPlanColumn();

  if (planCol) {
    await pool.query(`
      UPDATE public.users
      SET ${planCol}=$1, status='active'
      WHERE id::text=$2
    `, [payment.plan_id, String(payment.user_id)]);
  }
}


async function ndspPaymentEnabled() {
  try {
    const r = await pool.query(
      `SELECT value FROM public.ndsp_settings WHERE key='payment_enabled' LIMIT 1`
    );

    if (!r.rows[0]) return false;

    const value = r.rows[0].value;
    return value === true || value === 'true';
  } catch (_) {
    return false;
  }
}

function installNowPayments(app) {
  const router = express.Router();

  router.use(express.json({ limit: '2mb' }));

  router.get('/nowpayments/health', (_req, res) => {
    res.json({
      ok: true,
      provider: 'nowpayments',
      currency: NOWPAYMENTS_PRICE_CURRENCY
    });
  });

  router.post('/checkout/create', async (req, res) => {
    try {
      if (!(await ndspPaymentEnabled())) {
        return res.status(403).json({
          error: 'PAYMENT_DISABLED',
          message: 'الدفع غير متاح حالياً. المنصة تعمل حالياً بنظام تجربة مجانية لمدة 16 يوم.'
        });
      }


      if (!NOWPAYMENTS_API_KEY) {
        return res.status(500).json({ error: 'NOWPAYMENTS_API_KEY_MISSING' });
      }

      const user = await getAuthUser(req);
      if (!user) {
        return res.status(401).json({
          error: 'LOGIN_REQUIRED',
          message: 'يجب تسجيل الدخول قبل الدفع'
        });
      }

      const planCode = String(req.body.plan_code || req.body.planCode || 'pro').trim().toLowerCase();
      const billingCycle = String(req.body.billing_cycle || req.body.billingCycle || 'monthly').trim().toLowerCase();

      const planRes = await pool.query(`
        SELECT *
        FROM public.ndsp_plans
        WHERE lower(code)=lower($1)
          AND is_active=true
        LIMIT 1
      `, [planCode]);

      const plan = planRes.rows[0];

      if (!plan) {
        return res.status(404).json({
          error: 'PLAN_NOT_FOUND',
          message: 'الباقة غير موجودة أو غير مفعلة'
        });
      }

      let amount = Number(plan.price || 0);

      if (billingCycle === 'yearly' || billingCycle === 'annual') {
        amount = amount * 12;
      }

      if (!Number.isFinite(amount) || amount <= 0) {
        return res.status(400).json({
          error: 'INVALID_PLAN_PRICE',
          message: 'سعر الباقة غير صالح للدفع'
        });
      }

      const orderId = `ndsp_${crypto.randomUUID()}`;

      await pool.query(`
        INSERT INTO public.ndsp_nowpayments_payments
          (order_id, user_id, user_email, plan_id, plan_code, billing_cycle, price_amount, price_currency, payment_status)
        VALUES
          ($1,$2,$3,$4,$5,$6,$7,$8,'created')
      `, [
        orderId,
        String(user.id),
        user.email || null,
        plan.id,
        plan.code,
        billingCycle,
        amount,
        NOWPAYMENTS_PRICE_CURRENCY
      ]);

      const body = {
        price_amount: amount,
        price_currency: NOWPAYMENTS_PRICE_CURRENCY,
        order_id: orderId,
        order_description: `NDSP ${plan.name} - ${billingCycle}`,
        ipn_callback_url: `${PUBLIC_URL}/api/webhooks/nowpayments`,
        success_url: `${PUBLIC_URL}/#/checkout/success`,
        cancel_url: `${PUBLIC_URL}/#/checkout`
      };

      const npRes = await fetch('https://api.nowpayments.io/v1/invoice', {
        method: 'POST',
        headers: {
          'x-api-key': NOWPAYMENTS_API_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });

      const npText = await npRes.text();
      let npData = {};

      try {
        npData = npText ? JSON.parse(npText) : {};
      } catch {
        npData = { raw: npText };
      }

      if (!npRes.ok) {
        await pool.query(`
          UPDATE public.ndsp_nowpayments_payments
          SET payment_status='create_failed',
              raw_create_response=$2,
              updated_at=now()
          WHERE order_id=$1
        `, [orderId, JSON.stringify(npData)]);

        return res.status(502).json({
          error: 'NOWPAYMENTS_CREATE_FAILED',
          details: npData
        });
      }

      await pool.query(`
        UPDATE public.ndsp_nowpayments_payments
        SET provider_invoice_id=$2,
            invoice_url=$3,
            raw_create_response=$4,
            payment_status='invoice_created',
            updated_at=now()
        WHERE order_id=$1
      `, [
        orderId,
        String(npData.id || npData.invoice_id || ''),
        npData.invoice_url || npData.url || null,
        JSON.stringify(npData)
      ]);

      await pool.query(`
        INSERT INTO public.ndsp_payment_audit
          (provider, event_type, order_id, payment_status, payload)
        VALUES
          ('nowpayments','invoice_created',$1,'invoice_created',$2)
      `, [orderId, JSON.stringify(npData)]);

      res.json({
        ok: true,
        provider: 'nowpayments',
        order_id: orderId,
        invoice_url: npData.invoice_url || npData.url,
        checkout_url: npData.invoice_url || npData.url,
        raw: npData
      });
    } catch (err) {
      console.error('NOWPayments checkout error:', err);
      res.status(500).json({
        error: 'CHECKOUT_ERROR',
        message: err.message
      });
    }
  });

  
  // NDSP_NOWPAYMENTS_WEBHOOK_GET_CHECK
  router.get('/webhooks/nowpayments', (_req, res) => {
    res.json({
      ok: true,
      provider: 'nowpayments',
      endpoint: '/api/webhooks/nowpayments',
      method_required: 'POST',
      message: 'NOWPayments IPN endpoint is active. Browser GET is only a health check.'
    });
  });

  router.post('/webhooks/nowpayments', async (req, res) => {
    try {
      const body = req.body || {};

      if (!verifyIpnSignature(req, body)) {
        return res.status(401).json({ error: 'INVALID_IPN_SIGNATURE' });
      }

      const orderId = body.order_id || body.orderId || null;
      const paymentStatus = body.payment_status || body.status || 'unknown';
      const providerPaymentId = body.payment_id || body.id || body.invoice_id || null;

      await pool.query(`
        INSERT INTO public.ndsp_payment_audit
          (provider, event_type, order_id, payment_status, payload)
        VALUES
          ('nowpayments','ipn',$1,$2,$3)
      `, [orderId, paymentStatus, JSON.stringify(body)]);

      if (!orderId) {
        return res.json({ ok: true, ignored: 'missing_order_id' });
      }

      const updated = await pool.query(`
        UPDATE public.ndsp_nowpayments_payments
        SET payment_status=$2,
            provider_payment_id=COALESCE($3, provider_payment_id),
            raw_ipn=$4,
            updated_at=now()
        WHERE order_id=$1
        RETURNING *
      `, [
        orderId,
        paymentStatus,
        providerPaymentId ? String(providerPaymentId) : null,
        JSON.stringify(body)
      ]);

      const payment = updated.rows[0];

      if (payment && ['confirmed', 'finished'].includes(String(paymentStatus).toLowerCase())) {
        const existing = await pool.query(`
          SELECT id
          FROM public.ndsp_subscriptions
          WHERE provider_order_id=$1
          LIMIT 1
        `, [orderId]);

        if (!existing.rows[0]) {
          await activateSubscription(payment);
        }
      }

      res.json({ ok: true });
    } catch (err) {
      console.error('NOWPayments IPN error:', err);
      res.status(500).json({
        error: 'IPN_ERROR',
        message: err.message
      });
    }
  });

  app.use('/api', router);

  console.log('✅ NDSP NOWPayments mounted: /api/checkout/create and /api/webhooks/nowpayments');
}

module.exports = { installNowPayments };
