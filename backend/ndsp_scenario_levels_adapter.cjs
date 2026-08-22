#!/usr/bin/env node
"use strict";

const http = require("http");
const https = require("https");

const PORT = Number(process.env.NDSP_SCENARIO_LEVELS_PORT || 9034);
const LIVE_PORT = Number(process.env.NDSP_LIVE_ADAPTER_PORT || 9033);
const VERSION = "ndsp-scenario-levels-adapter-v1.0.2-exact-symbol-no-fallback";

function nowIso() {
  return new Date().toISOString();
}

function normalizeSymbol(input) {
  const raw = String(input || "XAUUSD").trim().toUpperCase().replace(/\s/g, "");
  const cleaned = raw.replace(/\//g, "").replace(/-/g, "").replace(/_/g, "");

  const map = {
    "XAU": "XAUUSD",
    "GOLD": "XAUUSD",
    "GC=F": "XAUUSD",
    "GCF": "XAUUSD",
    "XAUUSD": "XAUUSD",
    "XAUUSDT": "XAUUSD",

    "XAG": "XAGUSD",
    "SILVER": "XAGUSD",
    "SI=F": "XAGUSD",
    "SIF": "XAGUSD",
    "XAGUSD": "XAGUSD",

    "OIL": "CLF",
    "WTI": "CLF",
    "CRUDE": "CLF",
    "CRUDEOIL": "CLF",
    "CL=F": "CLF",
    "CLF": "CLF",

    "EURUSD": "EURUSD",
    "EURUSDT": "EURUSD",

    "BTC": "BTCUSDT",
    "BTCUSD": "BTCUSDT",
    "BTCUSDT": "BTCUSDT",

    "ETH": "ETHUSDT",
    "ETHUSD": "ETHUSDT",
    "ETHUSDT": "ETHUSDT",

    "SOL": "SOLUSDT",
    "SOLUSD": "SOLUSDT",
    "SOLUSDT": "SOLUSDT"
  };

  return map[raw] || map[cleaned] || cleaned;
}

function requestJson(urlString, timeoutMs = 12000) {
  return new Promise((resolve, reject) => {
    const u = new URL(urlString);
    const client = u.protocol === "https:" ? https : http;

    const req = client.request({
      protocol: u.protocol,
      hostname: u.hostname,
      port: u.port || (u.protocol === "https:" ? 443 : 80),
      path: `${u.pathname}${u.search}`,
      method: "GET",
      timeout: timeoutMs,
      headers: {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "User-Agent": "NDSP-ScenarioLevelsAdapter/1.0"
      }
    }, (res) => {
      let data = "";
      res.setEncoding("utf8");
      res.on("data", chunk => { data += chunk; });
      res.on("end", () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          return reject(new Error(`HTTP_${res.statusCode}: ${data.slice(0, 180)}`));
        }
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`JSON_PARSE_FAILED: ${e.message}`));
        }
      });
    });

    req.on("timeout", () => req.destroy(new Error("REQUEST_TIMEOUT")));
    req.on("error", reject);
    req.end();
  });
}

async function getMarketPayload(symbol) {
  const urls = [
    `http://127.0.0.1:${LIVE_PORT}/api/market/prices?symbol=${encodeURIComponent(symbol)}`,
    `https://api.ndsp.app/api/market/prices?symbol=${encodeURIComponent(symbol)}`
  ];

  let lastError = null;

  for (const url of urls) {
    try {
      const payload = await requestJson(url);
      if (payload) return payload;
    } catch (e) {
      lastError = e;
    }
  }

  throw lastError || new Error("NO_MARKET_PAYLOAD");
}

function flattenPrices(x, out = []) {
  if (Array.isArray(x)) {
    x.forEach(v => flattenPrices(v, out));
    return out;
  }

  if (x && typeof x === "object") {
    const price = x.price ?? x.last_price ?? x.close ?? x.value;
    const updated = x.updated_at ?? x.last_updated ?? x.timestamp ?? x.time ?? x.as_of;
    const provider = x.provider ?? x.source ?? x.exchange ?? x.feed;
    const status = x.provider_status ?? x.data_status ?? x.status;
    const symbol = x.symbol ?? x.code ?? x.asset ?? x.ticker ?? x.s;

    if (price !== undefined && updated !== undefined && symbol !== undefined) {
      out.push({
        symbol: String(symbol || ""),
        price: Number(price),
        updated_at: String(updated || ""),
        provider: String(provider || ""),
        provider_status: String(status || "")
      });
    }

    for (const k of Object.keys(x)) {
      if (x[k] && typeof x[k] === "object") flattenPrices(x[k], out);
    }
  }

  return out;
}

