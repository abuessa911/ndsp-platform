from __future__ import annotations

import json
import csv
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

from app.core.decision_active_governance import enforce_decision_active_governance
from app.core.decision_engine import run_decision
from app.core.market_profile import resolve_market
from app.core.conflict_engine import run as detect_conflict
from app.core.compliance_layer import enforce
from app.core.explainability_layer import explain
from app.core.tdl_data_provider import build_tdl_data
from app.core.tdl_router import run_tdl
from app.core.momentum_dual import run_momentum_dual
from app.core.black_layer import evaluate_black_layer
from app.services.price_router import get_market_snapshot
from app.core.nmp_adapter import evaluate_nmp_context, evaluate_nmp_tdl_quality
from app.core.governance_runtime import apply_governance_runtime
from app.governance.tdl_v2_adapter import attach_tdl_v2_to_decision

GOVERNANCE_VERSION = "4.1.0"
PIPELINE_VERSION = "4.1.0-v6-governed-master-ndsp"

# NDSP_TDL_V2_LIVE_INTEGRATION_START
def _ndsp_attach_tdl_v2_safe(decision_payload: dict) -> dict:
    """
    Safely attach timing_model v2 to the final governed decision payload.
    If timing_model v2 fails for any reason, preserve the original payload.
    """
    try:
        if isinstance(decision_payload, dict):
            decision_payload = attach_tdl_v2_to_decision(decision_payload)
            return apply_governance_runtime(decision_payload)
    except Exception as exc:
        try:
            decision_payload.setdefault("meta", {})
            decision_payload["meta"]["tdl_v2_integration_error"] = str(exc)
        except Exception:
            pass
    return enforce_decision_active_governance(decision_payload)
# NDSP_TDL_V2_LIVE_INTEGRATION_END

# NDSP_MT4_FRESHNESS_BINDING_START
def _load_mt4_freshness_status() -> dict:
    json_path = Path("/home/nawaf511/empire-core-new/backend/runtime/mt4_freshness_status.json")
    csv_path = Path("/home/nawaf511/empire-core-new/backend/runtime/mt4_freshness_status.csv")

    # First: JSON status written atomically by the freshness guard.
    try:
        if json_path.exists():
            raw = json_path.read_text(encoding="utf-8").strip()
            if raw:
                data = json.loads(raw)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass

    # Fallback: CSV status, useful if JSON is briefly unreadable.
    try:
        if csv_path.exists():
            with csv_path.open("r", encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))

            symbols = []
            for row in rows:
                state = row.get("state") or "unknown"
                age_raw = row.get("age_seconds")
                try:
                    age = int(float(age_raw)) if age_raw not in (None, "") else None
                except Exception:
                    age = None

                ok_raw = str(row.get("ok") or "").lower().strip()
                ok = ok_raw in ("true", "1", "yes", "y")

                symbols.append({
                    "symbol": row.get("symbol"),
                    "ok": ok,
                    "state": state,
                    "age_seconds": age,
                    "file": row.get("file"),
                })

            return {
                "available": True,
                "state": "live" if symbols and all(x.get("ok") for x in symbols) else "stale_or_missing",
                "all_ok": bool(symbols and all(x.get("ok") for x in symbols)),
                "checked_at": rows[0].get("checked_at") if rows else None,
                "symbols": symbols,
            }
    except Exception as exc:
        return {
            "available": False,
            "state": "guard_status_error",
            "all_ok": False,
            "error": str(exc)[:180],
        }

    return {
        "available": False,
        "state": "missing_guard_status",
        "all_ok": False,
        "symbols": [],
    }

def _mt4_freshness_for_symbol(symbol: str) -> dict:
    s = str(symbol or "").upper().strip()
    status = _load_mt4_freshness_status()
    symbols = status.get("symbols") if isinstance(status, dict) else []

    match = None
    if isinstance(symbols, list):
        for row in symbols:
            if isinstance(row, dict) and str(row.get("symbol") or "").upper().strip() == s:
                match = row
                break

    if not match:
        return {
            "available": bool(status),
            "symbol": s,
            "ok": False,
            "state": status.get("state", "symbol_not_monitored") if isinstance(status, dict) else "symbol_not_monitored",
            "all_ok": bool(status.get("all_ok")) if isinstance(status, dict) else False,
            "checked_at": status.get("checked_at") if isinstance(status, dict) else None,
        }

    return {
        "available": True,
        "symbol": s,
        "ok": bool(match.get("ok")),
        "state": match.get("state"),
        "age_seconds": match.get("age_seconds"),
        "max_age_seconds": match.get("max_age_seconds"),
        "checked_at": status.get("checked_at") if isinstance(status, dict) else None,
        "file": match.get("file"),
    }

