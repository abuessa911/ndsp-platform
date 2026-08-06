import {
  CLASSIFICATIONS,
  CLARITIES,
  CONTRACT_VERSION,
  DIRECTIONS,
  HORIZONS,
} from './contract.js';

import { validateParticipants } from './validator.js';

const EPSILON = 1e-9;

function isZero(value) {
  return Math.abs(value) <= EPSILON;
}

function equal(a, b) {
  return Math.abs(a - b) <= EPSILON;
}

function signed(value) {
  return value > 0 ? `+${value}` : `${value}`;
}

function result({
  participants,
  longTotal,
  shortTotal,
  direction,
  clarity,
  horizon,
  classification,
  arabicLabel,
  explanation,
  movementSource,
}) {
  return Object.freeze({
    contractVersion: CONTRACT_VERSION,

    // الحالة الأساسية. لا تختزل إلى L-S.
    state: Object.freeze([longTotal, shortTotal]),

    longTotal,
    shortTotal,
    direction,
    clarity,
    horizon,
    classification,
    arabicLabel,
    explanation,
    movementSource: Object.freeze(movementSource),
    participants,
    generatedAt: new Date().toISOString(),
  });
}

export function analyzeCotDirection(rawParticipants) {
  const participants = validateParticipants(rawParticipants);

  const longTotal = participants.reduce(
    (sum, row) => sum + row.longChange,
    0,
  );

  const shortTotal = participants.reduce(
    (sum, row) => sum + row.shortChange,
    0,
  );

  /*
   * شراء صريح ذو أفق ممتد:
   *
   * L > 0
   * S < 0
   *
   * مثال:
   * L = (+2) + (+1) = +3
   * S = (-2) + (+1) = -1
   *
   * [L,S] = [+3,-1]
   */

  if (longTotal > 0 && shortTotal < 0) {
    return result({
      participants,
      longTotal,
      shortTotal,
      direction: DIRECTIONS.BUY,
      clarity: CLARITIES.EXPLICIT,
      horizon: HORIZONS.EXTENDED,
      classification: CLASSIFICATIONS.EXPLICIT_EXTENDED_BUY,
      arabicLabel: 'اتجاه شراء صريح ذو أفق ممتد',
      explanation:
        `زاد اللونق بمحصلة ${signed(longTotal)}، ` +
        `بينما انخفض الشورت بمحصلة ${signed(shortTotal)}. ` +
        'التحالف يبني عقود شراء ويخفض عقود البيع.',
      movementSource: [
        'LONG_BUILDING',
        'SHORT_REDUCTION',
      ],
    });
  }

  if (longTotal < 0 && shortTotal > 0) {
    return result({
      participants,
      longTotal,
      shortTotal,
      direction: DIRECTIONS.SELL,
      clarity: CLARITIES.EXPLICIT,
      horizon: HORIZONS.EXTENDED,
      classification: CLASSIFICATIONS.EXPLICIT_EXTENDED_SELL,
      arabicLabel: 'اتجاه بيع صريح ذو أفق ممتد',
      explanation:
        `انخفض اللونق بمحصلة ${signed(longTotal)}، ` +
        `بينما زاد الشورت بمحصلة ${signed(shortTotal)}.`,
      movementSource: [
        'LONG_REDUCTION',
        'SHORT_BUILDING',
      ],
    });
  }

  if (longTotal > 0 && shortTotal > 0) {
    if (equal(longTotal, shortTotal)) {
      return result({
        participants,
        longTotal,
        shortTotal,
        direction: DIRECTIONS.NEUTRAL,
        clarity: CLARITIES.NON_EXPLICIT,
        horizon: HORIZONS.NARROW,
        classification: CLASSIFICATIONS.EXPANSION_BALANCE,
        arabicLabel: 'تعادل توسعي',
        explanation:
          'زاد اللونق والشورت بالمقدار نفسه.',
        movementSource: [
          'LONG_BUILDING',
          'SHORT_BUILDING',
        ],
      });
    }

    if (longTotal > shortTotal) {
      return result({
        participants,
        longTotal,
        shortTotal,
        direction: DIRECTIONS.BUY,
        clarity: CLARITIES.NON_EXPLICIT,
        horizon: HORIZONS.NARROW,
        classification:
          CLASSIFICATIONS.NON_EXPLICIT_NARROW_BUY,
        arabicLabel: 'اتجاه شراء غير صريح ذو أفق ضيق',
        explanation:
          `زاد اللونق ${signed(longTotal)} وزاد الشورت ` +
          `${signed(shortTotal)}، لكن اللونق كان أكبر.`,
        movementSource: [
          'LONG_BUILDING',
          'SHORT_BUILDING',
          'LONG_DOMINANCE',
        ],
      });
    }

    return result({
      participants,
      longTotal,
      shortTotal,
      direction: DIRECTIONS.SELL,
      clarity: CLARITIES.NON_EXPLICIT,
      horizon: HORIZONS.NARROW,
      classification:
        CLASSIFICATIONS.NON_EXPLICIT_NARROW_SELL,
      arabicLabel: 'اتجاه بيع غير صريح ذو أفق ضيق',
      explanation:
        `زاد اللونق ${signed(longTotal)} وزاد الشورت ` +
        `${signed(shortTotal)}، لكن الشورت كان أكبر.`,
      movementSource: [
        'LONG_BUILDING',
        'SHORT_BUILDING',
        'SHORT_DOMINANCE',
      ],
    });
  }

  if (longTotal < 0 && shortTotal < 0) {
    const longMagnitude = Math.abs(longTotal);
    const shortMagnitude = Math.abs(shortTotal);

    if (equal(longMagnitude, shortMagnitude)) {
      return result({
        participants,
        longTotal,
        shortTotal,
        direction: DIRECTIONS.NEUTRAL,
        clarity: CLARITIES.TRANSITIONAL,
        horizon: HORIZONS.NARROW,
        classification:
          CLASSIFICATIONS.CONTRACTION_BALANCE,
        arabicLabel: 'تعادل انكماشي',
        explanation:
          'انخفض اللونق والشورت بالمقدار نفسه.',
        movementSource: [
          'LONG_REDUCTION',
          'SHORT_REDUCTION',
        ],
      });
    }

    if (shortMagnitude > longMagnitude) {
      return result({
        participants,
        longTotal,
        shortTotal,
        direction: DIRECTIONS.BUY,
        clarity: CLARITIES.TRANSITIONAL,
        horizon: HORIZONS.NARROW,
        classification:
          CLASSIFICATIONS.SHORT_COVERING_BUY,
        arabicLabel: 'ميل شراء ناتج عن تغطية الشورت',
        explanation:
          `انخفض اللونق ${signed(longTotal)}، لكن انخفاض ` +
          `الشورت ${signed(shortTotal)} كان أكبر.`,
        movementSource: [
          'LONG_REDUCTION',
          'SHORT_REDUCTION',
          'SHORT_COVERING_DOMINANCE',
        ],
      });
    }

    return result({
      participants,
      longTotal,
      shortTotal,
      direction: DIRECTIONS.SELL,
      clarity: CLARITIES.TRANSITIONAL,
      horizon: HORIZONS.NARROW,
      classification:
        CLASSIFICATIONS.LONG_LIQUIDATION_SELL,
      arabicLabel: 'ميل بيع ناتج عن تصفية اللونق',
      explanation:
        `انخفض اللونق ${signed(longTotal)} بصورة أكبر من ` +
        `انخفاض الشورت ${signed(shortTotal)}.`,
      movementSource: [
        'LONG_REDUCTION',
        'SHORT_REDUCTION',
        'LONG_LIQUIDATION_DOMINANCE',
      ],
    });
  }

  if (longTotal > 0 && isZero(shortTotal)) {
    return result({
      participants,
      longTotal,
      shortTotal: 0,
      direction: DIRECTIONS.BUY,
      clarity: CLARITIES.NON_EXPLICIT,
      horizon: HORIZONS.NARROW,
      classification: CLASSIFICATIONS.DIRECT_BUY,
      arabicLabel: 'شراء مباشر دون تغير في الشورت',
      explanation:
        `زاد اللونق ${signed(longTotal)} ولم يتغير الشورت.`,
      movementSource: ['LONG_BUILDING'],
    });
  }

  if (isZero(longTotal) && shortTotal < 0) {
    return result({
      participants,
      longTotal: 0,
      shortTotal,
      direction: DIRECTIONS.BUY,
      clarity: CLARITIES.TRANSITIONAL,
      horizon: HORIZONS.NARROW,
      classification:
        CLASSIFICATIONS.SHORT_COVERING_ONLY,
      arabicLabel: 'شراء ناتج عن تغطية الشورت فقط',
      explanation:
        `لم يتغير اللونق وانخفض الشورت ${signed(shortTotal)}.`,
      movementSource: ['SHORT_REDUCTION'],
    });
  }

  if (longTotal < 0 && isZero(shortTotal)) {
    return result({
      participants,
      longTotal,
      shortTotal: 0,
      direction: DIRECTIONS.SELL,
      clarity: CLARITIES.TRANSITIONAL,
      horizon: HORIZONS.NARROW,
      classification:
        CLASSIFICATIONS.LONG_LIQUIDATION_ONLY,
      arabicLabel: 'بيع ناتج عن تصفية اللونق فقط',
      explanation:
        `انخفض اللونق ${signed(longTotal)} ولم يتغير الشورت.`,
      movementSource: ['LONG_REDUCTION'],
    });
  }

  if (isZero(longTotal) && shortTotal > 0) {
    return result({
      participants,
      longTotal: 0,
      shortTotal,
      direction: DIRECTIONS.SELL,
      clarity: CLARITIES.NON_EXPLICIT,
      horizon: HORIZONS.NARROW,
      classification: CLASSIFICATIONS.DIRECT_SELL,
      arabicLabel: 'بيع مباشر دون تغير في اللونق',
      explanation:
        `لم يتغير اللونق وزاد الشورت ${signed(shortTotal)}.`,
      movementSource: ['SHORT_BUILDING'],
    });
  }

  return result({
    participants,
    longTotal: 0,
    shortTotal: 0,
    direction: DIRECTIONS.NEUTRAL,
    clarity: CLARITIES.NEUTRAL,
    horizon: HORIZONS.NEUTRAL,
    classification: CLASSIFICATIONS.FULL_NEUTRAL,
    arabicLabel: 'حياد كامل',
    explanation:
      'لم يحدث تغير صافٍ في اللونق أو الشورت.',
    movementSource: [],
  });
}
