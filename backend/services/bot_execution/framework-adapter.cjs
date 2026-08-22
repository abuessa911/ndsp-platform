'use strict';

const { createNDSPService } = require('../../framework');

const SERVICE_ID = 'BOT-001';
const SERVICE_NAME = 'NDSP Bot Execution Service';
const SERVICE_VERSION = '1.0.0';

function buildFrameworkInfo() {
  return {
    id: 'ENG-001',
    factory: 'createNDSPService',
    factory_available: typeof createNDSPService === 'function',
    migration_mode: 'transitional_express_adapter',
    note: 'BOT preserves existing Express routes while exposing ENG-001 standard metadata endpoints.'
  };
}

function attachFrameworkStandard(app, options = {}) {
  if (!app || typeof app.get !== 'function') {
    throw new Error('attachFrameworkStandard requires an Express-compatible app');
  }

  const serviceId = options.serviceId || SERVICE_ID;
  const serviceName = options.serviceName || SERVICE_NAME;
  const version = options.version || SERVICE_VERSION;
  const description = options.description || 'NDSP bot execution boundary service.';

  app.get('/version', (_req, res) => {
    res.json({
      ok: true,
      service: serviceId,
      name: serviceName,
      version,
      build: version,
      framework: buildFrameworkInfo()
    });
  });

  app.get('/about', (_req, res) => {
    res.json({
      ok: true,
      service: serviceId,
      name: serviceName,
      description,
      role: 'bot_execution_boundary_after_completed_decision',
      decision_policy: 'execution_boundary_only_after_governed_completed_decision',
      not_financial_advice: true,
      not_buy_sell_recommendation: true,
      not_manual_execution_instruction: true,
      dry_run_required_during_migration: true,
      framework: buildFrameworkInfo(),
      upstream_dependency: 'DGC-001 Decision Governance Core and CDS-001 Completed Decision Service',
      endpoints: [
        'GET /health',
        'GET /version',
        'GET /about'
      ]
    });
  });

  return {
    ok: true,
    service: serviceId,
    framework: buildFrameworkInfo()
  };
}

module.exports = {
  attachFrameworkStandard,
  buildFrameworkInfo
};
