'use strict';

/*
  NDSP Layer Name Masking Policy Engine
  Public rule:
  - 4 layer names may appear:
    TDL, NMP, Devil's Advocate, Nawaf Golden Alignment
  - The other 12 layer names and internal IDs are hidden.
  - Their outputs remain allowed, but must be sanitized.
*/

const POLICY = Object.freeze({
  policy: 'NDSP_LAYER_NAME_MASKING_POLICY',
  total_layers: 16,
  visible_named_layers_count: 4,
  hidden_named_layers_count: 12,
  visible_named_layers: [
    { name: 'TDL', ar: 'منطق البعد الزمني' },
    { name: 'NMP', ar: 'نقطة التقاء نواف' },
    { name: "Devil's Advocate", ar: 'محامي الشيطان' },
    { name: 'Nawaf Golden Alignment', ar: 'إشارة نواف الذهبية' }
  ],
  public_output_sanitized: true,
  hidden_outputs_allowed: true,
  raw_logic_exposed: false
});

const ALLOWED_NAMES = [
  'TDL',
  'NMP',
  "Devil's Advocate",
  'Devil&#39;s Advocate',
  'Nawaf Golden Alignment',
  'منطق البعد الزمني',
  'نقطة التقاء نواف',
  'محامي الشيطان',
  'إشارة نواف الذهبية'
];

const FORBIDDEN_PATTERNS = [
  /\bLayer\s*(?:1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16)\b/gi,
  /\bProtected\s+Layers?\b/gi,
  /\b(?:14|16)[-\s]*Layer\s+(?:Map|Governance|System)\b/gi,
  /\bD(?:1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16)\b/g,
  /طبقة\s*(?:1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16)/g,
  /الطبقات\s+المحمية\s*(?:8|9|10|11|12|16|[0-9\s·و]+)/g,
  /Protected\s+Internal\s+Layer/gi,
  /Activation\s+Layer/gi,
  /Market\s+Context\s+Layer/gi,
  /Liquidity\s+Mapping\s+Layer/gi,
  /Structure\s+Reading\s+Layer/gi,
  /Risk\s*&?\s*Volatility\s+Envelope\s+Layer/gi,
  /Public\s+Decision\s+Narrative\s+Layer/gi,
  /Final\s+Governance\s+Layer/gi
];

const FORBIDDEN_KEYS = new Set([
  'layer_map',
  'layers_map',
  'internal_layer_map',
  'protected_layers',
  'hidden_layer_names',
  'internal_layers',
  'raw_layers',
  'layer_numbers',
  'layer_ids',
  'layer_ordering'
]);

function isObject(x) {
  return x && typeof x === 'object' && !Array.isArray(x);
}

function clone(x) {
  try {
    return JSON.parse(JSON.stringify(x));
  } catch (_) {
    return x;
  }
}

function preserveAllowedNames(text) {
  let out = String(text);
  const placeholders = [];

  ALLOWED_NAMES.forEach((name, idx) => {
    const token = `__NDSP_ALLOWED_LAYER_${idx}__`;
    if (out.includes(name)) {
      out = out.split(name).join(token);
      placeholders.push([token, name]);
    }
  });

  return { out, placeholders };
}

function restoreAllowedNames(text, placeholders) {
  let out = String(text);

  placeholders.forEach(([token, name]) => {
    out = out.split(token).join(name);
  });

  return out;
}

function sanitizeString(value) {
  if (typeof value !== 'string') return value;

  const preserved = preserveAllowedNames(value);
  let out = preserved.out;

  for (const re of FORBIDDEN_PATTERNS) {
    out = out.replace(re, 'نتيجة داخلية محكومة');
  }

  out = out
    .replace(/8\s*·\s*9\s*·\s*10\s*·\s*11\s*·\s*12\s*·\s*16/g, '12 طبقة مخفية الاسم')
    .replace(/8\s*و\s*9\s*و\s*10\s*و\s*11\s*و\s*12\s*و\s*16/g, '12 طبقة مخفية الاسم');

  return restoreAllowedNames(out, preserved.placeholders);
}

function sanitizeAny(value) {
  if (Array.isArray(value)) {
    return value.map(sanitizeAny);
  }

  if (isObject(value)) {
    const out = {};

    for (const [key, val] of Object.entries(value)) {
      const lk = String(key).toLowerCase();

      if (FORBIDDEN_KEYS.has(lk)) continue;

      // Remove obvious internal-only diagnostic fields from public output.
      if (
        lk.includes('raw_layer') ||
        lk.includes('internal_layer') ||
        lk.includes('protected_layer') ||
        lk.includes('layer_id') ||
        lk.includes('layer_number') ||
        lk.includes('layer_order')
      ) {
        continue;
      }

      out[key] = sanitizeAny(val);
    }

    return out;
  }

  if (typeof value === 'string') {
    return sanitizeString(value);
  }

  return value;
}

function attachPolicy(obj) {
  const out = isObject(obj) ? obj : {};

  out.layer_name_masking_policy = {
    policy: POLICY.policy,
    total_layers: POLICY.total_layers,
    visible_named_layers_count: POLICY.visible_named_layers_count,
    hidden_named_layers_count: POLICY.hidden_named_layers_count,
    visible_named_layers: POLICY.visible_named_layers,
    hidden_layer_names_exposed: false,
    hidden_layer_outputs_allowed: true,
    public_output_sanitized: true,
    raw_logic_exposed: false,
    formulas_exposed: false,
    weights_exposed: false,
    internal_ordering_exposed: false
  };

  out.governance = Object.assign({}, out.governance || {}, {
    layer_name_masking_policy_active: true,
    visible_named_layers_count: 4,
    hidden_named_layers_count: 12,
    hidden_layer_names_exposed: false,
    hidden_layer_outputs_allowed: true,
    public_output_sanitized: true,
    no_raw_logic_disclosure: true
  });

  return out;
}

function sanitizeAnalysisForPublic(analysis) {
  const safe = sanitizeAny(clone(analysis || {}));
  return attachPolicy(safe);
}

function sanitizeResponseForPublic(payload) {
  const safe = sanitizeAny(clone(payload || {}));

  if (safe && safe.analysis) {
    safe.analysis = attachPolicy(safe.analysis);
  }

  return safe;
}

function selfTest() {
  const sample = {
    analysis: {
      layer_map: ['D1', 'D2', 'Layer 8'],
      visible: ['TDL', 'NMP', "Devil's Advocate", 'Nawaf Golden Alignment'],
      text: 'D1 and Protected Layers 8 · 9 · 10 · 11 · 12 · 16 must not appear. TDL remains visible.'
    }
  };

  const out = sanitizeResponseForPublic(sample);
  const body = JSON.stringify(out);

  return {
    ok:
      !body.includes('D1') &&
      !body.includes('Protected Layers') &&
      !body.includes('8 · 9 · 10') &&
      body.includes('TDL') &&
      body.includes('NMP') &&
      body.includes("Devil's Advocate") &&
      body.includes('Nawaf Golden Alignment'),
    body
  };
}

module.exports = {
  POLICY,
  sanitizeAnalysisForPublic,
  sanitizeResponseForPublic,
  selfTest
};
