const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const auditDir = path.join(
  root,
  "docs/99-governance/pr-062-cot-direction-time-backend-audit",
);

const summary = JSON.parse(
  fs.readFileSync(path.join(auditDir, "PR062_SUMMARY.json"), "utf8"),
);
const inventory = JSON.parse(
  fs.readFileSync(
    path.join(auditDir, "PR062_LOGIC_INVENTORY.json"),
    "utf8",
  ),
);
const impact = JSON.parse(
  fs.readFileSync(
    path.join(auditDir, "PR062_CODE_IMPACT_MAP.json"),
    "utf8",
  ),
);

test("PR-062 performs a read-only backend audit", () => {
  assert.equal(summary.scan_mode, "READ_ONLY");
  assert.equal(summary.product_code_changes, 0);
  assert.equal(summary.traceability_rows_modified, 0);
  assert.equal(summary.production_services_restarted, 0);
  assert.equal(summary.mutating_requests_executed, 0);
  assert.equal(summary.runtime_changes, "none");
});

test("PR-062 inventory and impact accounting are exact", () => {
  assert.ok(summary.candidate_files_scanned > 0);
  assert.ok(summary.logic_candidate_file_count > 0);
  assert.equal(summary.logic_candidate_file_count, inventory.length);
  assert.equal(summary.impact_map_record_count, impact.length);

  const riskTotal =
    summary.critical_risk_count +
    summary.high_risk_count +
    summary.medium_risk_count +
    summary.low_risk_count;

  assert.equal(riskTotal, impact.length);
});

test("PR-062 preserves the approved direction and timing baseline", () => {
  assert.equal(
    summary.approved_direction_rule,
    "delta = long - short",
  );
  assert.match(summary.approved_investment_rule, /Positions/);
  assert.match(summary.approved_investment_rule, /Changes/);
  assert.match(summary.approved_speculation_rule, /Changes only/);
  assert.match(summary.approved_time_rule, /UTC only/);
  assert.equal(summary.approved_public_rule, "CORE only");
  assert.match(summary.approved_shadow_rule, /SHADOW_MODE/);
});

test("PR-062 requires human review before correction", () => {
  assert.equal(summary.human_review_required, true);
  assert.ok(summary.unresolved_item_count >= 4);
  assert.equal(
    summary.status,
    "COT_DIRECTION_TIME_BACKEND_AUDIT_COMPLETE",
  );
});
