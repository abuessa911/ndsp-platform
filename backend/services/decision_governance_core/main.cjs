'use strict';

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const PORT = Number(process.env.NDSP_GOVERNANCE_PORT || 9079);
const HOST = process.env.NDSP_GOVERNANCE_HOST || '127.0.0.1';
const COMPLETED_URL = process.env.NDSP_COMPLETED_DECISION_URL || 'http://127.0.0.1:9078';

const app = express();
app.use(helmet({ contentSecurityPolicy:false }));
app.use(cors({ origin:true, credentials:true }));
app.use(express.json({ limit:'2mb' }));

function cleanSymbol(v){
  return String(v || '').trim().toUpperCase().replace(/[^A-Z0-9._:-]/g,'').slice(0,32);
}

function num(v){
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function validateDecision(input){
  const errors = [];
  const warnings = [];

  const symbol = cleanSymbol(input.symbol);
  const quality = num(input.decision_quality ?? input.quality);

  if (!symbol) errors.push('SYMBOL_REQUIRED');
  if (quality === null || quality < 0 || quality > 100) errors.push('QUALITY_MUST_BE_0_TO_100');

  const devil = String(input.devil_advocate_status || '').toUpperCase();
  if (devil.includes('BLOCK')) errors.push('DEVIL_ADVOCATE_BLOCKED');

  if (!input.scenario_state) warnings.push('SCENARIO_STATE_MISSING');
  if (!input.direction_context && !input.directional_context) warnings.push('DIRECTION_CONTEXT_MISSING');
  if (!input.risk_status) warnings.push('RISK_STATUS_MISSING');

  return { ok: errors.length === 0, errors, warnings, symbol, quality };
}

function decideState(validation, input){
  if (!validation.ok) return 'Draft';

  const requested = String(input.decision_state || '').trim();

  if (requested === 'Published') return 'Published';
  if (requested === 'Completed') return 'Completed';

  if (validation.quality >= 80) return 'Completed';
  if (validation.quality >= 65) return 'Candidate';
  return 'Monitoring';
}

function toCompletedPayload(input, validation, state){
  return {
    symbol: validation.symbol,
    market: input.market || null,
    decision_state: state,
    decision_quality: validation.quality,
    scenario_state: input.scenario_state || null,
    direction_context: input.direction_context || input.directional_context || null,
    activation_level: input.activation_level || input.scenario_activation_level || null,
    arrival_level: input.arrival_level || input.scenario_arrival_level || null,
    review_zone: input.review_zone || input.scenario_review_zone || null,
    invalidation_level: input.invalidation_level || input.scenario_invalidation_level || null,
    nmp_zone: input.nmp_zone || input.nmp || null,
    risk_status: input.risk_status || null,
    devil_advocate_status: input.devil_advocate_status || 'PASSED',
    visibility: input.visibility || 'private',
    source: input.source || 'decision_governance_core',
    payload: {
      governance_core: {
        version: 'v1.0',
        warnings: validation.warnings,
        received_at: new Date().toISOString()
      },
      engine_payload: input.payload || {}
    }
  };
}

app.get('/health', async (_req, res) => {
  try {
    const r = await fetch(COMPLETED_URL + '/health');
    const j = await r.json().catch(() => null);
    res.json({
      ok:true,
      service:'ndsp-decision-governance-core',
      port:PORT,
      completed_decision_service:j
    });
  } catch(e) {
    res.status(500).json({
      ok:false,
      service:'ndsp-decision-governance-core',
      error:'COMPLETED_SERVICE_UNREACHABLE',
      message:e.message
    });
  }
});

app.post('/api/governance/evaluate', async (req, res) => {
  const input = req.body || {};
  const validation = validateDecision(input);
  const state = decideState(validation, input);

  res.status(validation.ok ? 200 : 400).json({
    ok: validation.ok,
    source:'decision_governance_core',
    validation,
    decision_state: state,
    publishable: ['Completed','Published'].includes(state),
    rule:'Decision is official only after Completed Decision Service accepts it.'
  });
});

app.post('/api/governance/submit', async (req, res) => {
  try {
    const input = req.body || {};
    const validation = validateDecision(input);
    const state = decideState(validation, input);

    if (!validation.ok) {
      return res.status(400).json({
        ok:false,
        source:'decision_governance_core',
        error:'GOVERNANCE_VALIDATION_FAILED',
        validation,
        decision_state:state
      });
    }

    if (!['Completed','Published'].includes(state)) {
      return res.json({
        ok:true,
        source:'decision_governance_core',
        decision_state:state,
        forwarded:false,
        message:'Decision is not completed yet. It remains internal monitoring/candidate.'
      });
    }

    const payload = toCompletedPayload(input, validation, state);

    const r = await fetch(COMPLETED_URL + '/api/completed/ingest', {
      method:'POST',
      headers:{ 'Content-Type':'application/json' },
      body:JSON.stringify(payload)
    });

    const j = await r.json().catch(() => ({}));

    res.status(r.ok ? 200 : 502).json({
      ok:r.ok,
      source:'decision_governance_core',
      forwarded:true,
      decision_state:state,
      completed_decision_response:j
    });
  } catch(e) {
    res.status(500).json({
      ok:false,
      source:'decision_governance_core',
      error:'GOVERNANCE_SUBMIT_FAILED',
      message:e.message
    });
  }
});

app.listen(PORT, HOST, () => {
  console.log(`[NDSP] Decision Governance Core listening on http://${HOST}:${PORT}`);
});
