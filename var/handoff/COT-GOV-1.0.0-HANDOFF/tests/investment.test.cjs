'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const {
  runInvestmentAnalysis
} = require('../src/investment/investment-engine.cjs');

const fixture = JSON.parse(
  fs.readFileSync(
    path.join(
      __dirname,
      '../fixtures/cot-report-2026-07-21.json'
    ),
    'utf8'
  )
);

test('investment CORE uses Asset Manager Positions only', () => {
  const result = runInvestmentAnalysis({
    cot: fixture,
    perspective: 'CORE'
  });

  assert.deepEqual(
    result.directionResult.categories,
    ['ASSET_MANAGER']
  );

  assert.equal(result.directionResult.longValue, 4684);
  assert.equal(result.directionResult.shortValue, 1957);
  assert.equal(result.directionResult.dominanceDelta, 2727);
  assert.equal(result.directionResult.direction, 'BULLISH');
  assert.equal(
    result.directionResult.explicitness,
    'NON_EXPLICIT'
  );
  assert.equal(result.directionResult.horizon, 'NARROW');
});

test('investment weekly Changes cannot override total direction', () => {
  const result = runInvestmentAnalysis({
    cot: fixture,
    perspective: 'CORE'
  });

  assert.equal(result.directionResult.direction, 'BULLISH');
  assert.equal(
    result.weeklySupport.directionResult.direction,
    'BEARISH'
  );
  assert.equal(
    result.weeklySupport.status,
    'NOT_CONFIRMED'
  );
  assert.equal(
    result.weeklySupport.displayAr,
    'الدعم الأسبوعي غير متحقق'
  );
  assert.equal(
    result.weeklySupport.canOverrideOfficialDirection,
    false
  );
});

test('investment timing is fully disabled', () => {
  const result = runInvestmentAnalysis({
    cot: fixture,
    perspective: 'CORE'
  });

  assert.equal(result.timing.enabled, false);
  assert.equal(result.timing.dayControl, false);
  assert.equal(result.timing.tdlML, false);
  assert.equal(result.timing.tdlS, false);
});

test('investment EXPANDED is shadow only', () => {
  const result = runInvestmentAnalysis({
    cot: fixture,
    perspective: 'EXPANDED'
  });

  assert.equal(result.resultType, 'SHADOW');
  assert.deepEqual(
    result.directionResult.categories,
    ['ASSET_MANAGER', 'OTHER_REPORTABLES']
  );
  assert.equal(result.directionResult.dominanceDelta, 3384);
  assert.equal(
    result.weeklySupport.directionResult.dominanceDelta,
    338
  );
});
