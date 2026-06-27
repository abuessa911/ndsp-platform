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

async function main() {
  const port = 19081 + Math.floor(Math.random() * 1000);
  const child = spawn(process.execPath, ['main.cjs'], {
    cwd: __dirname + '/..',
    env: { ...process.env, PORT: String(port), NDSP_PORT: String(port), NODE_ENV: 'test' },
    stdio: ['ignore', 'pipe', 'pipe']
  });

  let stderr = '';
  child.stderr.on('data', d => { stderr += d.toString(); });

  await wait(900);

  const base = `http://127.0.0.1:${port}`;

  const health = await fetchJson(`${base}/health`);
  assert.strictEqual(health.status, 200);
  assert.strictEqual(health.json.ok, true);
  assert.strictEqual(health.json.service, 'CTL-001');

  const version = await fetchJson(`${base}/version`);
  assert.strictEqual(version.status, 200);
  assert.strictEqual(version.json.version, '1.0.0');

  const about = await fetchJson(`${base}/about`);
  assert.strictEqual(about.status, 200);
  assert.strictEqual(about.json.framework.id, 'ENG-001');

  const identity = await fetchJson(`${base}/identity`);
  assert.strictEqual(identity.status, 200);
  assert.strictEqual(identity.json.service, 'CTL-001');
  assert.strictEqual(identity.json.workspace, 'NDSP');
  assert.strictEqual(identity.json.framework, 'ENG-001');

  child.kill('SIGTERM');
  await wait(300);

  console.log('CTL001_TEST_PASS=YES');
}

main().catch(err => {
  console.error('CTL001_TEST_PASS=NO');
  console.error(err);
  process.exit(1);
});
