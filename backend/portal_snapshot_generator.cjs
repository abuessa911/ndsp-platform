#!/usr/bin/env node
"use strict";

const fs = require("fs");
const http = require("http");
const https = require("https");
const path = require("path");

const ENV_PATH = path.join(__dirname, "auth_api", ".env");
const BACKUP_DIR = "/home/nawaf511/ndsp_backups";
const REPORT_DIR = "/home/nawaf511/ndsp_launch_reports";
const LIVE_MARKET_URL = "http://127.0.0.1:9033/api/market/prices?symbol=XAU";
const SCENARIO_LEVELS_URL = "http://127.0.0.1:9034/api/scenario/levels?symbol=XAU";
const PORTAL_ASSET_VIEW_URL = "http://127.0.0.1:9047/api/portal/asset-view?symbol=XAU&timeframe=weekly";
const PORTAL_DAILY_BRIEF_URL = "http://127.0.0.1:9047/api/portal/daily-brief";
const SYMBOL = "XAUUSD";
const TIMEFRAME = "weekly";
const GENERATED_BY = "portal_snapshot_generator";
const MAX_HTTP_AGE_MS = 30 * 60 * 1000;
const WRITE_TTL_HOURS = 2;
const DAILY_BRIEF_DISCLAIMER = "هذا موجز مرجعي للعرض فقط، ولا يمثل أمراً تنفيذياً أو قراراً آلياً.";
const COMMAND_CENTER_DISCLAIMER = "هذه لوحة حالة مرجعية للعرض فقط، ولا تمثل أمراً تنفيذياً أو قراراً آلياً.";
const BANNED_TERMS = [
  "BUY",
  "SELL",
  "LONG",
  "SHORT",
  "أمر شراء",
  "أمر بيع",
  "توصية دخول",
  "توصية خروج"
];

function nowIso() {
  return new Date().toISOString();
}

