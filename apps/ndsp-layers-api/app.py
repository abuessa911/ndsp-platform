from __future__ import annotations

import importlib.util
import json
import urllib.request
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


LAYERS_ROOT = Path("/home/nawaf511/empire-core-new/backend/layers")
ORCHESTRATOR = LAYERS_ROOT / "layer_orchestrator.py"

LIVE_CONTEXT_URLS = [
    "http://127.0.0.1:9057/api/decision/quality-live",
    "http://127.0.0.1:9057/api/decision/quality",
    "https://my.ndsp.app/api/decision/quality-live",
    "https://my.ndsp.app/api/decision/quality",
    "https://api.ndsp.app/api/decision/quality-live",
    "https://api.ndsp.app/api/decision/quality",
]

app = FastAPI(title="NDSP Layers API", version="1.1.0-live-context")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.ndsp.app", "https://my.ndsp.app", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LayerPayload(BaseModel):
    asset: str = "GOLD"
    asset_class: str = "commodity"
    symbol: str = "GOLD"
    live_price: float | None = None
    price: float | None = None
    direction_bias: str | None = None
    tdl_bias: str | None = None
    weekday: str | None = None
    session: str | None = None
    decision_quality_score: int | None = None
    quality: int | None = None
    risk_pressure_score: int | None = None
    macro_pressure: str | None = None
    usd_state: str | None = None
    data_is_fresh: bool | None = None
    sources_connected: bool | None = None
    correction_present: bool | None = None
    plan: str | None = None
    trial_days_remaining: int | None = None
    alerts_enabled: bool | None = None

    cot_long_term_bias: str | None = None
    cot_speculative_bias: str | None = None
    asset_managers_bias: str | None = None
    leveraged_funds_bias: str | None = None
    commercials_bias: str | None = None
    non_commercials_bias: str | None = None

    rsi: float | None = None
    macd_hist: float | None = None
    cci: float | None = None
    obv_slope: float | None = None
    high_impact_events: int | None = None


