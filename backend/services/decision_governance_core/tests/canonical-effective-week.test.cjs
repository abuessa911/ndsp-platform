"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const {
  calculateEffectiveWeek,
  isWithinEffectiveWeek,
} = require("../time/canonical-effective-week.cjs");

test("calculates Monday UTC boundaries", () => {
  const result = calculateEffectiveWeek({
    report_date_utc: "2026-08-02T03:40:19Z",
  });

  assert.equal(result.timezone, "UTC");
  assert.equal(result.effective_from, "2026-07-27T00:00:00.000Z");
  assert.equal(result.effective_until, "2026-08-03T00:00:00.000Z");
  assert.equal(
    result.interval_semantics,
    "[effective_from,effective_until)",
  );
});

test("effective_from is inclusive", () => {
  assert.equal(isWithinEffectiveWeek({
    instant_utc: "2026-07-27T00:00:00.000Z",
    effective_from: "2026-07-27T00:00:00.000Z",
    effective_until: "2026-08-03T00:00:00.000Z",
  }), true);
});

test("effective_until is exclusive", () => {
  assert.equal(isWithinEffectiveWeek({
    instant_utc: "2026-08-03T00:00:00.000Z",
    effective_from: "2026-07-27T00:00:00.000Z",
    effective_until: "2026-08-03T00:00:00.000Z",
  }), false);
});

test("rejects non-Z timestamps", () => {
  assert.throws(
    () => calculateEffectiveWeek({
      report_date_utc: "2026-08-02T03:40:19+02:00",
    }),
    { code: "INVALID_UTC_TIMESTAMP" },
  );
});