function loadEnv(envPath) {
  const out = {};
  const raw = fs.readFileSync(envPath, "utf8");
  raw.split(/\r?\n/).forEach((line) => {
    const trimmed = String(line || "").trim();
    if (!trimmed || trimmed.startsWith("#")) return;
    const idx = trimmed.indexOf("=");
    if (idx < 0) return;
    const key = trimmed.slice(0, idx).trim();
    const value = trimmed.slice(idx + 1).trim().replace(/^['"]|['"]$/g, "");
    out[key] = value;
  });
  return out;
}

function parseArgs(argv) {
  const pageArg = argv.find((arg) => arg.indexOf("--page=") === 0) || "";
  const page = pageArg ? pageArg.slice("--page=".length).trim() : "asset-view";
  return {
    page: page || "asset-view",
    dryRun: argv.includes("--dry-run"),
    write: argv.includes("--write")
  };
}

function getPageConfig(page) {
  if (page === "daily-brief") {
    return {
      pageType: "daily-brief",
      symbol: "none",
      timeframe: "none",
      portalUrl: PORTAL_DAILY_BRIEF_URL
    };
  }

  if (page === "command-center") {
    return {
      pageType: "command-center",
      symbol: "none",
      timeframe: "none",
      portalUrl: "/api/portal/command-center"
    };
  }

  return {
    pageType: "asset-view",
    symbol: SYMBOL,
    timeframe: TIMEFRAME,
    portalUrl: PORTAL_ASSET_VIEW_URL
  };
}

function requestJson(urlString, timeoutMs = 8000) {
  return new Promise((resolve) => {
    try {
      const url = new URL(urlString);
      const client = url.protocol === "https:" ? https : http;
      const req = client.request({
        protocol: url.protocol,
        hostname: url.hostname,
        port: url.port || (url.protocol === "https:" ? 443 : 80),
        path: `${url.pathname}${url.search}`,
        method: "GET",
        timeout: timeoutMs,
        headers: {
          "Accept": "application/json",
          "Cache-Control": "no-cache",
          "User-Agent": "NDSP-PortalSnapshotGenerator/1.0"
        }
      }, (res) => {
        let body = "";
        res.setEncoding("utf8");
        res.on("data", (chunk) => { body += chunk; });
        res.on("end", () => {
          let json = null;
          try {
            json = JSON.parse(body);
          } catch (_) {}

          resolve({
            ok: res.statusCode >= 200 && res.statusCode < 300,
            status: res.statusCode,
            url: urlString,
            body,
            json
          });
        });
      });

      req.on("timeout", () => {
        try { req.destroy(); } catch (_) {}
        resolve({ ok: false, status: 0, url: urlString, error: "TIMEOUT", json: null });
      });

      req.on("error", (error) => {
        resolve({ ok: false, status: 0, url: urlString, error: String(error.message || error), json: null });
      });

      req.end();
    } catch (error) {
      resolve({ ok: false, status: 0, url: urlString, error: String(error.message || error), json: null });
    }
  });
}

function normalizeSymbol(value) {
  const raw = String(value || "").trim().toUpperCase();
  if (raw === "XAU" || raw === "XAUUSD") return "XAUUSD";
  return raw;
}

function isFiniteNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function parseIsoDate(value) {
  const ts = Date.parse(String(value || ""));
  return Number.isFinite(ts) ? ts : null;
}

function isFreshIso(value, maxAgeMs = MAX_HTTP_AGE_MS) {
  const ts = parseIsoDate(value);
  if (ts === null) return false;
  return Math.abs(Date.now() - ts) <= maxAgeMs;
}

function safeText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function ensureNoBannedTerms(payload) {
  const blob = JSON.stringify(payload);
  const matches = BANNED_TERMS.filter((term) => blob.includes(term));
  if (matches.length) {
    throw new Error(`BANNED_TERMS_PRESENT:${matches.join(",")}`);
  }
}

function buildSummary(market, levels, portalAsset) {
  const price = market.price.toFixed(2);
  const activation = levels.activation_price.toFixed(2);
  const review = levels.review_price.toFixed(2);
  const cancel = levels.cancel_price.toFixed(2);
  const assetName = safeText(
    (portalAsset && (portalAsset.name_ar || portalAsset.name_en || portalAsset.name || portalAsset.code)) || SYMBOL
  );

  return safeText(
    `قراءة مرجعية وصفية لـ ${assetName} على الإطار ${TIMEFRAME}. ` +
    `السعر المرصود ${price}. ` +
    `المستويات المرجعية الحالية تشمل مستوى مراقبة علوي ${activation} ومستوى مراجعة ${review} ومستوى إبطال مرجعي ${cancel}. ` +
    `المحتوى مخصص للعرض المرجعي فقط.`
  );
}

function buildPayload(market, scenario, portalAssetMeta) {
  const payload = {
    title: "XAUUSD Weekly Reference Snapshot",
    page_type: "asset-view",
    symbol: SYMBOL,
    timeframe: TIMEFRAME,
    generated_at: nowIso(),
    market_price: {
      value: market.price,
      change_24h: market.change_24h,
      change_pct: market.change_pct,
      provider: market.provider,
      updated_at: market.updated_at
    },
    reference_levels: {
      arrival: scenario.levels.arrival_price,
      review: scenario.levels.review_price,
      activation: scenario.levels.activation_price,
      cancel: scenario.levels.cancel_price,
      updated_at: scenario.updated_at || scenario.price_updated_at || null
    },
    asset_context: portalAssetMeta,
    summary: buildSummary(market, scenario.levels, portalAssetMeta),
    disclaimer: "هذه قراءة مرجعية للعرض فقط، ولا تمثل أمراً تنفيذياً أو قراراً آلياً."
  };

  ensureNoBannedTerms(payload);
  return payload;
}

function validateAssetSnapshotPayload(snapshot) {
  if (!snapshot || typeof snapshot !== "object") {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_SNAPSHOT_MISSING" };
  }

  if (normalizeSymbol(snapshot.symbol) !== SYMBOL) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_SNAPSHOT_SYMBOL_MISMATCH" };
  }

  if (String(snapshot.timeframe || "").toLowerCase() !== TIMEFRAME) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_SNAPSHOT_TIMEFRAME_MISMATCH" };
  }

  if (!snapshot.reference_levels || !isFiniteNumber(snapshot.reference_levels.activation)) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_SNAPSHOT_LEVELS_INVALID" };
  }

  return { ok: true, data: snapshot };
}