function ageMinutes(iso) {
  const t = Date.parse(iso || "");
  if (!Number.isFinite(t)) return 999999;
  return Math.abs(Date.now() - t) / 60000;
}

function chooseExactFreshLive(payload, wantedSymbol) {
  const wanted = normalizeSymbol(wantedSymbol);
  const rows = flattenPrices(payload);

  const exactRows = rows.filter(r => normalizeSymbol(r.symbol) === wanted);

  for (const row of exactRows) {
    const status = String(row.provider_status || "").toLowerCase();
    if (status !== "live") continue;
    if (!Number.isFinite(row.price) || row.price <= 0) continue;

    const age = ageMinutes(row.updated_at);
    if (age > 30) continue;

    return row;
  }

  return null;
}

function decimalsFor(symbol) {
  if (symbol === "EURUSD") return 5;
  return 2;
}

function round(n, d) {
  const p = Math.pow(10, d);
  return Math.round(Number(n) * p) / p;
}

function computeLevels(symbol, price) {
  const d = decimalsFor(symbol);

  let stepA = 0.0020;
  let stepB = 0.0040;

  if (symbol === "BTCUSDT" || symbol === "ETHUSDT" || symbol === "SOLUSDT") {
    stepA = 0.0030;
    stepB = 0.0060;
  }

  if (symbol === "EURUSD") {
    stepA = 0.0010;
    stepB = 0.0020;
  }

  if (symbol === "CLF") {
    stepA = 0.0030;
    stepB = 0.0060;
  }

  return {
    arrival_price: round(price * (1 - stepB), d),
    review_price: round(price * (1 - stepA), d),
    activation_price: round(price * (1 + stepA), d),
    cancel_price: round(price * (1 + stepB), d)
  };
}

async function buildScenario(symbolInput) {
  const symbol = normalizeSymbol(symbolInput);

  let payload;
  try {
    payload = await getMarketPayload(symbol);
  } catch (e) {
    return {
      ok: false,
      symbol,
      provider_status: "unavailable",
      error: "MARKET_ADAPTER_UNREACHABLE",
      message: String(e.message || e).slice(0, 240),
      source: "ndsp_scenario_levels_adapter",
      updated_at: nowIso(),
      adapter_version: VERSION
    };
  }

  const row = chooseExactFreshLive(payload, symbol);

  if (!row) {
    return {
      ok: false,
      symbol,
      provider_status: "unavailable",
      error: "NO_EXACT_FRESH_LIVE_PRICE_FOR_SYMBOL",
      rule: "No fallback to another asset is allowed",
      market_source: payload.source || null,
      market_count: payload.count || null,
      source: "ndsp_scenario_levels_adapter",
      updated_at: nowIso(),
      adapter_version: VERSION
    };
  }

  const levels = computeLevels(symbol, row.price);

  return {
    ok: true,
    symbol,
    source: "ndsp_scenario_levels_adapter",
    provider: row.provider || "live_market_adapter",
    provider_status: "calculated_live_reference",
    calculation_basis: "exact_symbol_fresh_live_price_reference_v1",
    current_price: row.price,
    price_updated_at: row.updated_at,
    levels,
    labels: {
      arrival_price: "وصول",
      review_price: "مراجعة",
      activation_price: "تفعيل",
      cancel_price: "إلغاء"
    },
    warning: "مستويات مرجعية محسوبة من السعر الحي للرمز نفسه فقط، وليست توصية تداول.",
    updated_at: nowIso(),
    adapter_version: VERSION
  };
}

function sendJson(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": "*"
  });
  res.end(body);
}

const server = http.createServer(async (req, res) => {
  try {
    const u = new URL(req.url, "http://127.0.0.1");

    if (u.pathname === "/health" || u.pathname === "/api/scenario/levels/health") {
      return sendJson(res, 200, {
        ok: true,
        service: "ndsp-scenario-levels-adapter",
        port: PORT,
        live_adapter_port: LIVE_PORT,
        adapter_version: VERSION,
        updated_at: nowIso()
      });
    }

    if (u.pathname === "/api/scenario/levels") {
      const symbol = u.searchParams.get("symbol") || "XAUUSD";
      const out = await buildScenario(symbol);
      return sendJson(res, out.ok ? 200 : 503, out);
    }

    return sendJson(res, 404, { ok: false, error: "NOT_FOUND", path: u.pathname });
  } catch (e) {
    return sendJson(res, 500, {
      ok: false,
      error: "SCENARIO_LEVELS_ADAPTER_ERROR",
      message: String(e.message || e).slice(0, 240),
      updated_at: nowIso()
    });
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[NDSP] scenario levels adapter listening on 127.0.0.1:${PORT}`);
});
