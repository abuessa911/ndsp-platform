'use strict';

const { analyzeCategories } = require('../shared/dominance.cjs');
const { getEffectiveWindow } = require('../timing/report-calendar.cjs');

const PERSPECTIVE_CATEGORIES = Object.freeze({
  CORE: Object.freeze(['ASSET_MANAGER']),
  EXPANDED: Object.freeze([
    'ASSET_MANAGER',
    'OTHER_REPORTABLES'
  ])
});

function runInvestmentAnalysis({ cot, perspective = 'CORE' }) {
  if (!cot || typeof cot !== 'object') {
    throw new TypeError('cot input is required');
  }

  const categories = PERSPECTIVE_CATEGORIES[perspective];

  if (!categories) {
    throw new Error(`Unknown investment perspective: ${perspective}`);
  }

  const officialDirection = analyzeCategories(
    cot.positions,
    categories
  );

  const weeklyDirection = analyzeCategories(
    cot.changes,
    categories
  );

  const weeklySupportStatus =
    weeklyDirection.direction === officialDirection.direction
      ? 'CONFIRMED'
      : 'NOT_CONFIRMED';

  return {
    governanceVersion: 'COT-GOV-1.0.0',
    analysisMode: 'INVESTMENT',
    perspective,
    resultType: perspective === 'CORE' ? 'OFFICIAL' : 'SHADOW',
    controller: 'NOT_APPLICABLE',
    effectiveWindow: getEffectiveWindow(cot.reportDate),
    directionResult: officialDirection,
    weeklySupport: {
      status: weeklySupportStatus,
      directionResult: weeklyDirection,
      displayAr:
        weeklySupportStatus === 'CONFIRMED'
          ? 'الدعم الأسبوعي متحقق'
          : 'الدعم الأسبوعي غير متحقق',
      displayEn:
        weeklySupportStatus === 'CONFIRMED'
          ? 'Weekly support is confirmed'
          : 'Weekly support is not confirmed',
      canOverrideOfficialDirection: false,
      canHideOfficialDirection: false
    },
    timing: {
      enabled: false,
      dayControl: false,
      tdlML: false,
      tdlS: false,
      status: 'DISABLED_FOR_INVESTMENT'
    }
  };
}

module.exports = {
  runInvestmentAnalysis
};
