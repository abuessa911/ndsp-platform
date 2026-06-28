'use strict';

const { createNDSPService } = require('../../framework');

const SERVICE_ID = 'DGC-001';
const SERVICE_NAME = 'Decision Governance Core';
const SERVICE_VERSION = '1.0.0';

function buildFrameworkInfo() {
  return {
    id: 'ENG-001',
    factory: 'createNDSPService',
    factory_available: typeof createNDSPService === 'function',
    migration_mode: 'transitional_express_adapter',
    note: 'DGC preserves existing Express routes while exposing ENG-001 standard metadata endpoints.'
  };
}

function attachFrameworkStandard(app, options = {}) {
  if (!app || typeof app.get !== 'function') {
    throw new Error('attachFrameworkStandard requires an Express-compatible app');
  }

  const serviceId = options.serviceId || SERVICE_ID;
  const serviceName = options.serviceName || SERVICE_NAME;
  const version = options.version || SERVICE_VERSION;
  const description = options.description || 'Official NDSP decision governance validation service.';

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
      role: 'governance_validation_before_completed_decision',
      decision_policy: 'decision_support_only',
      not_financial_advice: true,
      not_buy_sell_recommendation: true,
      not_execution_instruction: true,
      framework: buildFrameworkInfo(),
      upstream_dependency: 'CDS-001 Completed Decision Service',
      endpoints: [
        'GET /health',
        'GET /version',
        'GET /about',
        'POST /api/governance/evaluate',
        'POST /api/governance/submit'
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
