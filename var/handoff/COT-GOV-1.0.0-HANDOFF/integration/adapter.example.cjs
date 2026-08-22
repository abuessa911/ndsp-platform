'use strict';

/*
  Example only.
  Do not connect this adapter to production before mapping the
  current service request and response contracts.
*/

const {
  runGovernedAnalysis,
  toPublicResult
} = require('../src/index.cjs');

async function evaluateCotGovernance(payload, timingAdapter = null) {
  const governed = await runGovernedAnalysis({
    analysisMode: payload.analysisMode,
    cot: payload.cot,
    timestamp: payload.timestamp,
    dayControlPerspective:
      payload.dayControlPerspective || 'D1',
    timingAdapter
  });

  return {
    publicResult: toPublicResult(governed),
    internalShadowResult: governed.shadow
  };
}

module.exports = {
  evaluateCotGovernance
};
