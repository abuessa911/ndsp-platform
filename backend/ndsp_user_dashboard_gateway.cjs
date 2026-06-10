
// NDSP_PUBLIC_ANALYZE_RESPONSE_SANITIZER_BEGIN
function ndspSanitizeAnalyzePublicOutput(obj) {
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

  function walk(x) {
    if (!x || typeof x !== 'object') return x;

    if (Array.isArray(x)) {
      x.forEach(walk);
      return x;
    }

    for (const key of Object.keys(x)) {
      if (blocked.has(key)) {
        delete x[key];
        continue;
      }

      walk(x[key]);
    }

    return x;
  }

  return walk(obj);
}
// NDSP_PUBLIC_ANALYZE_RESPONSE_SANITIZER_END


'use strict';

const http = require('http');
const https = require('https');
const tdlAddons = require('./ndsp_tdl_trade_horizon_addons.cjs');
const layerNameMaskingPolicy = require('./ndsp_layer_name_masking_policy.cjs');
const saasPackagesPolicy = require('./ndsp_saas_packages_policy.cjs');

const PORT = Number(process.env.NDSP_USER_DASHBOARD_PORT || 9021);

const CRYPTO_SYMBOLS = [
  'BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT',
  'ADAUSDT','AVAXUSDT','LINKUSDT','DOGEUSDT','TONUSDT'
];

const FX_PAIRS = [
  ['EURUSD','EUR','USD'],
  ['GBPUSD','GBP','USD'],
  ['USDJPY','USD','JPY'],
  ['USDCHF','USD','CHF'],
  ['AUDUSD','AUD','USD'],
  ['USDCAD','USD','CAD']
];

const MARKET_PROXIES = [
  ['SPY','S&P 500 ETF Proxy','indices'],
  ['QQQ','Nasdaq 100 ETF Proxy','indices'],
  ['DIA','Dow Jones ETF Proxy','indices'],
  ['IWM','Russell 2000 ETF Proxy','indices'],
  ['GLD','Gold ETF Proxy','commodities'],
  ['USO','Oil ETF Proxy','commodities']
];

function send(res, code, obj) {
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(JSON.stringify(obj));
}

function envAny(...keys) {
  for (const k of keys) {
    const v = process.env[k];
    if (v && String(v).trim()) {
      return String(v).trim().replace(/^["']|["']$/g, '');
    }
  }
  return '';
}

function getJson(url, timeoutMs = 9000) {
  return new Promise((resolve) => {
    try {
      const req = https.get(url, {
        timeout: timeoutMs,
        headers: {
          'User-Agent': 'NDSP/1.0',
          'Accept': 'application/json'
        }
      }, (res) => {
        let raw = '';
        res.on('data', chunk => { raw += chunk; });
        res.on('end', () => {
          try {
            resolve({
              ok: res.statusCode >= 200 && res.statusCode < 300,
              status: res.statusCode,
              json: JSON.parse(raw)
            });
          } catch (_) {
            resolve({ ok:false, status:res.statusCode, error:'INVALID_JSON' });
          }
        });
      });

      req.on('timeout', () => {
        try { req.destroy(); } catch (_) {}
        resolve({ ok:false, error:'TIMEOUT' });
      });

      req.on('error', (e) => {
        resolve({ ok:false, error:String(e && e.message ? e.message : e) });
      });
    } catch (e) {
      resolve({ ok:false, error:String(e && e.message ? e.message : e) });
    }
  });
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let raw = '';

    req.on('data', chunk => {
      raw += chunk;
      if (raw.length > 1024 * 1024) {
        reject(new Error('BODY_TOO_LARGE'));
        req.destroy();
      }
    });

    req.on('end', () => {
      if (!raw.trim()) return resolve({});
      try { resolve(JSON.parse(raw)); }
      catch (_) { reject(new Error('INVALID_JSON')); }
    });

    req.on('error', reject);
  });
}

async function binanceCrypto() {
  const url = `https://api.binance.com/api/v3/ticker/24hr?symbols=${encodeURIComponent(JSON.stringify(CRYPTO_SYMBOLS))}`;
  const r = await getJson(url, 9000);

  if (!r.ok || !Array.isArray(r.json)) {
    return CRYPTO_SYMBOLS.map(s => ({
      group:'crypto',
      symbol:s,
      name:s.replace('USDT','/USDT'),
      price:null,
      change_pct:null,
      provider:'binance',
      live:false
    }));
  }

  return r.json.map(x => ({
    group:'crypto',
    symbol:x.symbol,
    name:x.symbol.replace('USDT','/USDT'),
    price:Number(x.lastPrice),
    change_pct:Number(x.priceChangePercent),
    volume:Number(x.volume),
    provider:'binance',
    live:true
  }));
}

