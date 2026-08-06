from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import urllib.request, json, time, datetime

app = FastAPI(title="NDSP Decision Package API v1")

BASE_QUALITY_URL = "https://api.ndsp.app/api/decision/quality-live"

def fetch_json(url: str, timeout: int = 8):
    req = urllib.request.Request(url, headers={"User-Agent": "NDSP-Decision-Package-v1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))

def score_from_text(value):
    s = str(value or "")
    if "مرتفع" in s or "قوي" in s:
        return 85
    if "متوسط" in s:
        return 65
    if "منخفض" in s or "ضعيف" in s:
        return 45
    if "هابط" in s or "صاعد" in s:
        return 70
    return 50

def direction_from_context(ctx):
    s = str(ctx or "")
    if "هابط" in s:
        return "SHORT"
    if "صاعد" in s:
        return "LONG"
    return "NEUTRAL"

def state_from_quality(q, blocked=False, degraded=False):
    if blocked:
        return "BLOCKED"
    if degraded:
        return "WATCH"
    if q >= 90:
        return "HIGH_CONFIDENCE"
    if q >= 75:
        return "GOOD"
    if q >= 55:
        return "WATCH"
    if q >= 40:
        return "CAUTION"
    return "LOW_QUALITY"

@app.get("/health")
def health():
    return {"ok": True, "service": "ndsp-decision-package-v1", "port": 9061}

@app.get("/api/decision/package-live")
def package_live(symbol: str = Query("BTCUSDT")):
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    warnings = []
    reasons = []

    try:
        q = fetch_json(f"{BASE_QUALITY_URL}?symbol={symbol}")
    except Exception as e:
        return JSONResponse(status_code=503, content={
            "ok": False,
            "engine_status": "BLOCKED",
            "decision_state": "BLOCKED",
            "reason": "QUALITY_LIVE_UNAVAILABLE",
            "error": str(e),
            "symbol": symbol,
            "generated_at": now
        })

    scenario = q.get("scenario") or {}
    instrument = q.get("instrument") or {}
    ctx = scenario.get("scenario_directional_context")
    direction = direction_from_context(ctx)

    scenario_score = score_from_text(ctx)
    confidence_score = score_from_text(scenario.get("scenario_confidence_band"))
    quality = round((scenario_score * 0.55) + (confidence_score * 0.45))

    required_missing = []
    for key in ["momentum", "divergence", "nmp", "usd_strength", "economic_news", "risk", "devil"]:
        required_missing.append(key)

    if required_missing:
        warnings.append("Some advanced layers are not yet fully calculated by this adapter; marked as pending, not faked.")

    engine_status = "DEGRADED" if required_missing else "OK"

    package = {
        "ok": True,
        "project": "NDSP",
        "contract_version": "decision-package-v1",
        "engine_status": engine_status,
        "decision_state": state_from_quality(quality, degraded=(engine_status == "DEGRADED")),
        "symbol": symbol,
        "generated_at": now,
        "source_mode": q.get("source_mode"),
        "direction": direction,
        "decision_quality": quality,
        "stability": "MEDIUM",
        "risk_level": "UNKNOWN",
        "instrument": instrument,
        "scenario": {
            "state": scenario.get("scenario_state"),
            "directional_context": ctx,
            "activation": scenario.get("scenario_activation_level"),
            "arrival": scenario.get("scenario_arrival_level"),
            "review": scenario.get("scenario_review_zone"),
            "invalidation": scenario.get("scenario_invalidation_level"),
            "confidence_band": scenario.get("scenario_confidence_band"),
            "time_horizon": scenario.get("scenario_time_horizon"),
            "last_updated": scenario.get("scenario_last_updated")
        },
        "layers": {
            "cot_freshness": {
                "status": "UNKNOWN",
                "can_block": True,
                "score": None
            },
            "tdl": {
                "status": "AVAILABLE",
                "can_block": False,
                "direction": direction,
                "score": scenario_score
            },
            "scenario_levels": {
                "status": "AVAILABLE",
                "can_block": False,
                "score": scenario_score
            },
            "momentum": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": False,
                "score": None
            },
            "divergence": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": False,
                "regular_divergence": None,
                "hidden_divergence": None,
                "score": None
            },
            "nmp": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": False,
                "score": None
            },
            "usd_strength": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": False,
                "score": None
            },
            "economic_news": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": False,
                "score": None
            },
            "risk": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": False,
                "score": None
            },
            "devil": {
                "status": "PENDING_ENGINE_BINDING",
                "can_block": True,
                "emergency_stop": False,
                "score": None
            },
            "data_governance": {
                "status": "DEGRADED",
                "can_block": True,
                "missing_layers": required_missing,
                "no_fake_values": True
            }
        },
        "timeframes": {
            "weekly": {
                "status": "SOURCE_AVAILABLE",
                "scenario": "calculated_from_quality_live"
            },
            "daily": {
                "status": "PENDING_ENGINE_BINDING"
            },
            "4h": {
                "status": "PENDING_ENGINE_BINDING"
            },
            "1h": {
                "status": "PENDING_ENGINE_BINDING"
            }
        },
        "reasons": [
            "Decision package generated from existing quality-live engine.",
            "Scenario levels are real from backend quality-live.",
            "Missing advanced layers are not fabricated."
        ],
        "warnings": warnings,
        "raw_quality_live": q
    }

    return package