function extractLatestAssetSnapshot(response) {
  if (!response.ok || !response.json || response.json.ok !== true) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_UNAVAILABLE" };
  }

  if (response.json.fake_data === true) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_FAKE_DATA" };
  }

  return validateAssetSnapshotPayload(response.json.snapshot || null);
}

function buildDailyBriefPayload(market, scenario, assetSnapshot) {
  const marketOverview = safeText(
    `حالة السوق المرجعية لرمز XAUUSD تُظهر سعراً مرصوداً عند ${market.price.toFixed(2)} ` +
    `مع مراجعة وصفية للمستويات المرجعية الحالية دون أي توجيه تنفيذي.`
  );
  const keyReference = safeText(
    `أقرب مستويات المتابعة الحالية: وصول ${scenario.levels.arrival_price.toFixed(2)}، ` +
    `مراجعة ${scenario.levels.review_price.toFixed(2)}، تفعيل ${scenario.levels.activation_price.toFixed(2)}، ` +
    `وإلغاء ${scenario.levels.cancel_price.toFixed(2)}.`
  );
  const summary = safeText(
    `موجز اليوم يعرض قراءة مرجعية وصفية من لقطة XAUUSD الأسبوعية الأحدث، ` +
    `ويجمع بين السعر المرصود، السياق العام، والمستويات المرجعية الصالحة للعرض فقط.`
  );

  const payload = {
    title: "NDSP Daily Brief Snapshot",
    page_type: "daily-brief",
    generated_at: nowIso(),
    summary,
    market_overview: marketOverview,
    key_reference: keyReference,
    source_notes: [
      "live_market_adapter",
      "scenario_levels_adapter",
      "portal_asset_view",
      "ndsp_portal_readings_cache.asset-view.latest_valid"
    ],
    disclaimer: DAILY_BRIEF_DISCLAIMER,
    asset_snapshot: {
      symbol: assetSnapshot.symbol,
      timeframe: assetSnapshot.timeframe,
      market_price: assetSnapshot.market_price,
      reference_levels: assetSnapshot.reference_levels
    }
  };

  ensureNoBannedTerms(payload);
  return payload;
}

function validateDailyBriefSnapshotPayload(snapshot) {
  if (!snapshot || typeof snapshot !== "object") {
    return { ok: false, reason: "DAILY_BRIEF_SNAPSHOT_MISSING" };
  }

  if (String(snapshot.page_type || "").toLowerCase() !== "daily-brief") {
    return { ok: false, reason: "DAILY_BRIEF_SNAPSHOT_PAGE_TYPE_MISMATCH" };
  }

  if (!safeText(snapshot.title) || !safeText(snapshot.summary) || !safeText(snapshot.disclaimer)) {
    return { ok: false, reason: "DAILY_BRIEF_SNAPSHOT_FIELDS_MISSING" };
  }

  return { ok: true, data: snapshot };
}

function buildCommandCenterPayload(assetSnapshot, dailyBriefSnapshot, market, scenario) {
  const marketUpdatedAt = market && market.updated_at ? market.updated_at : null;
  const scenarioUpdatedAt = scenario && (scenario.updated_at || scenario.price_updated_at)
    ? (scenario.updated_at || scenario.price_updated_at)
    : null;
  const freshness = [
    marketUpdatedAt ? "market " + marketUpdatedAt : null,
    scenarioUpdatedAt ? "scenario " + scenarioUpdatedAt : null,
    assetSnapshot && assetSnapshot.generated_at ? "asset " + assetSnapshot.generated_at : null,
    dailyBriefSnapshot && dailyBriefSnapshot.generated_at ? "brief " + dailyBriefSnapshot.generated_at : null
  ].filter(Boolean).join(" · ");

  const payload = {
    title: "NDSP Command Center Snapshot",
    page_type: "command-center",
    generated_at: nowIso(),
    operational_state: "ready with valid reference snapshots and live source context",
    asset_snapshot_status: "usable",
    daily_brief_status: "usable",
    data_freshness: freshness,
    summary: safeText(
      "لوحة الحالة المرجعية تعرض جاهزية snapshot الأصل وsnapshot الموجز اليومي مع تغذية سوقية ومراجع سيناريو صالحة للعرض فقط."
    ),
    source_notes: [
      "ndsp_portal_readings_cache.asset-view.latest_valid",
      "ndsp_portal_readings_cache.daily-brief.latest_valid",
      "live_market_adapter",
      "scenario_levels_adapter"
    ],
    disclaimer: COMMAND_CENTER_DISCLAIMER
  };

  ensureNoBannedTerms(payload);
  return payload;
}

