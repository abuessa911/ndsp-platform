'use strict';

function registerAbout(app, ctx) {
  app.get('/about', (_req, res) => {
    res.json({
      ok: true,
      service: ctx.serviceId,
      service_name: ctx.serviceName,
      component: ctx.component || 'ENG-001',
      product: ctx.product,
      domain: ctx.domain,
      owner: ctx.owner,
      description: ctx.description,
      documentation_version: ctx.documentationVersion || ctx.version,
      framework: {
        id: 'ENG-001',
        name: 'NDSP Service Framework',
        version: ctx.frameworkVersion || '1.0.0'
      },
      timestamp: new Date().toISOString()
    });
  });
}

module.exports = { registerAbout };
