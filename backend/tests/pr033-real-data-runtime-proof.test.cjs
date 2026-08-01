'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..');
const proofPath = path.join(
  root,
  'docs/99-governance/pr-033-real-data-runtime-proof',
  'PR033_RUNTIME_PROOF.json',
);
const proof = JSON.parse(fs.readFileSync(proofPath, 'utf8'));

test('PR-033 contains exactly two closed capabilities', () => {
  assert.equal(proof.length, 2);
  assert.deepEqual(
    proof.map((row) => row.capability_id).sort(),
    ['CAP-4FF90CCC6DFE', 'CAP-8A9DD9B6E7D5'],
  );
  assert.ok(
    proof.every(
      (row) => row.closure_state === 'CLOSED_MACHINE_VERIFIED',
    ),
  );
});

for (const row of proof) {
  test(`PR-033 runtime proof: ${row.capability_id}`, () => {
    assert.match(
      row.canonical_endpoint,
      /^GET \/api\/admin\/timing_model-v2\/(policy|auth-debug)$/,
    );
    assert.match(row.data_state, /^REAL_(LIVE|SNAPSHOT)$/);
    assert.ok(row.data_source);
    assert.equal(Number(row.http_status), 200);
    assert.match(row.payload_sha256, /^[a-f0-9]{64}$/);
    assert.ok(Number(row.payload_bytes) > 0);
    assert.ok(Number(row.root_item_count) > 0);
    assert.equal(row.runtime_mode, 'ISOLATED_REAL_CODE');
    assert.equal(row.payload_values_persisted, 'false');
    assert.equal(row.ui_complete_created, 'false');

    const source = row.source_file.split('::', 1)[0];
    assert.ok(
      fs.existsSync(path.join(root, source)),
      `source file missing: ${source}`,
    );
  });
}