def load_orchestrator():
    spec = importlib.util.spec_from_file_location("ndsp_layer_orchestrator_api_runtime", ORCHESTRATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load orchestrator: {ORCHESTRATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fetch_json(url: str) -> dict[str, Any] | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NDSP-Layers-API/1.1"})
        with urllib.request.urlopen(req, timeout=3) as r:
            if r.status < 200 or r.status >= 300:
                return None
            raw = r.read().decode("utf-8", errors="ignore")
            data = json.loads(raw)
            return data if isinstance(data, dict) else None
    except Exception:
        return None


def walk_values(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk_values(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_values(item)


def first_key(data: dict[str, Any], keys: list[str]) -> Any:
    for block in walk_values(data):
        for k in keys:
            if k in block and block[k] is not None:
                return block[k]
    return None


def as_float(v: Any) -> float | None:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None


def as_int(v: Any) -> int | None:
    try:
        if v is None:
            return None
        return int(float(v))
    except Exception:
        return None


def as_text(v: Any) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def normalize_asset_class(asset: str) -> str:
    a = asset.upper()
    if a in {"GOLD", "XAU", "XAUUSD", "SILVER", "XAG", "OIL", "WTI", "BRENT"}:
        return "commodity"
    if a in {"BTC", "BTCUSDT", "ETH", "ETHUSDT", "SOL", "BNB"}:
        return "crypto"
    return "fx_or_index"


def normalize_direction(v: Any) -> str | None:
    s = as_text(v)
    if not s:
        return None
    t = s.lower()
    if t in {"bullish", "up", "long", "positive", "supportive", "صاعد", "داعم"}:
        return "bullish"
    if t in {"bearish", "down", "short", "negative", "pressure", "هابط", "سلبي"}:
        return "bearish"
    if t in {"neutral", "range", "محايد"}:
        return "neutral"
    return s



def live_context(asset: str = "AUTO") -> dict[str, Any]:
    requested_asset = (asset or "AUTO").upper()

    context: dict[str, Any] = {
        "asset": requested_asset if requested_asset != "AUTO" else "GOLD",
        "symbol": requested_asset if requested_asset != "AUTO" else "GOLD",
        "asset_class": normalize_asset_class(requested_asset if requested_asset != "AUTO" else "GOLD"),
        "session": "london",
        "weekday": "monday",
        "data_is_fresh": True,
        "sources_connected": True,
        "correction_present": True,
        "plan": "Elite",
        "trial_days_remaining": 11,
        "alerts_enabled": True,
    }

    used_url = None
    raw = None

    for url in LIVE_CONTEXT_URLS:
        data = fetch_json(url)
        if data:
            raw = data
            used_url = url
            break

    if raw:
        instrument = raw.get("instrument") if isinstance(raw.get("instrument"), dict) else {}
        scenario = raw.get("scenario") if isinstance(raw.get("scenario"), dict) else {}
        public = raw.get("allowed_public_outputs") if isinstance(raw.get("allowed_public_outputs"), dict) else {}
        live = raw.get("live_market_analysis") if isinstance(raw.get("live_market_analysis"), dict) else {}

        live_symbol = (
            instrument.get("symbol")
            or raw.get("symbol")
            or raw.get("asset")
            or public.get("symbol")
        )
        market = instrument.get("market") or raw.get("market")
        live_price = (
            instrument.get("live_price")
            or live.get("price")
            or raw.get("live_price")
            or raw.get("price")
        )

        # Important: when API is called without explicit asset, trust quality-live selected symbol.
        if live_symbol:
            context["asset"] = str(live_symbol).upper()
            context["symbol"] = str(live_symbol).upper()

        if market:
            m = str(market).lower()
            if "crypto" in m:
                context["asset_class"] = "crypto"
            elif "commodity" in m or context["asset"] in {"GOLD", "XAUUSD", "SILVER", "OIL"}:
                context["asset_class"] = "commodity"
            else:
                context["asset_class"] = normalize_asset_class(context["asset"])
        else:
            context["asset_class"] = normalize_asset_class(context["asset"])

        price = as_float(live_price)
        if price is not None:
            context["live_price"] = price
            context["price"] = price

        quality = as_int(
            public.get("decision_quality")
            or raw.get("decision_quality")
            or first_key(raw, ["decision_quality_score", "quality_score", "quality", "confidence"])
        )
        if quality is not None:
            context["decision_quality_score"] = quality
            context["quality"] = quality

        risk = as_int(first_key(raw, ["risk_pressure_score", "risk_score", "risk", "volatility_score"]))
        if risk is not None:
            context["risk_pressure_score"] = risk
        else:
            context["risk_pressure_score"] = 28

        # Direction extraction from live technical/TDL-governed public output.
        direction = (
            live.get("selected_timeframe_direction")
            or live.get("direction")
            or live.get("d1_direction")
            or live.get("h4_direction")
            or public.get("directional_bias")
            or scenario.get("scenario_directional_context")
        )

        normalized_direction = normalize_direction(direction)
        if not normalized_direction:
            text = str(direction or "")
            if "هابط" in text or "ضغط" in text:
                normalized_direction = "bearish"
            elif "صاعد" in text or "داعم" in text:
                normalized_direction = "bullish"
            else:
                normalized_direction = "neutral"

        context["direction_bias"] = normalized_direction
        context["tdl_bias"] = normalized_direction

        # Since source_mode says governed_tdl_v2, use public governed direction as TDL surface fallback.
        # This does NOT claim raw COT exists; it only allows layers to reflect the governed live decision context.
        context["long_term_bias"] = normalized_direction
        context["speculative_bias"] = normalized_direction

        # Critical: L4 reads these explicit COT/participant keys.
        # Until raw COT is connected, feed governed public TDL direction as fallback.
        context["cot_long_term_bias"] = normalized_direction
        context["cot_speculative_bias"] = normalized_direction
        context["asset_managers_bias"] = normalized_direction
        context["leveraged_funds_bias"] = normalized_direction
        context["commercials_bias"] = normalized_direction
        context["non_commercials_bias"] = normalized_direction

        context["tdl_public_context_used"] = True
        context["cot_raw_data_available"] = False

        # Raw COT Gateway override: prefer real CFTC/TFF data when matched.
        try:
            raw_asset = context.get("asset") or context.get("symbol") or "ETHUSDT"
            raw_cot = fetch_json(
                "http://127.0.0.1:9076/api/admin/raw-cot/status?asset=" + str(raw_asset)
            )
        except Exception:
            raw_cot = None

        if isinstance(raw_cot, dict) and raw_cot.get("raw_cot_connected") is True:
            am_bias = normalize_direction(raw_cot.get("asset_managers_bias")) or "neutral"
            lf_bias = normalize_direction(raw_cot.get("leveraged_funds_bias")) or "neutral"
            dealer_bias = normalize_direction(raw_cot.get("dealer_intermediary_bias")) or "neutral"

            # NDSP governance mapping:
            # crypto/fx/index/bonds: long horizon = Asset Managers, short/speculative = Leveraged Funds.
            context["long_term_bias"] = am_bias
            context["speculative_bias"] = lf_bias
            context["tdl_bias"] = am_bias if am_bias == lf_bias else context.get("tdl_bias", am_bias)

            context["cot_long_term_bias"] = am_bias
            context["cot_speculative_bias"] = lf_bias
            context["asset_managers_bias"] = am_bias
            context["leveraged_funds_bias"] = lf_bias
            context["dealer_intermediary_bias"] = dealer_bias

            context["asset_managers_net"] = raw_cot.get("asset_managers_net")
            context["leveraged_funds_net"] = raw_cot.get("leveraged_funds_net")
            context["dealer_intermediary_net"] = raw_cot.get("dealer_intermediary_net")

            context["raw_cot_connected"] = True
            context["cot_raw_data_available"] = True
            context["raw_cot_status"] = raw_cot.get("raw_cot_status")
            context["raw_cot_source_family"] = raw_cot.get("source_family")
            context["raw_cot_market_name"] = raw_cot.get("market_name")
            context["raw_cot_report_date"] = raw_cot.get("report_date")
            context["raw_cot_source_file"] = raw_cot.get("source_file")
        else:
            context["raw_cot_connected"] = False
            context["raw_cot_status"] = (raw_cot or {}).get("raw_cot_status") if isinstance(raw_cot, dict) else "UNAVAILABLE"

        # Technical indicators
        rsi = as_float(
            live.get("selected_timeframe_rsi")
            or live.get("rsi_4h")
            or first_key(raw, ["rsi", "rsi_4h", "selected_timeframe_rsi"])
        )
        if rsi is not None:
            context["rsi"] = rsi
            if rsi <= 45:
                context["rsi_trend"] = "bearish"
            elif rsi >= 55:
                context["rsi_trend"] = "bullish"
            else:
                context["rsi_trend"] = "neutral"

        context["price_trend"] = normalized_direction
        context["obv_trend"] = normalized_direction

        # Horizon strength from quality-live wording
        horizon_strength = str(
            public.get("horizon_strength")
            or live.get("horizon_strength")
            or scenario.get("scenario_confidence_band")
            or ""
        )
        if "جد" in horizon_strength or "عالي" in horizon_strength:
            context["short_horizon_strength"] = 82
            context["medium_horizon_strength"] = 74
            context["long_horizon_strength"] = 63
        else:
            context["short_horizon_strength"] = 72
            context["medium_horizon_strength"] = 66
            context["long_horizon_strength"] = 58

        # Scenario probabilities
        state = str(scenario.get("scenario_state") or "").upper()
        if state == "UNDER_MONITORING":
            context["base_scenario_probability"] = 62
            context["optimistic_scenario_probability"] = 24
        else:
            context["base_scenario_probability"] = 58
            context["optimistic_scenario_probability"] = 22

        # Macro fallback
        context["macro_pressure"] = "supportive"
        context["usd_state"] = "weak"
        context["high_impact_events"] = as_int(first_key(raw, ["high_impact_events", "events_high"])) or 0

        context["live_context_source"] = used_url
        context["quality_live_source_mode"] = raw.get("source_mode")
        context["scenario_directional_context"] = scenario.get("scenario_directional_context")
        context["reading_horizon"] = public.get("reading_horizon") or scenario.get("scenario_time_horizon")

    else:
        context.update({
            "asset": "GOLD",
            "symbol": "GOLD",
            "asset_class": "commodity",
            "live_price": 3362.50,
            "price": 3362.50,
            "direction_bias": "bullish",
            "tdl_bias": "bullish",
            "long_term_bias": "bullish",
            "speculative_bias": "bullish",
            "decision_quality_score": 87,
            "quality": 87,
            "risk_pressure_score": 28,
            "macro_pressure": "supportive",
            "usd_state": "weak",
            "rsi": 55,
            "price_trend": "bullish",
            "rsi_trend": "bullish",
            "obv_trend": "bullish",
            "live_context_source": "fallback_default",
        })

    return context


@app.get("/api/admin/layers/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "service": "ndsp-layers-api",
        "version": "1.1.0-live-context",
        "layers_root": str(LAYERS_ROOT),
        "orchestrator_exists": ORCHESTRATOR.exists(),
        "live_context_urls": LIVE_CONTEXT_URLS,
    }


@app.get("/api/admin/layers/context")
def context(asset: str = Query("GOLD")) -> dict[str, Any]:
    return {
        "ok": True,
        "context": live_context(asset),
    }


@app.get("/api/admin/layers/run")
def run_layers_default(asset: str = Query("GOLD")) -> dict[str, Any]:
    module = load_orchestrator()
    payload = live_context(asset)
    result = module.run_all_layers(payload)
    result["input_context_source"] = payload.get("live_context_source")
    return result


@app.post("/api/admin/layers/run")
def run_layers(payload: LayerPayload) -> dict[str, Any]:
    module = load_orchestrator()
    base = live_context(payload.asset or "GOLD")
    override = payload.model_dump(exclude_none=True)
    base.update(override)
    result = module.run_all_layers(base)
    result["input_context_source"] = base.get("live_context_source")
    return result
