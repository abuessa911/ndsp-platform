from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timezone

app = FastAPI(title="NDSP UI Bridge API", version="1.0.0")

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

def now():
    return datetime.now(timezone.utc).isoformat()

def fetch_quality(symbol: str):
    r = requests.get(QUALITY_URL, params={"symbol": symbol}, timeout=12)
    try:
        data = r.json()
    except Exception:
        return {"ok": False, "error": "QUALITY_LIVE_BAD_RESPONSE", "raw": r.text[:500]}

    if not data.get("ok"):
        return {"ok": False, "error": "QUALITY_LIVE_FAILED", "upstream": data}

    return data

@app.get("/api/ui-bridge/health")
def health():
    return {
        "ok": True,
        "service": "ndsp-ui-bridge-api",
        "generated_at": now(),
        "source": QUALITY_URL,
        "endpoints": [
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

@app.get("/api/dashboard/overview")
def dashboard_overview(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
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
        "golden_label": golden.get("label"),
        "price_change_24h_pct": live.get("price_change_24h_pct"),
        "provider": q.get("data_provider"),
        "generated_at": q.get("generated_at") or now(),
        "source_mode": q.get("source_mode"),
    }

@app.get("/api/market/assets")
def market_assets(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
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
def layers(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
    if not q.get("ok"):
        return q

    public = q.get("allowed_public_outputs", {})
    live = q.get("live_market_analysis", {})
    exp = q.get("explainability", {})

    return {
        "ok": True,
        "symbol": symbol,
        "layers": [
            {
                "name": "طبقة قراءة الاتجاه",
                "status": public.get("directional_bias"),
                "strength": public.get("horizon_strength"),
                "visible": True,
            },
            {
                "name": "طبقة جودة القرار",
                "status": public.get("decision_quality"),
                "strength": public.get("horizon_strength"),
                "visible": True,
            },
            {
                "name": "طبقة السعر الحي",
                "status": "متصلة" if q.get("live_price_bound") else "غير متصلة",
                "provider": q.get("data_provider"),
                "visible": True,
            },
            {
                "name": "طبقة الإطار الزمني",
                "status": live.get("selected_timeframe_label"),
                "direction": live.get("selected_timeframe_direction"),
                "visible": True,
            },
            {
                "name": "الطبقات المحمية",
                "status": "مخفية من الواجهة",
                "protected_layers_masked": exp.get("protected_layers_masked", True),
                "visible": False,
            },
        ],
        "generated_at": q.get("generated_at") or now(),
    }

@app.get("/api/market-structure")
def market_structure(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
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
def technical_confirmation(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
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
def macro_analysis(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
    if not q.get("ok"):
        return q

    public = q.get("allowed_public_outputs", {})

    return {
        "ok": True,
        "symbol": symbol,
        "macro_state": "محايد / غير معلن تفصيلياً",
        "public_context": public.get("market_state"),
        "reading_horizon": public.get("reading_horizon"),
        "horizon_strength": public.get("horizon_strength"),
        "notice": "هذه الواجهة تعرض المخرجات العامة فقط ولا تكشف الطبقات المحمية.",
        "generated_at": q.get("generated_at") or now(),
    }

@app.get("/api/risk-layer")
def risk_layer(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
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
        "not_recommendation": True,
        "no_buy_sell": True,
        "generated_at": q.get("generated_at") or now(),
    }

@app.get("/api/nawaf-signal")
def nawaf_signal(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
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
def alerts(symbol: str = Query("BTCUSDT")):
    q = fetch_quality(symbol)
    if not q.get("ok"):
        return q

    scenario = q.get("scenario", {})
    public = q.get("allowed_public_outputs", {})

    items = []
    if public.get("caution_reason"):
        items.append({
            "type": "caution",
            "title": "تنبيه تحفظ",
            "message": public.get("caution_reason"),
        })

    if scenario.get("scenario_state"):
        items.append({
            "type": "scenario",
            "title": "حالة السيناريو",
            "message": scenario.get("scenario_state"),
        })

    return {
        "ok": True,
        "symbol": symbol,
        "alerts": items,
        "generated_at": q.get("generated_at") or now(),
    }

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
