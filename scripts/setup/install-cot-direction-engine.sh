#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

ENGINE_DIR="${PROJECT_ROOT}/backend/intelligence/cot-direction"
TEST_DIR="${PROJECT_ROOT}/backend/tests/cot-direction"
CLI_DIR="${PROJECT_ROOT}/scripts/cot"
DOCS_DIR="${PROJECT_ROOT}/governance/cot/directional-state-v1"

BACKUP_DIR="${PROJECT_ROOT}/var/backups/cot-direction-${TIMESTAMP}"
AUDIT_DIR="${PROJECT_ROOT}/var/audits/cot-direction-${TIMESTAMP}"

INSTALL_COMPLETE=0

log() {
  printf '\033[1;34m[COT]\033[0m %s\n' "$1"
}

success() {
  printf '\033[1;32m[OK]\033[0m %s\n' "$1"
}

fail() {
  printf '\033[1;31m[ERROR]\033[0m %s\n' "$1" >&2
  exit 1
}

rollback() {
  local exit_code=$?

  if [[ "${INSTALL_COMPLETE}" -eq 1 ]]; then
    return
  fi

  echo "فشل التثبيت. تتم استعادة النسخة السابقة..." >&2

  rm -rf \
    "${ENGINE_DIR}" \
    "${TEST_DIR}" \
    "${CLI_DIR}" \
    "${DOCS_DIR}"

  for relative_path in \
    "backend/intelligence/cot-direction" \
    "backend/tests/cot-direction" \
    "scripts/cot" \
    "governance/cot/directional-state-v1"
  do
    if [[ -e "${BACKUP_DIR}/${relative_path}" ]]; then
      mkdir -p "$(dirname "${PROJECT_ROOT}/${relative_path}")"
      cp -a \
        "${BACKUP_DIR}/${relative_path}" \
        "${PROJECT_ROOT}/${relative_path}"
    fi
  done

  if [[ -f "${BACKUP_DIR}/package.json" ]]; then
    cp -a "${BACKUP_DIR}/package.json" "${PROJECT_ROOT}/package.json"
  fi

  exit "${exit_code}"
}

trap rollback EXIT

[[ -d "${PROJECT_ROOT}" ]] ||
  fail "المشروع غير موجود: ${PROJECT_ROOT}"

[[ -f "${PROJECT_ROOT}/package.json" ]] ||
  fail "package.json غير موجود."

command -v node >/dev/null 2>&1 ||
  fail "Node.js غير مثبت."

cd "${PROJECT_ROOT}"

mkdir -p "${BACKUP_DIR}" "${AUDIT_DIR}"

log "إنشاء نسخة احتياطية"

cp -a package.json "${BACKUP_DIR}/package.json"

for relative_path in \
  "backend/intelligence/cot-direction" \
  "backend/tests/cot-direction" \
  "scripts/cot" \
  "governance/cot/directional-state-v1"
do
  if [[ -e "${PROJECT_ROOT}/${relative_path}" ]]; then
    mkdir -p "$(dirname "${BACKUP_DIR}/${relative_path}")"
    cp -a \
      "${PROJECT_ROOT}/${relative_path}" \
      "${BACKUP_DIR}/${relative_path}"
  fi
done

mkdir -p \
  "${ENGINE_DIR}" \
  "${TEST_DIR}" \
  "${CLI_DIR}" \
  "${DOCS_DIR}"

log "إنشاء عقد محرك COT"

cat > "${ENGINE_DIR}/contract.js" <<'EOF'
export const CONTRACT_VERSION = '1.0.0';

export const DIRECTIONS = Object.freeze({
  BUY: 'BUY',
  SELL: 'SELL',
  NEUTRAL: 'NEUTRAL',
});

export const CLARITIES = Object.freeze({
  EXPLICIT: 'EXPLICIT',
  NON_EXPLICIT: 'NON_EXPLICIT',
  TRANSITIONAL: 'TRANSITIONAL',
  NEUTRAL: 'NEUTRAL',
});

export const HORIZONS = Object.freeze({
  EXTENDED: 'EXTENDED',
  NARROW: 'NARROW',
  NEUTRAL: 'NEUTRAL',
});

