import http from "http";
import fs from "fs";
import path from "path";

const PORT = Number(process.env.PORT || 9044);
const PRIVATE_ROOT = "/home/nawaf511/empire-core-new/backend/runtime/private_governance";

function readJson(name, fallback = {}) {
  try {
    const p = path.join(PRIVATE_ROOT, name);
    if (fs.existsSync(p)) return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch (_) {}
  return fallback;
}

const CRYPTO_BASES = new Set([
  "BTC","ETH","SOL","BNB","XRP","ADA","DOGE","AVAX","LINK",
  "DOT","MATIC","LTC","BCH","TRX","TON","NEAR","ATOM","UNI","SHIB"
]);

function normalizeSymbol(symbol) {
  return String(symbol || "").trim().toUpperCase().replace(/[\/\-_]/g, "");
}

function isCrypto(symbol) {
  const s = normalizeSymbol(symbol);
  if (s.endsWith("USDT")) return CRYPTO_BASES.has(s.slice(0, -4));
  if (s.endsWith("USD")) return CRYPTO_BASES.has(s.slice(0, -3));
  return CRYPTO_BASES.has(s);
}

function toBinanceSymbol(symbol) {
  const s = normalizeSymbol(symbol);
  if (s.endsWith("USDT")) return s;
  if (s.endsWith("USD") && CRYPTO_BASES.has(s.slice(0, -3))) return s.slice(0, -3) + "USDT";
  if (CRYPTO_BASES.has(s)) return s + "USDT";
  return s;
}

function packagePolicy(planRaw) {
  const plan = String(planRaw || "free").toLowerCase();

  if (plan === "saas" || plan === "institutional") {
    return {
      plan: "SAAS",
      markets: ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","SHIBUSDT","EURUSD","GBPUSD","USDJPY","XAUUSD","US100","US500","US30","USOIL","UKOIL"],
      max_alerts: 999,
      api_access: true,
      governance_access: true,
      websocket_access: true,
      runtime_level: "FULL_INFRASTRUCTURE"
    };
  }

  if (plan === "elite" || plan === "elite_trial") {
    return {
      plan: "ELITE",
      markets: ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","EURUSD","GBPUSD","USDJPY","AUDUSD","XAUUSD","XAGUSD","US100","US500","US30","USOIL","UKOIL"],
      max_alerts: 100,
      api_access: true,
      governance_access: true,
      websocket_access: true,
      runtime_level: "INSTITUTIONAL"
    };
  }

  if (plan === "pro") {
    return {
      plan: "PRO",
      markets: ["BTCUSDT","ETHUSDT","EURUSD","GBPUSD"],
      max_alerts: 25,
      api_access: false,
      governance_access: false,
      websocket_access: false,
      runtime_level: "PROFESSIONAL"
    };
  }

  return {
    plan: "FREE",
    markets: ["AUDUSD"],
    max_alerts: 5,
    api_access: false,
    governance_access: false,
    websocket_access: false,
    runtime_level: "PREVIEW"
  };
}

function sanitizeText(value) {
  let text = value == null ? "" : String(value);
  const pairs = [
    [/\bbuy now\b/gi, "سياق اتجاهي صاعد"],
    [/\bsell now\b/gi, "سياق اتجاهي هابط"],
    [/\bbuy\b/gi, "سياق صاعد"],
    [/\bsell\b/gi, "سياق هابط"],
    [/\bentry\b/gi, "مستوى تفعيل السيناريو"],
    [/\btake profit\b/gi, "مستوى وصول السيناريو"],
    [/\bstop loss\b/gi, "مستوى إلغاء السيناريو"],
    [/شراء الآن/g, "سياق اتجاهي صاعد"],
    [/بيع الآن/g, "سياق اتجاهي هابط"],
    [/شراء/g, "سياق صاعد"],
    [/بيع/g, "سياق هابط"],
    [/دخول/g, "مستوى تفعيل السيناريو"],
    [/جني ربح/g, "مستوى وصول السيناريو"],
    [/وقف خسارة/g, "مستوى إلغاء السيناريو"]
  ];
  for (const [re, repl] of pairs) text = text.replace(re, repl);
  return text;
}

function governPayload(payload = {}, plan = "free") {
  const symbol = sanitizeText(payload.symbol || payload.asset || payload.instrument || "UNKNOWN");
  const market = sanitizeText(payload.market || payload.market_type || "UNKNOWN");
  const timeframe = sanitizeText(payload.timeframe || payload.interval || payload.tf || "UNSPECIFIED");

  return {
    ok: true,
    source_mode: "node_governance_bridge_sanitized",
    project: "NDSP — منصة نواف لدعم القرار",
    package: String(plan || "free"),
    instrument: { symbol, market, timeframe },
    allowed_public_outputs: {
      directional_bias: sanitizeText(payload.directional_bias || payload.direction || "قراءة سياقية"),
      reading_horizon: sanitizeText(payload.reading_horizon || payload.horizon || "غير محدد"),
      horizon_strength: sanitizeText(payload.horizon_strength || "تحتاج متابعة"),
      decision_quality: sanitizeText(payload.decision_quality || payload.quality || "تحتاج متابعة"),
      caution_reason: sanitizeText(payload.caution_reason || "تتم متابعة السيناريو دون اعتبار القراءة أمر تنفيذ."),
      sanitized_summary: sanitizeText(payload.summary || payload.message || "قراءة سياقية صادرة من الباك إند.")
    },
    governance: {
      MODE: "DECISION_ACTIVE",
      EXECUTION_POLICY: "EXECUTION_SANITIZED",
      ALL_LAYERS_PARTICIPATE: true,
      NO_LAYER_DISABLED: true,
      DIRECT_TRADE_EXECUTION: false,
      PUBLIC_OUTPUT_SANITIZED: true,
      NO_FINANCIAL_ADVICE: true,
      NO_GUARANTEED_RESULTS: true,
      NO_SECRET_EXPOSURE: true,
      FRONTEND_IS_DISPLAY_ONLY: true,
      BACKEND_IS_DECISION_AUTHORITY: true,
      RAW_LOGIC_EXPOSED: false,
      FORMULAS_EXPOSED: false,
      WEIGHTS_EXPOSED: false,
      HIDDEN_LAYER_NAMES_EXPOSED: false
    },
    public_safe: true,
    governance_note: "مستويات السيناريو هي مراجع سياقية لدعم القرار فقط، وليست نصيحة مالية أو أمر تداول أو توجيه تنفيذ أو ضمانًا للنتائج.",
    generated_at: new Date().toISOString()
  };
}

function json(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "x-ndsp-governance-bridge": "active"
  });
  res.end(body);
}