function validateMarketResponse(response) {
  if (!response.ok || !response.json || !Array.isArray(response.json.prices)) {
    return { ok: false, reason: "LIVE_MARKET_UNAVAILABLE" };
  }

  const row = response.json.prices.find((item) => normalizeSymbol(item && item.symbol) === SYMBOL) || null;
  if (!row) {
    return { ok: false, reason: "LIVE_MARKET_SYMBOL_MISSING" };
  }

  if (!isFiniteNumber(row.price) || row.price <= 0) {
    return { ok: false, reason: "LIVE_MARKET_PRICE_INVALID" };
  }

  if (!isFreshIso(row.updated_at)) {
    return { ok: false, reason: "LIVE_MARKET_PRICE_STALE" };
  }

  return { ok: true, data: row };
}

function validateScenarioResponse(response) {
  if (!response.ok || !response.json || response.json.ok !== true) {
    return { ok: false, reason: "SCENARIO_LEVELS_UNAVAILABLE" };
  }

  const levels = response.json.levels || null;
  if (!levels) {
    return { ok: false, reason: "SCENARIO_LEVELS_MISSING" };
  }

  const required = [
    "arrival_price",
    "review_price",
    "activation_price",
    "cancel_price"
  ];

  for (const key of required) {
    if (!isFiniteNumber(levels[key])) {
      return { ok: false, reason: `SCENARIO_LEVELS_INVALID_${key.toUpperCase()}` };
    }
  }

  return { ok: true, data: response.json };
}

function validatePortalAssetResponse(response) {
  if (!response.ok || !response.json || response.json.ok !== true) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_UNAVAILABLE" };
  }

  if (response.json.fake_data === true) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_FAKE_DATA" };
  }

  const data = response.json.data || null;
  if (!data || data.configured !== true) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_NOT_CONFIGURED" };
  }

  const row = data.row || null;
  if (!row || normalizeSymbol(row.symbol || row.code) !== SYMBOL) {
    return { ok: false, reason: "PORTAL_ASSET_VIEW_SYMBOL_MISMATCH" };
  }

  return {
    ok: true,
    data: {
      source_table: data.source || null,
      code: row.code || null,
      symbol: row.symbol || null,
      name: row.name || null,
      name_ar: row.name_ar || null,
      name_en: row.name_en || null,
      category: row.category || null,
      source: row.source || null,
      updated_at: row.updated_at || null
    }
  };
}

