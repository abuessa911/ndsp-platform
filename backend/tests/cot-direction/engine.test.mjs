import assert from 'node:assert/strict';
import test from 'node:test';

import {
  analyzeCotDirection,
  analyzeNamedCoalition,
} from '../../intelligence/cot-direction/index.js';

test('[+3,-1] شراء صريح ذو أفق ممتد', () => {
  const output = analyzeCotDirection([
    {
      participant: 'ASSET_MANAGERS',
      longChange: 2,
      shortChange: -2,
    },
    {
      participant: 'OTHER_REPORTABLES',
      longChange: 1,
      shortChange: 1,
    },
  ]);

  assert.deepEqual(output.state, [3, -1]);

  assert.equal(
    output.classification,
    'EXPLICIT_EXTENDED_BUY',
  );

  assert.equal(
    output.arabicLabel,
    'اتجاه شراء صريح ذو أفق ممتد',
  );

  assert.equal(
    Object.hasOwn(output, 'directionalScore'),
    false,
  );
});

test('[+3,+2] شراء غير صريح ذو أفق ضيق', () => {
  const output = analyzeCotDirection([
    {
      participant: 'ASSET_MANAGERS',
      longChange: 2,
      shortChange: 1,
    },
    {
      participant: 'OTHER_REPORTABLES',
      longChange: 1,
      shortChange: 1,
    },
  ]);

  assert.deepEqual(output.state, [3, 2]);

  assert.equal(
    output.classification,
    'NON_EXPLICIT_NARROW_BUY',
  );
});

test('[-3,+2] بيع صريح ذو أفق ممتد', () => {
  const output = analyzeCotDirection([
    {
      participant: 'ASSET_MANAGERS',
      longChange: -2,
      shortChange: 1,
    },
    {
      participant: 'OTHER_REPORTABLES',
      longChange: -1,
      shortChange: 1,
    },
  ]);

  assert.deepEqual(output.state, [-3, 2]);

  assert.equal(
    output.classification,
    'EXPLICIT_EXTENDED_SELL',
  );
});

test('تحالف مديري الأصول والآخرين', () => {
  const output = analyzeNamedCoalition(
    'ASSET_MANAGERS_OTHER',
    [
      {
        participant: 'ASSET_MANAGERS',
        longChange: 2,
        shortChange: -2,
      },
      {
        participant: 'OTHER_REPORTABLES',
        longChange: 1,
        shortChange: 1,
      },
      {
        participant: 'LEVERAGED_FUNDS',
        longChange: -10,
        shortChange: 10,
      },
    ],
  );

  assert.deepEqual(output.state, [3, -1]);
});
