
"use strict";

const http = require("http");
const { URL } = require("url");

const PORT = Number(process.env.NDSP_LIVE_ADAPTER_PORT || 9033);
const REFRESH_MS = Number(process.env.NDSP_MARKET_REFRESH_MS || 60000);
const STALE_MS = Number(process.env.NDSP_MARKET_STALE_MS || 180000);

const ADAPTER_VERSION = "ndsp-live-market-adapter-v2.0.0-full-universe-backend-cache";

const ASSETS = [{"source": "yahoo", "symbol": "HG", "name_ar": "النحاس", "name_en": "Copper", "category": "commodity", "upstream_symbol": "HG"}, {"source": "yahoo", "symbol": "NG", "name_ar": "الغاز الطبيعي", "name_en": "Natural Gas", "category": "commodity", "upstream_symbol": "NG"}, {"source": "yahoo", "symbol": "UKOIL", "name_ar": "برنت", "name_en": "Brent Crude Oil", "category": "commodity", "upstream_symbol": "UKOIL"}, {"source": "yahoo", "symbol": "USOIL", "name_ar": "النفط الأمريكي", "name_en": "WTI Crude Oil", "category": "commodity", "upstream_symbol": "USOIL"}, {"source": "yahoo", "symbol": "XAGUSD", "name_ar": "الفضة", "name_en": "Silver Spot", "category": "commodity", "upstream_symbol": "XAGUSD"}, {"source": "yahoo", "symbol": "XAUUSD", "name_ar": "الذهب", "name_en": "Gold Spot", "category": "commodity", "upstream_symbol": "XAUUSD"}, {"source": "yahoo", "symbol": "ZC", "name_ar": "الذرة", "name_en": "Corn", "category": "commodity", "upstream_symbol": "ZC"}, {"source": "yahoo", "symbol": "ZS", "name_ar": "فول الصويا", "name_en": "Soybeans", "category": "commodity", "upstream_symbol": "ZS"}, {"source": "yahoo", "symbol": "ZW", "name_ar": "القمح", "name_en": "Wheat", "category": "commodity", "upstream_symbol": "ZW"}, {"source": "binance", "symbol": "AAVEUSDT", "name_ar": "آفي", "name_en": "Aave", "category": "crypto", "upstream_symbol": "AAVEUSDT"}, {"source": "binance", "symbol": "ADAUSDT", "name_ar": "كاردانو", "name_en": "Cardano", "category": "crypto", "upstream_symbol": "ADAUSDT"}, {"source": "binance", "symbol": "APTUSDT", "name_ar": "أبتوس", "name_en": "Aptos", "category": "crypto", "upstream_symbol": "APTUSDT"}, {"source": "binance", "symbol": "ARBUSDT", "name_ar": "آربترم", "name_en": "Arbitrum", "category": "crypto", "upstream_symbol": "ARBUSDT"}, {"source": "binance", "symbol": "ATOMUSDT", "name_ar": "كوزموس", "name_en": "Cosmos", "category": "crypto", "upstream_symbol": "ATOMUSDT"}, {"source": "binance", "symbol": "AVAXUSDT", "name_ar": "أفالانش", "name_en": "Avalanche", "category": "crypto", "upstream_symbol": "AVAXUSDT"}, {"source": "binance", "symbol": "BCHUSDT", "name_ar": "بيتكوين كاش", "name_en": "Bitcoin Cash", "category": "crypto", "upstream_symbol": "BCHUSDT"}, {"source": "binance", "symbol": "BNBUSDT", "name_ar": "بي إن بي", "name_en": "BNB", "category": "crypto", "upstream_symbol": "BNBUSDT"}, {"source": "binance", "symbol": "BTCUSDT", "name_ar": "بيتكوين", "name_en": "Bitcoin", "category": "crypto", "upstream_symbol": "BTCUSDT"}, {"source": "binance", "symbol": "DOGEUSDT", "name_ar": "دوجكوين", "name_en": "Dogecoin", "category": "crypto", "upstream_symbol": "DOGEUSDT"}, {"source": "binance", "symbol": "DOTUSDT", "name_ar": "بولكادوت", "name_en": "Polkadot", "category": "crypto", "upstream_symbol": "DOTUSDT"}, {"source": "binance", "symbol": "ETHUSDT", "name_ar": "إيثريوم", "name_en": "Ethereum", "category": "crypto", "upstream_symbol": "ETHUSDT"}, {"source": "binance", "symbol": "INJUSDT", "name_ar": "إنجكتف", "name_en": "Injective", "category": "crypto", "upstream_symbol": "INJUSDT"}, {"source": "binance", "symbol": "LINKUSDT", "name_ar": "تشين لينك", "name_en": "Chainlink", "category": "crypto", "upstream_symbol": "LINKUSDT"}, {"source": "binance", "symbol": "LTCUSDT", "name_ar": "لايتكوين", "name_en": "Litecoin", "category": "crypto", "upstream_symbol": "LTCUSDT"}, {"source": "binance", "symbol": "NEARUSDT", "name_ar": "نير", "name_en": "NEAR Protocol", "category": "crypto", "upstream_symbol": "NEARUSDT"}, {"source": "binance", "symbol": "OPUSDT", "name_ar": "أوبتيمزم", "name_en": "Optimism", "category": "crypto", "upstream_symbol": "OPUSDT"}, {"source": "binance", "symbol": "SOLUSDT", "name_ar": "سولانا", "name_en": "Solana", "category": "crypto", "upstream_symbol": "SOLUSDT"}, {"source": "binance", "symbol": "TRXUSDT", "name_ar": "ترون", "name_en": "TRON", "category": "crypto", "upstream_symbol": "TRXUSDT"}, {"source": "binance", "symbol": "UNIUSDT", "name_ar": "يونيسواب", "name_en": "Uniswap", "category": "crypto", "upstream_symbol": "UNIUSDT"}, {"source": "binance", "symbol": "XRPUSDT", "name_ar": "ريبل", "name_en": "XRP", "category": "crypto", "upstream_symbol": "XRPUSDT"}, {"source": "yahoo", "symbol": "AUDUSD", "name_ar": "الأسترالي دولار", "name_en": "Australian Dollar / US Dollar", "category": "forex", "upstream_symbol": "AUDUSD"}, {"source": "yahoo", "symbol": "EURGBP", "name_ar": "اليورو باوند", "name_en": "Euro / British Pound", "category": "forex", "upstream_symbol": "EURGBP"}, {"source": "yahoo", "symbol": "EURJPY", "name_ar": "اليورو ين", "name_en": "Euro / Japanese Yen", "category": "forex", "upstream_symbol": "EURJPY"}, {"source": "yahoo", "symbol": "EURUSD", "name_ar": "اليورو دولار", "name_en": "Euro / US Dollar", "category": "forex", "upstream_symbol": "EURUSD"}, {"source": "yahoo", "symbol": "GBPJPY", "name_ar": "الباوند ين", "name_en": "British Pound / Japanese Yen", "category": "forex", "upstream_symbol": "GBPJPY"}, {"source": "yahoo", "symbol": "GBPUSD", "name_ar": "الباوند دولار", "name_en": "British Pound / US Dollar", "category": "forex", "upstream_symbol": "GBPUSD"}, {"source": "yahoo", "symbol": "NZDUSD", "name_ar": "النيوزلندي دولار", "name_en": "New Zealand Dollar / US Dollar", "category": "forex", "upstream_symbol": "NZDUSD"}, {"source": "yahoo", "symbol": "USDCAD", "name_ar": "الدولار كندي", "name_en": "US Dollar / Canadian Dollar", "category": "forex", "upstream_symbol": "USDCAD"}, {"source": "yahoo", "symbol": "USDCHF", "name_ar": "الدولار فرنك", "name_en": "US Dollar / Swiss Franc", "category": "forex", "upstream_symbol": "USDCHF"}, {"source": "yahoo", "symbol": "USDJPY", "name_ar": "الدولار ين", "name_en": "US Dollar / Japanese Yen", "category": "forex", "upstream_symbol": "USDJPY"}, {"source": "yahoo", "symbol": "CAC", "name_ar": "كاك الفرنسي", "name_en": "CAC 40", "category": "index", "upstream_symbol": "CAC"}, {"source": "yahoo", "symbol": "DAX", "name_ar": "داكس الألماني", "name_en": "DAX", "category": "index", "upstream_symbol": "DAX"}, {"source": "yahoo", "symbol": "DJI", "name_ar": "داو جونز", "name_en": "Dow Jones Industrial Average", "category": "index", "upstream_symbol": "DJI"}, {"source": "yahoo", "symbol": "DXY", "name_ar": "مؤشر الدولار", "name_en": "US Dollar Index", "category": "index", "upstream_symbol": "DXY"}, {"source": "yahoo", "symbol": "FTSE", "name_ar": "فوتسي 100", "name_en": "FTSE 100", "category": "index", "upstream_symbol": "FTSE"}, {"source": "yahoo", "symbol": "HSI", "name_ar": "هانغ سنغ", "name_en": "Hang Seng Index", "category": "index", "upstream_symbol": "HSI"}, {"source": "yahoo", "symbol": "N225", "name_ar": "نيكاي 225", "name_en": "Nikkei 225", "category": "index", "upstream_symbol": "N225"}, {"source": "yahoo", "symbol": "NDX", "name_ar": "ناسداك 100", "name_en": "Nasdaq 100", "category": "index", "upstream_symbol": "NDX"}, {"source": "yahoo", "symbol": "RUT", "name_ar": "راسل 2000", "name_en": "Russell 2000", "category": "index", "upstream_symbol": "RUT"}, {"source": "yahoo", "symbol": "SPX", "name_ar": "ستاندرد آند بورز 500", "name_en": "S&P 500", "category": "index", "upstream_symbol": "SPX"}, {"source": "yahoo", "symbol": "VIX", "name_ar": "مؤشر الخوف", "name_en": "CBOE Volatility Index", "category": "index", "upstream_symbol": "VIX"}];

