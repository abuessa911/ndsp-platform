'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..', '..');
const packageDir = path.join(
  root,
  'docs/99-governance/pr-035-full-coverage-recalculation',
);
const summary = JSON.parse(
  fs.readFileSync(path.join(packageDir, 'PR035_SUMMARY.json'), 'utf8'),
);
const matrix = JSON.parse(
  fs.readFileSync(
    path.join(packageDir, 'PR035_CAPABILITY_COVERAGE_MATRIX.json'),
    'utf8',
  ),
);

test('PR-035 recalculates exactly 526 capabilities', () => {
  assert.equal(summary.total_capabilities, 526);
  assert.equal(matrix.length, 526);
});

test('PR-035 status accounting equals 526', () => {
  const accounted =
    summary.fully_evidenced_capabilities +
    summary.partially_evidenced_capabilities +
    summary.discovery_required_capabilities;
  assert.equal(accounted, 526);
});

test('PR-035 never overclaims full coverage', () => {
  const expected =
    summary.remaining_capability_count === 0 &&
    summary.fully_evidenced_capabilities === 526;
  assert.equal(summary.full_capability_coverage_claimed, expected);
});

test('PR-035 includes both PR-033 capabilities', () => {
  assert.equal(summary.pr033_closed_capabilities_verified, 2);
  const ids = new Set(matrix.map((row) => row.capability_id));
  assert.ok(ids.has('CAP-4FF90CCC6DFE'));
  assert.ok(ids.has('CAP-8A9DD9B6E7D5'));
});
