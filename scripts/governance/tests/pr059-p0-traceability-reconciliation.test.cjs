'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..', '..');
const packageDir = path.join(
  root,
  'docs/99-governance/pr-059-p0-traceability-reconciliation',
);
const summary = JSON.parse(
  fs.readFileSync(path.join(packageDir, 'PR059_SUMMARY.json'), 'utf8'),
);
const audit = JSON.parse(
  fs.readFileSync(
    path.join(packageDir, 'PR059_RECONCILIATION_AUDIT.json'),
    'utf8',
  ),
);
const coverage = JSON.parse(
  fs.readFileSync(
    path.join(packageDir, 'PR059_POST_RECONCILIATION_COVERAGE.json'),
    'utf8',
  ),
);

test('PR-059 accounts for all P0 closures', () => {
  assert.equal(summary.p0_assignment_count, 391);
  assert.equal(summary.p0_batch_count, 19);
  assert.equal(summary.p0_machine_closed_count, 391);
  assert.equal(summary.p0_closure_records_accounted, 391);
  assert.equal(audit.length, 391);
});

test('PR-059 eliminates canonical P0 standard gaps', () => {
  assert.equal(summary.p0_canonical_standard_gap_count, 0);
  for (const row of audit) {
    if (JSON.parse(row.service_required)) {
      assert.notEqual(row.new_runtime_service.trim(), '');
    }
    if (JSON.parse(row.endpoint_required)) {
      assert.notEqual(row.new_endpoint_or_contract.trim(), '');
    }
    if (JSON.parse(row.real_data_required)) {
      assert.notEqual(row.new_data_source.trim(), '');
      assert.ok(
        ['REAL_LIVE', 'REAL_SNAPSHOT'].includes(row.new_data_state),
        `Unexpected real-data state: ${row.new_data_state}`,
      );
    }
  }
});

test('PR-059 recalculates exactly 526 capabilities', () => {
  assert.equal(summary.total_capabilities, 526);
  assert.equal(coverage.length, 526);
  assert.equal(
    summary.fully_evidenced_capabilities +
      summary.partially_evidenced_capabilities +
      summary.discovery_required_capabilities,
    526,
  );
});

test('PR-059 preserves safety and does not overclaim UI', () => {
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
  assert.equal(summary.ui_complete_records_created, 0);
  assert.equal(summary.runtime_changes, 'none');
  assert.equal(summary.human_confirmation_required, true);
});
