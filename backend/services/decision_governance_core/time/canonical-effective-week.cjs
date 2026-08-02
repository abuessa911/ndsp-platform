"use strict";

const DAY_MS = 24 * 60 * 60 * 1000;
const WEEK_MS = 7 * DAY_MS;

function parseUtc(value, field) {
  if (typeof value !== "string" || !value.endsWith("Z")) {
    const error = new TypeError(`${field} must end with Z`);
    error.code = "INVALID_UTC_TIMESTAMP";
    throw error;
  }

  const timestamp = Date.parse(value);
  if (!Number.isFinite(timestamp)) {
    const error = new TypeError(`${field} must be valid ISO-8601 UTC`);
    error.code = "INVALID_UTC_TIMESTAMP";
    throw error;
  }

  return timestamp;
}

function startOfUtcMonday(timestamp) {
  const date = new Date(timestamp);
  const dayStart = Date.UTC(
    date.getUTCFullYear(),
    date.getUTCMonth(),
    date.getUTCDate(),
  );
  const daysSinceMonday = (new Date(dayStart).getUTCDay() + 6) % 7;
  return dayStart - (daysSinceMonday * DAY_MS);
}

function calculateEffectiveWeek(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    const error = new TypeError("input must be an object");
    error.code = "INVALID_EFFECTIVE_WEEK_INPUT";
    throw error;
  }

  const reportTimestamp = parseUtc(
    input.report_date_utc,
    "report_date_utc",
  );
  const effectiveFrom = startOfUtcMonday(reportTimestamp);
  const effectiveUntil = effectiveFrom + WEEK_MS;

  return Object.freeze({
    contract_version: "1.0.0",
    timezone: "UTC",
    interval_semantics: "[effective_from,effective_until)",
    report_date_utc: new Date(reportTimestamp).toISOString(),
    effective_from: new Date(effectiveFrom).toISOString(),
    effective_until: new Date(effectiveUntil).toISOString(),
  });
}

function isWithinEffectiveWeek(input) {
  const instant = parseUtc(input.instant_utc, "instant_utc");
  const effectiveFrom = parseUtc(
    input.effective_from,
    "effective_from",
  );
  const effectiveUntil = parseUtc(
    input.effective_until,
    "effective_until",
  );

  if (effectiveUntil <= effectiveFrom) {
    const error = new RangeError(
      "effective_until must be greater than effective_from",
    );
    error.code = "INVALID_EFFECTIVE_WEEK_INTERVAL";
    throw error;
  }

  return instant >= effectiveFrom && instant < effectiveUntil;
}

module.exports = Object.freeze({
  calculateEffectiveWeek,
  isWithinEffectiveWeek,
});