# =========================
# NDSP Decision Package v2
# Governance / Engine Health
# =========================

REQUIRED_ENGINES_V2 = [
    "cot_freshness",
    "tdl",
    "scenario_levels",
    "multi_timeframe_alignment",
    "scenario_maturity",
    "nmp",
    "momentum",
    "regular_divergence",
    "hidden_divergence",
    "usd_strength",
    "economic_news",
    "economic_calendar",
    "risk",
    "devil",
    "data_integrity",
    "data_governance",
]

REQUIRED_TIMEFRAMES_V2 = ["weekly", "daily", "4h", "1h", "15m"]

def _now_utc():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def _engine_ok(name, source="quality-live", score=None, details=None):
    return {
        "engine": name,
        "status": "OK",
        "source": source,
        "score": score,
        "last_updated": _now_utc(),
        "execution_ms": None,
        "needs_action": False,
        "issue": None,
        "repair_action": None,
        "details": details or {}
    }

def _engine_action(name, issue, repair_action, source="not-bound-yet"):
    return {
        "engine": name,
        "status": "ACTION_REQUIRED",
        "source": source,
        "score": None,
        "last_updated": None,
        "execution_ms": None,
        "needs_action": True,
        "issue": issue,
        "repair_action": repair_action,
        "details": {}
    }

def _verified_from_health(health):
    bad = [x for x in health if x.get("status") != "OK"]
    if bad:
        return "ACTION_REQUIRED"
    return "VERIFIED"

def _health_summary(health):
    total = len(health)
    ok = len([x for x in health if x.get("status") == "OK"])
    action = len([x for x in health if x.get("status") == "ACTION_REQUIRED"])
    blocked = len([x for x in health if x.get("status") == "BLOCKED"])
    return {
        "total_engines": total,
        "ok": ok,
        "action_required": action,
        "blocked": blocked,
        "completeness_percent": round((ok / total) * 100) if total else 0
    }