const cache = new Map();
let lastRefreshAt = null;
let lastErrors = [];

function nowIso() {
  return new Date().toISOString();
}

function clean(x) {
  return String(x || "").trim();
}

function num(x) {
  const n = Number(x);
  return Number.isFinite(n) ? n : null;
}

function isCrypto(asset) {
  const c = clean(asset.category).toLowerCase();
  const s = clean(asset.symbol).toUpperCase();
  return c.includes("crypto") || s.endsWith("USDT");
}

function providerOf(asset) {
  const source = clean(asset.source).toLowerCase();
  const category = clean(asset.category).toLowerCase();

  if (isCrypto(asset)) return "binance";
  if (source.includes("binance")) return "binance";
  if (source.includes("fxcm")) return "fxcm";
  if (source.includes("yahoo")) return "yahoo";
  if (category.includes("forex")) return "yahoo";
  if (category.includes("commodity") || category.includes("metal") || category.includes("index")) return "yahoo";

  return source || "unknown";
}

function yahooSymbol(asset) {
  const s = clean(asset.symbol || asset.upstream_symbol).toUpperCase();

  const map = {
    "XAUUSD": "GC=F",
    "XAU": "GC=F",
    "GOLD": "GC=F",
    "XAGUSD": "SI=F",
    "XAG": "SI=F",
    "SILVER": "SI=F",
    "HG": "HG=F",
    "COPPER": "HG=F",
    "PL": "PL=F",
    "PA": "PA=F",
    "USOIL": "CL=F",
    "CLF": "CL=F",
    "CL=F": "CL=F",
    "UKOIL": "BZ=F",
    "BRENT": "BZ=F",
    "NG": "NG=F",
    "ZC": "ZC=F",
    "ZS": "ZS=F",
    "ZW": "ZW=F",

    "SPX": "^GSPC",
    "NDX": "^IXIC",
    "NASDAQ": "^IXIC",
    "DJI": "^DJI",
    "DOW": "^DJI",
    "RUT": "^RUT",
    "VIX": "^VIX",
    "DXY": "DX-Y.NYB",
    "N225": "^N225",
    "FTSE": "^FTSE",
    "DAX": "^GDAXI",
    "CAC": "^FCHI",
    "HSI": "^HSI"
  };

  if (map[s]) return map[s];

  if (/^[A-Z]{6}$/.test(s)) return s + "=X";
  if (s.includes("/")) return s.replace("/", "") + "=X";

  return clean(asset.upstream_symbol || asset.symbol);
}

