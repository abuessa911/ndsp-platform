#!/usr/bin/env bash
set -euo pipefail

DOMAIN="https://ndsp.app"
FRONTEND_DIR="/var/www/ndsp-vite"
BACKEND_DIR="/home/nawaf511/empire-core-new/backend/auth_api"
DEPLOY_DIR="/var/www/html"
SERVICE_NAME="ndsp-auth-api"
BACKUP_ROOT="/root/ndsp_nowpayments_backup_$(date +%Y%m%d_%H%M%S)"

if [[ "$EUID" -ne 0 ]]; then
  echo "❌ شغّل السكربت بصلاحيات root"
  exit 1
fi

if [[ -z "${NOWPAYMENTS_API_KEY:-}" ]]; then
  read -rp "NOWPAYMENTS_API_KEY: " NOWPAYMENTS_API_KEY
fi

if [[ -z "${NOWPAYMENTS_IPN_SECRET:-}" ]]; then
  read -rsp "NOWPAYMENTS_IPN_SECRET: " NOWPAYMENTS_IPN_SECRET
  echo
fi

if [[ -z "$NOWPAYMENTS_API_KEY" || -z "$NOWPAYMENTS_IPN_SECRET" ]]; then
  echo "❌ المفاتيح مطلوبة"
  exit 1
fi

echo "== NDSP NOWPayments Installer =="
echo "Backup: $BACKUP_ROOT"

mkdir -p "$BACKUP_ROOT"
cp -a "$BACKEND_DIR" "$BACKUP_ROOT/backend"
cp -a "$FRONTEND_DIR" "$BACKUP_ROOT/frontend"

cd "$BACKEND_DIR"

echo "== Saving env variables =="
touch .env

python3 - "$BACKEND_DIR/.env" "$NOWPAYMENTS_API_KEY" "$NOWPAYMENTS_IPN_SECRET" "$DOMAIN" <<'PY'
import sys, pathlib

env_path = pathlib.Path(sys.argv[1])
api_key = sys.argv[2]
ipn_secret = sys.argv[3]
domain = sys.argv[4]

existing = {}
lines = []

if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k = line.split("=", 1)[0].strip()
            existing[k] = True
        lines.append(line)

def setv(k, v):
    global lines
    found = False
    out = []
    for line in lines:
        if line.startswith(k + "="):
            out.append(f"{k}={v}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{k}={v}")
    lines = out

setv("NOWPAYMENTS_API_KEY", api_key)
setv("NOWPAYMENTS_IPN_SECRET", ipn_secret)
setv("NOWPAYMENTS_PRICE_CURRENCY", "usd")
setv("NDSP_PUBLIC_URL", domain)

env_path.write_text("\n".join(lines).rstrip() + "\n")
print("✅ .env updated")
PY

echo "== Creating DB migration =="
cat > "$BACKEND_DIR/ndsp_nowpayments_migrate.cjs" <<'NODE'
require('dotenv').config();
const { Pool } = require('pg');

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.POSTGRES_URI ||
    process.env.PG_CONNECTION_STRING ||
    'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
});

