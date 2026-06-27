'use strict';

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { Pool } = require('pg');
const crypto = require('crypto');

const PORT = Number(process.env.NDSP_COMPLETED_DECISION_PORT || 9078);
const HOST = process.env.NDSP_COMPLETED_DECISION_HOST || '127.0.0.1';

const DATABASE_URL =
  process.env.DATABASE_URL ||
  process.env.POSTGRES_URL ||
  process.env.NDSP_DATABASE_URL ||
  '';

const pool = DATABASE_URL
  ? new Pool({ connectionString: DATABASE_URL, ssl: process.env.PGSSL === '1' ? { rejectUnauthorized: false } : false })
  : new Pool({
      host: process.env.PGHOST || '127.0.0.1',
      port: Number(process.env.PGPORT || 5432),
      database: process.env.PGDATABASE || process.env.DB_NAME || 'ndsp',
      user: process.env.PGUSER || process.env.DB_USER || 'ndsp',
      password: process.env.PGPASSWORD || process.env.DB_PASSWORD || ''
    });

const app = express();
app.use(helmet({ contentSecurityPolicy: false }));
app.use(cors({ origin: true, credentials: true }));
app.use(express.json({ limit: '2mb' }));

function nowIso(){ return new Date().toISOString(); }

function makeDecisionId(symbol){
  const seed = `${symbol || 'NDSP'}:${Date.now()}:${Math.random()}`;
  return 'CD-' + crypto.createHash('sha256').update(seed).digest('hex').slice(0, 16).toUpperCase();
}

function sanitizeSymbol(symbol){
  return String(symbol || '').trim().toUpperCase().replace(/[^A-Z0-9._:-]/g, '').slice(0, 32);
}

function sanitizeState(s){
  const v = String(s || 'Draft').trim();
  const allowed = new Set(['Draft','Monitoring','Candidate','Governance Validation','Completed','Published','Expired','Archived']);
  return allowed.has(v) ? v : 'Draft';
}

function publicDisclaimer(){
  return 'NDSP provides decision support only. This is not financial advice, not a buy/sell recommendation, and not an execution instruction.';
}

async function initDb(){
  await pool.query(`
    CREATE TABLE IF NOT EXISTS ndsp_completed_decisions (
      id BIGSERIAL PRIMARY KEY,
      decision_id TEXT UNIQUE NOT NULL,
      symbol TEXT NOT NULL,
      market TEXT NULL,
      decision_state TEXT NOT NULL DEFAULT 'Draft',
      decision_quality NUMERIC NULL,
      scenario_state TEXT NULL,
      direction_context TEXT NULL,
      activation_level TEXT NULL,
      arrival_level TEXT NULL,
      review_zone TEXT NULL,
      invalidation_level TEXT NULL,
      nmp_zone TEXT NULL,
      risk_status TEXT NULL,
      devil_advocate_status TEXT NULL,
      visibility TEXT NOT NULL DEFAULT 'private',
      payload JSONB NOT NULL DEFAULT '{}'::jsonb,
      disclaimer TEXT NOT NULL,
      completed_at TIMESTAMPTZ NULL,
      published_at TIMESTAMPTZ NULL,
      expires_at TIMESTAMPTZ NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);

  await pool.query(`CREATE INDEX IF NOT EXISTS ndsp_completed_decisions_symbol_idx ON ndsp_completed_decisions(symbol);`);
  await pool.query(`CREATE INDEX IF NOT EXISTS ndsp_completed_decisions_state_idx ON ndsp_completed_decisions(decision_state);`);
  await pool.query(`CREATE INDEX IF NOT EXISTS ndsp_completed_decisions_created_idx ON ndsp_completed_decisions(created_at DESC);`);

  await pool.query(`
    CREATE TABLE IF NOT EXISTS ndsp_decision_timeline (
      id BIGSERIAL PRIMARY KEY,
      decision_id TEXT NOT NULL,
      event_type TEXT NOT NULL,
      event_title TEXT NOT NULL,
      event_detail TEXT NULL,
      event_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);

  await pool.query(`CREATE INDEX IF NOT EXISTS ndsp_decision_timeline_decision_idx ON ndsp_decision_timeline(decision_id, created_at);`);
}

function rowToDecision(r){
  if (!r) return null;
  return {
    id: r.decision_id,
    symbol: r.symbol,
    market: r.market,
    decision_state: r.decision_state,
    decision_quality: r.decision_quality === null ? null : Number(r.decision_quality),
    scenario_state: r.scenario_state,
    direction_context: r.direction_context,
    levels: {
      activation: r.activation_level,
      arrival: r.arrival_level,
      review_zone: r.review_zone,
      invalidation: r.invalidation_level,
      nmp_zone: r.nmp_zone
    },
    risk_status: r.risk_status,
    devil_advocate_status: r.devil_advocate_status,
    visibility: r.visibility,
    completed_at: r.completed_at,
    published_at: r.published_at,
    expires_at: r.expires_at,
    created_at: r.created_at,
    updated_at: r.updated_at,
    disclaimer: r.disclaimer,
    payload: r.payload || {}
  };
}

async function addTimeline(decisionId, type, title, detail, payload){
  await pool.query(
    `INSERT INTO ndsp_decision_timeline(decision_id,event_type,event_title,event_detail,event_payload)
     VALUES($1,$2,$3,$4,$5::jsonb)`,
    [decisionId, type, title, detail || null, JSON.stringify(payload || {})]
  );
}

function validateForCompleted(body){
  const errors = [];
  if (!sanitizeSymbol(body.symbol)) errors.push('SYMBOL_REQUIRED');

  const quality = Number(body.decision_quality ?? body.quality ?? 0);
  if (!Number.isFinite(quality) || quality < 0 || quality > 100) errors.push('QUALITY_MUST_BE_0_TO_100');

  if (String(body.devil_advocate_status || '').toLowerCase().includes('blocked')) {
    errors.push('DEVIL_ADVOCATE_BLOCKED');
  }

  return { ok: errors.length === 0, errors, quality };
}

app.get('/health', async (_req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({
      ok: true,
      service: 'ndsp-completed-decision-service',
      port: PORT,
      time: nowIso(),
      database: true
    });
  } catch (e) {
    res.status(500).json({
      ok: false,
      service: 'ndsp-completed-decision-service',
      error: 'DB_HEALTH_FAILED',
      message: e.message
    });
  }
});