async function alphaFx() {
  const key = envAny('ALPHA_VANTAGE_API_KEY','ALPHAVANTAGE_API_KEY','ALPHA_VANTAGE_KEY','ALPHA_KEY');

  if (!key) {
    return FX_PAIRS.map(([symbol, from, to]) => ({
      group:'forex',
      symbol,
      name:`${from}/${to}`,
      price:null,
      change_pct:null,
      provider:'alpha_vantage',
      live:false
    }));
  }

  const assets = [];

  for (const [symbol, from, to] of FX_PAIRS) {
    const url = `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=${from}&to_currency=${to}&apikey=${encodeURIComponent(key)}`;
    const r = await getJson(url, 9000);
    const data = r.json && r.json['Realtime Currency Exchange Rate'];

    assets.push({
      group:'forex',
      symbol,
      name:`${from}/${to}`,
      price:r.ok && data ? Number(data['5. Exchange Rate']) : null,
      change_pct:null,
      provider:'alpha_vantage',
      live:Boolean(r.ok && data)
    });
  }

  return assets;
}

async function alphaProxies() {
  const key = envAny('ALPHA_VANTAGE_API_KEY','ALPHAVANTAGE_API_KEY','ALPHA_VANTAGE_KEY','ALPHA_KEY');

  if (!key) {
    return MARKET_PROXIES.map(([symbol, name, group]) => ({
      group,
      symbol,
      name,
      price:null,
      change_pct:null,
      provider:'alpha_vantage',
      live:false
    }));
  }

  const assets = [];

  for (const [symbol, name, group] of MARKET_PROXIES) {
    const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${encodeURIComponent(symbol)}&apikey=${encodeURIComponent(key)}`;
    const r = await getJson(url, 9000);
    const q = r.json && r.json['Global Quote'];
    const pct = q && q['10. change percent'] ? String(q['10. change percent']).replace('%','') : null;

    assets.push({
      group,
      symbol,
      name,
      price:r.ok && q && q['05. price'] ? Number(q['05. price']) : null,
      change_pct:pct === null ? null : Number(pct),
      provider:'alpha_vantage',
      live:Boolean(r.ok && q && q['05. price'])
    });
  }

  return assets;
}

function filterAssets(assets, group) {
  if (!group || group === 'all') return assets;
  return assets.filter(x => x.group === group);
}

async function buildPayload(group = 'all') {
  const [crypto, fx, proxies] = await Promise.all([
    binanceCrypto(),
    alphaFx(),
    alphaProxies()
  ]);

  const assets = [...crypto, ...fx, ...proxies];

  return {
    ok:true,
    service:'ndsp-user-dashboard-gateway',
    generated_at:new Date().toISOString(),
    selected_group:group,
    mode:'Decision Active / Execution Sanitized / Public Output Sanitized',
    direct_trade_execution:false,
    counts:{
      total:assets.length,
      live:assets.filter(x => x.live).length,
      groups:{
        crypto:assets.filter(x => x.group === 'crypto').length,
        forex:assets.filter(x => x.group === 'forex').length,
        commodities:assets.filter(x => x.group === 'commodities').length,
        indices:assets.filter(x => x.group === 'indices').length
      }
    },
    assets:filterAssets(assets, group),
    governance:{
      decision_support_only:true,
      no_financial_advice:true,
      public_output_sanitized:true,
      raw_logic_exposed:false
    }
  };
}

function simpleDirection(changePct) {
  if (changePct === null || changePct === undefined || Number.isNaN(Number(changePct))) {
    return { label:'غير كافٍ', confidence:'منخفضة', risk:'متوسط' };
  }

  const x = Number(changePct);

  if (x >= 2) return { label:'ميل صاعد سياقي', confidence:'متوسطة', risk:'متوسط' };
  if (x >= 0.35) return { label:'تحسن محدود', confidence:'منخفضة إلى متوسطة', risk:'متوسط' };
  if (x <= -2) return { label:'ضغط هابط سياقي', confidence:'متوسطة', risk:'مرتفع' };
  if (x <= -0.35) return { label:'ضعف محدود', confidence:'منخفضة إلى متوسطة', risk:'متوسط' };

  return { label:'حياد / تذبذب ضيق', confidence:'منخفضة', risk:'متوسط' };
}

function finalLayerPolicy() {
  return {
    hidden_layers:{
      layer_numbers:[8,9,10,11,12,16],
      hidden_during_trial:true,
      hidden_after_trial:true,
      hidden_in_all_plans:true,
      names_exposed:false,
      raw_logic_exposed:false,
      weights_exposed:false,
      formulas_exposed:false,
      calculation_method_exposed:false
    },
    visible_layers:[
      { label:'TDL', visible_during_trial:true, visible_after_trial_by_plan:true },
      { label:'NMP', visible_during_trial:true, visible_after_trial_by_plan:true },
      { label:"Devil's Advocate", visible_during_trial:true, visible_after_trial_by_plan:true },
      { label:'Golden Alignment', visible_during_trial:true, visible_after_trial_by_plan:true }
    ],
    governance:{
      decision_active:true,
      execution_sanitized:true,
      public_output_sanitized:true,
      direct_trade_execution:false,
      no_raw_logic_disclosure:true
    }
  };
}

function buildSafeAnalysis(asset) {
  const d = simpleDirection(asset.change_pct);

  return {
    selected_symbol:asset.symbol,
    selected_name:asset.name,
    group:asset.group,
    provider:asset.provider,
    live:Boolean(asset.live),
    reading:{
      title:`قراءة مبسطة لـ ${asset.name || asset.symbol}`,
      context_label:d.label,
      confidence_label:d.confidence,
      risk_level:d.risk,
      plain_summary:[
        asset.live ? 'البيانات متصلة بمصدر حي.' : 'هذا الأصل ينتظر مفتاح مزود بيانات أو يعمل بوضع fallback.',
        asset.price === null || asset.price === undefined ? 'السعر غير متاح من المصدر الحالي.' : `السعر الحالي المقروء: ${asset.price}`,
        asset.change_pct === null || asset.change_pct === undefined ? 'نسبة التغير غير متاحة.' : `نسبة التغير: ${Number(asset.change_pct).toFixed(2)}%.`,
        'هذه القراءة تصف السياق الحالي فقط ولا تعني أمر شراء أو بيع.',
        'استخدمها لفهم الحالة العامة قبل اتخاذ أي قرار مستقل.'
      ]
    },
    frameworks:{
      tdl:{ visible:true, label:'TDL' },
      nmp:{ visible:true, label:'NMP' },
      devils_advocate:{ visible:true, label:"Devil's Advocate" },
      golden_alignment:{ visible:true, label:'Golden Alignment' }
    },
    layer_visibility_policy:finalLayerPolicy(),
    protected_layers:{
      hidden_layer_numbers:[8,9,10,11,12,16],
      hidden_permanently:true,
      hidden_during_trial:true,
      hidden_after_trial:true,
      raw_logic_exposed:false,
      weights_exposed:false,
      formulas_exposed:false,
      calculation_method_exposed:false,
      public_output_sanitized:true
    },
    governance:{
      decision_support_only:true,
      direct_trade_execution:false,
      no_financial_advice:true,
      public_output_sanitized:true
    }
  };
}

const server = http.createServer(async (req, res) => {
  try {
    const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);

    if (req.method === 'GET' && u.pathname === '/api/user-dashboard/health') {
      return send(res, 200, {
        ok:true,
        service:'ndsp-user-dashboard-gateway',
        endpoints:[
          '/api/user-dashboard/health',
          '/api/user-dashboard/markets?group=all|crypto|forex|commodities|indices',
          '/api/user-dashboard/analyze'
        ],
        policy:{
          hidden_always:[8,9,10,11,12,16],
          visible_during_trial:['TDL','NMP',"Devil's Advocate",'Golden Alignment']
        }
      });
    }

    if (req.method === 'GET' && (u.pathname === '/api/user-dashboard/markets' || u.pathname === '/api/user-dashboard/brief')) {
      const group = String(u.searchParams.get('group') || 'all').toLowerCase();
      const payload = await buildPayload(group);
      return send(res, 200, payload);
    }

    if (req.method === 'POST' && u.pathname === '/api/user-dashboard/analyze') {
      const body = await readJson(req);
      const symbol = String(body.symbol || '').trim().toUpperCase();

      if (!symbol) {
        return send(res, 400, { ok:false, error:'SYMBOL_REQUIRED' });
      }

      const payload = await buildPayload('all');
      const asset = payload.assets.find(x => String(x.symbol || '').toUpperCase() === symbol);

      if (!asset) {
        return send(res, 404, { ok:false, error:'ASSET_NOT_FOUND', symbol });
      }

      return send(res, 200, {
        ok:true,
        generated_at:new Date().toISOString(),
        analysis:saasPackagesPolicy.attachSaasPackagePolicy(layerNameMaskingPolicy.sanitizeAnalysisForPublic(tdlAddons.attachTdlTradeHorizonAddons(asset, buildSafeAnalysis(asset))), (typeof req !== 'undefined' ? req.user : null), { plan: (typeof req !== 'undefined' && req.query ? req.query.plan : undefined) })
      });
    }

    return send(res, 404, { ok:false, error:'NOT_FOUND', path:u.pathname });

  } catch (e) {
    return send(res, 500, {
      ok:false,
      error:'USER_DASHBOARD_GATEWAY_EXCEPTION',
      detail:String(e && e.message ? e.message : e)
    });
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] user dashboard gateway listening on 127.0.0.1:${PORT}`);
});


/* NDSP_SAAS_PACKAGES_POLICY_ENDPOINT_BEGIN */
try {
  if (typeof app !== 'undefined' && app && typeof app.get === 'function') {
    app.get('/api/user-dashboard/saas-policy', (req, res) => {
      const plan = (req.query && req.query.plan) || (req.user && req.user.plan) || 'free';
      res.json({
        ok: true,
        service: 'ndsp-user-dashboard-gateway',
        endpoint: '/api/user-dashboard/saas-policy',
        active_plan: saasPackagesPolicy.normalizePlan(plan),
        policy: saasPackagesPolicy.publicPackages(),
        effective_visibility: saasPackagesPolicy.layerVisibilityForPlan(plan)
      });
    });
  }
} catch (_) {}
/* NDSP_SAAS_PACKAGES_POLICY_ENDPOINT_END */

