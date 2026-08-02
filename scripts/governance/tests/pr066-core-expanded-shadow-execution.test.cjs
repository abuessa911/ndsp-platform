"use strict";

const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(
  __dirname,
  "..",
  "..",
  "..",
);

const runner = require(path.join(
  root,
  "backend/services/decision_governance_core",
  "execution/core-expanded-shadow-runner.cjs",
));

const summary = JSON.parse(
  fs.readFileSync(
    path.join(
      root,
      "docs/99-governance",
      "pr-066-core-expanded-shadow-execution",
      "PR066_SUMMARY.json",
    ),
    "utf8",
  ),
);

test("CORE remains the declared official model", () => {
  assert.equal(summary.official_model, "CORE_V1");
  assert.equal(summary.official_result_write, false);
});

test("EXPANDED remains internal and shadow-only", () => {
  assert.equal(
    summary.experimental_model,
    "EXPANDED_SHADOW",
  );
  assert.equal(
    summary.expanded_public_exposure,
    false,
  );
  assert.equal(summary.automatic_promotion, false);
});

test("runner uses canonical direction and UTC week", () => {
  const value = runner.runCoreExpandedShadow({
    report_date_utc: "2026-08-02T03:40:19Z",
    core: {
      long: 10,
      short: 4,
    },
    expanded: {
      long: 2,
      short: 9,
    },
  });

  assert.equal(
    value.core.direction.direction,
    "BULLISH",
  );
  assert.equal(
    value.expanded.direction.direction,
    "BEARISH",
  );
  assert.equal(
    value.effective_week.timezone,
    "UTC",
  );
});

test("PR-066 does not alter runtime infrastructure", () => {
  assert.equal(summary.runtime_route_changes, 0);
  assert.equal(summary.database_changes, 0);
  assert.equal(summary.systemd_changes, 0);
  assert.equal(summary.nginx_changes, 0);
  assert.equal(summary.runtime_changes, "none");
});