function publicSymbol(asset) {
  return clean(asset.symbol || asset.upstream_symbol).toUpperCase();
}

async function fetchJson(url, timeoutMs = 12000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const r = await fetch(url, {
      signal: controller.signal,
      headers: { "User-Agent": "NDSP-Market-Adapter/2.0" },
      cache: "no-store"
    });

    if (!r.ok) {
      throw new Error("HTTP_" + r.status);
    }

    return await r.json();
  } finally {
    clearTimeout(timer);
  }
}

async function fetchBinance(asset) {
  const symbol = publicSymbol(asset);
  const url = "https://api.binance.com/api/v3/ticker/24hr?symbol=" + encodeURIComponent(symbol);
  const d = await fetchJson(url);

  return {
    symbol,
    upstream_symbol: symbol,
    name_ar: clean(asset.name_ar || symbol),
    name_en: clean(asset.name_en || symbol),
    category: clean(asset.category || "crypto"),
    source: "binance",
    provider: "binance",
    price: num(d.lastPrice),
    change_24h: num(d.priceChange),
    change_pct: num(d.priceChangePercent),
    high_24h: num(d.highPrice),
    low_24h: num(d.lowPrice),
    volume: num(d.volume),
    updated_at: nowIso(),
    status: "active",
    provider_status: "live",
    freshness: "fresh",
    adapter_version: ADAPTER_VERSION
  };
}

