"use strict";

const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const api = require(path.join(
  root,
  "backend/services/decision_governance_core/time/canonical-effective-week.cjs",
));
const summary = JSON.parse(fs.readFileSync(
  path.join(
    root,
    "docs/99-governance/pr-065-utc-effective-week-correction/PR065_SUMMARY.json",
  ),
  "utf8",
));

test("uses UTC half-open semantics", () => {
  const value = api.calculateEffectiveWeek({
    report_date_utc: "2026-08-02T03:40:19Z",
  });

  assert.equal(value.timezone, "UTC");
  assert.equal(
    value.interval_semantics,
    "[effective_from,effective_until)",
  );
});

test("keeps direction logic separate", () => {
  assert.equal(summary.direction_logic_changes, 0);
  assert.equal(summary.runtime_integration_changes, 0);
});

test("does not authorize deployment", () => {
  assert.equal(summary.deployment_authorized, false);
  assert.equal(summary.runtime_changes, "none");
});
