'use strict';

const {
  runInvestmentAnalysis
} = require('../investment/investment-engine.cjs');
const {
  runSpeculationAnalysis
} = require('../speculation/speculation-engine.cjs');

async function runGovernedAnalysis({
  analysisMode,
  cot,
  timestamp,
  dayControlPerspective = 'D1',
  timingAdapter = null
}) {
  if (analysisMode === 'INVESTMENT') {
    return {
      official: runInvestmentAnalysis({
        cot,
        perspective: 'CORE'
      }),
      shadow: runInvestmentAnalysis({
        cot,
        perspective: 'EXPANDED'
      })
    };
  }

  if (analysisMode === 'SPECULATION') {
    if (!timestamp) {
      throw new Error('timestamp is required for speculation mode');
    }

    const official = await runSpeculationAnalysis({
      cot,
      timestamp,
      perspective: 'CORE',
      dayControlPerspective,
      timingAdapter
    });

    const shadow = await runSpeculationAnalysis({
      cot,
      timestamp,
      perspective: 'EXPANDED',
      dayControlPerspective,
      timingAdapter
    });

    return {
      official,
      shadow
    };
  }

  throw new Error(`Unsupported analysis mode: ${analysisMode}`);
}

module.exports = {
  runGovernedAnalysis
};
