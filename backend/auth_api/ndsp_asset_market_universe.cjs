'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');

const REGISTRY_PATH = process.env.NDSP_ASSET_REGISTRY_PATH || path.resolve(
  __dirname,
  '../../docs/03-contracts/NDSP_ASSET_MASTER_REGISTRY_V1.json'
);
const CACHE_TTL_MS = Math.max(15000, Number(process.env.NDSP_MARKET_CACHE_TTL_MS || 60000));
const EXTERNAL_CONCURRENCY = Math.max(1, Math.min(12, Number(process.env.NDSP_EXTERNAL_MARKET_CONCURRENCY || 8)));

function loadRegistry() {
  const parsed = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
  const assets = Array.isArray(parsed.assets) ? parsed.assets.filter(item => item && item.status === 'active') : [];
  const symbols = assets.map(item => String(item.decision_symbol || '').trim().toUpperCase());

  if (assets.length < 50) throw new Error(`ASSET_REGISTRY_UNDERSIZED:${assets.length}`);
  if (symbols.some(symbol => !symbol)) throw new Error('ASSET_REGISTRY_EMPTY_DECISION_SYMBOL');
  if (new Set(symbols).size !== symbols.length) throw new Error('ASSET_REGISTRY_DUPLICATE_DECISION_SYMBOL');
  if (assets.some(item => !item.internal_asset_id || !item.group || !item.provider_symbols)) {
    throw new Error('ASSET_REGISTRY_REQUIRED_FIELD_MISSING');
  }

  return { metadata: parsed, assets };
}

const REGISTRY = loadRegistry();

function getJson(url, timeoutMs = 7000) {
  return new Promise(resolve => {
    let settled = false;
    const finish = value => {
      if (settled) return;
      settled = true;
      resolve(value);
    };

    try {
      const req = https.get(url, {
        timeout: timeoutMs,
        headers: {
          'User-Agent': 'NDSP-Asset-Universe/31',
          Accept: 'application/json'
        }
      }, res => {
        let raw = '';
        res.on('data', chunk => { raw += chunk; });
        res.on('end', () => {
          try {
            finish({
              ok: res.statusCode >= 200 && res.statusCode < 300,
              status: res.statusCode,
              json: JSON.parse(raw)
            });
          } catch (_) {
            finish({ ok: false, status: res.statusCode, error: 'INVALID_JSON' });
          }
        });
      });
      req.on('timeout', () => {
        try { req.destroy(); } catch (_) {}
        finish({ ok: false, error: 'TIMEOUT' });
      });
      req.on('error', error => finish({ ok: false, error: String(error && error.message || error) }));
    } catch (error) {
      finish({ ok: false, error: String(error && error.message || error) });
    }
  });
}

function finiteNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function publicShell(asset) {
  const names = asset.display_names || {};
  const providerPriority = Array.isArray(asset.provider_priority) && asset.provider_priority.length
    ? asset.provider_priority
    : Object.keys(asset.provider_symbols || {});
  return {
    group: asset.group,
    symbol: asset.decision_symbol,
    name: names.en || asset.decision_symbol,
    name_ar: names.ar || names.en || asset.decision_symbol,
    name_en: names.en || asset.decision_symbol,
    canonical_symbol: asset.canonical_symbol || asset.decision_symbol,
    price: null,
    change_pct: null,
    provider: providerPriority[0] || 'unavailable',
    provider_sources: providerPriority.map((provider, index) => ({
      provider,
      priority: index + 1,
      scope: asset.provider_scopes && asset.provider_scopes[provider] || 'configured',
      active: false
    })),
    live: false,
    data_status: 'PROVIDER_UNAVAILABLE'
  };
}

function withActiveProvider(asset, row, provider, dataStatus) {
  const active = String(dataStatus || '').startsWith('LIVE');
  return {
    ...row,
    provider,
    provider_sources: (row.provider_sources || []).map(source => ({
      ...source,
      active: active && source.provider === provider
    })),
    data_status: dataStatus
  };
}

async function fetchBinance(assets) {
  if (!assets.length) return new Map();
  const providerSymbols = assets.map(item => item.provider_symbols.binance);
  const url = `https://api.binance.com/api/v3/ticker/24hr?symbols=${encodeURIComponent(JSON.stringify(providerSymbols))}`;
  const response = await getJson(url, 8000);
  const rows = response.ok && Array.isArray(response.json) ? response.json : [];
  const bySymbol = new Map(rows.map(row => [String(row.symbol || '').toUpperCase(), row]));

  return new Map(assets.map(asset => {
    const shell = publicShell(asset);
    const row = bySymbol.get(String(asset.provider_symbols.binance).toUpperCase());
    const price = row ? finiteNumber(row.lastPrice) : null;
    const change = row ? finiteNumber(row.priceChangePercent) : null;
    return [asset.internal_asset_id, {
      ...withActiveProvider(asset, shell, 'binance', price !== null ? 'LIVE_PRIMARY' : 'PROVIDER_UNAVAILABLE'),
      price,
      change_pct: change,
      volume: row ? finiteNumber(row.volume) : null,
      live: price !== null
    }];
  }));
}

