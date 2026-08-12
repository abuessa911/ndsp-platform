'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const {
  classifyPair
} = require('../src/shared/dominance.cjs');

test('one-contract long advantage is bullish', () => {
  const result = classifyPair(101, 100);
  assert.equal(result.direction, 'BULLISH');
  assert.equal(result.dominanceDelta, 1);
});

test('one-contract short advantage is bearish', () => {
  const result = classifyPair(100, 101);
  assert.equal(result.direction, 'BEARISH');
  assert.equal(result.dominanceDelta, -1);
});

test('exact equality is neutral', () => {
  const result = classifyPair(100, 100);
  assert.equal(result.direction, 'NEUTRAL');
  assert.equal(result.horizon, 'NONE');
});

test('opposite signs are explicit and extended', () => {
  const result = classifyPair(332, -6);
  assert.equal(result.direction, 'BULLISH');
  assert.equal(result.explicitness, 'EXPLICIT');
  assert.equal(result.horizon, 'EXTENDED');
});

test('same-sign values are non-explicit and narrow', () => {
  const result = classifyPair(-95, -7);
  assert.equal(result.direction, 'BEARISH');
  assert.equal(result.explicitness, 'NON_EXPLICIT');
  assert.equal(result.horizon, 'NARROW');
});
