'use strict';

const { createNDSPService } = require('../../framework');

const SERVICE_ID = 'CDS-001';
const SERVICE_NAME = 'Completed Decision Service';
const SERVICE_VERSION = '1.0.0';

function buildFrameworkInfo() {
  return {
    id: 'ENG-001',
    factory: 'createNDSPService',
    factory_available: typeof createNDSPService === 'function',
    migration_mode: 'transitional_express_adapter',
    note: 'CDS preserves existing Express routes while exposing ENG-001 standard metadata endpoints.'
  };
}

function attachFrameworkStandard(app, options = {}) {
  if (!app || typeof app.get !== 'function') {
    throw new Error('attachFrameworkStandard requires an Express-compatible app');
  }

  const serviceId = options.serviceId || SERVICE_ID;
  const serviceName = options.serviceName || SERVICE_NAME;
  const version = options.version || SERVICE_VERSION;
  const description = options.description || 'Official NDSP completed decision source of truth.';

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
      role: 'single_source_of_truth_for_completed_decisions',
      decision_policy: 'decision_support_only',
      not_financial_advice: true,
      not_execution_instruction: true,
      framework: buildFrameworkInfo(),
      endpoints: [
        'GET /health',
        'GET /version',
        'GET /about',
        'GET /api/completed',
        'GET /api/completed/latest',
        'GET /api/completed/:symbol',
        'GET /api/completed/id/:decision_id',
        'GET /api/completed/id/:decision_id/timeline',
        'POST /api/completed/ingest',
        'POST /api/completed/:decision_id/publish'
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
