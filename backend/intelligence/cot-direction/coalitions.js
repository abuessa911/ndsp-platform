import { analyzeCotDirection } from './engine.js';

export const COALITIONS = Object.freeze({
  ASSET_MANAGERS_OTHER: Object.freeze([
    'ASSET_MANAGERS',
    'OTHER_REPORTABLES',
  ]),

  LEVERAGED_FUNDS_OTHER: Object.freeze([
    'LEVERAGED_FUNDS',
    'OTHER_REPORTABLES',
  ]),
});

function normalizeName(value) {
  return value
    .trim()
    .toUpperCase()
    .replaceAll('-', '_')
    .replaceAll(' ', '_');
}

export function analyzeNamedCoalition(
  coalitionKey,
  participants,
) {
  const members = COALITIONS[coalitionKey];

  if (!members) {
    throw new Error(`تحالف غير معروف: ${coalitionKey}`);
  }

  const map = new Map(
    participants.map((row) => [
      normalizeName(row.participant),
      row,
    ]),
  );

  const selected = members.map((member) => {
    const row = map.get(member);

    if (!row) {
      throw new Error(
        `الفئة ${member} مطلوبة للتحالف ${coalitionKey}.`,
      );
    }

    return row;
  });

  return Object.freeze({
    coalitionKey,
    coalitionMembers: members,
    ...analyzeCotDirection(selected),
  });
}

export function compareCanonicalCoalitions(participants) {
  const assetManagersOther = analyzeNamedCoalition(
    'ASSET_MANAGERS_OTHER',
    participants,
  );

  const leveragedFundsOther = analyzeNamedCoalition(
    'LEVERAGED_FUNDS_OTHER',
    participants,
  );

  return Object.freeze({
    assetManagersOther,
    leveragedFundsOther,

    comparison: Object.freeze({
      sameDirection:
        assetManagersOther.direction ===
        leveragedFundsOther.direction,

      sameClarity:
        assetManagersOther.clarity ===
        leveragedFundsOther.clarity,

      sameHorizon:
        assetManagersOther.horizon ===
        leveragedFundsOther.horizon,
    }),
  });
}
