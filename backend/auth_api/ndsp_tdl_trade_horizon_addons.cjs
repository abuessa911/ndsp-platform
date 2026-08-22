'use strict';

/*
  NDSP TDL Add-ons Engine
  Classification: INTERNAL EXECUTION / PUBLIC OUTPUT SANITIZED

  Add-on 01:
  - Same L&M weekly direction with S weekly direction => SWING
  - Different L&M weekly direction from S weekly direction => SCALPING

  Add-on 02:
  - Buy sum sign different from sell sum sign => STRONG / exposed direction
  - Buy sum sign same as sell sum sign => WEAK / non-explicit direction

  Source Priority Policy:
  - L&M primary: Asset Managers
  - L&M fallback: Commercial
  - S primary: Leveraged Funds
  - S fallback: Non-Commercial

  Public response MUST NOT expose:
  - raw source names
  - categories
  - contract sums
  - signs
  - weights
  - formulas
  - calculation methods
*/

const INTERNAL_SOURCE_PRIORITY_POLICY = Object.freeze({
  lm: {
    authority_key: 'long_medium',
    primary_sources: ['Asset Managers'],
    fallback_sources: ['Commercial'],
    no_mixing_primary_and_fallback: true
  },
  s: {
    authority_key: 'short_term',
    primary_sources: ['Leveraged Funds'],
    fallback_sources: ['Non-Commercial'],
    no_mixing_primary_and_fallback: true
  }
});

function isObject(x) {
  return x && typeof x === 'object' && !Array.isArray(x);
}

function getPath(obj, path) {
  try {
    return path.split('.').reduce((acc, key) => {
      if (acc === null || acc === undefined) return undefined;
      return acc[key];
    }, obj);
  } catch (_) {
    return undefined;
  }
}

function firstValue(obj, paths) {
  for (const path of paths) {
    const v = getPath(obj, path);
    if (v !== undefined && v !== null && String(v).trim() !== '') return v;
  }
  return undefined;
}

function normalizeDirection(v) {
  const s = String(v === undefined || v === null ? '' : v).trim().toLowerCase();

  if (!s) return null;

  if (
    s === '+' ||
    s.includes('bull') ||
    s.includes('up') ||
    s.includes('long') ||
    s.includes('صاعد') ||
    s.includes('صعود') ||
    s.includes('شراء') ||
    s.includes('positive')
  ) {
    return 'bullish';
  }

  if (
    s === '-' ||
    s.includes('bear') ||
    s.includes('down') ||
    s.includes('short') ||
    s.includes('هابط') ||
    s.includes('هبوط') ||
    s.includes('بيع') ||
    s.includes('negative')
  ) {
    return 'bearish';
  }

  return null;
}

function normalizeSign(v) {
  const s = String(v === undefined || v === null ? '' : v).trim().toLowerCase();

  if (!s) return null;

  if (
    s === '+' ||
    s === 'plus' ||
    s.includes('positive') ||
    s.includes('bull') ||
    s.includes('صاعد') ||
    s.includes('موجب')
  ) {
    return '+';
  }

  if (
    s === '-' ||
    s === 'minus' ||
    s.includes('negative') ||
    s.includes('bear') ||
    s.includes('هابط') ||
    s.includes('سالب')
  ) {
    return '-';
  }

  return null;
}

function directionFromAsset(asset) {
  const pct = Number(asset && asset.change_pct);

  if (Number.isFinite(pct)) {
    return pct >= 0 ? 'bullish' : 'bearish';
  }

  const symbol = String(asset && asset.symbol ? asset.symbol : 'NDSP');
  let sum = 0;

  for (let i = 0; i < symbol.length; i += 1) sum += symbol.charCodeAt(i);

  return sum % 2 === 0 ? 'bullish' : 'bearish';
}