async function buildSnapshotCandidate(page) {
  const pageConfig = getPageConfig(page);
  const requests = [
    requestJson(LIVE_MARKET_URL),
    requestJson(SCENARIO_LEVELS_URL)
  ];
  if (pageConfig.pageType !== "command-center") {
    requests.push(requestJson(PORTAL_ASSET_VIEW_URL));
  }
  const responses = await Promise.all(requests);
  const marketResponse = responses[0];
  const scenarioResponse = responses[1];
  const portalAssetResponse = responses[2] || null;

  const market = validateMarketResponse(marketResponse);
  const scenario = validateScenarioResponse(scenarioResponse);
  const portalAsset = pageConfig.pageType === "command-center"
    ? { ok: true, data: null }
    : validatePortalAssetResponse(portalAssetResponse);

  const sourceChecks = {
    live_market_adapter: market.ok ? "usable" : market.reason,
    scenario_levels_adapter: scenario.ok ? "usable" : scenario.reason,
    portal_asset_view: portalAsset.ok ? "usable" : portalAsset.reason
  };

  const insufficiencyReasons = [];
  if (!market.ok) insufficiencyReasons.push(market.reason);
  if (!scenario.ok) insufficiencyReasons.push(scenario.reason);
  if (!portalAsset.ok) insufficiencyReasons.push(portalAsset.reason);

  if (insufficiencyReasons.length) {
    return {
      ok: false,
      reason: "INSUFFICIENT_SOURCE_DATA",
      insufficiency_reasons: insufficiencyReasons,
      source_checks: sourceChecks,
      proposed_payload: null
    };
  }

  const dailyBriefAssetSnapshot = pageConfig.pageType === "daily-brief"
    ? await fetchLatestAssetViewSnapshotFromCache()
    : (pageConfig.pageType === "command-center"
        ? null
        : extractLatestAssetSnapshot(portalAssetResponse));
  const commandCenterAssetSnapshot = pageConfig.pageType === "command-center"
    ? await fetchLatestAssetViewSnapshotFromCache()
    : null;
  const commandCenterDailyBriefSnapshot = pageConfig.pageType === "command-center"
    ? await fetchLatestDailyBriefSnapshotFromCache()
    : null;
  if (pageConfig.pageType === "daily-brief" && (!dailyBriefAssetSnapshot || dailyBriefAssetSnapshot.ok !== true)) {
    return {
      ok: false,
      reason: "INSUFFICIENT_SOURCE_DATA",
      insufficiency_reasons: [
        dailyBriefAssetSnapshot && dailyBriefAssetSnapshot.reason
          ? dailyBriefAssetSnapshot.reason
          : "COMMAND_CENTER_ASSET_VIEW_SNAPSHOT_MISSING"
      ],
      source_checks: {
        live_market_adapter: market.ok ? "usable" : market.reason,
        scenario_levels_adapter: scenario.ok ? "usable" : scenario.reason,
        portal_asset_view: portalAsset.ok ? "usable" : portalAsset.reason,
        latest_asset_view_snapshot: dailyBriefAssetSnapshot && dailyBriefAssetSnapshot.ok === true
          ? "usable"
          : (dailyBriefAssetSnapshot && dailyBriefAssetSnapshot.reason
              ? dailyBriefAssetSnapshot.reason
              : "COMMAND_CENTER_ASSET_VIEW_SNAPSHOT_MISSING")
      },
      proposed_payload: null
    };
  }
  if (pageConfig.pageType === "command-center" &&
      ((!commandCenterAssetSnapshot || commandCenterAssetSnapshot.ok !== true) ||
       (!commandCenterDailyBriefSnapshot || commandCenterDailyBriefSnapshot.ok !== true))) {
    return {
      ok: false,
      reason: "INSUFFICIENT_SOURCE_DATA",
      insufficiency_reasons: [
        !commandCenterAssetSnapshot || commandCenterAssetSnapshot.ok !== true
          ? (commandCenterAssetSnapshot && commandCenterAssetSnapshot.reason
              ? commandCenterAssetSnapshot.reason
              : "COMMAND_CENTER_ASSET_VIEW_SNAPSHOT_MISSING")
          : null,
        !commandCenterDailyBriefSnapshot || commandCenterDailyBriefSnapshot.ok !== true
          ? (commandCenterDailyBriefSnapshot && commandCenterDailyBriefSnapshot.reason
              ? commandCenterDailyBriefSnapshot.reason
              : "COMMAND_CENTER_DAILY_BRIEF_SNAPSHOT_MISSING")
          : null
      ].filter(Boolean),
      source_checks: {
        live_market_adapter: market.ok ? "usable" : market.reason,
        scenario_levels_adapter: scenario.ok ? "usable" : scenario.reason,
        latest_asset_view_snapshot: commandCenterAssetSnapshot && commandCenterAssetSnapshot.ok === true
          ? "usable"
          : (commandCenterAssetSnapshot && commandCenterAssetSnapshot.reason
              ? commandCenterAssetSnapshot.reason
              : "COMMAND_CENTER_ASSET_VIEW_SNAPSHOT_MISSING"),
        latest_daily_brief_snapshot: commandCenterDailyBriefSnapshot && commandCenterDailyBriefSnapshot.ok === true
          ? "usable"
          : (commandCenterDailyBriefSnapshot && commandCenterDailyBriefSnapshot.reason
              ? commandCenterDailyBriefSnapshot.reason
              : "COMMAND_CENTER_DAILY_BRIEF_SNAPSHOT_MISSING")
      },
      proposed_payload: null
    };
  }

  const payload = pageConfig.pageType === "daily-brief"
    ? buildDailyBriefPayload(market.data, scenario.data, dailyBriefAssetSnapshot.data)
    : pageConfig.pageType === "command-center"
      ? buildCommandCenterPayload(
          commandCenterAssetSnapshot.data,
          commandCenterDailyBriefSnapshot.data,
          market.data,
          scenario.data
        )
      : buildPayload(market.data, scenario.data, portalAsset.data);

  return {
    ok: true,
    page_type: pageConfig.pageType,
    symbol: pageConfig.symbol,
    timeframe: pageConfig.timeframe,
    source_service: pageConfig.pageType === "daily-brief"
      ? "live_market_adapter+scenario_levels_adapter+portal_asset_view+ndsp_portal_readings_cache.asset-view.latest_valid"
      : pageConfig.pageType === "command-center"
        ? "ndsp_portal_readings_cache.asset-view.latest_valid+ndsp_portal_readings_cache.daily-brief.latest_valid+live_market_adapter+scenario_levels_adapter"
      : "live_market_adapter+scenario_levels_adapter+portal_asset_view",
    generated_by: GENERATED_BY,
    expires_at: new Date(Date.now() + WRITE_TTL_HOURS * 60 * 60 * 1000).toISOString(),
    proposed_payload: payload,
    source_checks: pageConfig.pageType === "daily-brief" ? {
      live_market_adapter: market.ok ? "usable" : market.reason,
      scenario_levels_adapter: scenario.ok ? "usable" : scenario.reason,
      portal_asset_view: portalAsset.ok ? "usable" : portalAsset.reason,
      latest_asset_view_snapshot: dailyBriefAssetSnapshot && dailyBriefAssetSnapshot.ok === true
        ? "usable"
        : (dailyBriefAssetSnapshot && dailyBriefAssetSnapshot.reason
            ? dailyBriefAssetSnapshot.reason
            : "COMMAND_CENTER_ASSET_VIEW_SNAPSHOT_MISSING")
    } : pageConfig.pageType === "command-center" ? {
      live_market_adapter: market.ok ? "usable" : market.reason,
      scenario_levels_adapter: scenario.ok ? "usable" : scenario.reason,
      latest_asset_view_snapshot: commandCenterAssetSnapshot && commandCenterAssetSnapshot.ok === true
        ? "usable"
        : (commandCenterAssetSnapshot && commandCenterAssetSnapshot.reason
            ? commandCenterAssetSnapshot.reason
            : "COMMAND_CENTER_ASSET_VIEW_SNAPSHOT_MISSING"),
      latest_daily_brief_snapshot: commandCenterDailyBriefSnapshot && commandCenterDailyBriefSnapshot.ok === true
        ? "usable"
        : (commandCenterDailyBriefSnapshot && commandCenterDailyBriefSnapshot.reason
            ? commandCenterDailyBriefSnapshot.reason
            : "COMMAND_CENTER_DAILY_BRIEF_SNAPSHOT_MISSING")
    } : sourceChecks,
    insufficiency_reasons: []
  };
}

