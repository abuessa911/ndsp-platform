'use strict';

function registerHealth(app, ctx) {
  app.get('/health', (_req, res) => {
    res.json({
      ok: true,
      service: ctx.serviceId,
      service_name: ctx.serviceName,
      product: ctx.product,
      domain: ctx.domain,
      version: ctx.version,
      release: ctx.release,
      uptime_seconds: Math.floor(process.uptime()),
      timestamp: new Date().toISOString(),
      status: 'UP'
    });
  });
}

module.exports = { registerHealth };
