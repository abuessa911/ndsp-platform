'use strict';

const TDL_DAY_LOGIC_V2 = {
  version: 'TDL_WEEKLY_DAY_LOGIC_V2',
  status: 'ACTIVE_BASELINE',
  days: {
    monday: { controller: 'ASSET_MANAGERS', mode: 'weekly_anchor' },
    tuesday: { controller: 'LEVERAGED_FUNDS', mode: 'tactical_structure' },
    wednesday: { controller: 'LEVERAGED_FUNDS', mode: 'tactical_structure' },
    thursday: { controller: 'LEVERAGED_FUNDS', mode: 'tactical_structure' },
    friday: { controller: 'ASSET_MANAGERS', mode: 'weekly_anchor' },
    saturday: { controller: 'LEVERAGED_FUNDS', mode: 'crypto_only', applies_to: ['CRYPTO'] },
    sunday: { controller: 'LEVERAGED_FUNDS', mode: 'crypto_only', applies_to: ['CRYPTO'] }
  }
};

function normalizeAssetClass(assetClass) {
  return String(assetClass || '').trim().toUpperCase();
}

function normalizeDayName(input) {
  const s = String(input || '').trim().toLowerCase();
  const map = {
    mon: 'monday', monday: 'monday', الاثنين: 'monday',
    tue: 'tuesday', tues: 'tuesday', tuesday: 'tuesday', الثلاثاء: 'tuesday',
    wed: 'wednesday', wednesday: 'wednesday', الأربعاء: 'wednesday', الاربعاء: 'wednesday',
    thu: 'thursday', thur: 'thursday', thurs: 'thursday', thursday: 'thursday', الخميس: 'thursday',
    fri: 'friday', friday: 'friday', الجمعة: 'friday',
    sat: 'saturday', saturday: 'saturday', السبت: 'saturday',
    sun: 'sunday', sunday: 'sunday', الأحد: 'sunday', الاحد: 'sunday'
  };
  return map[s] || s;
}

function getTdlDayController(dayName, assetClass) {
  const day = normalizeDayName(dayName);
  const cls = normalizeAssetClass(assetClass);
  const row = TDL_DAY_LOGIC_V2.days[day];

  if (!row) {
    return {
      ok: false,
      controller: 'UNKNOWN',
      mode: 'unknown_day',
      day,
      asset_class: cls
    };
  }

  if ((day === 'saturday' || day === 'sunday') && cls !== 'CRYPTO') {
    return {
      ok: true,
      controller: 'MARKET_CLOSED_OR_IGNORED',
      mode: 'non_crypto_weekend',
      day,
      asset_class: cls
    };
  }

  return {
    ok: true,
    controller: row.controller,
    mode: row.mode,
    day,
    asset_class: cls,
    version: TDL_DAY_LOGIC_V2.version
  };
}

module.exports = {
  TDL_DAY_LOGIC_V2,
  normalizeDayName,
  getTdlDayController
};