@app.get("/api/decision/package-v2")
def package_v2(symbol: str = Query("BTCUSDT")):
    now = _now_utc()

    try:
        q = fetch_json(f"{BASE_QUALITY_URL}?symbol={symbol}")
    except Exception as e:
        health = [
            _engine_action(
                "quality_live_source",
                "Existing quality-live source is unavailable.",
                "Check api.ndsp.app /api/decision/quality-live route and backend service."
            )
        ]
        return JSONResponse(status_code=503, content={
            "ok": False,
            "project": "NDSP",
            "contract_version": "decision-package-v2",
            "symbol": symbol,
            "generated_at": now,
            "engine_status": "BLOCKED",
            "decision_verification": "BLOCKED",
            "decision_state": "BLOCKED",
            "decision_quality": None,
            "decision_quality_status": "NOT_CALCULATED",
            "reason": "QUALITY_LIVE_UNAVAILABLE",
            "error": str(e),
            "engine_health": health,
            "system_integrity": _health_summary(health),
            "alerts": [
                {
                    "severity": "critical",
                    "title_ar": "تعذر إنتاج حزمة القرار",
                    "message_ar": "مصدر quality-live غير متاح، لذلك لا يمكن إصدار قرار مكتمل الأركان."
                }
            ]
        })

    scenario = q.get("scenario") or {}
    instrument = q.get("instrument") or {}
    ctx = scenario.get("scenario_directional_context")
    direction = direction_from_context(ctx)

    health = []

    # Real values currently available from quality-live
    health.append(_engine_ok("tdl", score=None, details={"direction": direction, "context": ctx}))
    health.append(_engine_ok("scenario_levels", score=None, details={
        "activation": scenario.get("scenario_activation_level"),
        "arrival": scenario.get("scenario_arrival_level"),
        "review": scenario.get("scenario_review_zone"),
        "invalidation": scenario.get("scenario_invalidation_level")
    }))

    # Engines not yet fully bound must be explicit, not faked
    pending_specs = {
        "cot_freshness": "Connect real COT freshness validator.",
        "multi_timeframe_alignment": "Calculate real alignment across weekly/daily/4h/1h/15m.",
        "scenario_maturity": "Calculate real scenario maturity: EARLY/MID/LATE/EXHAUSTED.",
        "nmp": "Calculate real NMP for every required timeframe.",
        "momentum": "Calculate real momentum for every required timeframe.",
        "regular_divergence": "Calculate real regular divergence for every required timeframe.",
        "hidden_divergence": "Calculate real hidden divergence for every required timeframe.",
        "usd_strength": "Connect real USD strength engine.",
        "economic_news": "Connect real economic news impact engine.",
        "economic_calendar": "Connect real economic calendar engine.",
        "risk": "Connect real risk engine.",
        "devil": "Connect real devil final auditor.",
        "data_integrity": "Validate no null, unknown, pending, copied, or stale values.",
        "data_governance": "Validate all engines completed with auditable real values."
    }

    for engine, action in pending_specs.items():
        health.append(_engine_action(
            engine,
            "Engine is not fully bound to real calculated data yet.",
            action
        ))

    verification = _verified_from_health(health)
    summary = _health_summary(health)

    alerts = []
    if verification != "VERIFIED":
        alerts.append({
            "severity": "warning",
            "title_ar": "القرار يحتاج معالجة بيانات",
            "message_ar": "حزمة القرار ظاهرة بشفافية، لكنها ليست VERIFIED لأن بعض المحركات لم تنتج بيانات حقيقية مكتملة بعد.",
            "repair_ar": "راجع Engine Health لمعرفة المحركات التي تحتاج ربط أو إصلاح."
        })

    package = {
        "ok": True,
        "project": "NDSP",
        "contract_version": "decision-package-v2",
        "symbol": symbol,
        "generated_at": now,

        "engine_status": "ACTION_REQUIRED" if verification != "VERIFIED" else "OK",
        "decision_verification": verification,

        "decision_state": "WATCH" if verification != "VERIFIED" else "READY",
        "decision_quality": None if verification != "VERIFIED" else "CALCULATED_BY_ENGINE",
        "decision_quality_status": "PENDING_VERIFICATION" if verification != "VERIFIED" else "VERIFIED",

        "direction": direction,
        "stability": None,
        "risk_level": None,

        "instrument": instrument,
        "scenario": {
            "state": scenario.get("scenario_state"),
            "directional_context": ctx,
            "activation": scenario.get("scenario_activation_level"),
            "arrival": scenario.get("scenario_arrival_level"),
            "review": scenario.get("scenario_review_zone"),
            "invalidation": scenario.get("scenario_invalidation_level"),
            "confidence_band": scenario.get("scenario_confidence_band"),
            "time_horizon": scenario.get("scenario_time_horizon"),
            "last_updated": scenario.get("scenario_last_updated")
        },

        "required_timeframes": REQUIRED_TIMEFRAMES_V2,
        "timeframes": {
            tf: {
                "status": "ACTION_REQUIRED",
                "issue": "Real timeframe calculations are not fully bound yet.",
                "required_values": ["scenario_levels", "nmp", "momentum", "regular_divergence", "hidden_divergence"]
            } for tf in REQUIRED_TIMEFRAMES_V2
        },

        "engine_health": health,
        "system_integrity": summary,
        "alerts": alerts,

        "decision_explanation": {
            "ar": "يعرض NDSP هنا القرار بشفافية. لا يتم اعتماد جودة قرار نهائية حتى تكتمل جميع المحركات ببيانات حقيقية قابلة للتحقق.",
            "user_reading_rule_ar": "إذا كانت Decision Verification = ACTION_REQUIRED فهذا يعني أن القرار يحتاج معالجة بيانات قبل اعتباره مكتمل الأركان."
        },

        "no_fake_values": True,
        "no_copied_timeframe_numbers": True,
        "raw_quality_live": q
    }

    return package