function loadPgPool() {
  const pg = require("./auth_api/node_modules/pg");
  return pg.Pool;
}

async function fetchLatestAssetViewSnapshotFromCache() {
  const env = loadEnv(ENV_PATH);
  const Pool = loadPgPool();
  const pool = new Pool({
    connectionString: env.DATABASE_URL || env.POSTGRES_URL || env.AUTH_DATABASE_URL
  });

  const sql = `
    SELECT payload
    FROM ndsp_portal_readings_cache
    WHERE page_type = 'asset-view'
      AND symbol = $1
      AND timeframe = $2
      AND status = 'configured'
      AND (expires_at IS NULL OR expires_at > now())
    ORDER BY created_at DESC
    LIMIT 1
  `;

  try {
    const result = await pool.query(sql, [SYMBOL, TIMEFRAME]);
    const row = result.rows[0] || null;
    return validateAssetSnapshotPayload(row && row.payload ? row.payload : null);
  } catch (error) {
    return { ok: false, reason: "LATEST_ASSET_VIEW_SNAPSHOT_QUERY_FAILED", detail: String(error.message || error) };
  } finally {
    await pool.end();
  }
}

async function fetchLatestDailyBriefSnapshotFromCache() {
  const env = loadEnv(ENV_PATH);
  const Pool = loadPgPool();
  const pool = new Pool({
    connectionString: env.DATABASE_URL || env.POSTGRES_URL || env.AUTH_DATABASE_URL
  });

  const sql = `
    SELECT payload
    FROM ndsp_portal_readings_cache
    WHERE page_type = 'daily-brief'
      AND symbol = 'none'
      AND timeframe = 'none'
      AND status = 'configured'
      AND (expires_at IS NULL OR expires_at > now())
    ORDER BY created_at DESC
    LIMIT 1
  `;

  try {
    const result = await pool.query(sql);
    const row = result.rows[0] || null;
    return validateDailyBriefSnapshotPayload(row && row.payload ? row.payload : null);
  } catch (error) {
    return { ok: false, reason: "LATEST_DAILY_BRIEF_SNAPSHOT_QUERY_FAILED", detail: String(error.message || error) };
  } finally {
    await pool.end();
  }
}

