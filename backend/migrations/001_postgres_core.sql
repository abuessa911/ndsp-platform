CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id TEXT UNIQUE,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    status TEXT NOT NULL DEFAULT 'new',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
    telegram_id TEXT,
    plan_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    starts_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    invite_link TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE SET NULL,
    provider TEXT NOT NULL DEFAULT 'nowpayments',
    provider_payment_id TEXT UNIQUE,
    payment_status TEXT NOT NULL DEFAULT 'created',
    price_amount NUMERIC(20, 8),
    pay_amount NUMERIC(20, 8),
    pay_currency TEXT,
    order_id TEXT,
    payment_url TEXT,
    raw_payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS webhook_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider TEXT NOT NULL,
    event_id TEXT,
    idempotency_key TEXT UNIQUE,
    payload JSONB NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol TEXT NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('LONG', 'SHORT')),
    entry_price NUMERIC(20, 8) NOT NULL,
    exit_price NUMERIC(20, 8),
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'evaluated')),
    result TEXT
        CHECK (result IN ('win', 'loss', 'breakeven')),
    confidence NUMERIC(5, 2),
    source TEXT DEFAULT 'ndip',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    evaluated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_leads_telegram_id
ON leads (telegram_id);

CREATE INDEX IF NOT EXISTS idx_subscriptions_telegram_id
ON subscriptions (telegram_id);

CREATE INDEX IF NOT EXISTS idx_subscriptions_status
ON subscriptions (status);

CREATE INDEX IF NOT EXISTS idx_payments_provider_payment_id
ON payments (provider_payment_id);

CREATE INDEX IF NOT EXISTS idx_payments_status
ON payments (payment_status);

CREATE INDEX IF NOT EXISTS idx_webhook_events_idempotency_key
ON webhook_events (idempotency_key);

CREATE INDEX IF NOT EXISTS idx_signals_status_created_at
ON signals (status, created_at);

CREATE INDEX IF NOT EXISTS idx_signals_symbol_created_at
ON signals (symbol, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_signals_result
ON signals (result);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_leads_updated_at ON leads;
CREATE TRIGGER trg_leads_updated_at
BEFORE UPDATE ON leads
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_subscriptions_updated_at ON subscriptions;
CREATE TRIGGER trg_subscriptions_updated_at
BEFORE UPDATE ON subscriptions
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_payments_updated_at ON payments;
CREATE TRIGGER trg_payments_updated_at
BEFORE UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
