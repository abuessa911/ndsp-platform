CREATE TABLE IF NOT EXISTS signal_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    symbol TEXT NOT NULL,
    direction TEXT NOT NULL,
    confidence NUMERIC(5, 2),
    price NUMERIC(20, 8),

    alert_status TEXT,
    alert_reason TEXT,

    lifecycle TEXT,
    trade_id TEXT,

    risk_state TEXT,
    risk_reason TEXT,

    raw_result JSONB,
    raw_alert JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_signal_decisions_symbol_created_at
ON signal_decisions (symbol, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_signal_decisions_direction
ON signal_decisions (direction);

CREATE INDEX IF NOT EXISTS idx_signal_decisions_alert_status
ON signal_decisions (alert_status);

CREATE INDEX IF NOT EXISTS idx_signal_decisions_confidence
ON signal_decisions (confidence);