def _attach_mt4_freshness_to_market(symbol: str, market: dict) -> dict:
    market = _safe_dict(market)
    source = str(market.get("source") or "").lower().strip()

    if source != "mt4_fxcm":
        return market

    freshness = _mt4_freshness_for_symbol(symbol)
    source_status = market.get("source_status")
    if not isinstance(source_status, dict):
        source_status = {}

    source_status["freshness"] = freshness
    source_status["freshness_state"] = freshness.get("state")
    source_status["fresh"] = bool(freshness.get("ok"))

    market["source_status"] = source_status

    if not freshness.get("ok"):
        market["stale"] = True
        market["live"] = False
    else:
        market["stale"] = False
        market["live"] = True

    return market
# NDSP_MT4_FRESHNESS_BINDING_END

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _safe_dict(value) -> dict:
    return value if isinstance(value, dict) else {}

def _normalize_confidence(value) -> int:
    try:
        value = float(value)
    except Exception:
        return 0
    if value <= 1:
        value *= 100
    return int(max(0, min(100, round(value))))

def _direction(value) -> str:
    value = str(value or "").lower().strip()
    if value in ("buy", "bullish", "long"): return "bullish"
    if value in ("sell", "bearish", "short"): return "bearish"
    return "neutral"

def _tdl_primary_direction(timing_model: dict) -> str:
    return _direction(timing_model.get("tdl_lm_direction") or timing_model.get("dominant_side") or "neutral")

def _is_mt4_symbol(symbol: str) -> bool:
    s = str(symbol or "").upper().strip()
    try:
        watchlist_file = Path(__file__).resolve().parents[2] / "runtime" / "fxcm_watchlist.txt"
        if watchlist_file.exists():
            watchlist_symbols = {
                line.split("#", 1)[0].strip().upper()
                for line in watchlist_file.read_text(encoding="utf-8", errors="ignore").splitlines()
                if line.split("#", 1)[0].strip()
            }
            if s in watchlist_symbols: return True
    except Exception:
        pass
    mt4_symbols = {
        "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
        "BTCUSD", "BTCUSDT", "ETHUSD", "ETHUSDT", "BNBUSD", "BNBUSDT", "SOLUSD", "SOLUSDT",
        "XAUUSD", "XAGUSD",
        "US30", "NAS100", "SPX500", "UK100", "GER30", "FRA40", "JPN225", "AUS200",
        "UKOIL", "UKOILSPOT", "USOIL", "USOILSPOT",
    }
    return s in mt4_symbols

def _get_market(symbol: str) -> dict:
    symbol_upper = str(symbol or "").upper().strip()
    try:
        market = _safe_dict(get_market_snapshot(symbol_upper))
    except Exception as exc:
        market = {
            "symbol": symbol_upper,
            "symbol_id": f"{symbol_upper}-DATA",
            "price": None,
            "ohlcv": [],
            "candles": [],
            "last_candle": None,
            "source": "data_router",
            "source_status": {
                "available": False,
                "error": "price_router_failed",
                "detail": str(exc)[:180],
            },
        }

    if "ohlcv" not in market and "candles" in market:
        market["ohlcv"] = market.get("candles") or []
    if "candles" not in market and "ohlcv" in market:
        market["candles"] = market.get("ohlcv") or []

    market.setdefault("symbol", symbol_upper)
    market.setdefault("source", "price_router")
    return market

