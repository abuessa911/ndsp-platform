'use strict';

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const PORT = Number(process.env.NDSP_BOT_EXECUTION_PORT || 9080);
const HOST = process.env.NDSP_BOT_EXECUTION_HOST || '127.0.0.1';
const COMPLETED_URL = process.env.NDSP_COMPLETED_DECISION_URL || 'http://127.0.0.1:9078';

const app = express();
app.use(helmet({ contentSecurityPolicy:false }));
app.use(cors({ origin:true, credentials:true }));
app.use(express.json({ limit:'1mb' }));

function disclaimer(){
  return 'NDSP Bot Execution Service is currently in DRY_RUN mode. No real trade is executed.';
}

async function fetchCompleted(symbol){
  const url = symbol
    ? `${COMPLETED_URL}/api/completed/${encodeURIComponent(symbol)}`
    : `${COMPLETED_URL}/api/completed/latest`;

  const r = await fetch(url);
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || 'COMPLETED_DECISION_FETCH_FAILED');
  return j.decision || null;
}

function executionGuard(decision){
  const errors = [];
  const warnings = [];

  if (!decision) errors.push('NO_COMPLETED_DECISION');
  if (decision && !['Completed','Published'].includes(String(decision.decision_state || ''))) {
    errors.push('DECISION_NOT_COMPLETED');
  }
  if (decision && String(decision.devil_advocate_status || '').toUpperCase().includes('BLOCK')) {
    errors.push('DEVIL_ADVOCATE_BLOCKED');
  }
  if (decision && Number(decision.decision_quality || 0) < 80) {
    errors.push('QUALITY_BELOW_EXECUTION_THRESHOLD');
  }
  if (decision && String(decision.risk_status || '').toUpperCase() === 'HIGH') {
    warnings.push('HIGH_RISK_STATUS');
  }

  return {
    ok: errors.length === 0,
    errors,
    warnings,
    mode: 'DRY_RUN'
  };
}

function buildDryRunPlan(decision){
  return {
    mode: 'DRY_RUN',
    action: 'NO_REAL_EXECUTION',
    symbol: decision.symbol,
    market: decision.market,
    decision_id: decision.id,
    quality: decision.decision_quality,
    state: decision.decision_state,
    levels: decision.levels,
    risk_status: decision.risk_status,
    devil_advocate_status: decision.devil_advocate_status,
    message: 'Decision is eligible for simulated execution only. Broker execution is not enabled.'
  };
}

app.get('/health', async (_req, res) => {
  res.json({
    ok:true,
    service:'ndsp-bot-execution-service',
    product:'NDSP Bot',
    connected_platform:'NDSP — Nawaf Decision Support Platform',
    port:PORT,
    mode:'DRY_RUN',
    completed_decision_url:COMPLETED_URL
  });
});

app.get('/api/bot/latest', async (_req, res) => {
  try {
    const decision = await fetchCompleted();
    const guard = executionGuard(decision);
    res.json({
      ok:true,
      source:'ndsp_bot_execution_service',
      decision,
      execution_guard:guard,
      execution_plan: guard.ok ? buildDryRunPlan(decision) : null,
      disclaimer:disclaimer()
    });
  } catch(e) {
    res.status(500).json({ ok:false, error:'BOT_LATEST_FAILED', message:e.message });
  }
});

app.get('/api/bot/:symbol', async (req, res) => {
  try {
    const decision = await fetchCompleted(req.params.symbol);
    const guard = executionGuard(decision);
    res.json({
      ok:true,
      source:'ndsp_bot_execution_service',
      decision,
      execution_guard:guard,
      execution_plan: guard.ok ? buildDryRunPlan(decision) : null,
      disclaimer:disclaimer()
    });
  } catch(e) {
    res.status(500).json({ ok:false, error:'BOT_SYMBOL_FAILED', message:e.message });
  }
});

app.post('/api/bot/simulate', async (req, res) => {
  try {
    const symbol = req.body?.symbol || '';
    const decision = await fetchCompleted(symbol);
    const guard = executionGuard(decision);

    if (!guard.ok) {
      return res.status(400).json({
        ok:false,
        source:'ndsp_bot_execution_service',
        error:'EXECUTION_GUARD_REJECTED',
        execution_guard:guard,
        decision,
        disclaimer:disclaimer()
      });
    }

    res.json({
      ok:true,
      source:'ndsp_bot_execution_service',
      simulated:true,
      execution_plan:buildDryRunPlan(decision),
      disclaimer:disclaimer()
    });
  } catch(e) {
    res.status(500).json({ ok:false, error:'BOT_SIMULATION_FAILED', message:e.message });
  }
});

app.listen(PORT, HOST, () => {
  console.log(`[NDSP] Bot Execution Service listening on http://${HOST}:${PORT}`);
});