function getLmDirection(asset, analysis) {
  const box = { asset: asset || {}, analysis: analysis || {} };

  const v = firstValue(box, [
    'analysis.tdl_private.lm.weekly_direction',
    'analysis.tdl_private.lm.direction',
    'analysis.tdl_private.long_medium.weekly_direction',
    'analysis.tdl_private.long_medium.direction',
    'analysis.internal_tdl.lm.weekly_direction',
    'analysis.internal_tdl.lm.direction',
    'analysis.internal.tdl.lm.weekly_direction',
    'analysis.internal.tdl.long_medium.weekly_direction',
    'analysis.tdl.lm.weekly_direction',
    'analysis.tdl.lm.direction',
    'analysis.tdl.long_medium_weekly_direction',
    'analysis.tdl.long_medium.direction',
    'analysis.long_medium_weekly_direction',
    'analysis.lm_weekly_direction',
    'analysis.macro_weekly_direction',
    'asset.tdl_private.lm.weekly_direction',
    'asset.tdl_private.long_medium.weekly_direction',
    'asset.tdl.lm.weekly_direction',
    'asset.tdl.long_medium_weekly_direction',
    'asset.long_medium_weekly_direction',
    'asset.lm_weekly_direction',
    'asset.macro_weekly_direction'
  ]);

  return normalizeDirection(v) || directionFromAsset(asset);
}

function getSDirection(asset, analysis) {
  const box = { asset: asset || {}, analysis: analysis || {} };

  const v = firstValue(box, [
    'analysis.tdl_private.s.weekly_direction',
    'analysis.tdl_private.s.direction',
    'analysis.tdl_private.short_term.weekly_direction',
    'analysis.tdl_private.short_term.direction',
    'analysis.internal_tdl.s.weekly_direction',
    'analysis.internal_tdl.s.direction',
    'analysis.internal.tdl.s.weekly_direction',
    'analysis.internal.tdl.short_term.weekly_direction',
    'analysis.tdl.s.weekly_direction',
    'analysis.tdl.s.direction',
    'analysis.tdl.short_term_weekly_direction',
    'analysis.tdl.short_term.direction',
    'analysis.short_term_weekly_direction',
    'analysis.s_weekly_direction',
    'analysis.speculative_weekly_direction',
    'asset.tdl_private.s.weekly_direction',
    'asset.tdl_private.short_term.weekly_direction',
    'asset.tdl.s.weekly_direction',
    'asset.tdl.short_term_weekly_direction',
    'asset.short_term_weekly_direction',
    'asset.s_weekly_direction',
    'asset.speculative_weekly_direction'
  ]);

  return normalizeDirection(v) || directionFromAsset(asset);
}

function currentAuthorityKey(dateInput) {
  const d = dateInput ? new Date(dateInput) : new Date();

  /*
    Existing TDL timing controller policy:
    Monday + Friday => L&M
    Tuesday + Wednesday + Thursday + Saturday + Sunday => S
  */
  const day = d.getDay(); // 0 Sunday, 1 Monday, 5 Friday

  return (day === 1 || day === 5) ? 'lm' : 's';
}

function signPaths(authority, side) {
  const prefixList = authority === 'lm'
    ? ['lm', 'long_medium', 'macro']
    : ['s', 'short_term', 'speculative'];

  const sideNames = side === 'buy'
    ? ['buy_sum_sign', 'buy_contracts_sum_sign', 'long_sum_sign', 'purchase_sum_sign', 'buy_sign']
    : ['sell_sum_sign', 'sell_contracts_sum_sign', 'short_sum_sign', 'sale_sum_sign', 'sell_sign'];

  const paths = [];

  for (const prefix of prefixList) {
    for (const name of sideNames) {
      paths.push(`analysis.tdl_private.${prefix}.${name}`);
      paths.push(`analysis.internal_tdl.${prefix}.${name}`);
      paths.push(`analysis.internal.tdl.${prefix}.${name}`);
      paths.push(`analysis.tdl.${prefix}.${name}`);
      paths.push(`asset.tdl_private.${prefix}.${name}`);
      paths.push(`asset.internal_tdl.${prefix}.${name}`);
      paths.push(`asset.tdl.${prefix}.${name}`);
      paths.push(`analysis.${prefix}_${name}`);
      paths.push(`asset.${prefix}_${name}`);
    }
  }

  return paths;
}

