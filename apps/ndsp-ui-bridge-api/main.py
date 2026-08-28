from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timezone
from typing import Any

app = FastAPI(title="NDSP UI Bridge API", version="2.0.0-governed-analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://my.ndsp.app",
        "https://ndsp.app",
        "https://www.ndsp.app",
        "https://admin.ndsp.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QUALITY_URL = "https://api.ndsp.app/api/decision/quality-live"
QUALITY_HEALTH_URL = "https://api.ndsp.app/api/decision/quality-live/health"
DECISION_PACKAGE_URL = "https://api.ndsp.app/api/decision/package-v2"
BINANCE_EXCHANGE_INFO_URL = "https://api.binance.com/api/v3/exchangeInfo"

QUALITY_TIMEFRAMES = [
    {"id": "daily", "label_ar": "يومي", "label_en": "Daily"},
    {"id": "weekly", "label_ar": "أسبوعي", "label_en": "Weekly"},
    {"id": "monthly", "label_ar": "شهري", "label_en": "Monthly"},
]
ANALYSIS_MODES = [
    {"id": "investment", "label_ar": "استثماري / طويل الأفق", "label_en": "Investment / Long Horizon"},
    {"id": "speculative", "label_ar": "مضاربي / أسبوعي", "label_en": "Speculative / Weekly"},
]
PRESENTATION_MODES = [
    {"id": "beginner", "label_ar": "مبتدئ", "label_en": "Beginner"},
    {"id": "professional", "label_ar": "محترف", "label_en": "Professional"},
]

EXTERNAL_MARKETS = {
    "forex": {"EURUSD", "GBPUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF"},
    "commodity": {"XAUUSD", "XAGUSD", "USOIL", "UKOIL", "NG", "ZC", "ZS", "ZW"},
    "index": {"SPX", "NDX", "DXY", "DJI", "VIX", "CAC", "DAX"},
}

CAPABILITY_DEFINITIONS = [
    ("TDL", "TDL", True),
    ("NMP", "NMP", True),
    ("GOLDEN_SIGNAL", "الإشارة الذهبية", True),
    ("ENHANCED_GOLDEN", "الإشارة الذهبية المعززة", True),
    ("DEVILS_ADVOCATE", "محامي الشيطان", True),
    ("DIVERGENCE", "الانحرافات", True),
    ("TECHNICAL", "الأدلة الفنية", False),
    ("MACRO", "السياق الكلي", True),
    ("MARKET_STRUCTURE", "هيكل السوق", False),
    ("RISK", "المخاطر", True),
    ("LIQUIDITY", "السيولة", False),
    ("VOLATILITY", "التذبذب", False),
    ("SENTIMENT", "المعنويات", False),
    ("COT", "السياق الاتجاهي المؤسسي", True),
    ("ECONOMIC_NEWS", "الأخبار الاقتصادية", False),
    ("ECONOMIC_CALENDAR", "التقويم الاقتصادي", False),
    ("DECISION_QUALITY", "جودة القرار", False),
    ("ALIGNMENT_SCORE", "درجة التوافق", True),
    ("CONFIRMATION_SCORE", "درجة التأكيد", True),
    ("BLOCKERS", "عوائق القرار", True),
    ("DECISION_STATE", "حالة القرار", False),
    ("ACTIVATION", "مستويات السيناريو", False),
    ("FRESHNESS", "حداثة البيانات", False),
    ("EXPLAINABILITY", "تفسير القرار", False),
    ("DECISION_PACKAGE", "حزمة القرار", False),
    ("DECISION_HISTORY", "سجل القرارات", False),
    ("ALERT_POLICY", "سياسة التنبيهات", False),
    ("ASSET_UNIVERSE", "الأصول والأسواق", False),
    ("TIMEFRAME", "الإطار الزمني", False),
    ("ANALYSIS_MODE", "نمط التحليل", False),
    ("PRESENTATION_MODE", "نمط العرض", False),
]

LAYER_REGISTRY = [
    (1, "سلامة المصدر", "SOURCE"),
    (2, "سلطة الجلسة", "SESSION"),
    (3, "سلطة التوقيت", "TIMING"),
    (4, "تموضع الفئات", "COT"),
    (5, "TDL", "TDL"),
    (6, "سلطة الاتجاه الزمني", "DIRECTION"),
    (7, "السياق الكلي والدولار", "MACRO"),
    (8, "NMP", "NMP"),
    (9, "بنية الأفق", "HORIZON"),
    (10, "الزخم", "MOMENTUM"),
    (11, "الانحرافات", "DIVERGENCE"),
    (12, "طبقة العوائق المحمية", "BLOCKERS"),
    (13, "جودة القرار", "DECISION_QUALITY"),
    (14, "حوكمة المخاطر", "RISK"),
    (15, "حالة القرار النهائي", "FINAL_DECISION"),
    (16, "تنبيهات السيناريو", "ALERTS"),
]


def now():
    return datetime.now(timezone.utc).isoformat()


def _request_json(url: str, params: dict[str, Any] | None = None, timeout: int = 12):
    response = requests.get(url, params=params or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_quality(symbol: str, timeframe: str = "weekly"):
    try:
        data = _request_json(QUALITY_URL, {"symbol": symbol, "timeframe": timeframe}, timeout=16)
    except Exception as exc:
        return {"ok": False, "error": "QUALITY_LIVE_UNAVAILABLE", "message": str(exc)}

    if not data.get("ok"):
        return {"ok": False, "error": "QUALITY_LIVE_FAILED", "upstream": data}
    return data


def fetch_decision_package(symbol: str):
    try:
        data = _request_json(DECISION_PACKAGE_URL, {"symbol": symbol}, timeout=12)
        return data if isinstance(data, dict) else {"ok": False}
    except Exception as exc:
        return {"ok": False, "error": "DECISION_PACKAGE_UNAVAILABLE", "message": str(exc)}


def _market_for_external(symbol: str):
    value = str(symbol or "").upper()
    for market, symbols in EXTERNAL_MARKETS.items():
        if value in symbols:
            return market
    return "unknown"


def _market_normalized(value: Any):
    text = str(value or "").strip().lower()
    aliases = {
        "crypto": "crypto",
        "forex": "forex",
        "fx": "forex",
        "commodity": "commodity",
        "commodities": "commodity",
        "index": "index",
        "indices": "index",
    }
    return aliases.get(text, text or "unknown")


def _deep_has(value: Any, needles: tuple[str, ...]):
    lowered = tuple(x.lower() for x in needles)
    if isinstance(value, dict):
        for key, item in value.items():
            if any(needle in str(key).lower() for needle in lowered) and item not in (None, "", [], {}):
                return True
            if _deep_has(item, needles):
                return True
    elif isinstance(value, list):
        return any(_deep_has(item, needles) for item in value)
    return False


def _engine_status_map(package: dict[str, Any]):
    result: dict[str, str] = {}
    for row in package.get("engine_health") or []:
        if isinstance(row, dict) and row.get("engine"):
            result[str(row["engine"]).lower()] = str(row.get("status") or "UNKNOWN").upper()
    return result


def _governed_status(status: str):
    status = str(status or "UNKNOWN").upper()
    if status in {"OK", "VERIFIED", "AVAILABLE", "SOURCE_AVAILABLE"}:
        return "CONTRIBUTED"
    if status in {"ACTION_REQUIRED", "PENDING_ENGINE_BINDING", "DEGRADED", "WATCH"}:
        return "PARTIAL"
    if status in {"BLOCKED", "FAILED", "ERROR"}:
        return "BLOCKED"
    return "UNAVAILABLE"


def _capability(cap_id: str, label: str, protected: bool, status: str, effect: str, detail: str, freshness: str | None):
    return {
        "id": cap_id,
        "public_label": label,
        "protected": protected,
        "state": status,
        "effect": effect,
        "safe_detail": detail,
        "freshness": freshness,
    }


def _setup_universe():
    external_health = _request_json(QUALITY_HEALTH_URL, timeout=10)
    external_symbols = sorted(set(external_health.get("supported_external_symbols") or []))

    exchange = _request_json(BINANCE_EXCHANGE_INFO_URL, timeout=12)
    crypto_symbols = sorted({
        str(row.get("symbol"))
        for row in (exchange.get("symbols") or [])
        if row.get("status") == "TRADING"
        and row.get("quoteAsset") == "USDT"
        and row.get("symbol")
    })

    assets = []
    for symbol in crypto_symbols:
        assets.append({"symbol": symbol, "market": "crypto", "label": symbol, "source": "binance_exchange_info"})
    for symbol in external_symbols:
        assets.append({"symbol": symbol, "market": _market_for_external(symbol), "label": symbol, "source": "quality_live_health"})

    counts: dict[str, int] = {}
    for asset in assets:
        counts[asset["market"]] = counts.get(asset["market"], 0) + 1

    market_labels = {
        "crypto": ("الأصول الرقمية", "Crypto"),
        "forex": ("العملات", "Forex"),
        "commodity": ("السلع", "Commodities"),
        "index": ("المؤشرات", "Indices"),
        "unknown": ("أخرى", "Other"),
    }
    markets = [
        {"id": market, "label_ar": market_labels.get(market, (market, market))[0], "label_en": market_labels.get(market, (market, market))[1], "assets_count": count}
        for market, count in sorted(counts.items())
        if count > 0
    ]

    return {
        "markets": markets,
        "assets": assets,
        "timeframes": QUALITY_TIMEFRAMES,
        "analysis_modes": ANALYSIS_MODES,
        "presentation_modes": PRESENTATION_MODES,
        "sources": {
            "crypto": "Binance public exchangeInfo",
            "external": "quality-live health registry",
        },
    }


@app.get("/api/ui-bridge/health")
def health():
    return {
        "ok": True,
        "service": "ndsp-ui-bridge-api",
        "generated_at": now(),
        "source": QUALITY_URL,
        "endpoints": [
            "/api/ui-bridge/analysis/setup/options",
            "/api/ui-bridge/analysis/context/validate",
            "/api/ui-bridge/analysis/capability-coverage",
            "/api/dashboard/overview",
            "/api/market/assets",
            "/api/layers",
            "/api/market-structure",
            "/api/technical-confirmation",
            "/api/macro-analysis",
            "/api/risk-layer",
            "/api/nawaf-signal",
            "/api/alerts",
            "/api/settings",
            "/api/account/profile",
        ],
    }


@app.get("/api/ui-bridge/analysis/setup/options")
def analysis_setup_options():
    try:
        universe = _setup_universe()
        return {"ok": True, "generated_at": now(), **universe}
    except Exception as exc:
        return {
            "ok": False,
            "error": "SETUP_OPTIONS_UNAVAILABLE",
            "message": str(exc),
            "markets": [],
            "assets": [],
            "timeframes": QUALITY_TIMEFRAMES,
            "analysis_modes": ANALYSIS_MODES,
            "presentation_modes": PRESENTATION_MODES,
            "generated_at": now(),
        }


@app.get("/api/ui-bridge/analysis/context/validate")
def validate_analysis_context(
    market: str = Query(...),
    symbol: str = Query(...),
    timeframe: str = Query(...),
    analysis_mode: str = Query(...),
    presentation_mode: str = Query(...),
):
    errors = []
    timeframe = str(timeframe).lower()
    analysis_mode = str(analysis_mode).lower()
    presentation_mode = str(presentation_mode).lower()
    requested_market = _market_normalized(market)

    if timeframe not in {row["id"] for row in QUALITY_TIMEFRAMES}:
        errors.append("UNSUPPORTED_TIMEFRAME")
    if analysis_mode not in {row["id"] for row in ANALYSIS_MODES}:
        errors.append("UNSUPPORTED_ANALYSIS_MODE")
    if presentation_mode not in {row["id"] for row in PRESENTATION_MODES}:
        errors.append("UNSUPPORTED_PRESENTATION_MODE")

    quality = fetch_quality(symbol, timeframe)
    if not quality.get("ok"):
        errors.append("QUALITY_SOURCE_UNAVAILABLE")
        actual_market = "unknown"
    else:
        actual_market = _market_normalized((quality.get("instrument") or {}).get("market"))
        if actual_market != "unknown" and requested_market != actual_market:
            errors.append("MARKET_SYMBOL_MISMATCH")

    mode_binding = "UNAVAILABLE"
    source_mode = str(quality.get("source_mode") or "").lower()
    if analysis_mode == "speculative" and timeframe == "weekly" and "tdl" in source_mode:
        mode_binding = "PARTIAL"
    elif analysis_mode == "investment" and _deep_has(quality, ("asset_managers", "long_term", "investment")):
        mode_binding = "PARTIAL"

    valid_context = not errors
    return {
        "ok": True,
        "valid_context": valid_context,
        "decision_ready": valid_context and mode_binding == "CONTRIBUTED",
        "errors": errors,
        "context": {
            "market": requested_market,
            "actual_market": actual_market,
            "symbol": str(symbol).upper().replace("/", ""),
            "timeframe": timeframe,
            "analysis_mode": analysis_mode,
            "presentation_mode": presentation_mode,
            "presentation_only": True,
            "analysis_mode_binding": mode_binding,
            "as_of": quality.get("generated_at") if isinstance(quality, dict) else now(),
        },
        "governance_note": "Analysis mode must be explicitly bound by backend evidence before an official READY decision is allowed.",
    }


@app.get("/api/ui-bridge/analysis/capability-coverage")
def capability_coverage(
    market: str = Query(...),
    symbol: str = Query(...),
    timeframe: str = Query(...),
    analysis_mode: str = Query(...),
    presentation_mode: str = Query(...),
):
    validation = validate_analysis_context(market, symbol, timeframe, analysis_mode, presentation_mode)
    quality = fetch_quality(symbol, timeframe)
    package = fetch_decision_package(symbol)
    generated_at = quality.get("generated_at") if isinstance(quality, dict) else now()
    engine = _engine_status_map(package)
    public = quality.get("allowed_public_outputs") or {}
    live = quality.get("live_market_analysis") or {}
    scenario = quality.get("scenario") or {}
    source_mode = str(quality.get("source_mode") or "").lower()

    capabilities: list[dict[str, Any]] = []
    status_by_id: dict[str, str] = {}

    def add(cap_id: str, status: str, effect: str, detail: str):
        definition = next((row for row in CAPABILITY_DEFINITIONS if row[0] == cap_id), (cap_id, cap_id, False))
        item = _capability(definition[0], definition[1], definition[2], status, effect, detail, generated_at)
        capabilities.append(item)
        status_by_id[cap_id] = status

    source_ok = quality.get("ok") is True and quality.get("live_price_bound") is True
    add("TDL", "CONTRIBUTED" if "tdl" in source_mode else _governed_status(engine.get("tdl")), "supports" if "tdl" in source_mode else "informational", "TDL contribution is acknowledged only from backend source/runtime evidence.")
    add("NMP", "CONTRIBUTED" if _deep_has(quality, ("nmp", "reference_zone")) else _governed_status(engine.get("nmp")), "supports" if _deep_has(quality, ("nmp", "reference_zone")) else "informational", "NMP formulas and thresholds remain protected; only governed availability/effect is exposed.")
    add("GOLDEN_SIGNAL", "CONTRIBUTED" if _deep_has(quality, ("golden_signal", "golden_status")) else "UNAVAILABLE", "supports", "Golden signal is exposed only when a backend field exists.")
    add("ENHANCED_GOLDEN", "GOVERNANCE_PROTECTED" if _deep_has(quality, ("golden_alignment",)) else "UNAVAILABLE", "supports", "Enhanced alignment internals are protected.")
    add("DEVILS_ADVOCATE", "GOVERNANCE_PROTECTED" if _deep_has(quality, ("devil",)) else _governed_status(engine.get("devil")), "blocks", "Protected final-auditor logic is never recomputed in the frontend.")
    divergence_available = _deep_has(quality, ("divergence", "regular_divergence", "hidden_divergence"))
    add("DIVERGENCE", "CONTRIBUTED" if divergence_available else _governed_status(engine.get("regular_divergence")), "supports", "Regular/hidden divergence appears only when backend evidence is present.")
    technical_partial = source_ok and any(live.get(key) is not None for key in ("selected_timeframe_rsi", "rsi_4h", "selected_timeframe_atr", "atr_4h"))
    add("TECHNICAL", "PARTIAL" if technical_partial else "UNAVAILABLE", "supports", "Current quality source exposes a subset of technical evidence; missing indicators are not fabricated.")
    macro_available = _deep_has(quality, ("usd_pressure", "usd_strength", "macro_state"))
    add("MACRO", "CONTRIBUTED" if macro_available else _governed_status(engine.get("usd_strength")), "conflicts", "Macro/USD effect is shown only when real backend evidence is bound.")
    add("MARKET_STRUCTURE", "CONTRIBUTED" if public.get("market_state") or live.get("selected_timeframe_direction") else "UNAVAILABLE", "supports", "Market structure comes from the selected live timeframe.")
    risk_partial = bool(public.get("caution_reason") or scenario.get("scenario_risk_note"))
    add("RISK", "PARTIAL" if risk_partial else _governed_status(engine.get("risk")), "blocks", "Risk output is fail-closed until the full risk engine is bound.")
    add("LIQUIDITY", "CONTRIBUTED" if _deep_has(quality, ("liquidity",)) else "UNAVAILABLE", "informational", "Liquidity is never inferred from unrelated fields.")
    add("VOLATILITY", "CONTRIBUTED" if live.get("selected_timeframe_atr") is not None or live.get("atr_4h") is not None else "UNAVAILABLE", "informational", "Volatility uses backend ATR evidence only.")
    add("SENTIMENT", "CONTRIBUTED" if _deep_has(quality, ("sentiment",)) else "UNAVAILABLE", "informational", "Sentiment requires an explicit backend source.")
    add("COT", "CONTRIBUTED" if _deep_has(quality, ("cot", "asset_managers", "leveraged_funds")) else _governed_status(engine.get("cot_freshness")), "supports", "COT/positioning is not synthesized when the live contract does not expose it.")
    add("ECONOMIC_NEWS", "CONTRIBUTED" if _deep_has(quality, ("economic_news",)) else _governed_status(engine.get("economic_news")), "conflicts", "Economic-news effect requires a bound engine.")
    add("ECONOMIC_CALENDAR", "CONTRIBUTED" if _deep_has(quality, ("economic_calendar",)) else _governed_status(engine.get("economic_calendar")), "informational", "Calendar availability is explicit.")
    add("DECISION_QUALITY", "CONTRIBUTED" if public.get("decision_quality") is not None else "UNAVAILABLE", "supports", "Decision-quality value is backend-owned.")
    add("ALIGNMENT_SCORE", "CONTRIBUTED" if _deep_has(quality, ("alignment_score",)) else "UNAVAILABLE", "supports", "Alignment score is not approximated in the browser.")
    add("CONFIRMATION_SCORE", "CONTRIBUTED" if _deep_has(quality, ("confirmation_score",)) else "UNAVAILABLE", "supports", "Confirmation score requires an explicit contract field.")
    add("BLOCKERS", "GOVERNANCE_PROTECTED" if _deep_has(quality, ("blocker", "blocking_factor")) else "UNAVAILABLE", "blocks", "Blocker internals stay protected; presence/effect may be exposed safely.")
    add("DECISION_STATE", "PARTIAL" if scenario.get("scenario_state") else "UNAVAILABLE", "informational", "Scenario state is not promoted to a final decision state.")
    add("ACTIVATION", "CONTRIBUTED" if scenario.get("scenario_activation_level") is not None or scenario.get("scenario_arrival_level") is not None else "UNAVAILABLE", "informational", "Scenario levels come directly from backend output.")
    add("FRESHNESS", "CONTRIBUTED" if generated_at else "STALE", "blocks", "Freshness is carried with the backend reading.")
    add("EXPLAINABILITY", "CONTRIBUTED" if public.get("sanitized_summary") or public.get("caution_reason") else "UNAVAILABLE", "informational", "Only sanitized explanation is exposed.")
    add("DECISION_PACKAGE", "CONTRIBUTED" if package.get("ok") else "UNAVAILABLE", "informational", "Decision-package health is used as coverage evidence, not as a substitute for missing engines.")
    add("DECISION_HISTORY", "UNAVAILABLE", "informational", "Completed-decision history is not yet bound to this UI bridge contract.")
    add("ALERT_POLICY", "UNAVAILABLE", "informational", "Alert preferences are governed separately and are not assumed active here.")
    add("ASSET_UNIVERSE", "CONTRIBUTED", "informational", "Asset universe is sourced from Binance exchange metadata plus quality-live external registry.")
    selected_tf = str(live.get("selected_timeframe") or "").lower()
    add("TIMEFRAME", "CONTRIBUTED" if selected_tf == str(timeframe).lower() else "PARTIAL", "supports", "The requested timeframe must match the backend-selected timeframe.")
    mode_state = str((validation.get("context") or {}).get("analysis_mode_binding") or "UNAVAILABLE")
    add("ANALYSIS_MODE", mode_state, "blocks", "Analysis mode remains fail-closed until backend evidence proves the requested mode is bound.")
    add("PRESENTATION_MODE", "CONTRIBUTED", "informational", "Presentation mode changes density only and does not alter calculation context.")

    known_ids = {row[0] for row in CAPABILITY_DEFINITIONS}
    emitted_ids = {row["id"] for row in capabilities}
    silent_omissions = sorted(known_ids - emitted_ids)

    layer_state_map = {
        "SOURCE": "CONTRIBUTED" if source_ok else "BLOCKED",
        "SESSION": "UNAVAILABLE",
        "TIMING": "UNAVAILABLE",
        "COT": status_by_id.get("COT", "UNAVAILABLE"),
        "TDL": status_by_id.get("TDL", "UNAVAILABLE"),
        "DIRECTION": status_by_id.get("MARKET_STRUCTURE", "UNAVAILABLE"),
        "MACRO": status_by_id.get("MACRO", "UNAVAILABLE"),
        "NMP": status_by_id.get("NMP", "UNAVAILABLE"),
        "HORIZON": "CONTRIBUTED" if public.get("reading_horizon") or public.get("horizon_strength") else "UNAVAILABLE",
        "MOMENTUM": "PARTIAL" if technical_partial else "UNAVAILABLE",
        "DIVERGENCE": status_by_id.get("DIVERGENCE", "UNAVAILABLE"),
        "BLOCKERS": status_by_id.get("BLOCKERS", "UNAVAILABLE"),
        "DECISION_QUALITY": status_by_id.get("DECISION_QUALITY", "UNAVAILABLE"),
        "RISK": status_by_id.get("RISK", "UNAVAILABLE"),
        "FINAL_DECISION": "BLOCKED",
        "ALERTS": status_by_id.get("ALERT_POLICY", "UNAVAILABLE"),
    }
    layer_coverage = [
        {
            "layer": layer_id,
            "public_label": label,
            "state": layer_state_map.get(capability_key, "UNAVAILABLE"),
            "protected": capability_key in {"COT", "TDL", "MACRO", "NMP", "BLOCKERS", "RISK", "FINAL_DECISION"},
        }
        for layer_id, label, capability_key in LAYER_REGISTRY
    ]

    critical_ids = {"TDL", "NMP", "RISK", "BLOCKERS", "TIMEFRAME", "ANALYSIS_MODE", "FRESHNESS"}
    critical_bad = [
        row for row in capabilities
        if row["id"] in critical_ids and row["state"] not in {"CONTRIBUTED", "GOVERNANCE_PROTECTED"}
    ]
    decision_ready = validation.get("valid_context") is True and not critical_bad and not silent_omissions

    counts: dict[str, int] = {}
    for row in capabilities:
        counts[row["state"]] = counts.get(row["state"], 0) + 1

    return {
        "ok": True,
        "contract": "NDSP_CAPABILITY_COVERAGE_V1",
        "context": validation.get("context"),
        "validation_errors": validation.get("errors") or [],
        "decision_ready": decision_ready,
        "official_state": "READY" if decision_ready else "BLOCKED",
        "silent_omission_count": len(silent_omissions),
        "silent_omissions": silent_omissions,
        "capability_counts": counts,
        "capabilities": capabilities,
        "layer_coverage": layer_coverage,
        "decision_summary": {
            "directional_bias": public.get("directional_bias"),
            "decision_quality": public.get("decision_quality"),
            "reading_horizon": public.get("reading_horizon"),
            "market_state": public.get("market_state"),
            "caution_reason": public.get("caution_reason"),
            "sanitized_summary": public.get("sanitized_summary"),
            "scenario_state": scenario.get("scenario_state"),
            "activation": scenario.get("scenario_activation_level"),
            "arrival": scenario.get("scenario_arrival_level"),
            "review": scenario.get("scenario_review_zone"),
            "invalidation": scenario.get("scenario_invalidation_level"),
            "generated_at": generated_at,
        },
        "governance": {
            "frontend_recomputes_protected_logic": False,
            "protected_formulas_exposed": False,
            "presentation_mode_changes_calculation": False,
            "no_silent_omission": len(silent_omissions) == 0,
            "fail_closed": True,
        },
        "generated_at": now(),
    }


@app.get("/api/dashboard/overview")
def dashboard_overview(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q

    inst = q.get("instrument", {})
    public = q.get("allowed_public_outputs", {})
    live = q.get("live_market_analysis", {})
    scenario = q.get("scenario", {})
    golden = q.get("golden_spotlight", {})

    return {
        "ok": True,
        "symbol": inst.get("symbol", symbol),
        "live_price": inst.get("live_price"),
        "market": inst.get("market"),
        "directional_bias": public.get("directional_bias"),
        "market_state": public.get("market_state"),
        "decision_quality": public.get("decision_quality"),
        "reading_horizon": public.get("reading_horizon"),
        "horizon_strength": public.get("horizon_strength"),
        "scenario_state": scenario.get("scenario_state"),
        "golden_signal": q.get("golden_signal"),
        "golden_status": q.get("golden_status"),
        "golden_label": golden.get("label") if isinstance(golden, dict) else None,
        "price_change_24h_pct": live.get("price_change_24h_pct"),
        "provider": q.get("data_provider"),
        "generated_at": q.get("generated_at") or now(),
        "source_mode": q.get("source_mode"),
    }


@app.get("/api/market/assets")
def market_assets(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q

    inst = q.get("instrument", {})
    live = q.get("live_market_analysis", {})

    return {
        "ok": True,
        "selected": {
            "symbol": inst.get("symbol", symbol),
            "market": inst.get("market"),
            "timeframe": inst.get("timeframe"),
            "live_price": inst.get("live_price"),
            "provider": q.get("data_provider"),
        },
        "live": {
            "price": live.get("price"),
            "price_change_24h_pct": live.get("price_change_24h_pct"),
            "atr_4h": live.get("atr_4h"),
            "atr_4h_pct": live.get("atr_4h_pct"),
            "rsi_4h": live.get("rsi_4h"),
            "h1_direction": live.get("h1_direction"),
            "h4_direction": live.get("h4_direction"),
            "d1_direction": live.get("d1_direction"),
            "selected_timeframe": live.get("selected_timeframe"),
            "selected_timeframe_label": live.get("selected_timeframe_label"),
            "selected_timeframe_direction": live.get("selected_timeframe_direction"),
            "selected_timeframe_close": live.get("selected_timeframe_close"),
            "selected_timeframe_rsi": live.get("selected_timeframe_rsi"),
            "selected_timeframe_atr": live.get("selected_timeframe_atr"),
        },
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/layers")
def layers(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q

    public = q.get("allowed_public_outputs", {})
    live = q.get("live_market_analysis", {})
    exp = q.get("explainability", {})

    return {
        "ok": True,
        "symbol": symbol,
        "layers": [
            {"name": "طبقة قراءة الاتجاه", "status": public.get("directional_bias"), "strength": public.get("horizon_strength"), "visible": True},
            {"name": "طبقة جودة القرار", "status": public.get("decision_quality"), "strength": public.get("horizon_strength"), "visible": True},
            {"name": "طبقة السعر الحي", "status": "متصلة" if q.get("live_price_bound") else "غير متصلة", "provider": q.get("data_provider"), "visible": True},
            {"name": "طبقة الإطار الزمني", "status": live.get("selected_timeframe_label"), "direction": live.get("selected_timeframe_direction"), "visible": True},
            {"name": "الطبقات المحمية", "status": "محكومة", "protected_layers_masked": exp.get("protected_layers_masked", True) if isinstance(exp, dict) else True, "visible": True},
        ],
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/market-structure")
def market_structure(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q
    live = q.get("live_market_analysis", {})
    public = q.get("allowed_public_outputs", {})
    return {
        "ok": True,
        "symbol": symbol,
        "market_state": public.get("market_state") or live.get("market_state"),
        "direction": live.get("direction"),
        "h1_direction": live.get("h1_direction"),
        "h4_direction": live.get("h4_direction"),
        "d1_direction": live.get("d1_direction"),
        "selected_timeframe": live.get("selected_timeframe"),
        "selected_timeframe_label": live.get("selected_timeframe_label"),
        "selected_timeframe_direction": live.get("selected_timeframe_direction"),
        "technical_review_price": live.get("technical_review_price"),
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/technical-confirmation")
def technical_confirmation(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q
    live = q.get("live_market_analysis", {})
    return {
        "ok": True,
        "symbol": symbol,
        "rsi_4h": live.get("rsi_4h"),
        "atr_4h": live.get("atr_4h"),
        "atr_4h_pct": live.get("atr_4h_pct"),
        "selected_timeframe_rsi": live.get("selected_timeframe_rsi"),
        "selected_timeframe_atr": live.get("selected_timeframe_atr"),
        "momentum_price_4h": live.get("momentum_price_4h"),
        "momentum_close_time_4h": live.get("momentum_close_time_4h"),
        "technical_review_price": live.get("technical_review_price"),
        "confirmation_state": live.get("horizon_strength"),
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/macro-analysis")
def macro_analysis(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q
    public = q.get("allowed_public_outputs", {})
    explicit_macro = _deep_has(q, ("usd_pressure", "usd_strength", "macro_state"))
    return {
        "ok": True,
        "symbol": symbol,
        "macro_state": "AVAILABLE" if explicit_macro else "UNAVAILABLE",
        "public_context": public.get("market_state"),
        "reading_horizon": public.get("reading_horizon"),
        "horizon_strength": public.get("horizon_strength"),
        "notice": "لا يتم اختلاق قراءة للدولار أو السياق الكلي عند غياب محرك صريح.",
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/risk-layer")
def risk_layer(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q
    public = q.get("allowed_public_outputs", {})
    scenario = q.get("scenario", {})
    return {
        "ok": True,
        "symbol": symbol,
        "caution_reason": public.get("caution_reason"),
        "scenario_risk_note": scenario.get("scenario_risk_note"),
        "scenario_invalidation_level": scenario.get("scenario_invalidation_level"),
        "scenario_review_zone": scenario.get("scenario_review_zone"),
        "risk_binding": "PARTIAL" if public.get("caution_reason") or scenario.get("scenario_risk_note") else "UNAVAILABLE",
        "not_recommendation": True,
        "no_buy_sell": True,
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/nawaf-signal")
def nawaf_signal(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q
    return {
        "ok": True,
        "symbol": symbol,
        "golden_signal": q.get("golden_signal"),
        "golden_alignment_active": q.get("golden_alignment_active"),
        "golden_status": q.get("golden_status"),
        "golden_name": q.get("golden_name"),
        "golden_spotlight": q.get("golden_spotlight"),
        "golden_alignment": q.get("golden_alignment"),
        "explainability": q.get("public_explainability"),
        "generated_at": q.get("generated_at") or now(),
    }


@app.get("/api/alerts")
def alerts(symbol: str = Query("BTCUSDT"), timeframe: str = Query("weekly")):
    q = fetch_quality(symbol, timeframe)
    if not q.get("ok"):
        return q
    scenario = q.get("scenario", {})
    public = q.get("allowed_public_outputs", {})
    items = []
    if public.get("caution_reason"):
        items.append({"type": "caution", "title": "تنبيه تحفظ", "message": public.get("caution_reason")})
    if scenario.get("scenario_state"):
        items.append({"type": "scenario", "title": "حالة السيناريو", "message": scenario.get("scenario_state")})
    return {"ok": True, "symbol": symbol, "alerts": items, "generated_at": q.get("generated_at") or now()}


@app.get("/api/settings")
def settings():
    return {
        "ok": True,
        "language": "ar",
        "theme": "dark",
        "direction": "rtl",
        "data_mode": "live_backend",
        "protected_layers_masked": True,
        "generated_at": now(),
    }


@app.get("/api/account/profile")
def account_profile():
    return {
        "ok": True,
        "profile_mode": "session_required_frontend",
        "message": "اربط هذه الصفحة لاحقاً بجلسة المستخدم الفعلية من نظام الدخول.",
        "generated_at": now(),
    }
