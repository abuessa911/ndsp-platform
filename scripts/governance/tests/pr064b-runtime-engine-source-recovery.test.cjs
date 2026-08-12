const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const engine = path.join(
  root,
  "backend/services/decision_governance_core",
);
const doc = path.join(
  root,
  "docs/99-governance/pr-064b-runtime-engine-source-recovery",
);

const summary = JSON.parse(
  fs.readFileSync(path.join(doc, "PR064B_SUMMARY.json"), "utf8"),
);
const sourceManifest = fs.readFileSync(
  path.join(doc, "PR064B_RUNTIME_SOURCE_MANIFEST.csv"),
  "utf8",
);
const recoveredManifest = fs.readFileSync(
  path.join(doc, "PR064B_RECOVERED_SOURCE_MANIFEST.csv"),
  "utf8",
);
const main = fs.readFileSync(path.join(engine, "main.cjs"), "utf8");

test("PR-064B recovers the runtime engine source", () => {
  assert.equal(summary.runtime_engine_source_found, "PASS");
  assert.ok(summary.runtime_engine_files_recovered >= 5);
  assert.equal(sourceManifest, recoveredManifest);
});

test("PR-064B preserves governance routes", () => {
  assert.match(main, /\/health/);
  assert.match(main, /\/api\/governance\/evaluate/);
  assert.match(main, /\/api\/governance\/submit/);
});

test("PR-064B records zero behavior and direction changes", () => {
  assert.equal(summary.behavior_changes, 0);
  assert.equal(summary.direction_logic_changes, 0);
  assert.equal(summary.runtime_changes, "none");
});

test("PR-064B does not modify production infrastructure", () => {
  assert.equal(summary.systemd_changes, 0);
  assert.equal(summary.nginx_changes, 0);
  assert.equal(summary.database_changes, 0);
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
});

test("PR-064B excludes runtime dependencies and data", () => {
  assert.equal(summary.node_modules_excluded, "PASS");
  assert.equal(summary.runtime_data_excluded, "PASS");
  assert.equal(summary.secrets_excluded, "PASS");
});