def _get_timing_v4() -> dict:
    """
    NDSP Layer 3: Timing Authority
    تحديد المسيطر الزمني بناءً على القواعد المعتمدة في V4.1
    (الإثنين والجمعة = L&M) | (الثلاثاء للأحد = S)
    """
    now = datetime.now(timezone.utc)
    weekday = now.weekday() # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    
    if weekday in (0, 4):
        controller = "L&M"
        day_group = "MON_FRI_INSTITUTIONAL"
    elif weekday == 6:
        controller = "NEUTRAL"
        day_group = "SUNDAY_REVIEW"
    else:
        controller = "S"
        day_group = "TUE_WED_THU_SAT_SPECULATIVE"

    return {
        "active": f"timing_model-{controller}" if controller != "NEUTRAL" else "OFF",
        "controller": controller,
        "day_group": day_group,
        "timestamp": now.isoformat(),
    }

def _resolve_dominant_direction(timing: dict, timing_model: dict) -> dict:
    """
    NDSP Layer 6: Dominant Timed Direction
    [CRITICAL RULE]: الاتجاه يؤخذ حصراً من هذه الدالة. يُمنع مساسه من أي طبقة أخرى.
    """
    controller = timing.get("controller", "S")
    
    # محاولة سحب الاتجاه من الهيكلة القديمة لـ timing_model إذا لم تكن الهيكلة الجديدة مطبقة بالكامل
    tdl_lm = _direction(timing_model.get("tdl_lm_direction", timing_model.get("weekly", {}).get("lm_direction", "neutral")))
    tdl_s = _direction(timing_model.get("tdl_s_direction", timing_model.get("weekly", {}).get("s_direction", "neutral")))

    if controller == "L&M":
        return {"direction": tdl_lm, "source": "weekly.lm_direction", "controller": controller}
    elif controller == "S":
        return {"direction": tdl_s, "source": "weekly.s_direction", "controller": controller}
    else:
        return {"direction": "neutral", "source": "timing_neutral_review", "controller": controller}

def _phase_from_tdl(timing_model: dict) -> dict:
    lm = str(timing_model.get("tdl_lm_direction") or "").upper()
    delta = str(timing_model.get("tdl_lm_delta") or "").upper()

    if lm == "BUY" and delta == "BUY": phase = "NDSP_GOLDEN_SIGNAL_BULLISH"
    elif lm == "SELL" and delta == "SELL": phase = "NDSP_GOLDEN_SIGNAL_BEARISH"
    elif lm == "BUY" and delta == "SELL": phase = "BULLISH_PULLBACK"
    elif lm == "SELL" and delta == "BUY": phase = "BEARISH_PULLBACK"
    else: phase = "RANGE"
    return {"phase": phase}

def _run_momentum_dual_safe(symbol: str, market: dict, timing_model: dict) -> dict:
    try:
        result = _safe_dict(run_momentum_dual(symbol=symbol, market=market, timing_model=timing_model))
    except TypeError:
        try: result = _safe_dict(run_momentum_dual(symbol=symbol))
        except Exception: result = {}
    except Exception: result = {}

    signal = str(result.get("signal") or result.get("ndsp_signal") or "NEUTRAL").upper()
    allowed = {"BULLISH_CONFIRMATION", "BEARISH_CONFIRMATION", "BULLISH_WARNING", "BEARISH_WARNING", "NEUTRAL"}
    if signal not in allowed: signal = "NEUTRAL"

    tdl_dir = _tdl_primary_direction(timing_model)
    effect = result.get("confidence_effect", "neutral")

    if effect not in ("increase", "decrease", "neutral"): effect = "neutral"

    if signal == "BULLISH_CONFIRMATION" and tdl_dir == "bullish": effect = "increase"
    elif signal == "BEARISH_CONFIRMATION" and tdl_dir == "bearish": effect = "increase"
    elif signal == "BULLISH_CONFIRMATION" and tdl_dir == "bearish": effect = "decrease"
    elif signal == "BEARISH_CONFIRMATION" and tdl_dir == "bullish": effect = "decrease"
    elif signal in ("BULLISH_WARNING", "BEARISH_WARNING"): effect = "decrease"

    return {"signal": signal, "context": result.get("context", "momentum context evaluated"), "confidence_effect": effect}

def _run_nmp_safe(symbol, market, phase, timing):
    return evaluate_nmp_context(symbol=symbol, market=market, timing_model={}, phase=phase, timing=timing)