app.get('/api/completed', async (req, res) => {
  try {
    const symbol = sanitizeSymbol(req.query.symbol || '');
    const limit = Math.min(Math.max(Number(req.query.limit || 25), 1), 100);

    const params = [];
    let where = `WHERE decision_state IN ('Completed','Published')`;

    if (symbol) {
      params.push(symbol);
      where += ` AND symbol = $${params.length}`;
    }

    params.push(limit);

    const q = `
      SELECT *
      FROM ndsp_completed_decisions
      ${where}
      ORDER BY COALESCE(published_at, completed_at, created_at) DESC
      LIMIT $${params.length}
    `;

    const out = await pool.query(q, params);
    res.json({ ok:true, source:'completed_decision_service', decisions: out.rows.map(rowToDecision) });
  } catch (e) {
    res.status(500).json({ ok:false, error:'COMPLETED_LIST_FAILED', message:e.message });
  }
});

app.get('/api/completed/latest', async (_req, res) => {
  try {
    const out = await pool.query(`
      SELECT *
      FROM ndsp_completed_decisions
      WHERE decision_state IN ('Completed','Published')
      ORDER BY COALESCE(published_at, completed_at, created_at) DESC
      LIMIT 1
    `);
    res.json({ ok:true, source:'completed_decision_service', decision: rowToDecision(out.rows[0]) });
  } catch (e) {
    res.status(500).json({ ok:false, error:'COMPLETED_LATEST_FAILED', message:e.message });
  }
});

app.get('/api/completed/:symbol', async (req, res) => {
  try {
    const symbol = sanitizeSymbol(req.params.symbol);
    const out = await pool.query(`
      SELECT *
      FROM ndsp_completed_decisions
      WHERE symbol=$1 AND decision_state IN ('Completed','Published')
      ORDER BY COALESCE(published_at, completed_at, created_at) DESC
      LIMIT 1
    `, [symbol]);

    if (!out.rowCount) return res.status(404).json({ ok:false, error:'NO_COMPLETED_DECISION', symbol });
    res.json({ ok:true, source:'completed_decision_service', decision: rowToDecision(out.rows[0]) });
  } catch (e) {
    res.status(500).json({ ok:false, error:'COMPLETED_BY_SYMBOL_FAILED', message:e.message });
  }
});

app.get('/api/completed/id/:decision_id', async (req, res) => {
  try {
    const decisionId = String(req.params.decision_id || '').trim();
    const out = await pool.query(`SELECT * FROM ndsp_completed_decisions WHERE decision_id=$1 LIMIT 1`, [decisionId]);
    if (!out.rowCount) return res.status(404).json({ ok:false, error:'DECISION_NOT_FOUND' });
    res.json({ ok:true, source:'completed_decision_service', decision: rowToDecision(out.rows[0]) });
  } catch (e) {
    res.status(500).json({ ok:false, error:'COMPLETED_BY_ID_FAILED', message:e.message });
  }
});

app.get('/api/completed/id/:decision_id/timeline', async (req, res) => {
  try {
    const decisionId = String(req.params.decision_id || '').trim();
    const out = await pool.query(`
      SELECT event_type,event_title,event_detail,event_payload,created_at
      FROM ndsp_decision_timeline
      WHERE decision_id=$1
      ORDER BY created_at ASC, id ASC
    `, [decisionId]);

    res.json({ ok:true, source:'completed_decision_service', decision_id:decisionId, timeline:out.rows });
  } catch (e) {
    res.status(500).json({ ok:false, error:'TIMELINE_FAILED', message:e.message });
  }
});