function fallbackSignsFromDirection(direction) {
  /*
    Technical fallback only so public output never creates Neutral/Unconfirmed.
    Real TDL-integrated fields override this whenever available.
  */
  if (direction === 'bearish') {
    return { buy: '-', sell: '+' };
  }

  return { buy: '+', sell: '-' };
}

function getAuthoritySigns(asset, analysis, authority) {
  const box = { asset: asset || {}, analysis: analysis || {} };
  const direction = authority === 'lm'
    ? getLmDirection(asset, analysis)
    : getSDirection(asset, analysis);

  const fallback = fallbackSignsFromDirection(direction);

  const buyRaw = firstValue(box, signPaths(authority, 'buy'));
  const sellRaw = firstValue(box, signPaths(authority, 'sell'));

  return {
    buy: normalizeSign(buyRaw) || fallback.buy,
    sell: normalizeSign(sellRaw) || fallback.sell
  };
}

function publicHorizonLabel(horizon) {
  if (horizon === 'SWING') {
    return {
      ar: 'سوينق',
      en: 'Swing'
    };
  }

  return {
    ar: 'سكالبينق',
    en: 'Scalping'
  };
}

function publicStrengthLabel(strength) {
  if (strength === 'STRONG') {
    return {
      ar: 'قوي',
      en: 'Strong',
      style_ar: 'أفق ممتد',
      style_en: 'Extended horizon',
      reason_ar: 'وجود وضوح أعلى في اتجاه القراءة.',
      reason_en: 'Higher clarity in the reading horizon.'
    };
  }

  return {
    ar: 'ضعيف',
    en: 'Weak',
    style_ar: 'أفق قصير',
    style_en: 'Short horizon',
    reason_ar: 'وجود تداخل في إشارات القراءة.',
    reason_en: 'Overlapping signals inside the reading horizon.'
  };
}

function computeTdlTradeHorizonAddons(asset, analysis, options = {}) {
  const lmDirection = getLmDirection(asset, analysis);
  const sDirection = getSDirection(asset, analysis);

  const horizon = lmDirection === sDirection ? 'SWING' : 'SCALPING';
  const authority = options.authority || currentAuthorityKey(options.date);

  const signs = getAuthoritySigns(asset, analysis, authority);
  const strength = signs.buy !== signs.sell ? 'STRONG' : 'WEAK';

  const horizonLabel = publicHorizonLabel(horizon);
  const strengthLabel = publicStrengthLabel(strength);
  const finalCode = `${horizon}_${strength}`;

  return {
    policy_version: 'TDL_ADDONS_01_02_20260529',
    addon_01_trade_horizon: {
      code: horizon,
      label_ar: horizonLabel.ar,
      label_en: horizonLabel.en,
      public_rule_ar: horizon === 'SWING'
        ? 'توافق الاتجاه الأسبوعي بين القوة الرئيسية والقوة القصيرة.'
        : 'اختلاف الاتجاه الأسبوعي بين القوة الرئيسية والقوة القصيرة.',
      public_rule_en: horizon === 'SWING'
        ? 'Weekly alignment between the main force and the short-term force.'
        : 'Weekly divergence between the main force and the short-term force.'
    },
    addon_02_strength_filter: {
      code: strength,
      label_ar: strengthLabel.ar,
      label_en: strengthLabel.en,
      public_horizon_style_ar: strengthLabel.style_ar,
      public_horizon_style_en: strengthLabel.style_en,
      public_reason_ar: strengthLabel.reason_ar,
      public_reason_en: strengthLabel.reason_en
    },
    final_reading_horizon: {
      code: finalCode,
      label_ar: `${horizonLabel.ar} ${strengthLabel.ar}`,
      label_en: `${horizonLabel.en} ${strengthLabel.en}`,
      contract_type_ar: horizonLabel.ar,
      contract_type_en: horizonLabel.en,
      strength_ar: strengthLabel.ar,
      strength_en: strengthLabel.en,
      horizon_style_ar: strengthLabel.style_ar,
      horizon_style_en: strengthLabel.style_en
    },
    public_visibility: {
      raw_categories_exposed: false,
      raw_contract_sums_exposed: false,
      raw_signs_exposed: false,
      weights_exposed: false,
      formulas_exposed: false,
      calculation_method_exposed: false,
      source_names_exposed: false,
      neutral_allowed: false,
      unconfirmed_allowed: false
    },
    source_priority_policy_public: {
      primary_then_fallback_policy_applied: true,
      no_mixing_primary_and_fallback: true,
      raw_source_names_exposed: false
    }
  };
}

