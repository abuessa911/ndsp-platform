"use strict";

const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");
const { calculateCanonicalDirection } = require(
  "../direction/canonical-direction.cjs",
);

const root = path.resolve(__dirname, "..", "..", "..", "..");
const cases = JSON.parse(
  fs.readFileSync(
    path.join(
      root,
      "docs/99-governance/pr-064-canonical-direction-engine-correction",
      "PR064_NORMALIZED_REGRESSION_CASES.json",
    ),
    "utf8",
  ),
).cases;

for (const fixture of cases) {
  test(`canonical direction ${fixture.id}`, () => {
    const actual = calculateCanonicalDirection({
      long: fixture.long,
      short: fixture.short,
    });
    assert.equal(actual.delta, fixture.expected_delta);
    assert.equal(actual.direction, fixture.expected_direction);
    assert.equal(actual.neutral, fixture.long === fixture.short);
  });
}

test("rejects string coercion", () => {
  assert.throws(
    () => calculateCanonicalDirection({ long: "10", short: 1 }),
    { code: "INVALID_DIRECTION_INPUT" },
  );
});
