'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const {
  getEffectiveWindow,
  isWithinEffectiveWindow
} = require('../src/timing/report-calendar.cjs');

test('July 21 report activates on July 27 UTC', () => {
  const window = getEffectiveWindow('2026-07-21');

  assert.equal(
    window.effectiveFrom,
    '2026-07-27T00:00:00.000Z'
  );

  assert.equal(
    window.effectiveUntil,
    '2026-08-03T00:00:00.000Z'
  );
});

test('effective interval is half-open', () => {
  const window = getEffectiveWindow('2026-07-21');

  assert.equal(
    isWithinEffectiveWindow(
      '2026-07-27T00:00:00.000Z',
      window
    ),
    true
  );

  assert.equal(
    isWithinEffectiveWindow(
      '2026-08-03T00:00:00.000Z',
      window
    ),
    false
  );
});