export const CLASSIFICATIONS = Object.freeze({
  EXPLICIT_EXTENDED_BUY: 'EXPLICIT_EXTENDED_BUY',
  EXPLICIT_EXTENDED_SELL: 'EXPLICIT_EXTENDED_SELL',
  NON_EXPLICIT_NARROW_BUY: 'NON_EXPLICIT_NARROW_BUY',
  NON_EXPLICIT_NARROW_SELL: 'NON_EXPLICIT_NARROW_SELL',
  EXPANSION_BALANCE: 'EXPANSION_BALANCE',
  CONTRACTION_BALANCE: 'CONTRACTION_BALANCE',
  SHORT_COVERING_BUY: 'SHORT_COVERING_BUY',
  LONG_LIQUIDATION_SELL: 'LONG_LIQUIDATION_SELL',
  DIRECT_BUY: 'DIRECT_BUY',
  DIRECT_SELL: 'DIRECT_SELL',
  SHORT_COVERING_ONLY: 'SHORT_COVERING_ONLY',
  LONG_LIQUIDATION_ONLY: 'LONG_LIQUIDATION_ONLY',
  FULL_NEUTRAL: 'FULL_NEUTRAL',
});
EOF

log "إنشاء مدقق المدخلات"

cat > "${ENGINE_DIR}/validator.js" <<'EOF'
export class CotValidationError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = 'CotValidationError';
    this.details = details;
  }
}

function normalizeParticipant(value) {
  if (typeof value !== 'string' || value.trim() === '') {
    throw new CotValidationError('اسم الفئة مطلوب.');
  }

  return value
    .trim()
    .toUpperCase()
    .replaceAll('-', '_')
    .replaceAll(' ', '_');
}

function requireNumber(value, field, participant) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new CotValidationError(
      `${field} يجب أن يكون رقمًا صالحًا للفئة ${participant}.`,
    );
  }

  return value;
}

export function validateParticipants(participants) {
  if (!Array.isArray(participants) || participants.length === 0) {
    throw new CotValidationError(
      'يجب إدخال فئة واحدة على الأقل.',
    );
  }

  const normalized = participants.map((row, index) => {
    if (!row || typeof row !== 'object' || Array.isArray(row)) {
      throw new CotValidationError(
        `المدخل رقم ${index} غير صالح.`,
      );
    }

    const participant = normalizeParticipant(row.participant);

    return Object.freeze({
      participant,
      longChange: requireNumber(
        row.longChange,
        'longChange',
        participant,
      ),
      shortChange: requireNumber(
        row.shortChange,
        'shortChange',
        participant,
      ),
    });
  });

  const names = normalized.map((row) => row.participant);
  const duplicates = names.filter(
    (name, index) => names.indexOf(name) !== index,
  );

  if (duplicates.length > 0) {
    throw new CotValidationError(
      `الفئة مكررة: ${[...new Set(duplicates)].join(', ')}`,
    );
  }

  return Object.freeze(normalized);
}
EOF

log "إنشاء المحرك"

cat > "${ENGINE_DIR}/engine.js" <<'EOF'
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
EOF

log "إنشاء التحالفات"

cat > "${ENGINE_DIR}/coalitions.js" <<'EOF'
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
EOF

cat > "${ENGINE_DIR}/index.js" <<'EOF'
export { analyzeCotDirection } from './engine.js';

export {
  analyzeNamedCoalition,
  compareCanonicalCoalitions,
  COALITIONS,
} from './coalitions.js';

export {
  CONTRACT_VERSION,
  DIRECTIONS,
  CLARITIES,
  HORIZONS,
  CLASSIFICATIONS,
} from './contract.js';

export {
  validateParticipants,
  CotValidationError,
} from './validator.js';
EOF

log "إنشاء CLI"

cat > "${CLI_DIR}/analyze-week.mjs" <<'EOF'
#!/usr/bin/env node

import { readFile } from 'node:fs/promises';

import {
  analyzeCotDirection,
  analyzeNamedCoalition,
  compareCanonicalCoalitions,
} from '../../backend/intelligence/cot-direction/index.js';

async function readInput(path) {
  if (path === '-') {
    const chunks = [];

    for await (const chunk of process.stdin) {
      chunks.push(chunk);
    }

    return Buffer.concat(chunks).toString('utf8');
  }

  return readFile(path, 'utf8');
}

