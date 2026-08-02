"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");

const {
  runCoreExpandedShadow,
} = require("../execution/core-expanded-shadow-runner.cjs");

function sample(overrides = {}) {
  return {
    report_date_utc: "2026-08-02T03:40:19Z",
    core: {
      long: 10,
      short: 4,
    },
    expanded: {
      long: 8,
      short: 6,
    },
    ...overrides,
  };
}

test("runs CORE and EXPANDED against the same effective week", () => {
  const result = runCoreExpandedShadow(sample());

  assert.equal(result.official_model, "CORE_V1");
  assert.equal(result.experimental_model, "EXPANDED_SHADOW");
  assert.equal(result.execution_mode, "SHADOW_ONLY");
  assert.equal(
    result.effective_week.timezone,
    "UTC",
  );
});

test("does not write either result store", () => {
  const result = runCoreExpandedShadow(sample());

  assert.equal(result.official_result_write, false);
  assert.equal(result.experimental_result_write, false);
});

test("never exposes EXPANDED publicly", () => {
  const result = runCoreExpandedShadow(sample());

  assert.equal(result.expanded_public_exposure, false);
  assert.equal(result.automatic_promotion, false);
});

test("reports agreement without promoting EXPANDED", () => {
  const result = runCoreExpandedShadow(sample());

  assert.equal(result.comparison.agreement, true);
  assert.equal(result.comparison.core_direction, "BULLISH");
  assert.equal(result.comparison.expanded_direction, "BULLISH");
  assert.equal(result.automatic_promotion, false);
});

test("reports disagreement safely", () => {
  const result = runCoreExpandedShadow(sample({
    expanded: {
      long: 2,
      short: 9,
    },
  }));

  assert.equal(result.comparison.agreement, false);
  assert.equal(result.comparison.core_direction, "BULLISH");
  assert.equal(result.comparison.expanded_direction, "BEARISH");
  assert.equal(result.official_result_write, false);
});

test("rejects missing explicit perspectives", () => {
  assert.throws(
    () => runCoreExpandedShadow({
      report_date_utc: "2026-08-02T03:40:19Z",
      core: {
        long: 10,
        short: 4,
      },
    }),
    { code: "INVALID_SHADOW_EXECUTION_INPUT" },
  );
});
