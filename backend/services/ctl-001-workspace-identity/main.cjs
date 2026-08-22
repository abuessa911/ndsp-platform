'use strict';

const { createNDSPService } = require('../../framework');

const service = createNDSPService({
  serviceId: 'CTL-001',
  serviceName: 'Workspace Identity',
  product: 'SYS-001',
  domain: 'Operating System',
  version: '1.0.0',
  release: 'REL-1.1',
  owner: 'NDSP Engineering',
  component: 'CTL-001',
  description: 'NDSP-OS workspace identity service. Provides identity, health, version and about endpoints.',
  serviceRoot: __dirname,
  routes(app, { ctx }) {
    app.get('/identity', (_req, res) => {
      res.json({
        ok: true,
        service: ctx.serviceId,
        service_name: ctx.serviceName,
        product: ctx.product,
        workspace: 'NDSP',
        ecosystem: 'NDSP Ecosystem',
        operating_system: 'NDSP-OS',
        environment: process.env.NODE_ENV || 'production',
        release: ctx.release,
        version: ctx.version,
        framework: 'ENG-001',
        status: 'ACTIVE',
        timestamp: new Date().toISOString()
      });
    });
  }
});

service.start();
