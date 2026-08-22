'use strict';

const DAY_MS = 24 * 60 * 60 * 1000;

function parseDateOnlyUtc(dateOnly) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(dateOnly)) {
    throw new TypeError('reportDate must use YYYY-MM-DD');
  }

  const date = new Date(`${dateOnly}T00:00:00.000Z`);

  if (Number.isNaN(date.getTime())) {
    throw new TypeError('Invalid reportDate');
  }

  return date;
}

function nextMondayUtc(reportDate) {
  const date = parseDateOnlyUtc(reportDate);
  const utcDay = date.getUTCDay();
  let daysUntilMonday = (8 - utcDay) % 7;

  if (daysUntilMonday === 0) {
    daysUntilMonday = 7;
  }

  return new Date(date.getTime() + daysUntilMonday * DAY_MS);
}

function getEffectiveWindow(reportDate) {
  const effectiveFrom = nextMondayUtc(reportDate);
  const effectiveUntil = new Date(effectiveFrom.getTime() + 7 * DAY_MS);

  return {
    canonicalTimezone: 'UTC',
    intervalType: 'HALF_OPEN',
    effectiveFrom: effectiveFrom.toISOString(),
    effectiveUntil: effectiveUntil.toISOString()
  };
}

function isWithinEffectiveWindow(timestamp, window) {
  const value = new Date(timestamp).getTime();
  const from = new Date(window.effectiveFrom).getTime();
  const until = new Date(window.effectiveUntil).getTime();

  if ([value, from, until].some(Number.isNaN)) {
    throw new TypeError('Invalid timestamp or effective window');
  }

  return value >= from && value < until;
}

module.exports = {
  parseDateOnlyUtc,
  nextMondayUtc,
  getEffectiveWindow,
  isWithinEffectiveWindow
};
