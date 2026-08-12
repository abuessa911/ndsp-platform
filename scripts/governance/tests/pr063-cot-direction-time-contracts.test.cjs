const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const base = path.join(
  root,
  "docs/99-governance/pr-063-cot-direction-time-contracts",
);

const summary = JSON.parse(
  fs.readFileSync(path.join(base, "PR063_SUMMARY.json"), "utf8"),
);
const fixtures = JSON.parse(
  fs.readFileSync(
    path.join(base, "fixtures/regression-fixtures.json"),
    "utf8",
  ),
);

test("PR-063 freezes the approved direction rule", () => {
  assert.equal(summary.approved_direction_rule, "delta = long - short");
  assert.equal(summary.approved_neutral_rule, "long == short only");
});

test("PR-063 freezes UTC effective-week semantics", () => {
  assert.equal(summary.approved_timezone, "UTC");
  assert.equal(
    summary.approved_interval_semantics,
    "[effective_from,effective_until)",
  );
});

test("PR-063 preserves CORE and EXPANDED isolation", () => {
  assert.equal(summary.core_public_only, true);
  assert.equal(summary.expanded_shadow_only, true);
});

test("PR-063 contains bounded regression fixtures", () => {
  assert.equal(fixtures.length, 5);
  assert.ok(fixtures.some((item) => item.long === item.short));
  assert.ok(fixtures.some((item) => item.report_date.startsWith("2028-02")));
});

test("PR-063 makes no runtime changes", () => {
  assert.equal(summary.product_code_changes, 0);
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
  assert.equal(summary.runtime_changes, "none");
});