async function fetchYahoo(asset) {
  const symbol = publicSymbol(asset);
  const upstream = yahooSymbol(asset);
  const url = "https://query1.finance.yahoo.com/v8/finance/chart/" +
    encodeURIComponent(upstream) +
    "?range=1d&interval=5m";

  const d = await fetchJson(url);
  const result = d && d.chart && d.chart.result && d.chart.result[0];

  if (!result) throw new Error("YAHOO_EMPTY_RESULT");

  const meta = result.meta || {};
  const quote = result.indicators && result.indicators.quote && result.indicators.quote[0] || {};

  const closes = (quote.close || []).map(num).filter(v => v !== null);
  const highs = (quote.high || []).map(num).filter(v => v !== null);
  const lows = (quote.low || []).map(num).filter(v => v !== null);
  const vols = (quote.volume || []).map(num).filter(v => v !== null);

  const price = num(meta.regularMarketPrice) ?? closes[closes.length - 1] ?? null;
  const previous = num(meta.chartPreviousClose) ?? null;
  const change = price !== null && previous ? price - previous : null;
  const changePct = change !== null && previous ? (change / previous) * 100 : null;

  return {
    symbol,
    upstream_symbol: upstream,
    name_ar: clean(asset.name_ar || symbol),
    name_en: clean(asset.name_en || symbol),
    category: clean(asset.category || "unknown"),
    source: clean(asset.source || "yahoo"),
    provider: "yahoo",
    price,
    change_24h: change,
    change_pct: changePct,
    high_24h: highs.length ? Math.max(...highs) : null,
    low_24h: lows.length ? Math.min(...lows) : null,
    volume: vols.length ? vols[vols.length - 1] : null,
    provider_time: meta.regularMarketTime ? new Date(meta.regularMarketTime * 1000).toISOString() : null,
    updated_at: nowIso(),
    status: "active",
    provider_status: "live",
    freshness: "fresh",
    adapter_version: ADAPTER_VERSION
  };
}

async function fetchAsset(asset) {
  const provider = providerOf(asset);

  if (provider === "binance") return await fetchBinance(asset);
  return await fetchYahoo(asset);
}

async function refreshOne(asset) {
  const symbol = publicSymbol(asset);

  try {
    const row = await fetchAsset(asset);

    if (row.price === null || row.price === undefined) {
      throw new Error("NO_PRICE");
    }

    cache.set(symbol, row);
    return { ok: true, symbol };
  } catch (e) {
    const old = cache.get(symbol);
    if (old) {
      old.provider_status = "stale";
      old.freshness = "stale";
      old.error = String(e.message || e).slice(0, 160);
      cache.set(symbol, old);
    }

    return {
      ok: false,
      symbol,
      error: String(e.message || e).slice(0, 160)
    };
  }
}