def _run_black_layer_safe(symbol: str, market: dict, momentum_dual: dict, phase: dict, timing: dict) -> dict:
    try:
        signal = str(momentum_dual.get("signal") or "NEUTRAL").upper()
        effect = str(momentum_dual.get("confidence_effect") or "neutral").lower()

        strength = 0.5
        if signal in ("BULLISH_CONFIRMATION", "BEARISH_CONFIRMATION"): strength = 0.72
        elif signal in ("BULLISH_WARNING", "BEARISH_WARNING"): strength = 0.28

        if effect == "increase": strength = max(strength, 0.68)
        elif effect == "decrease": strength = min(strength, 0.35)

        liquidity_state, volatility_state, zone_state = "neutral", "normal", "undefined"
        if str(phase.get("phase") or "").endswith("PULLBACK"): zone_state = "support"
        if market.get("price") is None: volatility_state = "high"

        raw = _safe_dict(evaluate_black_layer(
            momentum={"strength": strength, "context": "governed_momentum_context"},
            liquidity={"state": liquidity_state},
            volatility={"state": volatility_state},
            zones={"state": zone_state},
        ))

        state = str(raw.get("state") or "neutral_context")
        score = max(0.0, min(1.0, float(raw.get("score", 0))))

        if state == "supportive_context" and score >= 0.65:
            confidence_effect, risk_effect = "increase", "normal"
        elif state == "protective_block" or score <= 0.25:
            confidence_effect, risk_effect = "decrease", "caution"
        else:
            confidence_effect, risk_effect = "neutral", "normal"

        return {
            "state": state if state in ("supportive_context", "neutral_context", "protective_block") else "neutral_context",
            "score": round(score, 2),
            "confidence_effect": confidence_effect,
            "risk_effect": risk_effect,
            "context": "protective filtering evaluated",
            "public_note": "risk shield refined protective context without defining direction.",
        }
    except Exception:
        return {"state": "neutral_context", "score": 0.0, "confidence_effect": "neutral", "risk_effect": "normal", "context": "protective filtering unavailable; decision continued safely", "public_note": "risk shield unavailable; governed pipeline continued safely."}

def _compute_decision_quality_stack(timing_model: dict, conflict: dict, momentum_dual: dict, black_layer: dict, timing: dict) -> dict:
    """
    NDSP Layer 13: Decision Quality Stack
    [CRITICAL RULE]: الثقة تُحسب هنا فقط بناءً على المؤثرات من الطبقات الداعمة.
    """
    base_confidence = 50
    breakdown = {}

    # 1. Conflict Impact
    conflict_score = float(conflict.get("score", 0)) if isinstance(conflict, dict) else 0
    if conflict_score >= 70:
        base_confidence -= 15
        breakdown['participant_conflict'] = -15
    elif conflict_score >= 40:
        base_confidence -= 7
        breakdown['participant_conflict'] = -7

    # 2. Momentum Impact
    mom_eff = momentum_dual.get("confidence_effect")
    if mom_eff == "increase":
        base_confidence += 5
        breakdown['momentum'] = 5
    elif mom_eff == "decrease":
        base_confidence -= 5
        breakdown['momentum'] = -5

    # 3. risk shield Penalty/Boost
    bl_eff = black_layer.get("confidence_effect")
    if bl_eff == "increase":
        base_confidence += 3
        breakdown['black_layer'] = 3
    elif bl_eff == "decrease":
        base_confidence -= 15 # تغليظ عقوبة الطبقة السوداء حسب V4.1
        breakdown['black_layer'] = -15

    # 4. Golden Alignment (Nawaf Golden Alignment)
    lm_dir = _direction(timing_model.get("tdl_lm_direction", "neutral"))
    s_dir = _direction(timing_model.get("tdl_s_direction", "neutral"))
    if lm_dir == s_dir and lm_dir != "neutral":
        base_confidence += 15
        breakdown['golden_alignment'] = 15

    # 5. Timing/Session Impact
    if timing.get("controller") == "NEUTRAL" or timing.get("day_group") == "SUNDAY_REVIEW":
        base_confidence -= 10
        breakdown['timing_penalty'] = -10

    # Bounds Enforcement
    final_confidence = _normalize_confidence(base_confidence)
    
    # Grading System
    if final_confidence >= 85: grade = "A"
    elif final_confidence >= 70: grade = "B"
    elif final_confidence >= 55: grade = "C"
    elif final_confidence >= 40: grade = "D"
    else: grade = "F"

    label = "Exceptional Institutional Alignment" if grade == "A" else ("Structurally Invalid" if grade == "F" else "Standard Context")

    return {
        "final_confidence": final_confidence,
        "grade": grade,
        "quality_label": label,
        "breakdown": breakdown
    }

