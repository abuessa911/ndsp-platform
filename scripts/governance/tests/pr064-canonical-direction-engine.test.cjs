"use strict";

const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const api = require(path.join(
  root,
  "backend/services/decision_governance_core/direction/canonical-direction.cjs",
));
const doc = path.join(
  root,
  "docs/99-governance/pr-064-canonical-direction-engine-correction",
);
const summary = JSON.parse(
  fs.readFileSync(path.join(doc, "PR064_SUMMARY.json"), "utf8"),
);
const mainText = fs.readFileSync(
  path.join(root, "backend/services/decision_governance_core/main.cjs"),
  "utf8",
);

test("frozen direction semantics", () => {
  assert.equal(
    api.calculateCanonicalDirection({ long: 9, short: 4 }).direction,
    "BULLISH",
  );
  assert.equal(
    api.calculateCanonicalDirection({ long: 2, short: 8 }).direction,
    "BEARISH",
  );
  assert.equal(
    api.calculateCanonicalDirection({ long: 5, short: 5 }).direction,
    "NEUTRAL",
  );
});

test("shadow-only integration", () => {
  assert.match(mainText, /\/api\/governance\/direction\/shadow/);
  assert.match(mainText, /SHADOW_ONLY/);
  assert.equal(summary.public_exposure, "DISABLED");
  assert.equal(summary.official_result_written, false);
});

test("time and stores unchanged", () => {
  assert.equal(summary.time_logic_changes, 0);
  assert.equal(summary.official_result_store_changes, 0);
  assert.equal(summary.experimental_result_store_changes, 0);
});

test("deployment remains unauthorized", () => {
  assert.equal(summary.deployment_authorized, false);
  assert.equal(summary.runtime_changes, "none");
});