app.post('/api/completed/ingest', async (req, res) => {
  try {
    const body = req.body || {};
    const validation = validateForCompleted(body);

    if (!validation.ok) {
      return res.status(400).json({
        ok:false,
        error:'GOVERNANCE_VALIDATION_FAILED',
        errors: validation.errors
      });
    }

    const symbol = sanitizeSymbol(body.symbol);
    const state = sanitizeState(body.decision_state || 'Completed');
    const decisionId = String(body.decision_id || makeDecisionId(symbol));

    const completedAt = state === 'Completed' || state === 'Published'
      ? (body.completed_at || nowIso())
      : null;

    const publishedAt = state === 'Published'
      ? (body.published_at || nowIso())
      : null;

    const payload = {
      source: body.source || 'manual_ingest',
      governance_version: 'v1.0',
      raw: body.payload || {},
      received_at: nowIso()
    };

    const out = await pool.query(`
      INSERT INTO ndsp_completed_decisions (
        decision_id,
        symbol,
        market,
        decision_state,
        decision_quality,
        scenario_state,
        direction_context,
        activation_level,
        arrival_level,
        review_zone,
        invalidation_level,
        nmp_zone,
        risk_status,
        devil_advocate_status,
        visibility,
        payload,
        disclaimer,
        completed_at,
        published_at,
        expires_at
      )
      VALUES (
        $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16::jsonb,$17,$18,$19,$20
      )
      ON CONFLICT (decision_id)
      DO UPDATE SET
        symbol=EXCLUDED.symbol,
        market=EXCLUDED.market,
        decision_state=EXCLUDED.decision_state,
        decision_quality=EXCLUDED.decision_quality,
        scenario_state=EXCLUDED.scenario_state,
        direction_context=EXCLUDED.direction_context,
        activation_level=EXCLUDED.activation_level,
        arrival_level=EXCLUDED.arrival_level,
        review_zone=EXCLUDED.review_zone,
        invalidation_level=EXCLUDED.invalidation_level,
        nmp_zone=EXCLUDED.nmp_zone,
        risk_status=EXCLUDED.risk_status,
        devil_advocate_status=EXCLUDED.devil_advocate_status,
        visibility=EXCLUDED.visibility,
        payload=EXCLUDED.payload,
        disclaimer=EXCLUDED.disclaimer,
        completed_at=COALESCE(EXCLUDED.completed_at, ndsp_completed_decisions.completed_at),
        published_at=COALESCE(EXCLUDED.published_at, ndsp_completed_decisions.published_at),
        expires_at=EXCLUDED.expires_at,
        updated_at=now()
      RETURNING *
    `, [
      decisionId,
      symbol,
      body.market || null,
      state,
      validation.quality,
      body.scenario_state || null,
      body.direction_context || body.directional_context || null,
      body.activation_level || null,
      body.arrival_level || null,
      body.review_zone || null,
      body.invalidation_level || null,
      body.nmp_zone || null,
      body.risk_status || null,
      body.devil_advocate_status || null,
      body.visibility || 'private',
      JSON.stringify(payload),
      publicDisclaimer(),
      completedAt,
      publishedAt,
      body.expires_at || null
    ]);

    await addTimeline(decisionId, 'ingest', 'Decision ingested', 'Decision received by Completed Decision Service.', { symbol, state });
    await addTimeline(decisionId, 'governance', 'Governance validation passed', 'Decision passed required governance checks.', { quality: validation.quality });

    if (state === 'Completed' || state === 'Published') {
      await addTimeline(decisionId, 'completed', 'Decision Completed', 'Official NDSP decision completed.', { symbol, quality: validation.quality });
    }

    res.json({ ok:true, source:'completed_decision_service', decision: rowToDecision(out.rows[0]) });
  } catch (e) {
    res.status(500).json({ ok:false, error:'INGEST_FAILED', message:e.message });
  }
});

app.post('/api/completed/:decision_id/publish', async (req, res) => {
  try {
    const decisionId = String(req.params.decision_id || '').trim();
    const out = await pool.query(`
      UPDATE ndsp_completed_decisions
      SET decision_state='Published',
          visibility=COALESCE($2, visibility),
          published_at=now(),
          updated_at=now()
      WHERE decision_id=$1
      RETURNING *
    `, [decisionId, req.body?.visibility || 'public']);

    if (!out.rowCount) return res.status(404).json({ ok:false, error:'DECISION_NOT_FOUND' });

    await addTimeline(decisionId, 'published', 'Decision Published', 'Decision became visible to official consumers.', { visibility: req.body?.visibility || 'public' });

    res.json({ ok:true, source:'completed_decision_service', decision: rowToDecision(out.rows[0]) });
  } catch (e) {
    res.status(500).json({ ok:false, error:'PUBLISH_FAILED', message:e.message });
  }
});

initDb()
  .then(() => {
    app.listen(PORT, HOST, () => {
      console.log(`[NDSP] Completed Decision Service listening on http://${HOST}:${PORT}`);
    });
  })
  .catch((e) => {
    console.error('[NDSP] Completed Decision Service failed to initialize:', e);
    process.exit(1);
  });
