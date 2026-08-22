'use strict';

const { analyzeCategories } = require('../shared/dominance.cjs');
const {
  CONTROLLER,
  controllerForTimestamp
} = require('../timing/day-control.cjs');
const {
  getEffectiveWindow,
  isWithinEffectiveWindow
} = require('../timing/report-calendar.cjs');

const CATEGORY_MAP = Object.freeze({
  CORE: Object.freeze({
    LONG_TERM: Object.freeze(['ASSET_MANAGER']),
    SHORT_TERM: Object.freeze(['LEVERAGED_FUNDS'])
  }),
  EXPANDED: Object.freeze({
    LONG_TERM: Object.freeze([
      'ASSET_MANAGER',
      'OTHER_REPORTABLES'
    ]),
    SHORT_TERM: Object.freeze([
      'LEVERAGED_FUNDS',
      'DEALER_INTERMEDIARY'
    ])
  })
});

async function runSpeculationAnalysis({
  cot,
  timestamp,
  perspective = 'CORE',
  dayControlPerspective = 'D1',
  timingAdapter = null
}) {
  if (!cot || typeof cot !== 'object') {
    throw new TypeError('cot input is required');
  }

  const categoryPerspective = CATEGORY_MAP[perspective];

  if (!categoryPerspective) {
    throw new Error(`Unknown speculation perspective: ${perspective}`);
  }

  const window = getEffectiveWindow(cot.reportDate);

  if (!isWithinEffectiveWindow(timestamp, window)) {
    throw new Error('TIMESTAMP_OUTSIDE_REPORT_EFFECTIVE_WINDOW');
  }

  const control = controllerForTimestamp(
    timestamp,
    dayControlPerspective
  );

  const categories =
    control.controller === CONTROLLER.LONG_TERM
      ? categoryPerspective.LONG_TERM
      : categoryPerspective.SHORT_TERM;

  const directionResult = analyzeCategories(
    cot.changes,
    categories
  );

  let timing = {
    enabled: false,
    status: 'NOT_CONFIGURED',
    canOverrideDirection: false
  };

  if (timingAdapter !== null) {
    if (typeof timingAdapter !== 'function') {
      throw new TypeError('timingAdapter must be a function');
    }

    const adapterResult = await timingAdapter({
      analysisMode: 'SPECULATION',
      timestamp,
      controller: control.controller,
      directionResult,
      categories,
      reportDate: cot.reportDate
    });

    timing = {
      enabled: true,
      status: 'EVALUATED',
      canOverrideDirection: false,
      result: adapterResult
    };
  }

  return {
    governanceVersion: 'COT-GOV-1.0.0',
    analysisMode: 'SPECULATION',
    perspective,
    resultType: perspective === 'CORE' ? 'OFFICIAL' : 'SHADOW',
    controller: control.controller,
    dayName: control.dayName,
    dayControlPerspective,
    effectiveWindow: window,
    directionResult,
    weeklySupport: {
      status: 'NOT_APPLICABLE'
    },
    timing
  };
}

module.exports = {
  CATEGORY_MAP,
  runSpeculationAnalysis
};