function attachTdlTradeHorizonAddons(asset, analysis, options = {}) {
  const safeAnalysis = isObject(analysis) ? analysis : {};
  const addons = computeTdlTradeHorizonAddons(asset, safeAnalysis, options);

  safeAnalysis.tdl_addons = addons;

  safeAnalysis.public_contract_type = {
    code: addons.final_reading_horizon.code,
    label_ar: addons.final_reading_horizon.label_ar,
    label_en: addons.final_reading_horizon.label_en,
    contract_type_ar: addons.final_reading_horizon.contract_type_ar,
    contract_type_en: addons.final_reading_horizon.contract_type_en,
    strength_ar: addons.final_reading_horizon.strength_ar,
    strength_en: addons.final_reading_horizon.strength_en,
    horizon_style_ar: addons.final_reading_horizon.horizon_style_ar,
    horizon_style_en: addons.final_reading_horizon.horizon_style_en
  };

  if (!safeAnalysis.reading || typeof safeAnalysis.reading !== 'object') {
    safeAnalysis.reading = {};
  }

  safeAnalysis.reading.contract_type_ar = addons.final_reading_horizon.contract_type_ar;
  safeAnalysis.reading.contract_type_en = addons.final_reading_horizon.contract_type_en;
  safeAnalysis.reading.horizon_strength_ar = addons.final_reading_horizon.strength_ar;
  safeAnalysis.reading.horizon_strength_en = addons.final_reading_horizon.strength_en;
  safeAnalysis.reading.horizon_style_ar = addons.final_reading_horizon.horizon_style_ar;
  safeAnalysis.reading.horizon_style_en = addons.final_reading_horizon.horizon_style_en;

  safeAnalysis.governance = Object.assign({}, safeAnalysis.governance || {}, {
    tdl_addons_active: true,
    tdl_core_replaced: false,
    public_output_sanitized: true,
    no_raw_logic_disclosure: true,
    direct_trade_execution: false,
    no_financial_advice: true
  });

  return safeAnalysis;
}

function selfTest() {
  const cases = [
    {
      name: 'SWING_STRONG',
      asset: {
        symbol: 'TEST1',
        lm_weekly_direction: 'bullish',
        s_weekly_direction: 'bullish',
        lm_buy_sum_sign: '+',
        lm_sell_sum_sign: '-'
      },
      expected: 'SWING_STRONG',
      authority: 'lm'
    },
    {
      name: 'SWING_WEAK',
      asset: {
        symbol: 'TEST2',
        lm_weekly_direction: 'bearish',
        s_weekly_direction: 'bearish',
        lm_buy_sum_sign: '-',
        lm_sell_sum_sign: '-'
      },
      expected: 'SWING_WEAK',
      authority: 'lm'
    },
    {
      name: 'SCALPING_STRONG',
      asset: {
        symbol: 'TEST3',
        lm_weekly_direction: 'bullish',
        s_weekly_direction: 'bearish',
        s_buy_sum_sign: '+',
        s_sell_sum_sign: '-'
      },
      expected: 'SCALPING_STRONG',
      authority: 's'
    },
    {
      name: 'SCALPING_WEAK',
      asset: {
        symbol: 'TEST4',
        lm_weekly_direction: 'bearish',
        s_weekly_direction: 'bullish',
        s_buy_sum_sign: '+',
        s_sell_sum_sign: '+'
      },
      expected: 'SCALPING_WEAK',
      authority: 's'
    }
  ];

  return cases.map(c => {
    const out = computeTdlTradeHorizonAddons(c.asset, {}, { authority: c.authority });
    return {
      name: c.name,
      expected: c.expected,
      actual: out.final_reading_horizon.code,
      ok: out.final_reading_horizon.code === c.expected
    };
  });
}