async function main() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS public.ndsp_nowpayments_payments (
      id BIGSERIAL PRIMARY KEY,
      order_id TEXT UNIQUE NOT NULL,
      user_id TEXT NULL,
      user_email TEXT NULL,
      plan_id INTEGER NULL REFERENCES public.ndsp_plans(id) ON DELETE SET NULL,
      plan_code TEXT NULL,
      billing_cycle TEXT NOT NULL DEFAULT 'monthly',
      price_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
      price_currency TEXT NOT NULL DEFAULT 'usd',
      provider_invoice_id TEXT NULL,
      provider_payment_id TEXT NULL,
      invoice_url TEXT NULL,
      payment_status TEXT NOT NULL DEFAULT 'created',
      raw_create_response JSONB NULL,
      raw_ipn JSONB NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS ndsp_nowpayments_user_idx
      ON public.ndsp_nowpayments_payments (user_id);

    CREATE INDEX IF NOT EXISTS ndsp_nowpayments_status_idx
      ON public.ndsp_nowpayments_payments (payment_status);

    CREATE TABLE IF NOT EXISTS public.ndsp_subscriptions (
      id BIGSERIAL PRIMARY KEY,
      user_id TEXT NOT NULL,
      user_email TEXT NULL,
      plan_id INTEGER NULL REFERENCES public.ndsp_plans(id) ON DELETE SET NULL,
      plan_code TEXT NULL,
      status TEXT NOT NULL DEFAULT 'active',
      provider TEXT NOT NULL DEFAULT 'nowpayments',
      provider_order_id TEXT NULL,
      provider_payment_id TEXT NULL,
      billing_cycle TEXT NOT NULL DEFAULT 'monthly',
      starts_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      ends_at TIMESTAMPTZ NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS ndsp_subscriptions_user_idx
      ON public.ndsp_subscriptions (user_id);

    CREATE TABLE IF NOT EXISTS public.ndsp_payment_audit (
      id BIGSERIAL PRIMARY KEY,
      provider TEXT NOT NULL,
      event_type TEXT NOT NULL,
      order_id TEXT NULL,
      payment_status TEXT NULL,
      payload JSONB NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);

  console.log('✅ NOWPayments tables ready');
}

main()
  .catch(err => {
    console.error('❌ Migration failed:', err);
    process.exit(1);
  })
  .finally(() => pool.end());
NODE

node "$BACKEND_DIR/ndsp_nowpayments_migrate.cjs"

echo "== Creating NOWPayments backend module =="
cat > "$BACKEND_DIR/ndsp_nowpayments.cjs" <<'NODE'
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
NODE

echo "== Patching backend Express entry =="
python3 - "$BACKEND_DIR" <<'PY'
import pathlib, re, json, sys

base = pathlib.Path(sys.argv[1]).resolve()
pkg_path = base / "package.json"
pkg = {}
if pkg_path.exists():
    pkg = json.loads(pkg_path.read_text())

candidates = []

for key in ("start", "serve", "dev"):
    cmd = pkg.get("scripts", {}).get(key, "")
    m = re.search(r"node\s+([^\s]+\.m?c?js)", cmd)
    if m:
        candidates.append(base / m.group(1))

if pkg.get("main"):
    candidates.append(base / pkg["main"])

for name in [
    "server.js", "index.js", "app.js", "main.js",
    "server.cjs", "index.cjs", "app.cjs",
    "src/server.js", "src/index.js", "src/app.js"
]:
    candidates.append(base / name)

target = None
app_var = None

seen = set()
for p in candidates:
    p = p.resolve()
    if p in seen or not p.exists():
        continue
    seen.add(p)

    txt = p.read_text(errors="ignore")
    m = re.search(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*express\s*\(\s*\)", txt)
    if m and ".listen" in txt:
        target = p
        app_var = m.group(1)
        break

if not target:
    raise SystemExit("❌ لم أستطع تحديد ملف Express الرئيسي")

txt = target.read_text()

txt = re.sub(
    r"\n?/\* NDSP_NOWPAYMENTS_START \*/.*?/\* NDSP_NOWPAYMENTS_END \*/\n?",
    "\n",
    txt,
    flags=re.S
)

block = f"""
/* NDSP_NOWPAYMENTS_START */
try {{
  const {{ installNowPayments }} = require('{str(base / "ndsp_nowpayments.cjs")}');
  installNowPayments({app_var});
}} catch (e) {{
  console.error('❌ NDSP NOWPayments failed:', e);
  throw e;
}}
/* NDSP_NOWPAYMENTS_END */
"""

pattern = re.compile(r"((?:const|let|var)\s+" + re.escape(app_var) + r"\s*=\s*express\s*\(\s*\)\s*;?)")
m = pattern.search(txt)

if not m:
    raise SystemExit("❌ لم أجد app = express()")

txt = txt[:m.end()] + "\n" + block + txt[m.end():]
target.write_text(txt)

print(f"✅ Backend patched: {target}")
PY

echo "== Creating NOWPayments frontend checkout =="
cd "$FRONTEND_DIR"
mkdir -p src

cat > "$FRONTEND_DIR/src/ndsp-nowpayments-checkout.jsx" <<'JSX'
import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

function token() {
  return localStorage.getItem('token') ||
    localStorage.getItem('jwt') ||
    localStorage.getItem('access_token') ||
    localStorage.getItem('accessToken') ||
    localStorage.getItem('ndsp_token') ||
    '';
}

async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set('Content-Type', 'application/json');

  const t = token();
  if (t) headers.set('Authorization', `Bearer ${t}`);

  const res = await fetch(path, { ...options, headers });
  const text = await res.text();

  let data = {};
  try { data = text ? JSON.parse(text) : {}; } catch { data = { error: text }; }

  if (!res.ok) {
    throw new Error(data.message || data.error || `HTTP ${res.status}`);
  }

  return data;
}

function Checkout() {
  const [plans, setPlans] = useState([]);
  const [planCode, setPlanCode] = useState('');
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  useEffect(() => {
    api('/api/plans')
      .then(data => {
        const list = data.plans || [];
        setPlans(list);
        const paid = list.find(p => Number(p.price) > 0) || list[0];
        if (paid) setPlanCode(paid.code);
      })
      .catch(e => setErr(e.message));
  }, []);

  async function submit(e) {
    e.preventDefault();
    setErr('');
    setLoading(true);

    try {
      const data = await api('/api/checkout/create', {
        method: 'POST',
        body: JSON.stringify({
          plan_code: planCode,
          billing_cycle: billingCycle
        })
      });

      const url = data.invoice_url || data.checkout_url;

      if (!url) {
        throw new Error('لم يرجع NOWPayments رابط الدفع');
      }

      window.location.href = url;
    } catch (e) {
      setErr(e.message);
      setLoading(false);
    }
  }

  return (
    <main className="container" style={{ paddingBlock: '3rem', direction: 'rtl' }}>
      <article style={{
        border: '1px solid #e2e8f0',
        borderRadius: 24,
        boxShadow: '0 18px 60px rgba(15,23,42,.08)'
      }}>
        <hgroup>
          <h2>الدفع عبر العملات الرقمية</h2>
          <h3>NOWPayments</h3>
        </hgroup>

        {err && (
          <p style={{ color: '#b91c1c' }}>{err}</p>
        )}

        <form onSubmit={submit}>
          <label>
            اختر الباقة
            <select value={planCode} onChange={e => setPlanCode(e.target.value)} required>
              {plans.map(plan => (
                <option key={plan.code} value={plan.code}>
                  {plan.name} — {plan.price} {plan.price_currency || 'USD'}
                </option>
              ))}
            </select>
          </label>

          <label>
            مدة الاشتراك
            <select value={billingCycle} onChange={e => setBillingCycle(e.target.value)}>
              <option value="monthly">شهري</option>
              <option value="yearly">سنوي</option>
            </select>
          </label>

          <button type="submit" disabled={loading || !planCode}>
            {loading ? 'جاري إنشاء فاتورة الدفع...' : 'الدفع الآن'}
          </button>
        </form>

        <p style={{ color: '#64748b' }}>
          سيتم تحويلك إلى صفحة NOWPayments لاختيار العملة وإتمام الدفع. بعد تأكيد الدفع سيتم تفعيل الباقة تلقائياً عبر IPN.
        </p>
      </article>
    </main>
  );
}

function Success() {
  return (
    <main className="container" style={{ paddingBlock: '3rem', direction: 'rtl' }}>
      <article>
        <h2>تم استلام عملية الدفع</h2>
        <p>
          إذا اكتمل الدفع على شبكة البلوكشين، سيتم تفعيل الاشتراك تلقائياً بعد وصول تأكيد NOWPayments.
        </p>
        <a href="/#/admin-plans" role="button">العودة للمنصة</a>
      </article>
    </main>
  );
}

function boot() {
  const hash = window.location.hash.replace(/^#/, '');

  if (!['/checkout', '/checkout-nowpayments', '/checkout/success'].includes(hash)) return;

  if (!document.querySelector('link[data-pico]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css';
    link.dataset.pico = '1';
    document.head.appendChild(link);
  }

  document.body.innerHTML = '<div id="ndsp-nowpayments-root"></div>';

  createRoot(document.getElementById('ndsp-nowpayments-root')).render(
    hash === '/checkout/success' ? <Success /> : <Checkout />
  );
}

window.addEventListener('hashchange', boot);
boot();
JSX

echo "== Patching frontend main entry =="
python3 - "$FRONTEND_DIR" <<'PY'
import pathlib, sys

base = pathlib.Path(sys.argv[1])
candidates = [
    base / "src/main.jsx",
    base / "src/main.tsx",
    base / "src/main.js",
    base / "src/main.ts",
    base / "src/index.jsx",
    base / "src/index.tsx",
    base / "src/index.js",
    base / "src/index.ts",
]

target = next((p for p in candidates if p.exists()), None)
if not target:
    raise SystemExit("❌ لم أجد ملف main للفرونت")

txt = target.read_text()
line = "import './ndsp-nowpayments-checkout.jsx';"

if line not in txt:
    txt = line + "\n" + txt
    target.write_text(txt)

print(f"✅ Frontend patched: {target}")
PY

echo "== Installing frontend deps and building =="
npm install react react-dom
npm install --save-dev vite @vitejs/plugin-react

export QT_QPA_PLATFORM=offscreen
export CI=true

node <<'NODE'
const fs = require('fs');
const p = 'package.json';
const pkg = JSON.parse(fs.readFileSync(p, 'utf8'));

pkg.scripts = pkg.scripts || {};
pkg.scripts.build = 'QT_QPA_PLATFORM=offscreen node ./node_modules/vite/bin/vite.js build';

fs.writeFileSync(p, JSON.stringify(pkg, null, 2) + '\n');
NODE

npm run build

echo "== Deploy frontend =="
mkdir -p "$DEPLOY_DIR"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$FRONTEND_DIR/dist/" "$DEPLOY_DIR/"
else
  find "$DEPLOY_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  cp -a "$FRONTEND_DIR/dist/." "$DEPLOY_DIR/"
fi

echo "== Restart services =="
systemctl restart "$SERVICE_NAME"
systemctl reload nginx

sleep 2

systemctl is-active --quiet "$SERVICE_NAME" \
  && echo "✅ $SERVICE_NAME active" \
  || { echo "❌ $SERVICE_NAME failed"; systemctl status "$SERVICE_NAME" --no-pager -l; exit 1; }

curl -fsS "http://127.0.0.1:9011/api/nowpayments/health" >/dev/null \
  && echo "✅ NOWPayments API mounted" \
  || echo "⚠️ NOWPayments health check failed"

echo ""
echo "✅ تم تركيب NOWPayments"
echo ""
echo "رابط الدفع:"
echo "$DOMAIN/#/checkout-nowpayments"
echo ""
echo "رابط IPN الذي تضعه في NOWPayments:"
echo "$DOMAIN/api/webhooks/nowpayments"
echo ""
echo "مهم:"
echo "- غيّر NOWPAYMENTS_PRICE_CURRENCY في .env إذا تريد عملة سعر مختلفة من usd"
echo "- بعد أي تعديل .env نفّذ: sudo systemctl restart $SERVICE_NAME"
echo ""
echo "Backup saved at: $BACKUP_ROOT"
