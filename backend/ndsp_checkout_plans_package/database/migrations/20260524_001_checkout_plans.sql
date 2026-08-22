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
    checkout_ref TEXT NOT NULL UNIQUE DEFAULT ('NDSP-' || upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 12))),
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
    '[
        "Market context overview",
        "Decision-support dashboard",
        "Public sanitized output",
        "Core assets coverage"
    ]'::jsonb,
    '{
        "max_assets": 25,
        "decision_depth": "standard",
        "admin_review_required": true
    }'::jsonb,
    '{
        "public_label": "Pro",
        "payment_currency": "USDT",
        "supported_networks": ["TRC20", "BEP20"]
    }'::jsonb
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
    '[
        "Advanced market interpretation",
        "Expanded asset coverage",
        "Elite decision surface",
        "Scenario explanation",
        "Sanitized multi-layer output"
    ]'::jsonb,
    '{
        "max_assets": 100,
        "decision_depth": "advanced",
        "trial_days": 16,
        "admin_review_required": true
    }'::jsonb,
    '{
        "public_label": "Elite",
        "payment_currency": "USDT",
        "supported_networks": ["TRC20", "BEP20"],
        "manual_activation": true
    }'::jsonb
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
    '[
        "Institutional workspace",
        "Team-oriented access",
        "Extended reporting",
        "Priority review",
        "Governance-safe output"
    ]'::jsonb,
    '{
        "max_assets": 500,
        "decision_depth": "institutional",
        "team_access": true,
        "admin_review_required": true
    }'::jsonb,
    '{
        "public_label": "SaaS",
        "payment_currency": "USDT",
        "supported_networks": ["TRC20", "BEP20"],
        "manual_activation": true
    }'::jsonb
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