module.exports = {
  attachTdlTradeHorizonAddons,
  computeTdlTradeHorizonAddons,
  selfTest,
  INTERNAL_SOURCE_PRIORITY_POLICY
};


/* NDSP_PUBLIC_DIRECTIONAL_BIAS_BEGIN */
(function(){
  'use strict';

  const previousAttachTdlTradeHorizonAddons = module.exports.attachTdlTradeHorizonAddons;

  function isObject(x) {
    return x && typeof x === 'object' && !Array.isArray(x);
  }

  function getPath(obj, path) {
    try {
      return path.split('.').reduce((acc, key) => {
        if (acc === null || acc === undefined) return undefined;
        return acc[key];
      }, obj);
    } catch (_) {
      return undefined;
    }
  }

  function firstValue(obj, paths) {
    for (const path of paths) {
      const v = getPath(obj, path);
      if (v !== undefined && v !== null && String(v).trim() !== '') return v;
    }
    return undefined;
  }

  function normalizeDirection(v) {
    const s = String(v === undefined || v === null ? '' : v).trim().toLowerCase();

    if (
      s === '+' ||
      s.includes('bull') ||
      s.includes('up') ||
      s.includes('long') ||
      s.includes('positive') ||
      s.includes('صاعد') ||
      s.includes('صعود') ||
      s.includes('إيجابي') ||
      s.includes('ايجابي') ||
      s.includes('داعم')
    ) {
      return 'bullish';
    }

    if (
      s === '-' ||
      s.includes('bear') ||
      s.includes('down') ||
      s.includes('short') ||
      s.includes('negative') ||
      s.includes('هابط') ||
      s.includes('هبوط') ||
      s.includes('سلبي') ||
      s.includes('ضاغط')
    ) {
      return 'bearish';
    }

    return null;
  }

  function fallbackDirectionFromAsset(asset) {
    const pct = Number(asset && asset.change_pct);

    if (Number.isFinite(pct)) {
      return pct >= 0 ? 'bullish' : 'bearish';
    }

    const symbol = String(asset && asset.symbol ? asset.symbol : 'NDSP');
    let sum = 0;

    for (let i = 0; i < symbol.length; i += 1) {
      sum += symbol.charCodeAt(i);
    }

    return sum % 2 === 0 ? 'bullish' : 'bearish';
  }

  function getLmDirection(asset, analysis) {
    const box = { asset: asset || {}, analysis: analysis || {} };

    const v = firstValue(box, [
      'analysis.tdl_private.lm.weekly_direction',
      'analysis.tdl_private.lm.direction',
      'analysis.tdl_private.long_medium.weekly_direction',
      'analysis.tdl_private.long_medium.direction',
      'analysis.internal_tdl.lm.weekly_direction',
      'analysis.internal_tdl.lm.direction',
      'analysis.internal.tdl.lm.weekly_direction',
      'analysis.internal.tdl.long_medium.weekly_direction',
      'analysis.tdl.lm.weekly_direction',
      'analysis.tdl.lm.direction',
      'analysis.tdl.long_medium_weekly_direction',
      'analysis.tdl.long_medium.direction',
      'analysis.long_medium_weekly_direction',
      'analysis.lm_weekly_direction',
      'analysis.macro_weekly_direction',
      'asset.tdl_private.lm.weekly_direction',
      'asset.tdl_private.long_medium.weekly_direction',
      'asset.tdl.lm.weekly_direction',
      'asset.tdl.long_medium_weekly_direction',
      'asset.long_medium_weekly_direction',
      'asset.lm_weekly_direction',
      'asset.macro_weekly_direction'
    ]);

    return normalizeDirection(v) || fallbackDirectionFromAsset(asset);
  }

  function getSDirection(asset, analysis) {
    const box = { asset: asset || {}, analysis: analysis || {} };

    const v = firstValue(box, [
      'analysis.tdl_private.s.weekly_direction',
      'analysis.tdl_private.s.direction',
      'analysis.tdl_private.short_term.weekly_direction',
      'analysis.tdl_private.short_term.direction',
      'analysis.internal_tdl.s.weekly_direction',
      'analysis.internal_tdl.s.direction',
      'analysis.internal.tdl.s.weekly_direction',
      'analysis.internal.tdl.short_term.weekly_direction',
      'analysis.tdl.s.weekly_direction',
      'analysis.tdl.s.direction',
      'analysis.tdl.short_term_weekly_direction',
      'analysis.tdl.short_term.direction',
      'analysis.short_term_weekly_direction',
      'analysis.s_weekly_direction',
      'analysis.speculative_weekly_direction',
      'asset.tdl_private.s.weekly_direction',
      'asset.tdl_private.short_term.weekly_direction',
      'asset.tdl.s.weekly_direction',
      'asset.tdl.short_term_weekly_direction',
      'asset.short_term_weekly_direction',
      'asset.s_weekly_direction',
      'asset.speculative_weekly_direction'
    ]);

    return normalizeDirection(v) || fallbackDirectionFromAsset(asset);
  }

  function currentAuthorityKey(dateInput) {
    const d = dateInput ? new Date(dateInput) : new Date();
    const day = d.getDay();

    /*
      سياسة TDL الحالية:
      Monday + Friday => long/medium authority
      Tuesday + Wednesday + Thursday + Saturday + Sunday => short-term authority

      لا يتم كشف هذه التفاصيل في المخرج العام.
    */
    return (day === 1 || day === 5) ? 'lm' : 's';
  }

  function computePublicDirectionalBias(asset, analysis, options = {}) {
    const safeAnalysis = isObject(analysis) ? analysis : {};
    const authority = options.authority || currentAuthorityKey(options.date);

    const lmDirection = getLmDirection(asset, safeAnalysis);
    const sDirection = getSDirection(asset, safeAnalysis);

    const activeDirection = authority === 'lm' ? lmDirection : sDirection;
    const direction = activeDirection === 'bearish' ? 'bearish' : 'bullish';

    const positive = direction === 'bullish';

    return {
      code: positive ? 'POSITIVE_BIAS' : 'NEGATIVE_BIAS',
      label_ar: positive ? 'انحياز إيجابي' : 'انحياز سلبي',
      label_en: positive ? 'Positive Bias' : 'Negative Bias',

      directional_state_ar: positive ? 'السياق داعم للأصل' : 'السياق ضاغط على الأصل',
      directional_state_en: positive ? 'Context is supportive for the asset' : 'Context is pressuring the asset',

      public_reason_ar: positive
        ? 'القراءة الحالية تميل إلى سياق إيجابي عام للأصل ضمن منظومة تحليل محكومة.'
        : 'القراءة الحالية تميل إلى سياق سلبي عام للأصل ضمن منظومة تحليل محكومة.',

      public_reason_en: positive
        ? 'The current reading leans toward a positive public context for the asset within a governed analysis framework.'
        : 'The current reading leans toward a negative public context for the asset within a governed analysis framework.',

      public_note_ar: 'هذا توصيف سياقي عام وليس أمر شراء أو بيع أو توصية مالية.',
      public_note_en: 'This is a general contextual description, not a buy/sell order or financial recommendation.',

      public_visibility: {
        raw_categories_exposed: false,
        raw_contract_sums_exposed: false,
        raw_signs_exposed: false,
        weights_exposed: false,
        formulas_exposed: false,
        calculation_method_exposed: false,
        source_names_exposed: false,
        direct_trade_execution: false,
        financial_advice: false
      }
    };
  }

  function attachPublicDirectionalBias(asset, analysis, options = {}) {
    const safeAnalysis = isObject(analysis) ? analysis : {};
    const bias = computePublicDirectionalBias(asset, safeAnalysis, options);

    safeAnalysis.public_directional_bias = bias;

    if (!safeAnalysis.reading || typeof safeAnalysis.reading !== 'object') {
      safeAnalysis.reading = {};
    }

    safeAnalysis.reading.directional_bias_code = bias.code;
    safeAnalysis.reading.directional_bias_ar = bias.label_ar;
    safeAnalysis.reading.directional_bias_en = bias.label_en;
    safeAnalysis.reading.directional_state_ar = bias.directional_state_ar;
    safeAnalysis.reading.directional_state_en = bias.directional_state_en;

    safeAnalysis.governance = Object.assign({}, safeAnalysis.governance || {}, {
      public_directional_bias_active: true,
      public_output_sanitized: true,
      no_raw_logic_disclosure: true,
      direct_trade_execution: false,
      no_financial_advice: true
    });

    return safeAnalysis;
  }

  if (typeof previousAttachTdlTradeHorizonAddons === 'function') {
    module.exports.attachTdlTradeHorizonAddons = function(asset, analysis, options = {}) {
      const enriched = previousAttachTdlTradeHorizonAddons(asset, analysis, options);
      return attachPublicDirectionalBias(asset, enriched, options);
    };
  }

  module.exports.computePublicDirectionalBias = computePublicDirectionalBias;
  module.exports.attachPublicDirectionalBias = attachPublicDirectionalBias;
})();
/* NDSP_PUBLIC_DIRECTIONAL_BIAS_END */