def _safe_mode_from_state(confidence: int, conflict: dict, market: dict) -> tuple[str, str]:
    risk_state, system_state = "normal", "live"

    if market.get("price") is None: risk_state, system_state = "paused", "safe_mode"
    if market.get("source") == "mt4_fxcm" and market.get("stale"): risk_state, system_state = "paused", "safe_mode"
    if confidence < 20: risk_state, system_state = "paused", "safe_mode"

    try: conflict_score = float(conflict.get("score", 0))
    except Exception: conflict_score = 0
    if conflict_score >= 85: risk_state, system_state = "paused", "safe_mode"

    return system_state, risk_state

def _run_governed_raw(symbol: str, user: dict | None = None, manual_tdl: dict | None = None) -> dict:
    """
    NDSP Layer 15: Final Decision Aggregator
    """
    generated_at = _now()
    request_id = str(uuid4())

    try: profile = _safe_dict(resolve_market(symbol))
    except Exception: profile = {"asset_class": "unknown"}

    market = _attach_mt4_freshness_to_market(symbol, _get_market(symbol))

    # timing_model Block
    try:
        tdl_data = build_tdl_data(symbol=symbol, market=market, manual=manual_tdl)
        timing_model = _safe_dict(run_tdl(symbol=symbol, data=tdl_data, profile=profile))
    except Exception:
        timing_model = {"tdl_lm_direction": "NEUTRAL", "tdl_lm_delta": "NEUTRAL", "tdl_s_direction": "NEUTRAL", "tdl_s_delta": "NEUTRAL", "dominant_side": "NEUTRAL"}

    phase = _phase_from_tdl(timing_model)
    timing = _get_timing_v4() # V4 Timing
    momentum_dual = _run_momentum_dual_safe(symbol=symbol, market=market, timing_model=timing_model)
    
    intelligence = {"momentum_dual": momentum_dual}

    black_layer = _run_black_layer_safe(symbol=symbol, market=market, momentum_dual=momentum_dual, phase=phase, timing=timing)
    intelligence["black_layer"] = black_layer

    market_alignment = _run_nmp_safe(symbol=symbol, market=market, phase=phase, timing=timing)
    intelligence["nmp_tdl_quality"] = evaluate_nmp_tdl_quality(market_alignment, timing_model, timing=timing)

    try: conflict = _safe_dict(detect_conflict({"timing_model": timing_model, "phase": phase, "intelligence": intelligence}))
    except Exception: conflict = {"score": 0, "conflict_state": "MIXED_PRESSURE"}

    # ---------------------------------------------------------
    # GOVERNANCE V4.1: Strictly Enforcing the Layers
    # ---------------------------------------------------------
    
    # Layer 6: Direction ONLY from Timing + timing_model
    dominant_direction = _resolve_dominant_direction(timing, timing_model)
    direction = dominant_direction["direction"]
    direction_source = dominant_direction["source"]

    # Layer 13: Confidence ONLY from Quality Stack
    quality_stack = _compute_decision_quality_stack(timing_model, conflict, momentum_dual, black_layer, timing)
    confidence = quality_stack["final_confidence"]

    # System State / Risk State
    system_state, risk_state = _safe_mode_from_state(confidence=confidence, conflict=conflict, market=market)
    if black_layer.get("state") == "protective_block" and black_layer.get("risk_effect") == "caution":
        risk_state, system_state = "paused", "safe_mode"

    # Layer 15: The Governed Output Payload
    governed = {
        "version": "1.0.0",
        "governance_version": GOVERNANCE_VERSION,
        "symbol": symbol,

        "decision": {
            "direction": direction,
            "direction_source": direction_source,
            "timing_controller": timing["controller"],
            "confidence": confidence,
            "grade": quality_stack["grade"],
            "quality_label": quality_stack["quality_label"],
            
            # MANDATORY V4.1 RULE: NO DIRECT EXECUTION
            "execution_allowed": False,
            "execution_mode": "decision_support_only"
        },

        "market_alignment": market_alignment,
        "intelligence": intelligence,

        "scenario": {
            "interest": "governed decision context with protective filtering",
            "invalidation": "invalidated if timing_model structure breaks or risk enters safe mode",
            "target": "next governed scenario zone",
        },

        "states": {
            "system_state": system_state,
            "risk_state": risk_state,
            "position_state": "none",
        },

        "execution": {
            "lifecycle": "waiting",
            "trade_id": None,
        },

        "risk": {
            "state": risk_state,
            "reason": "normal" if risk_state == "normal" else "safe mode condition triggered by governed risk/protective context",
        },

        "behavior": {
            "guidance": "Follow governed decision context only. No direct execution command is provided.",
        },

        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
        },

        "explainability": {
            "reason": "Decision derived through governed pipeline V4.1.",
            "context_explanation": "Direction resolved exclusively from Dominant Timed Direction (Timing + timing_model).",
            "confidence_explanation": f"Confidence defined by Decision Quality Stack. Grade: {quality_stack['grade']}.",
            "risk_explanation": "Risk state derived from confidence, market data, conflict state, and protective filtering.",
        },

        "meta": {
            "latency_ms": 0,
            "timestamp": generated_at,
            "symbol_id": symbol,
            "request_id": request_id,
            "pipeline_version": PIPELINE_VERSION,
            "profile": profile,
            "market": {
                "source": market.get("source"),
                "price": market.get("price"),
                "last_candle": market.get("last_candle"),
            },
            "timing_model": timing_model,
            "phase": phase,
            "timing": timing,
            "conflict": conflict,
            "black_layer": black_layer,
            "quality_breakdown": quality_stack["breakdown"]
        },

        "alerts": [],
        "history": [],
    }

    try: governed = enforce(governed)
    except Exception:
        governed["compliance"] = {"passed": False, "sanitized": True, "logic_leak": False}
        governed["states"]["system_state"] = "safe_mode"

    try: governed = explain(governed)
    except Exception: pass

    return apply_governance_runtime(_ndsp_attach_tdl_v2_safe(governed))