function previousDistinct(values, current) {
  for (let index = values.length - 2; index >= 0; index -= 1) {
    const value = finiteNumber(values[index]);
    if (value !== null && value !== current) return value;
  }
  return values.length > 1 ? finiteNumber(values[values.length - 2]) : null;
}

async function fetchYahooAsset(asset, fallback = false) {
  const shell = publicShell(asset);
  const providerSymbol = asset.provider_symbols.yahoo;
  const encoded = encodeURIComponent(providerSymbol);
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encoded}?range=5d&interval=1d&includePrePost=false&events=div%2Csplits`;
  const response = await getJson(url, 8000);

  try {
    const result = response.ok && response.json && response.json.chart && Array.isArray(response.json.chart.result)
      ? response.json.chart.result[0]
      : null;
    const meta = result && result.meta || {};
    const quote = result && result.indicators && Array.isArray(result.indicators.quote)
      ? result.indicators.quote[0] || {}
      : {};
    const closes = Array.isArray(quote.close) ? quote.close.filter(value => finiteNumber(value) !== null) : [];
    const price = finiteNumber(meta.regularMarketPrice) ?? finiteNumber(closes[closes.length - 1]);
    const previous = finiteNumber(meta.chartPreviousClose) ?? finiteNumber(meta.previousClose) ?? previousDistinct(closes, price);
    const change = price !== null && previous !== null && previous !== 0
      ? ((price - previous) / previous) * 100
      : null;

    return [asset.internal_asset_id, {
      ...withActiveProvider(asset, shell, 'yahoo', price !== null ? (fallback ? 'LIVE_FALLBACK' : 'LIVE_PRIMARY') : 'PROVIDER_UNAVAILABLE'),
      price,
      change_pct: finiteNumber(change),
      live: price !== null
    }];
  } catch (_) {
    return [asset.internal_asset_id, shell];
  }
}

function getText(url, timeoutMs = 7000) {
  return new Promise(resolve => {
    let settled = false;
    const finish = value => {
      if (settled) return;
      settled = true;
      resolve(value);
    };
    try {
      const req = https.get(url, {
        timeout: timeoutMs,
        headers: { 'User-Agent': 'NDSP-Asset-Universe/32', Accept: 'text/csv,text/plain,*/*' }
      }, res => {
        let raw = '';
        res.on('data', chunk => { raw += chunk; });
        res.on('end', () => finish({ ok: res.statusCode >= 200 && res.statusCode < 300, text: raw }));
      });
      req.on('timeout', () => { try { req.destroy(); } catch (_) {} finish({ ok: false, error: 'TIMEOUT' }); });
      req.on('error', error => finish({ ok: false, error: String(error && error.message || error) }));
    } catch (error) {
      finish({ ok: false, error: String(error && error.message || error) });
    }
  });
}

async function fetchStooqAsset(asset) {
  const shell = publicShell(asset);
  const providerSymbol = asset.provider_symbols && asset.provider_symbols.stooq;
  if (!providerSymbol) return [asset.internal_asset_id, shell];
  const url = `https://stooq.com/q/d/l/?s=${encodeURIComponent(providerSymbol)}&i=d`;
  const response = await getText(url, 9000);
  try {
    const lines = String(response.text || '').trim().split(/\r?\n/);
    const columns = String(lines.shift() || '').split(',');
    const closeIndex = columns.indexOf('Close');
    if (!response.ok || closeIndex < 0 || !lines.length) throw new Error('STOOQ_EMPTY');
    const closes = lines.map(line => finiteNumber(line.split(',')[closeIndex])).filter(value => value !== null);
    const price = closes[closes.length - 1] ?? null;
    const previous = previousDistinct(closes, price);
    const change = price !== null && previous !== null && previous !== 0 ? ((price - previous) / previous) * 100 : null;
    return [asset.internal_asset_id, {
      ...withActiveProvider(asset, shell, 'stooq', price !== null ? 'LIVE_FALLBACK_END_OF_DAY' : 'PROVIDER_UNAVAILABLE'),
      price,
      change_pct: finiteNumber(change),
      live: price !== null
    }];
  } catch (_) {
    return [asset.internal_asset_id, shell];
  }
}

