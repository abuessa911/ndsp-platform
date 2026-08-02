"use strict";

const {
  calculateCanonicalDirection,
} = require("../direction/canonical-direction.cjs");

const {
  calculateEffectiveWeek,
} = require("../time/canonical-effective-week.cjs");

function requireObject(value, field) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    const error = new TypeError(`${field} must be an object`);
    error.code = "INVALID_SHADOW_EXECUTION_INPUT";
    throw error;
  }

  return value;
}

function runPerspective(model, perspective) {
  const input = requireObject(perspective, model);

  const direction = calculateCanonicalDirection({
    long: input.long,
    short: input.short,
  });

  return Object.freeze({
    model,
    direction,
  });
}

function compareDirections(core, expanded) {
  return Object.freeze({
    agreement: core.direction.direction === expanded.direction.direction,
    core_direction: core.direction.direction,
    expanded_direction: expanded.direction.direction,
    delta_difference:
      expanded.direction.delta - core.direction.delta,
  });
}

function runCoreExpandedShadow(input) {
  const payload = requireObject(input, "input");

  const effectiveWeek = calculateEffectiveWeek({
    report_date_utc: payload.report_date_utc,
  });

  const core = runPerspective("CORE_V1", payload.core);
  const expanded = runPerspective(
    "EXPANDED_SHADOW",
    payload.expanded,
  );

  return Object.freeze({
    contract_version: "1.0.0",
    execution_mode: "SHADOW_ONLY",
    official_model: "CORE_V1",
    official_result_write: false,
    experimental_model: "EXPANDED_SHADOW",
    experimental_result_write: false,
    expanded_public_exposure: false,
    automatic_promotion: false,
    effective_week: effectiveWeek,
    core,
    expanded,
    comparison: compareDirections(core, expanded),
  });
}

module.exports = Object.freeze({
  runCoreExpandedShadow,
});