async function main() {
  const inputPath = process.argv[2];

  if (!inputPath) {
    throw new Error(
      'حدد ملف JSON: node scripts/cot/analyze-week.mjs input.json',
    );
  }

  const payload = JSON.parse(await readInput(inputPath));

  let analysis;

  if (payload.compareCanonicalCoalitions === true) {
    analysis = compareCanonicalCoalitions(
      payload.participants,
    );
  } else if (payload.coalitionKey) {
    analysis = analyzeNamedCoalition(
      payload.coalitionKey,
      payload.participants,
    );
  } else {
    analysis = analyzeCotDirection(payload.participants);
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        marketSymbol: payload.marketSymbol ?? null,
        reportDate: payload.reportDate ?? null,
        ...analysis,
      },
      null,
      2,
    )}\n`,
  );
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        error: error.name ?? 'Error',
        message: error.message,
        details: error.details ?? null,
      },
      null,
      2,
    ),
  );

  process.exitCode = 1;
});
EOF

chmod +x "${CLI_DIR}/analyze-week.mjs"

log "إنشاء مثال أسبوعي"

cat > "${CLI_DIR}/example-week.json" <<'EOF'
{
  "marketSymbol": "GOLD",
  "reportDate": "2026-08-04",
  "coalitionKey": "ASSET_MANAGERS_OTHER",
  "participants": [
    {
      "participant": "ASSET_MANAGERS",
      "longChange": 2,
      "shortChange": -2
    },
    {
      "participant": "OTHER_REPORTABLES",
      "longChange": 1,
      "shortChange": 1
    }
  ]
}
EOF

log "إنشاء الاختبارات"

cat > "${TEST_DIR}/engine.test.mjs" <<'EOF'
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
EOF

log "إنشاء الحوكمة"

cat > "${DOCS_DIR}/GOVERNANCE.md" <<'EOF'
# حوكمة NDSP COT Directional State

## الحالة الأسبوعية

يجب حفظ قراءة التحالف الأسبوعية في صورة:

```text
[L,S]
cat >> install-cot-direction-engine.sh <<'SCRIPT_REMAINDER'
```

حيث:

```text
L = مجموع تغيرات Long.
S = مجموع تغيرات Short.
```

لا يجوز تحويل الزوج إلى:

```text
L-S
```

## المثال المرجعي

```text
Long Asset Managers = +2
Long Other Reportables = +1
L = +3
```

```text
Short Asset Managers = -2
Short Other Reportables = +1
S = -1
```

الحالة:

```text
[L,S] = [+3,-1]
```

التصنيف:

```text
اتجاه شراء صريح ذو أفق ممتد
```

## التصنيفات

| L | S | التصنيف |
|---|---|---|
| موجب | سالب | شراء صريح ذو أفق ممتد |
| سالب | موجب | بيع صريح ذو أفق ممتد |
| موجبان وL أكبر | موجبان | شراء غير صريح ذو أفق ضيق |
| موجبان وS أكبر | موجبان | بيع غير صريح ذو أفق ضيق |
| موجبان متساويان | موجبان | تعادل توسعي |
| سالبان و\|S\| أكبر | سالبان | شراء بتغطية الشورت |
| سالبان و\|L\| أكبر | سالبان | بيع بتصفية اللونق |
| سالبان متساويان | سالبان | تعادل انكماشي |

كل أسبوع قراءة مستقلة، ولا يشترط تكرار الإشارة عدة أسابيع.
EOF

log "تحديث package.json"

node <<'NODE'
import fs from 'node:fs';

const packageJson = JSON.parse(
  fs.readFileSync('package.json', 'utf8'),
);

packageJson.scripts ??= {};

packageJson.scripts['test:cot-direction'] =
  'node --test backend/tests/cot-direction/*.test.mjs';

packageJson.scripts['cot:analyze-week'] =
  'node scripts/cot/analyze-week.mjs';

fs.writeFileSync(
  'package.json',
  `${JSON.stringify(packageJson, null, 2)}\n`,
);
NODE

log "تحديد نمط ES Modules داخل محرك COT"

cat > "${ENGINE_DIR}/package.json" <<'EOF'
{
  "name": "@ndsp/cot-direction-engine",
  "version": "1.0.0",
  "private": true,
  "type": "module"
}
EOF

log "فحص صياغة ملفات المحرك"

node --check "${ENGINE_DIR}/contract.js"
node --check "${ENGINE_DIR}/validator.js"
node --check "${ENGINE_DIR}/engine.js"
node --check "${ENGINE_DIR}/coalitions.js"
node --check "${ENGINE_DIR}/index.js"
node --check "${CLI_DIR}/analyze-week.mjs"

log "تشغيل الاختبارات"

node --test "${TEST_DIR}"/*.test.mjs

log "اختبار الحالة المرجعية"

node "${CLI_DIR}/analyze-week.mjs" \
  "${CLI_DIR}/example-week.json" \
  > "${AUDIT_DIR}/reference-output.json"

node --input-type=module - "${AUDIT_DIR}/reference-output.json" <<'NODE'
import fs from 'node:fs';

const output = JSON.parse(
  fs.readFileSync(process.argv[2], 'utf8'),
);

if (
  output.longTotal !== 3 ||
  output.shortTotal !== -1 ||
  output.classification !== 'EXPLICIT_EXTENDED_BUY'
) {
  console.error(output);

  throw new Error(
    'فشل اختبار الحالة المرجعية [+3,-1].',
  );
}

console.log(
  'الحالة المرجعية صحيحة:',
  JSON.stringify(output.state),
  output.arabicLabel,
);
NODE

log "إنشاء تقرير /opt دون حذف"

{
  echo "OPT Dependency Report"
  echo
  echo "Generated: $(date --iso-8601=seconds)"
  echo "Project: ${PROJECT_ROOT}"
  echo
  echo "لم يحذف هذا الفحص أي ملف."
  echo

  echo "=== /opt sizes ==="
  sudo du -h --max-depth=2 /opt 2>/dev/null |
    sort -h ||
    true

  echo
  echo "=== systemd references ==="
  sudo grep -RIn '/opt/' \
    /etc/systemd/system \
    /lib/systemd/system \
    2>/dev/null ||
    true

  echo
  echo "=== active processes ==="
  ps auxww |
    grep '/opt/' |
    grep -v grep ||
    true

  echo
  echo "=== cron references ==="
  sudo grep -RIn '/opt/' \
    /etc/cron.d \
    /etc/crontab \
    /var/spool/cron \
    2>/dev/null ||
    true

  echo
  echo "=== project references ==="
  grep -RIn '/opt/' "${PROJECT_ROOT}" \
    --exclude-dir=node_modules \
    --exclude-dir=venv \
    --exclude-dir=.git \
    --exclude-dir=archive \
    --exclude-dir=backups \
    --exclude='*.gz' \
    --exclude='*.tar.gz' \
    2>/dev/null |
    head -n 5000 ||
    true

  echo
  echo "=== top-level /opt directories ==="
  sudo find /opt \
    -mindepth 1 \
    -maxdepth 1 \
    -printf '%M %u:%g %TY-%Tm-%Td %TH:%TM %p\n' \
    2>/dev/null |
    sort ||
    true
} > "${AUDIT_DIR}/OPT_DEPENDENCY_REPORT.txt"

INSTALL_COMPLETE=1
trap - EXIT

success "تم تثبيت محرك COT واختباره."

cat <<EOF

============================================================
تم تثبيت محرك COT بنجاح
============================================================

المحرك:
${ENGINE_DIR}

الاختبارات:
${TEST_DIR}

الحوكمة:
${DOCS_DIR}/GOVERNANCE.md

أداة تحليل الأسبوع:
${CLI_DIR}/analyze-week.mjs

مثال التحليل:
${CLI_DIR}/example-week.json

تقرير /opt:
${AUDIT_DIR}/OPT_DEPENDENCY_REPORT.txt

النسخة الاحتياطية:
${BACKUP_DIR}

تشغيل الاختبارات:

cd ${PROJECT_ROOT}
npm run test:cot-direction

تشغيل المثال:

cd ${PROJECT_ROOT}
npm run cot:analyze-week -- scripts/cot/example-week.json

الحالة المرجعية:

L = (+2) + (+1) = +3
S = (-2) + (+1) = -1

[L,S] = [+3,-1]

اتجاه شراء صريح ذو أفق ممتد

مهم:
لم يتم حذف /opt.
لم يتم إعادة تشغيل خدمات الإنتاج.
لم يتم تعديل Nginx أو systemd.
============================================================

EOF
