'use strict';

const APPROVED_LAYER_NAMES = Object.freeze([
  'TDL',
  'NMP',
  "Devil's Advocate",
  'Nawaf Golden Alignment'
]);

const PACKAGES = Object.freeze({
  free: {
    key: 'free',
    name: 'Free',
    markets_limit: 1,
    assets_limit: 2,
    daily_analysis_limit: 1,
    visible_named_layers: [],
    hidden_named_layers_count: 16,
    decision_depth: 'basic',
    alerts: 'none',
    api: false,
    webhooks: false,
    teams: false,
    reports: false
  },
  pro: {
    key: 'pro',
    name: 'Pro',
    markets_limit: 2,
    assets_limit: 20,
    daily_analysis_limit: 15,
    visible_named_layers: ['TDL', 'NMP'],
    hidden_by_name_but_outputs_allowed: ["Devil's Advocate", 'Nawaf Golden Alignment'],
    hidden_named_layers_count: 14,
    decision_depth: 'advanced_entry',
    alerts: 'basic_limited',
    api: false,
    webhooks: false,
    teams: false,
    reports: 'limited'
  },
  elite: {
    key: 'elite',
    name: 'Elite',
    markets_limit: 'all',
    assets_limit: 100,
    daily_analysis_limit: 250,
    visible_named_layers: ['TDL', 'NMP', "Devil's Advocate", 'Nawaf Golden Alignment'],
    hidden_named_layers_count: 12,
    decision_depth: 'full_individual',
    alerts: 'advanced_telegram',
    comparison: true,
    decision_journal: true,
    scenario_followup: true,
    api: false,
    webhooks: false,
    teams: false,
    reports: 'advanced_user'
  },
  institutional_suite: {
    key: 'institutional_suite',
    name: 'Institutional Suite',
    markets_limit: 'all',
    assets_limit: '250+ or contract',
    daily_analysis_limit: 'contract',
    visible_named_layers: ['TDL', 'NMP', "Devil's Advocate", 'Nawaf Golden Alignment'],
    hidden_named_layers_count: 12,
    decision_depth: 'commercial_institutional',
    alerts: 'multi_channel',
    api: true,
    webhooks: true,
    teams: true,
    reports: true,
    custom_assets: true,
    contract_based: true
  }
});

const GLOBAL_RULES = Object.freeze({
  total_internal_layers: 16,
  approved_named_layers: APPROVED_LAYER_NAMES,
  hidden_internal_layer_names_always_hidden: true,
  hidden_layer_outputs_allowed: true,
  raw_logic_exposed: false,
  weights_exposed: false,
  formulas_exposed: false,
  internal_scoring_exposed: false,
  source_logic_exposed: false,
  public_output_sanitized: true
});

function normalizePlan(plan) {
  const s = String(plan || '').trim().toLowerCase();

  if (!s) return 'free';

  if (['free', 'starter', 'basic'].includes(s)) return 'free';
  if (['pro', 'professional', 'paid_pro'].includes(s)) return 'pro';
  if (['elite', 'premium', 'trial_elite', 'elite_trial'].includes(s)) return 'elite';

  if (
    s.includes('institutional') ||
    s.includes('institution') ||
    s.includes('suite') ||
    s.includes('saas') ||
    s.includes('business') ||
    s.includes('enterprise') ||
    s.includes('commercial')
  ) {
    return 'institutional_suite';
  }

  return 'free';
}

function detectPlanFromUser(user, overridePlan) {
  if (overridePlan) return normalizePlan(overridePlan);

  const u = user && typeof user === 'object' ? user : {};

  return normalizePlan(
    u.plan ||
    u.package ||
    u.subscription_plan ||
    u.account_plan ||
    u.tier ||
    u.role_plan ||
    'free'
  );
}

function getPackagePolicy(plan) {
  const key = normalizePlan(plan);
  return PACKAGES[key] || PACKAGES.free;
}

function publicPackages() {
  return {
    policy: 'NDSP_SAAS_PACKAGES_POLICY',
    status: 'authoritative',
    packages: PACKAGES,
    global_rules: GLOBAL_RULES
  };
}

function layerVisibilityForPlan(plan) {
  const pkg = getPackagePolicy(plan);

  return {
    plan_key: pkg.key,
    plan_name: pkg.name,
    total_internal_layers: 16,
    visible_named_layers: pkg.visible_named_layers,
    visible_named_layers_count: pkg.visible_named_layers.length,
    hidden_named_layers_count: pkg.hidden_named_layers_count,
    hidden_layer_outputs_allowed: true,
    raw_logic_exposed: false,
    weights_exposed: false,
    formulas_exposed: false,
    public_output_sanitized: true
  };
}

function attachSaasPackagePolicy(analysis, user, options = {}) {
  const safe = analysis && typeof analysis === 'object' ? analysis : {};
  const planKey = detectPlanFromUser(user, options.plan);
  const pkg = getPackagePolicy(planKey);

  safe.saas_package_policy = {
    policy: 'NDSP_SAAS_PACKAGES_POLICY',
    active_plan: pkg.key,
    active_plan_name: pkg.name,
    markets_limit: pkg.markets_limit,
    assets_limit: pkg.assets_limit,
    daily_analysis_limit: pkg.daily_analysis_limit,
    visible_named_layers: pkg.visible_named_layers,
    visible_named_layers_count: pkg.visible_named_layers.length,
    hidden_named_layers_count: pkg.hidden_named_layers_count,
    hidden_layer_outputs_allowed: true,
    decision_depth: pkg.decision_depth,
    public_output_sanitized: true,
    raw_logic_exposed: false,
    weights_exposed: false,
    formulas_exposed: false,
    internal_scoring_exposed: false,
    source_logic_exposed: false
  };

  safe.governance = Object.assign({}, safe.governance || {}, {
    saas_package_policy_active: true,
    active_plan: pkg.key,
    visible_named_layers_count: pkg.visible_named_layers.length,
    hidden_layer_names_exposed: false,
    hidden_layer_outputs_allowed: true,
    public_output_sanitized: true,
    no_raw_logic_disclosure: true
  });

  return safe;
}

function selfTest() {
  const tests = [
    ['free', 1, 2, 1, 0],
    ['pro', 2, 20, 15, 2],
    ['elite', 'all', 100, 250, 4],
    ['institutional_suite', 'all', '250+ or contract', 'contract', 4]
  ];

  const results = tests.map(([plan, markets, assets, daily, visibleCount]) => {
    const p = getPackagePolicy(plan);

    return {
      plan,
      ok:
        p.markets_limit === markets &&
        p.assets_limit === assets &&
        p.daily_analysis_limit === daily &&
        p.visible_named_layers.length === visibleCount
    };
  });

  return {
    ok: results.every(x => x.ok),
    results
  };
}

module.exports = {
  PACKAGES,
  GLOBAL_RULES,
  normalizePlan,
  detectPlanFromUser,
  getPackagePolicy,
  publicPackages,
  layerVisibilityForPlan,
  attachSaasPackagePolicy,
  selfTest
};
