'use strict';

const assert = require('assert');
const { createNDSPService } = require('../index.cjs');

async function main() {
  const service = createNDSPService({
    serviceId: 'TEST-001',
    serviceName: 'Framework Test Service',
    product: 'SYS-001',
    domain: 'Testing',
    version: '1.0.0',
    description: 'Framework self-test service'
  });

  const server = service.start({ host: '127.0.0.1', port: 0 });
  await new Promise(resolve => server.once('listening', resolve));

  const port = server.address().port;
  const base = `http://127.0.0.1:${port}`;

  const health = await fetch(`${base}/health`).then(r => r.json());
  assert.strictEqual(health.ok, true);
  assert.strictEqual(health.service, 'TEST-001');
  assert.strictEqual(health.status, 'UP');

  const version = await fetch(`${base}/version`).then(r => r.json());
  assert.strictEqual(version.ok, true);
  assert.strictEqual(version.version, '1.0.0');

  const about = await fetch(`${base}/about`).then(r => r.json());
  assert.strictEqual(about.ok, true);
  assert.strictEqual(about.framework.id, 'ENG-001');

  const notFound = await fetch(`${base}/missing`);
  assert.strictEqual(notFound.status, 404);

  await new Promise(resolve => server.close(resolve));
  console.log('FRAMEWORK_TEST_PASS=YES');
}

main().catch(err => {
  console.error('FRAMEWORK_TEST_PASS=NO');
  console.error(err);
  process.exit(1);
});