# NDSP_FINAL_MARKET_FRESHNESS_ATTACH_START
def _final_attach_market_freshness(payload: dict, symbol: str) -> dict:
    try:
        if not isinstance(payload, dict): return payload
        meta = payload.setdefault("meta", {})
        market = meta.get("market")
        if not isinstance(market, dict): return payload

        market = _attach_mt4_freshness_to_market(symbol, market)
        meta["market"] = market

        source_status = market.get("source_status") if isinstance(market.get("source_status"), dict) else {}
        freshness = source_status.get("freshness") if isinstance(source_status.get("freshness"), dict) else {}

        if str(market.get("source") or "").lower() == "mt4_fxcm" and market.get("stale"):
            payload.setdefault("states", {})["system_state"] = "safe_mode"
            payload.setdefault("states", {})["risk_state"] = "paused"

            risk = payload.setdefault("risk", {})
            risk["state"] = "paused"
            risk["reason"] = "MT4/FXCM market data is stale or missing; governed safe mode is active."
            risk["market_data_freshness"] = {
                "source": "mt4_fxcm", "fresh": False,
                "state": freshness.get("state") or source_status.get("freshness_state"),
                "age_seconds": freshness.get("age_seconds"), "checked_at": freshness.get("checked_at"),
            }

            payload.setdefault("explainability", {})["market_data_explanation"] = (
                "MT4/FXCM data freshness guard marked this market data as stale or missing. "
                "NDSP keeps the output in safe decision-support mode until fresh data is restored."
            )

        return payload
    except Exception as exc:
        try: payload.setdefault("meta", {})["freshness_attach_error"] = str(exc)[:180]
        except Exception: pass
        return payload
# NDSP_FINAL_MARKET_FRESHNESS_ATTACH_END

# NDSP_GOVERNANCE_RUNTIME_WRAPPER_START
def run_governed(symbol):
    raw = _run_governed_raw(symbol)
    governed = apply_governance_runtime(raw, symbol=symbol)
    governed = _final_attach_market_freshness(governed, symbol)
    return governed
# NDSP_GOVERNANCE_RUNTIME_WRAPPER_END
