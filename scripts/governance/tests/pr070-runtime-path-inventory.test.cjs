const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..", "..", "..");
const base = path.join(
  root,
  "docs/99-governance/pr-070-runtime-path-inventory",
);

const summary = JSON.parse(
  fs.readFileSync(path.join(base, "PR070_SUMMARY.json"), "utf8"),
);

test("PR-070 is read-only", () => {
  assert.equal(summary.scan_mode, "READ_ONLY");
  assert.equal(summary.systemd_mutations, 0);
  assert.equal(summary.nginx_mutations, 0);
  assert.equal(summary.files_deleted, 0);
  assert.equal(summary.files_moved, 0);
  assert.equal(summary.runtime_changes, "none");
});

test("PR-070 inventories required roots", () => {
  assert.deepEqual(summary.filesystem_roots, ["/opt", "/var/www"]);
});

test("PR-070 requires human review before migration", () => {
  assert.equal(summary.human_review_required, true);
  assert.equal(summary.status, "RUNTIME_PATH_INVENTORY_COMPLETE");
});
