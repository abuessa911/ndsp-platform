'use strict';

function registerVersion(app, ctx) {
  app.get('/version', (_req, res) => {
    res.json({
      ok: true,
      service: ctx.serviceId,
      service_name: ctx.serviceName,
      version: ctx.version,
      build: ctx.build || ctx.version,
      release: ctx.release,
      git_commit: process.env.GIT_COMMIT || null,
      timestamp: new Date().toISOString()
    });
  });
}

module.exports = { registerVersion };