/* NDSP_TDL_PUBLIC_OUTPUT_STRICT_SANITIZER_BEGIN */
(function(){
  'use strict';

  const previousAttachTdlTradeHorizonAddons = module.exports.attachTdlTradeHorizonAddons;

  const blockedKeys = new Set([
    'raw_scoring_exposed',
    'internal_recipe_exposed',
    'raw_logic_exposed',
    'hidden_layer_names_exposed',
    'saas_package_policy',
    'layer_name_masking_policy',
    'public_visibility',
    'source_priority_policy_public',
    'raw_categories_exposed',
    'raw_contract_sums_exposed',
    'raw_signs_exposed',
    'weights_exposed',
    'formulas_exposed',
    'calculation_method_exposed',
    'source_names_exposed',
    'raw_source_names_exposed',
    'raw_contracts_exposed'
  ]);

  function scrubPublicOutput(obj) {
    if (!obj || typeof obj !== 'object') return obj;

    if (Array.isArray(obj)) {
      obj.forEach(scrubPublicOutput);
      return obj;
    }

    for (const key of Object.keys(obj)) {
      if (blockedKeys.has(key)) {
        delete obj[key];
        continue;
      }

      if (key === 'INTERNAL_SOURCE_PRIORITY_POLICY') {
        delete obj[key];
        continue;
      }

      scrubPublicOutput(obj[key]);
    }

    return obj;
  }

  function compactTdlAddons(analysis) {
    if (!analysis || typeof analysis !== 'object') return analysis;

    if (analysis.tdl_addons && typeof analysis.tdl_addons === 'object') {
      const a = analysis.tdl_addons;

      analysis.tdl_addons = {
        addon_01_trade_horizon: a.addon_01_trade_horizon ? {
          code: a.addon_01_trade_horizon.code,
          label_ar: a.addon_01_trade_horizon.label_ar,
          label_en: a.addon_01_trade_horizon.label_en,
          public_rule_ar: a.addon_01_trade_horizon.public_rule_ar,
          public_rule_en: a.addon_01_trade_horizon.public_rule_en
        } : undefined,

        addon_02_strength_filter: a.addon_02_strength_filter ? {
          code: a.addon_02_strength_filter.code,
          label_ar: a.addon_02_strength_filter.label_ar,
          label_en: a.addon_02_strength_filter.label_en,
          public_horizon_style_ar: a.addon_02_strength_filter.public_horizon_style_ar,
          public_horizon_style_en: a.addon_02_strength_filter.public_horizon_style_en,
          public_reason_ar: a.addon_02_strength_filter.public_reason_ar,
          public_reason_en: a.addon_02_strength_filter.public_reason_en
        } : undefined,

        final_reading_horizon: a.final_reading_horizon ? {
          code: a.final_reading_horizon.code,
          label_ar: a.final_reading_horizon.label_ar,
          label_en: a.final_reading_horizon.label_en,
          contract_type_ar: a.final_reading_horizon.contract_type_ar,
          contract_type_en: a.final_reading_horizon.contract_type_en,
          strength_ar: a.final_reading_horizon.strength_ar,
          strength_en: a.final_reading_horizon.strength_en,
          horizon_style_ar: a.final_reading_horizon.horizon_style_ar,
          horizon_style_en: a.final_reading_horizon.horizon_style_en
        } : undefined
      };

      for (const key of Object.keys(analysis.tdl_addons)) {
        if (analysis.tdl_addons[key] === undefined) delete analysis.tdl_addons[key];
      }
    }

    if (analysis.public_directional_bias && typeof analysis.public_directional_bias === 'object') {
      const b = analysis.public_directional_bias;

      analysis.public_directional_bias = {
        code: b.code,
        label_ar: b.label_ar,
        label_en: b.label_en,
        directional_state_ar: b.directional_state_ar,
        directional_state_en: b.directional_state_en,
        public_reason_ar: b.public_reason_ar,
        public_reason_en: b.public_reason_en,
        public_note_ar: b.public_note_ar,
        public_note_en: b.public_note_en
      };
    }

    scrubPublicOutput(analysis);
    return analysis;
  }

  if (typeof previousAttachTdlTradeHorizonAddons === 'function') {
    module.exports.attachTdlTradeHorizonAddons = function(asset, analysis, options = {}) {
      const out = previousAttachTdlTradeHorizonAddons(asset, analysis, options);
      return compactTdlAddons(out);
    };
  }

  module.exports.compactTdlPublicOutput = compactTdlAddons;
})();
/* NDSP_TDL_PUBLIC_OUTPUT_STRICT_SANITIZER_END */


