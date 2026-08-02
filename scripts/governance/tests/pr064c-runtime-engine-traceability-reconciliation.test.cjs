const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const doc = path.join(
  root,
  "docs/99-governance/pr-064c-runtime-engine-traceability-reconciliation",
);
const traceability = path.join(
  root,
  "docs/99-governance/pr-018-full-capability-ui-governance",
  "CAPABILITY_UI_TRACEABILITY.csv",
);

const summary = JSON.parse(
  fs.readFileSync(path.join(doc, "PR064C_SUMMARY.json"), "utf8"),
);
const audit = JSON.parse(
  fs.readFileSync(
    path.join(doc, "PR064C_TRACEABILITY_RECONCILIATION_AUDIT.json"),
    "utf8",
  ),
);
const traceabilityText = fs.readFileSync(traceability, "utf8");

test("PR-064C accounts for recovered product source", () => {
  assert.equal(summary.product_source_recovery_accounted, "PASS");
  const matches =
    traceabilityText.match(
      /backend\/services\/decision_governance_core\/main\.cjs/g,
    ) || [];
  assert.ok(matches.length >= 2);
  assert.match(traceabilityText, /Ndsp Decision Governance Core/);
  assert.match(traceabilityText, /Validate Decision/);
});

test("PR-064C changes one existing capability row", () => {
  assert.equal(summary.traceability_rows_changed, 1);
  assert.equal(summary.new_capability_created, false);
  assert.equal(audit.new_capability_created, false);
});

test("PR-064C preserves evidence status", () => {
  assert.equal(summary.traceability_status_preserved, true);
  assert.equal(audit.status_preserved, true);
});

test("PR-064C makes no behavior or direction changes", () => {
  assert.equal(summary.behavior_changes, 0);
  assert.equal(summary.direction_logic_changes, 0);
  assert.equal(summary.runtime_changes, "none");
});

test("PR-064C makes no infrastructure mutations", () => {
  assert.equal(summary.systemd_changes, 0);
  assert.equal(summary.nginx_changes, 0);
  assert.equal(summary.database_changes, 0);
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
});
