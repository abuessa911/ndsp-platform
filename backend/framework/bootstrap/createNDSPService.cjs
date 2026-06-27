'use strict';

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const { createLogger } = require('../logger/logger.cjs');
const { loadConfig } = require('../config/config.cjs');
const { registerHealth } = require('../health/health.cjs');
const { registerVersion } = require('../version/version.cjs');
const { registerAbout } = require('../about/about.cjs');
const { errorMiddleware } = require('../errors/errors.cjs');
const { attachGracefulShutdown } = require('../lifecycle/lifecycle.cjs');

function createNDSPService(options = {}) {
  const required = ['serviceId', 'serviceName', 'product', 'domain', 'version'];
  for (const k of required) {
    if (!options[k]) throw new Error(`createNDSPService missing required option: ${k}`);
  }

  const config = loadConfig({ serviceRoot: options.serviceRoot || process.cwd(), port: options.port });

  const ctx = {
    serviceId: options.serviceId,
    serviceName: options.serviceName,
    product: options.product,
    domain: options.domain,
    version: options.version,
    release: options.release || 'REL-1.1',
    owner: options.owner || 'NDSP Engineering',
    description: options.description || '',
    component: options.component || 'ENG-001',
    documentationVersion: options.documentationVersion || options.version,
    frameworkVersion: '1.0.0',
    build: options.build || options.version,
    config
  };

  const logger = createLogger(ctx);
  const app = express();

  app.disable('x-powered-by');
  app.use(helmet({ contentSecurityPolicy: false }));
  app.use(cors({ origin: true, credentials: true }));
  app.use(express.json({ limit: options.jsonLimit || '2mb' }));

  app.use((req, res, next) => {
    res.setHeader('X-NDSP-Service', ctx.serviceId);
    res.setHeader('X-NDSP-Version', ctx.version);
    next();
  });

  registerHealth(app, ctx);
  registerVersion(app, ctx);
  registerAbout(app, ctx);

  if (typeof options.routes === 'function') {
    options.routes(app, { ctx, logger, config });
  }

  app.use((_req, res) => {
    res.status(404).json({
      ok: false,
      service: ctx.serviceId,
      version: ctx.version,
      timestamp: new Date().toISOString(),
      error: { code: 'NDSP-4040', message: 'Route not found' }
    });
  });

  app.use(errorMiddleware(ctx, logger));

  function start(startOptions = {}) {
    const host = startOptions.host || options.host || config.host || '127.0.0.1';
    const port = Number(startOptions.port ?? options.port ?? config.port ?? 0);
    const server = app.listen(port, host, () => {
      const address = server.address();
      logger.info('service_started', { host, port: address && address.port ? address.port : port, service_id: ctx.serviceId });
    });
    attachGracefulShutdown(server, logger);
    return server;
  }

  return { app, ctx, logger, config, start };
}

module.exports = { createNDSPService };