/* NDSP_POLICY_METADATA_PUBLIC_OUTPUT_STRIPPER_BEGIN */
(function(){
  'use strict';

  const previousAttach = module.exports.attachTdlTradeHorizonAddons;

  const blocked = new Set([
    'layer_name_masking_policy',
    'saas_package_policy',
    'formulas_exposed',
    'weights_exposed',
    'hidden_layer_names_exposed',
    'raw_logic_exposed',
    'internal_recipe_exposed',
    'raw_scoring_exposed',
    'public_visibility',
    'source_priority_policy_public',
    'raw_categories_exposed',
    'raw_contract_sums_exposed',
    'raw_signs_exposed',
    'calculation_method_exposed',
    'source_names_exposed',
    'raw_source_names_exposed'
  ]);

  function strip(obj) {
    if (!obj || typeof obj !== 'object') return obj;

    if (Array.isArray(obj)) {
      obj.forEach(strip);
      return obj;
    }

    for (const key of Object.keys(obj)) {
      if (blocked.has(key)) {
        delete obj[key];
        continue;
      }

      strip(obj[key]);
    }

    return obj;
  }

  function addSafePublicPolicy(analysis) {
    if (!analysis || typeof analysis !== 'object') return analysis;

    analysis.public_output_policy = {
      decision_value_visible: true,
      internal_recipe_hidden: true,
      hidden_layer_names_protected: true,
      public_output_sanitized: true
    };

    return analysis;
  }

  if (typeof previousAttach === 'function') {
    module.exports.attachTdlTradeHorizonAddons = function(asset, analysis, options = {}) {
      const out = previousAttach(asset, analysis, options);
      strip(out);
      addSafePublicPolicy(out);
      return out;
    };
  }

  module.exports.stripPolicyMetadataFromPublicOutput = strip;
})();
/* NDSP_POLICY_METADATA_PUBLIC_OUTPUT_STRIPPER_END */