function parseBody(req) {
  return new Promise((resolve) => {
    let body = "";
    req.on("data", chunk => { body += chunk; if (body.length > 1024 * 1024) req.destroy(); });
    req.on("end", () => {
      try { resolve(body ? JSON.parse(body) : {}); }
      catch (_) { resolve({}); }
    });
    req.on("error", () => resolve({}));
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);

  if (req.method === "GET" && url.pathname === "/api/governance/health") {
    return json(res, 200, {
      ok: true,
      service: "ndsp-governance-bridge",
      public_safe: true,
      frontend_is_display_only: true,
      backend_is_decision_authority: true
    });
  }

  if (req.method === "GET" && url.pathname === "/api/governance/mode") {
    const data = readJson("ndsp_governance_mode.json", {});
    return json(res, 200, {
      ok: true,
      system: data.system || "NDSP",
      governance_version: data.governance_version || "unknown",
      mode: data.mode || "DECISION_ACTIVE",
      execution_policy: data.execution_policy || "EXECUTION_SANITIZED",
      decision_active: data.decision_active !== false,
      execution_sanitized: data.execution_sanitized !== false,
      all_layers_participate: data.all_layers_participate !== false,
      no_layer_disabled: data.no_layer_disabled !== false,
      direct_trade_execution: false,
      public_buy_sell_commands: false,
      public_tp_sl: false,
      raw_logic_public: false,
      public_safe: true
    });
  }

  if (req.method === "GET" && url.pathname.startsWith("/api/governance/package/")) {
    const plan = decodeURIComponent(url.pathname.split("/").pop() || "free");
    return json(res, 200, { ok: true, policy: packagePolicy(plan), public_safe: true });
  }

  if (req.method === "GET" && url.pathname.startsWith("/api/governance/market-source/")) {
    const symbol = decodeURIComponent(url.pathname.split("/").pop() || "");
    const s = normalizeSymbol(symbol);
    const source = isCrypto(s) ? "binance" : "mt4_fxcm";
    return json(res, 200, {
      ok: true,
      policy: {
        input_symbol: symbol,
        normalized_symbol: s,
        preferred_source: source,
        binance_symbol: source === "binance" ? toBinanceSymbol(s) : null,
        mt4_symbol: source === "mt4_fxcm" ? s : null
      },
      public_safe: true
    });
  }

  if (req.method === "POST" && url.pathname === "/api/governance/decision/govern") {
    const payload = await parseBody(req);
    const plan = url.searchParams.get("package") || url.searchParams.get("plan") || "free";
    return json(res, 200, governPayload(payload, plan));
  }

  return json(res, 404, { ok: false, error: "NOT_FOUND", public_safe: true });
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[NDSP_GOVERNANCE_BRIDGE] listening on 127.0.0.1:${PORT}`);
});
