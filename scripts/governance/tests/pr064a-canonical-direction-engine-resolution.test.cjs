const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const base = path.join(
  root,
  "docs/99-governance/pr-064a-canonical-direction-engine-resolution",
);

const summary = JSON.parse(
  fs.readFileSync(path.join(base, "PR064A_SUMMARY.json"), "utf8"),
);
const target = JSON.parse(
  fs.readFileSync(
    path.join(base, "PR064A_CANONICAL_TARGET.json"),
    "utf8",
  ),
);
const tdl = JSON.parse(
  fs.readFileSync(path.join(base, "PR064A_TDL_DECISIONS.json"), "utf8"),
);

test("PR-064A is governance-only", () => {
  assert.equal(summary.product_code_changes, 0);
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
  assert.equal(summary.runtime_changes, "none");
});

test("PR-064A does not authorize implementation", () => {
  assert.equal(summary.implementation_authorized, false);
  assert.equal(summary.human_approval_required, true);
  assert.equal(summary.unresolved_rules_resolved, false);
  assert.equal(target.creation_allowed_before_approval, false);
});

test("PR-064A preserves CORE and EXPANDED isolation", () => {
  assert.equal(summary.core_expanded_isolation, "PASS");
  assert.equal(target.public_result_model, "CORE");
  assert.equal(target.expanded_mode, "SHADOW_MODE");
  assert.equal(target.expanded_public_exposure, false);
});

test("PR-064A disables investment TDL and Day Control", () => {
  assert.equal(tdl.investment.day_control, "DISABLED");
  assert.equal(tdl.investment.tdl_ml, "DISABLED");
  assert.equal(tdl.investment.tdl_s, "DISABLED");
});

test("PR-064A does not invent speculation TDL semantics", () => {
  assert.match(tdl.speculation.tdl_ml, /DISABLED_UNTIL/);
  assert.match(tdl.speculation.tdl_s, /DISABLED_UNTIL/);
  assert.equal(tdl.speculation.invented_semantics_allowed, false);
});