async function writeSnapshot(snapshot) {
  const env = loadEnv(ENV_PATH);
  const Pool = loadPgPool();
  const pool = new Pool({
    connectionString: env.DATABASE_URL || env.POSTGRES_URL || env.AUTH_DATABASE_URL
  });

  const sql = `
    INSERT INTO ndsp_portal_readings_cache
      (page_type, symbol, timeframe, source_service, payload, status, generated_by, expires_at)
    VALUES
      ($1, $2, $3, $4, $5::jsonb, 'configured', $6, $7::timestamptz)
    RETURNING id, page_type, symbol, timeframe, source_service, generated_by, expires_at, created_at
  `;

  const params = [
    snapshot.page_type,
    snapshot.symbol,
    snapshot.timeframe,
    snapshot.source_service,
    JSON.stringify(snapshot.proposed_payload),
    snapshot.generated_by,
    snapshot.expires_at
  ];

  try {
    const result = await pool.query(sql, params);
    return result.rows[0] || null;
  } finally {
    await pool.end();
  }
}

function reportFilePath() {
  return path.join(REPORT_DIR, `portal_snapshot_generator_${Date.now()}.json`);
}

function writeReport(output) {
  const target = reportFilePath();
  fs.writeFileSync(target, JSON.stringify(output, null, 2));
  return target;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const pageConfig = getPageConfig(args.page);
  if (args.dryRun === args.write) {
    console.error("Usage: node backend/portal_snapshot_generator.cjs --page=asset-view|daily-brief --dry-run | --write");
    process.exit(1);
  }

  const snapshot = await buildSnapshotCandidate(args.page);
  const output = {
    ok: snapshot.ok,
    mode: args.dryRun ? "dry-run" : "write",
    target: {
      page_type: pageConfig.pageType,
      symbol: pageConfig.symbol,
      timeframe: pageConfig.timeframe
    },
    data_sufficiency: snapshot.ok ? "sufficient" : "insufficient",
    reason: snapshot.ok ? null : snapshot.reason,
    insufficiency_reasons: snapshot.insufficiency_reasons || [],
    source_checks: snapshot.source_checks || {},
    proposed_payload: snapshot.proposed_payload || null,
    database_write_attempted: false,
    cache_write_skipped: args.dryRun,
    backup_dir: BACKUP_DIR,
    report_generated_at: nowIso()
  };

  if (!snapshot.ok) {
    const reportPath = writeReport(output);
    output.report_path = reportPath;
    console.log(JSON.stringify(output, null, 2));
    process.exit(2);
  }

  if (args.dryRun) {
    const reportPath = writeReport(output);
    output.report_path = reportPath;
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  output.database_write_attempted = true;
  const writtenRow = await writeSnapshot(snapshot);
  output.written_row = writtenRow;
  const reportPath = writeReport(output);
  output.report_path = reportPath;
  console.log(JSON.stringify(output, null, 2));
}

main().catch((error) => {
  const output = {
    ok: false,
    mode: process.argv.includes("--write") ? "write" : "dry-run",
    data_sufficiency: "insufficient",
    reason: "GENERATOR_RUNTIME_ERROR",
    insufficiency_reasons: [String(error.message || error)],
    proposed_payload: null,
    database_write_attempted: process.argv.includes("--write"),
    cache_write_skipped: !process.argv.includes("--write"),
    backup_dir: BACKUP_DIR,
    report_generated_at: nowIso()
  };

  try {
    output.report_path = writeReport(output);
  } catch (_) {}

  console.error(JSON.stringify(output, null, 2));
  process.exit(1);
});
