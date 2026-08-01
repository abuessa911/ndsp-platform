'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..', '..');
const packageDir = path.join(
  root,
  'docs/99-governance/pr-036-p0-remediation-batches',
);

const summary = JSON.parse(
  fs.readFileSync(path.join(packageDir, 'PR036_SUMMARY.json'), 'utf8'),
);
const top50 = JSON.parse(
  fs.readFileSync(
    path.join(packageDir, 'PR036_TOP_50_P0_CAPABILITIES.json'),
    'utf8',
  ),
);
const batches = JSON.parse(
  fs.readFileSync(
    path.join(packageDir, 'PR036_REMEDIATION_BATCHES.json'),
    'utf8',
  ),
);
const assignments = JSON.parse(
  fs.readFileSync(
    path.join(packageDir, 'PR036_BATCH_ASSIGNMENTS.json'),
    'utf8',
  ),
);

test('PR-036 accounts for all 391 P0 capabilities', () => {
  assert.equal(summary.p0_capability_count, 391);
  assert.equal(assignments.length, 391);
  assert.equal(new Set(assignments.map((row) => row.capability_id)).size, 391);
  assert.equal(summary.unassigned_p0_capabilities, 0);
  assert.equal(summary.duplicate_assignments, 0);
});

test('PR-036 exports a deterministic top 50', () => {
  assert.equal(top50.length, 50);

  for (let index = 0; index < top50.length; index += 1) {
    assert.equal(Number(top50[index].rank), index + 1);
  }

  for (let index = 1; index < top50.length; index += 1) {
    const previous = top50[index - 1];
    const current = top50[index];

    assert.ok(
      Number(previous.p0_gap_count) > Number(current.p0_gap_count) ||
        (
          Number(previous.p0_gap_count) === Number(current.p0_gap_count) &&
          (
            Number(previous.total_gap_count) > Number(current.total_gap_count) ||
            (
              Number(previous.total_gap_count) ===
                Number(current.total_gap_count) &&
              previous.capability_id.localeCompare(current.capability_id) <= 0
            )
          )
        ),
    );
  }
});

test('PR-036 batches are executable and bounded', () => {
  assert.ok(batches.length > 0);
  assert.ok(
    batches.every(
      (batch) =>
        Number(batch.capability_count) >= 1 &&
        Number(batch.capability_count) <= 25,
    ),
  );
  assert.ok(
    batches.every(
      (batch) =>
        batch.production_restart_allowed === 'false' &&
        batch.mutating_probe_allowed === 'false',
    ),
  );
});

test('PR-036 is planning-only', () => {
  assert.equal(summary.traceability_rows_modified, 0);
  assert.equal(summary.runtime_changes, 'none');
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
  assert.equal(summary.full_capability_coverage_claimed, false);
});
