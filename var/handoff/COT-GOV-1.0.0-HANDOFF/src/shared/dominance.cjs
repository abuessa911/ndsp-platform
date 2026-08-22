'use strict';

const DIRECTION = Object.freeze({
  BULLISH: 'BULLISH',
  BEARISH: 'BEARISH',
  NEUTRAL: 'NEUTRAL'
});

const EXPLICITNESS = Object.freeze({
  EXPLICIT: 'EXPLICIT',
  NON_EXPLICIT: 'NON_EXPLICIT',
  NOT_APPLICABLE: 'NOT_APPLICABLE'
});

const HORIZON = Object.freeze({
  EXTENDED: 'EXTENDED',
  NARROW: 'NARROW',
  NONE: 'NONE'
});

function assertFiniteNumber(value, fieldName) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new TypeError(`${fieldName} must be a finite number`);
  }
}

function classifyPair(longValue, shortValue) {
  assertFiniteNumber(longValue, 'longValue');
  assertFiniteNumber(shortValue, 'shortValue');

  const dominanceDelta = longValue - shortValue;

  let direction;
  if (longValue > shortValue) {
    direction = DIRECTION.BULLISH;
  } else if (shortValue > longValue) {
    direction = DIRECTION.BEARISH;
  } else {
    direction = DIRECTION.NEUTRAL;
  }

  if (direction === DIRECTION.NEUTRAL) {
    return {
      longValue,
      shortValue,
      dominanceDelta,
      direction,
      explicitness: EXPLICITNESS.NOT_APPLICABLE,
      horizon: HORIZON.NONE,
      labelAr: 'محايد',
      labelEn: 'Neutral'
    };
  }

  const oppositeSigns =
    (longValue > 0 && shortValue < 0) ||
    (longValue < 0 && shortValue > 0);

  const explicitness = oppositeSigns
    ? EXPLICITNESS.EXPLICIT
    : EXPLICITNESS.NON_EXPLICIT;

  const horizon = oppositeSigns
    ? HORIZON.EXTENDED
    : HORIZON.NARROW;

  return {
    longValue,
    shortValue,
    dominanceDelta,
    direction,
    explicitness,
    horizon,
    labelAr: formatArabic(direction, explicitness, horizon),
    labelEn: formatEnglish(direction, explicitness, horizon)
  };
}

function aggregateCategories(dataset, categories) {
  if (!dataset || typeof dataset !== 'object') {
    throw new TypeError('dataset must be an object');
  }

  if (!Array.isArray(categories) || categories.length === 0) {
    throw new TypeError('categories must be a non-empty array');
  }

  return categories.reduce(
    (total, category) => {
      const row = dataset[category];

      if (!row) {
        throw new Error(`Missing COT category: ${category}`);
      }

      assertFiniteNumber(row.long, `${category}.long`);
      assertFiniteNumber(row.short, `${category}.short`);

      total.long += row.long;
      total.short += row.short;
      return total;
    },
    { long: 0, short: 0 }
  );
}

function analyzeCategories(dataset, categories) {
  const aggregate = aggregateCategories(dataset, categories);
  return {
    categories: [...categories],
    ...classifyPair(aggregate.long, aggregate.short)
  };
}

function formatArabic(direction, explicitness, horizon) {
  const directionLabel =
    direction === DIRECTION.BULLISH ? 'صاعد' : 'هابط';

  const explicitnessLabel =
    explicitness === EXPLICITNESS.EXPLICIT ? 'صريح' : 'غير صريح';

  const horizonLabel =
    horizon === HORIZON.EXTENDED ? 'ذو أفق ممتد' : 'ذو أفق ضيق';

  return `${directionLabel} ${explicitnessLabel} — ${horizonLabel}`;
}

function formatEnglish(direction, explicitness, horizon) {
  const directionLabel =
    direction === DIRECTION.BULLISH ? 'Bullish' : 'Bearish';

  const explicitnessLabel =
    explicitness === EXPLICITNESS.EXPLICIT
      ? 'explicit'
      : 'non-explicit';

  const horizonLabel =
    horizon === HORIZON.EXTENDED
      ? 'extended horizon'
      : 'narrow horizon';

  return `${directionLabel} ${explicitnessLabel} — ${horizonLabel}`;
}

module.exports = {
  DIRECTION,
  EXPLICITNESS,
  HORIZON,
  classifyPair,
  aggregateCategories,
  analyzeCategories
};
