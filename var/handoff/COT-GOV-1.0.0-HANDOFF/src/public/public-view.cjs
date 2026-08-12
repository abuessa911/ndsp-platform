'use strict';

function toPublicResult(governedResult) {
  if (!governedResult || !governedResult.official) {
    throw new TypeError('governedResult.official is required');
  }

  const official = governedResult.official;

  return {
    governanceVersion: official.governanceVersion,
    analysisMode: official.analysisMode,
    perspective: 'CORE',
    resultType: 'OFFICIAL',
    controller: official.controller,
    dayName: official.dayName,
    dayControlPerspective: official.dayControlPerspective,
    effectiveWindow: official.effectiveWindow,
    directionResult: official.directionResult,
    weeklySupport: official.weeklySupport,
    timing:
      official.analysisMode === 'INVESTMENT'
        ? {
            enabled: false,
            status: 'DISABLED_FOR_INVESTMENT'
          }
        : official.timing
  };
}

module.exports = {
  toPublicResult
};
