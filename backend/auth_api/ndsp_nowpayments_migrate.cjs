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