async function refreshAll() {
  const errors = [];
  const started = Date.now();

  for (const asset of ASSETS) {
    const r = await refreshOne(asset);
    if (!r.ok) errors.push(r);
  }

  lastRefreshAt = nowIso();
  lastErrors = errors.slice(0, 80);

  console.log(
    "[NDSP] market refresh",
    "assets=" + ASSETS.length,
    "cached=" + cache.size,
    "errors=" + errors.length,
    "ms=" + (Date.now() - started)
  );
}

function withJson(res, status, body) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization"
  });
  res.end(JSON.stringify(body));
}

function getSnapshot(symbol) {
  const s = clean(symbol).toUpperCase();
  const row = cache.get(s);

  if (!row) {
    const asset = ASSETS.find(a => publicSymbol(a) === s);

    return {
      ok: true,
      symbol: s,
      found: false,
      price: null,
      freshness: "missing",
      provider_status: "missing",
      reference_reading: "pending",
      asset: asset || null,
      updated_at: null,
      adapter_version: ADAPTER_VERSION
    };
  }

  const ageMs = Date.now() - new Date(row.updated_at).getTime();
  const freshness = ageMs <= STALE_MS ? "fresh" : "stale";

  return {
    ok: true,
    ...row,
    freshness,
    provider_status: freshness === "fresh" ? "live" : "stale",
    reference_reading: "pending"
  };
}

function pricesResponse(url) {
  const category = clean(url.searchParams.get("category")).toLowerCase();
  const symbol = clean(url.searchParams.get("symbol")).toUpperCase();

  let rows = Array.from(cache.values());

  if (symbol) rows = rows.filter(r => clean(r.symbol).toUpperCase() === symbol);
  if (category) rows = rows.filter(r => clean(r.category).toLowerCase() === category);

  rows.sort((a, b) => clean(a.symbol).localeCompare(clean(b.symbol)));

  return {
    ok: true,
    source: "ndsp_live_market_adapter",
    provider_status: "live",
    count: rows.length,
    total_assets: ASSETS.length,
    cached_count: cache.size,
    prices: rows,
    errors: lastErrors,
    fetched_at: lastRefreshAt || nowIso(),
    adapter_version: ADAPTER_VERSION
  };
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === "OPTIONS") {
      return withJson(res, 200, { ok: true });
    }

    const url = new URL(req.url, "http://127.0.0.1:" + PORT);

    if (url.pathname === "/health") {
      return withJson(res, 200, {
        ok: true,
        service: "ndsp-live-market-adapter",
        port: PORT,
        assets: ASSETS.length,
        cached_count: cache.size,
        last_refresh_at: lastRefreshAt,
        adapter_version: ADAPTER_VERSION,
        updated_at: nowIso()
      });
    }

    if (url.pathname === "/api/market/prices") {
      return withJson(res, 200, pricesResponse(url));
    }

    if (url.pathname === "/api/market/snapshot") {
      const symbol = url.searchParams.get("symbol");
      if (!symbol) {
        return withJson(res, 400, {
          ok: false,
          error: "SYMBOL_REQUIRED",
          adapter_version: ADAPTER_VERSION
        });
      }

      return withJson(res, 200, getSnapshot(symbol));
    }

    if (url.pathname === "/api/market/refresh") {
      refreshAll().catch(e => console.error("[NDSP] manual refresh failed", e));
      return withJson(res, 202, {
        ok: true,
        refresh: "queued",
        adapter_version: ADAPTER_VERSION
      });
    }

    return withJson(res, 404, {
      ok: false,
      error: "NOT_FOUND",
      path: url.pathname
    });
  } catch (e) {
    return withJson(res, 500, {
      ok: false,
      error: "ADAPTER_ERROR",
      detail: String(e.message || e).slice(0, 180),
      adapter_version: ADAPTER_VERSION
    });
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log("[NDSP] live market adapter listening on 127.0.0.1:" + PORT);
  console.log("[NDSP] adapter version " + ADAPTER_VERSION);
  refreshAll().catch(e => console.error("[NDSP] initial refresh failed", e));
  setInterval(() => {
    refreshAll().catch(e => console.error("[NDSP] scheduled refresh failed", e));
  }, REFRESH_MS);
});
