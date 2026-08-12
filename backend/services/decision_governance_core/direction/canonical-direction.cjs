"use strict";

const DIRECTION = Object.freeze({
  BULLISH: "BULLISH",
  BEARISH: "BEARISH",
  NEUTRAL: "NEUTRAL",
});

function finite(value, field) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    const error = new TypeError(`${field} must be a finite number`);
    error.code = "INVALID_DIRECTION_INPUT";
    throw error;
  }
  return value;
}

function calculateCanonicalDirection(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    const error = new TypeError("input must be an object");
    error.code = "INVALID_DIRECTION_INPUT";
    throw error;
  }

  const long = finite(input.long, "long");
  const short = finite(input.short, "short");
  const delta = long - short;

  return Object.freeze({
    contract_version: "1.0.0",
    model: "CORE_V1",
    direction:
      delta > 0 ? DIRECTION.BULLISH :
      delta < 0 ? DIRECTION.BEARISH :
      DIRECTION.NEUTRAL,
    delta,
    long,
    short,
    neutral: long === short,
    rule: "delta = long - short",
    neutral_rule: "long == short only",
  });
}

module.exports = Object.freeze({
  DIRECTION,
  calculateCanonicalDirection,
});
