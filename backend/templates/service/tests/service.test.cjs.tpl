'use strict';

const assert = require('assert');
const { spawn } = require('child_process');

async function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchJson(url) {
  const r = await fetch(url);
  return { status: r.status, json: await r.json() };
}

async function waitForService(base, child, getLogs) {
  const deadline = Date.now() + 12000;

  while (Date.now() < deadline) {
    if (child.exitCode !== null) {
      const logs = getLogs();
      throw new Error(
        'Service exited before readiness. exitCode=' + child.exitCode +
        '\nSTDOUT:\n' + logs.stdout +
        '\nSTDERR:\n' + logs.stderr
      );
    }

    try {
      const health = await fetchJson(base + '/health');
      if (health.status === 200 && health.json.ok === true) {
        return health;
      }
    } catch (_err) {
      // wait until service is ready
    }

    await wait(300);
  }

  const logs = getLogs();
  throw new Error(
    'Service did not become ready before timeout.' +
    '\nSTDOUT:\n' + logs.stdout +
    '\nSTDERR:\n' + logs.stderr
  );
}

async function main() {
  const port = 20000 + Math.floor(Math.random() * 2000);
  let stdout = '';
  let stderr = '';

  const child = spawn(process.execPath, ['main.cjs'], {
    cwd: __dirname + '/..',
    env: {
      ...process.env,
      PORT: String(port),
      NDSP_PORT: String(port),
      NDSP_HOST: '127.0.0.1',
      NODE_ENV: 'test'
    },
    stdio: ['ignore', 'pipe', 'pipe']
  });

  child.stdout.on('data', d => { stdout += d.toString(); });
  child.stderr.on('data', d => { stderr += d.toString(); });

  const base = 'http://127.0.0.1:' + port;

  const health = await waitForService(base, child, () => ({ stdout, stderr }));
  assert.strictEqual(health.status, 200);
  assert.strictEqual(health.json.ok, true);
  assert.strictEqual(health.json.service, '__SERVICE_ID__');

  const version = await fetchJson(base + '/version');
  assert.strictEqual(version.status, 200);
  assert.strictEqual(version.json.version, '__VERSION__');

  const about = await fetchJson(base + '/about');
  assert.strictEqual(about.status, 200);
  assert.strictEqual(about.json.framework.id, 'ENG-001');

  const info = await fetchJson(base + '/service-info');
  assert.strictEqual(info.status, 200);
  assert.strictEqual(info.json.service, '__SERVICE_ID__');
  assert.strictEqual(info.json.framework, 'ENG-001');

  child.kill('SIGTERM');
  await wait(300);

  console.log('__SERVICE_ID___TEST_PASS=YES');
}

main().catch(err => {
  console.error('__SERVICE_ID___TEST_PASS=NO');
  console.error(err);
  process.exit(1);
});
