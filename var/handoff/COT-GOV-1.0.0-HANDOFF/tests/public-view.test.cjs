'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const {
  runGovernedAnalysis
} = require('../src/shadow/perspective-runner.cjs');
const {
  toPublicResult
} = require('../src/public/public-view.cjs');

const fixture = JSON.parse(
  fs.readFileSync(
    path.join(
      __dirname,
      '../fixtures/cot-report-2026-07-21.json'
    ),
    'utf8'
  )
);

test('public result never exposes shadow result', async () => {
  const governed = await runGovernedAnalysis({
    analysisMode: 'INVESTMENT',
    cot: fixture
  });

  const publicResult = toPublicResult(governed);

  assert.equal(publicResult.perspective, 'CORE');
  assert.equal(publicResult.resultType, 'OFFICIAL');
  assert.equal(
    Object.prototype.hasOwnProperty.call(
      publicResult,
      'shadow'
    ),
    false
  );
});
