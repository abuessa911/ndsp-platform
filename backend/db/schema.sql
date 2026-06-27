-- ==========================================================================
-- NDSP — PostgreSQL schema (reference DDL)
-- Governance: decision_outputs / scenario_levels store ONLY sanitized public
-- fields. Internal engine scores, weights and hidden-layer data are NOT stored
-- here and never leave the engine. audit_logs records every mutating action.
-- This DDL mirrors backend/app/models. You may use Alembic instead (see migrations/).
-- ==========================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ---------- users & auth ----------
CREATE TABLE IF NOT EXISTS users (
    id              VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    email           VARCHAR(255) UNIQUE NOT NULL,
    name            VARCHAR(120),
    locale          VARCHAR(2)  NOT NULL DEFAULT 'ar',
    role            VARCHAR(20) NOT NULL DEFAULT 'user',          -- user | admin
    password_hash   VARCHAR(255) NOT NULL,
    twofa_enabled   BOOLEAN     NOT NULL DEFAULT FALSE,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending_review',-- pending_review|active|suspended
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id     VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash  VARCHAR(255) NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    revoked     BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_refresh_user ON refresh_tokens(user_id);

-- ---------- packages & subscriptions ----------
CREATE TABLE IF NOT EXISTS packages (
    id       VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    code     VARCHAR(30) UNIQUE NOT NULL,        -- free|pro|elite|institutional
    name_ar  VARCHAR(80) NOT NULL,
    name_en  VARCHAR(80) NOT NULL,
    limits   JSONB       NOT NULL DEFAULT '{}',
    active   BOOLEAN     NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id            VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id       VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    package_code  VARCHAR(30) NOT NULL,
    state         VARCHAR(30) NOT NULL DEFAULT 'pending',  -- pending|pending_review|confirmed|rejected|expired|refunded|manual_review_required
    cycle         VARCHAR(10) NOT NULL DEFAULT 'monthly',
    ref           VARCHAR(60),
    started_at    TIMESTAMPTZ,
    renews_at     TIMESTAMPTZ,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_sub_user ON subscriptions(user_id);

-- ---------- trials (per-user 16-day clock) ----------
CREATE TABLE IF NOT EXISTS trials (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id     VARCHAR(36) UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    seat_type   VARCHAR(20) NOT NULL,                 -- ordinary|specialist|private
    started_at  TIMESTAMPTZ,                          -- set at activation
    ends_at     TIMESTAMPTZ,
    total_days  INTEGER     NOT NULL DEFAULT 16,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- payments ----------
CREATE TABLE IF NOT EXISTS payments (
    id              VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id         VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_id VARCHAR(36) REFERENCES subscriptions(id) ON DELETE SET NULL,
    method          VARCHAR(20) NOT NULL,             -- crypto|bank
    amount          NUMERIC(12,2),
    currency        VARCHAR(10) NOT NULL DEFAULT 'USD',
    state           VARCHAR(30) NOT NULL DEFAULT 'pending',
    provider_ref    VARCHAR(120),
    ref             VARCHAR(60),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_pay_user ON payments(user_id);

CREATE TABLE IF NOT EXISTS payment_reviews (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    payment_id  VARCHAR(36) NOT NULL REFERENCES payments(id) ON DELETE CASCADE,
    reviewer_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    decision    VARCHAR(20) NOT NULL,                 -- approve|reject
    note        TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- markets & assets ----------
CREATE TABLE IF NOT EXISTS markets (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    code        VARCHAR(20) UNIQUE NOT NULL,          -- fx|commodities|indices|crypto
    name_ar     VARCHAR(80) NOT NULL,
    name_en     VARCHAR(80) NOT NULL,
    state       VARCHAR(20) NOT NULL DEFAULT 'live',
    audit_class VARCHAR(40) NOT NULL DEFAULT 'VISIBLE_BY_PACKAGE'
);

CREATE TABLE IF NOT EXISTS assets (
    id           VARCHAR(40) PRIMARY KEY,             -- e.g. XAU
    symbol       VARCHAR(40) UNIQUE NOT NULL,         -- XAU/USD
    market_code  VARCHAR(20) NOT NULL REFERENCES markets(code),
    name_ar      VARCHAR(80) NOT NULL,
    name_en      VARCHAR(80) NOT NULL,
    active       BOOLEAN     NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS ix_assets_market ON assets(market_code);

CREATE TABLE IF NOT EXISTS user_assets (
    id         VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id    VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    asset_id   VARCHAR(40) NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_user_assets_user ON user_assets(user_id);

-- ---------- decisions (sanitized public outputs only) ----------
CREATE TABLE IF NOT EXISTS decision_requests (
    id           VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id      VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    asset_id     VARCHAR(40) NOT NULL REFERENCES assets(id),
    requested_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS decision_outputs (
    id                VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    asset_id          VARCHAR(40) NOT NULL REFERENCES assets(id),
    bias              VARCHAR(10),     -- up|down|flat
    horizon           VARCHAR(12),     -- short|extended
    horizon_strength  INTEGER,
    decision_quality  INTEGER,
    market_state      VARCHAR(20),
    liquidity         VARCHAR(20),
    risk              VARCHAR(20),
    volatility        VARCHAR(20),
    sentiment         VARCHAR(20),
    summary_ar        TEXT,
    summary_en        TEXT,
    public_payload    JSONB NOT NULL DEFAULT '{}',   -- full sanitized object
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_decision_asset ON decision_outputs(asset_id);

CREATE TABLE IF NOT EXISTS scenario_levels (
    id                            VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    decision_output_id            VARCHAR(36) NOT NULL REFERENCES decision_outputs(id) ON DELETE CASCADE,
    scenario_state                VARCHAR(30),
    scenario_directional_context  VARCHAR(30),
    scenario_activation_level     NUMERIC(18,6),
    scenario_arrival_level        NUMERIC(18,6),
    scenario_invalidation_level   NUMERIC(18,6),
    scenario_review_zone          VARCHAR(60),
    scenario_time_horizon         VARCHAR(30),
    scenario_confidence_band      VARCHAR(30),
    scenario_risk_note            TEXT,
    scenario_follow_up_note       TEXT,
    scenario_status_label         VARCHAR(40),
    governance_note               TEXT,
    scenario_last_updated         TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_scenario_decision ON scenario_levels(decision_output_id);

-- ---------- alerts & telegram ----------
CREATE TABLE IF NOT EXISTS alerts (
    id            VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id       VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    events        JSONB   NOT NULL DEFAULT '{}',
    dq_threshold  INTEGER NOT NULL DEFAULT 60,
    brief_time    VARCHAR(10),
    digest        VARCHAR(20),
    quiet_from    VARCHAR(10),
    quiet_to      VARCHAR(10),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_alerts_user ON alerts(user_id);

CREATE TABLE IF NOT EXISTS telegram_settings (
    id                    VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id               VARCHAR(36) UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    state                 VARCHAR(20) NOT NULL DEFAULT 'not_linked', -- not_linked|linked
    link_code             VARCHAR(40),
    link_code_expires_at  TIMESTAMPTZ,
    chat_id_hash          VARCHAR(255),   -- hashed only, never raw
    last_test_at          TIMESTAMPTZ
);

-- ---------- audit, settings, governance ----------
CREATE TABLE IF NOT EXISTS audit_logs (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    actor_id    VARCHAR(36),
    actor_role  VARCHAR(20),
    action      VARCHAR(80) NOT NULL,
    target      VARCHAR(120),
    meta        JSONB NOT NULL DEFAULT '{}',  -- masked only — no secrets
    ip_hash     VARCHAR(255),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_audit_actor ON audit_logs(actor_id);

CREATE TABLE IF NOT EXISTS system_settings (
    key        VARCHAR(60) PRIMARY KEY,
    value      TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS governance_status (
    key        VARCHAR(60) PRIMARY KEY,
    enabled    BOOLEAN NOT NULL DEFAULT TRUE,
    note       TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- backups / snapshots metadata ----------
CREATE TABLE IF NOT EXISTS backup_records (
    id         VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    kind       VARCHAR(20) NOT NULL,   -- backup|snapshot
    path       TEXT        NOT NULL,
    note       TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
