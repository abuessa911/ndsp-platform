'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..');
const selectionPath = path.join(
  root,
  'docs/99-governance/pr-034-restore-tdl-v2-policy',
  'PR034_SELECTED_SOURCE.json',
);
const selection = JSON.parse(
  fs.readFileSync(selectionPath, 'utf8'),
);
const restored = path.join(root, selection.restored_target);
const source = fs.readFileSync(restored, 'utf8');

test('PR-034 restored source exists and is non-empty', () => {
  assert.ok(fs.existsSync(restored));
  assert.ok(fs.statSync(restored).size > 0);
});

test('PR-034 restored both policy functions', () => {
  assert.match(
    source,
    /(?:async\s+)?def\s+read_tdl_v2_policy\s*\(/,
  );
  assert.match(
    source,
    /(?:async\s+)?def\s+write_tdl_v2_policy\s*\(/,
  );
});

test('PR-034 selection preserved local evidence', () => {
  assert.equal(selection.local_sources_deleted, false);
  assert.equal(selection.snapshots_deleted, false);
  assert.equal(selection.secrets_copied, false);
  assert.match(selection.selected_sha256, /^[a-f0-9]{64}$/);
});
