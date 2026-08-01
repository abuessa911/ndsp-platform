'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..', '..');
const packageDir = path.join(
  root,
  'docs/99-governance/pr-049-p0-batch-11-evidence-closure',
);
const summary = JSON.parse(
  fs.readFileSync(path.join(packageDir, 'PR049_SUMMARY.json'), 'utf8'),
);
const matrix = JSON.parse(
  fs.readFileSync(path.join(packageDir, 'PR049_EVIDENCE_MATRIX.json'), 'utf8'),
);
const results = JSON.parse(
  fs.readFileSync(path.join(packageDir, 'PR049_CLOSURE_RESULTS.json'), 'utf8'),
);

test('PR-049 processes one bounded PR-036 batch', () => {
  assert.ok(summary.input_capability_count >= 1);
  assert.ok(summary.input_capability_count <= 25);
  assert.equal(matrix.length, summary.input_capability_count);
  assert.equal(results.length, summary.input_capability_count);
});

test('PR-049 closure accounting is exact', () => {
  assert.equal(
    summary.machine_closed_count + summary.remaining_gap_count,
    summary.input_capability_count,
  );
  assert.equal(summary.traceability_rows_updated, summary.machine_closed_count);
});

test('PR-049 never closes incomplete evidence', () => {
  for (const row of matrix) {
    const requiredEvidencePresent =
      (!JSON.parse(row.service_required) ||
        JSON.parse(row.service_evidence_found)) &&
      (!JSON.parse(row.endpoint_required) ||
        JSON.parse(row.endpoint_evidence_found)) &&
      (!JSON.parse(row.real_data_required) ||
        JSON.parse(row.real_data_evidence_found));

    assert.equal(JSON.parse(row.machine_closed), requiredEvidencePresent);
  }
});

test('PR-049 preserves runtime safety', () => {
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
  assert.equal(summary.runtime_changes, 'none');
  assert.equal(summary.ui_complete_records_created, 0);
  assert.equal(summary.full_capability_coverage_claimed, false);
});
