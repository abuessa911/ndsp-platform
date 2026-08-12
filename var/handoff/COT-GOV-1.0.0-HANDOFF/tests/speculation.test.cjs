'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const {
  runSpeculationAnalysis
} = require('../src/speculation/speculation-engine.cjs');

const fixture = JSON.parse(
  fs.readFileSync(
    path.join(
      __dirname,
      '../fixtures/cot-report-2026-07-21.json'
    ),
    'utf8'
  )
);

test('D1 Monday uses long-term CORE category', async () => {
  const result = await runSpeculationAnalysis({
    cot: fixture,
    timestamp: '2026-07-27T12:00:00.000Z',
    perspective: 'CORE',
    dayControlPerspective: 'D1'
  });

  assert.equal(result.controller, 'LONG_TERM');
  assert.deepEqual(
    result.directionResult.categories,
    ['ASSET_MANAGER']
  );
  assert.equal(result.directionResult.direction, 'BEARISH');
});

test('D2 Monday uses short-term CORE category', async () => {
  const result = await runSpeculationAnalysis({
    cot: fixture,
    timestamp: '2026-07-27T12:00:00.000Z',
    perspective: 'CORE',
    dayControlPerspective: 'D2'
  });

  assert.equal(result.controller, 'SHORT_TERM');
  assert.deepEqual(
    result.directionResult.categories,
    ['LEVERAGED_FUNDS']
  );
  assert.equal(result.directionResult.direction, 'BEARISH');
});

test('D2 Thursday uses long-term EXPANDED categories', async () => {
  const result = await runSpeculationAnalysis({
    cot: fixture,
    timestamp: '2026-07-30T12:00:00.000Z',
    perspective: 'EXPANDED',
    dayControlPerspective: 'D2'
  });

  assert.equal(result.controller, 'LONG_TERM');
  assert.deepEqual(
    result.directionResult.categories,
    ['ASSET_MANAGER', 'OTHER_REPORTABLES']
  );
  assert.equal(result.directionResult.longValue, 332);
  assert.equal(result.directionResult.shortValue, -6);
  assert.equal(result.directionResult.direction, 'BULLISH');
  assert.equal(result.directionResult.explicitness, 'EXPLICIT');
  assert.equal(result.directionResult.horizon, 'EXTENDED');
});

test('timing adapter is called only in speculation mode', async () => {
  let calls = 0;

  const result = await runSpeculationAnalysis({
    cot: fixture,
    timestamp: '2026-07-30T12:00:00.000Z',
    perspective: 'CORE',
    dayControlPerspective: 'D1',
    timingAdapter: async context => {
      calls += 1;
      return {
        accepted: true,
        receivedMode: context.analysisMode
      };
    }
  });

  assert.equal(calls, 1);
  assert.equal(result.timing.enabled, true);
  assert.equal(result.timing.canOverrideDirection, false);
});