async function mapLimited(items, limit, mapper) {
  const output = new Array(items.length);
  let cursor = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (cursor < items.length) {
      const index = cursor;
      cursor += 1;
      output[index] = await mapper(items[index]);
    }
  });
  await Promise.all(workers);
  return output;
}

let cache = { expiresAt: 0, assets: [] };
let refreshPromise = null;

async function refreshUniverse() {
  const crypto = REGISTRY.assets.filter(item => item.provider_symbols.binance);
  const nonCrypto = REGISTRY.assets.filter(item => item.group !== 'crypto' && item.provider_symbols.yahoo);
  const [binanceRows, yahooRows] = await Promise.all([
    fetchBinance(crypto),
    mapLimited(nonCrypto, EXTERNAL_CONCURRENCY, asset => fetchYahooAsset(asset, false))
  ]);
  const byId = new Map([...binanceRows.entries(), ...yahooRows]);

  const cryptoFallback = crypto.filter(asset => !byId.get(asset.internal_asset_id)?.live && asset.provider_symbols.yahoo);
  const nonCryptoFallback = nonCrypto.filter(asset => !byId.get(asset.internal_asset_id)?.live && asset.provider_symbols.stooq);
  const [cryptoFallbackRows, nonCryptoFallbackRows] = await Promise.all([
    mapLimited(cryptoFallback, EXTERNAL_CONCURRENCY, asset => fetchYahooAsset(asset, true)),
    mapLimited(nonCryptoFallback, EXTERNAL_CONCURRENCY, fetchStooqAsset)
  ]);
  for (const [id, row] of [...cryptoFallbackRows, ...nonCryptoFallbackRows]) {
    if (row && row.live) byId.set(id, row);
  }
  const assets = REGISTRY.assets.map(asset => byId.get(asset.internal_asset_id) || publicShell(asset));
  cache = { expiresAt: Date.now() + CACHE_TTL_MS, assets };
  return assets;
}

async function currentAssets() {
  if (cache.assets.length && cache.expiresAt > Date.now()) return cache.assets;
  if (!refreshPromise) {
    refreshPromise = refreshUniverse().finally(() => { refreshPromise = null; });
  }
  return refreshPromise;
}

function filterAssets(assets, group) {
  if (!group || group === 'all') return assets;
  return assets.filter(item => item.group === group);
}

async function buildPayload(group = 'all') {
  const assets = await currentAssets();
  const liveAssets = assets.filter(item => item.live && item.price !== null);
  const missingSymbols = assets.filter(item => !item.live || item.price === null).map(item => item.symbol);
  const groups = {};
  for (const asset of assets) groups[asset.group] = (groups[asset.group] || 0) + 1;
  const providers = {};
  for (const asset of REGISTRY.assets) {
    for (const provider of asset.provider_priority || Object.keys(asset.provider_symbols || {})) {
      providers[provider] = providers[provider] || { configured_assets: 0, active_assets: 0, fallback_active_assets: 0 };
      providers[provider].configured_assets += 1;
    }
  }
  for (const asset of assets) {
    if (!providers[asset.provider]) continue;
    providers[asset.provider].active_assets += 1;
    if (asset.data_status && String(asset.data_status).startsWith('LIVE_FALLBACK')) providers[asset.provider].fallback_active_assets += 1;
  }

  return {
    ok: true,
    service: 'ndsp-user-dashboard-gateway',
    generated_at: new Date().toISOString(),
    selected_group: group,
    mode: 'Decision Active / Execution Sanitized / Public Output Sanitized',
    direct_trade_execution: false,
    counts: {
      total: assets.length,
      live: liveAssets.length,
      groups,
      coverage_pct: assets.length ? Number(((liveAssets.length / assets.length) * 100).toFixed(2)) : 0,
      missing: missingSymbols.length
    },
    assets: filterAssets(assets, group),
    data_quality: {
      registry_version: REGISTRY.metadata.version,
      expected_assets: assets.length,
      live_assets: liveAssets.length,
      complete: missingSymbols.length === 0,
      missing_symbols: missingSymbols
    },
    provider_coverage: providers,
    governance: {
      decision_support_only: true,
      no_financial_advice: true,
      public_output_sanitized: true,
      raw_logic_exposed: false,
      registry_governed: true
    }
  };
}

module.exports = {
  buildPayload,
  loadRegistry,
  registryPath: REGISTRY_PATH
};
