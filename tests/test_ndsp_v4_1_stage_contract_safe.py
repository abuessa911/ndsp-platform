#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NDSP V4.1 Stage Contract Safe Test

الغرض:
- اختبار منطق مرحلة كاملة بصورة مستقلة وآمنة.
- لا يغير Runtime الأساسي.
- لا يعدل backend/app.
- لا يعيد تشغيل الخدمات.
- لا يسمح بتنفيذ مباشر افتراضيًا.
- يحافظ على قاعدة:
  direction من Timing + simulated TDL فقط.
  confidence من Decision Quality Stack فقط.
  risk من Conflict + Protective Risk Layer فقط.
  execution_mode يبقى decision_support_only.
"""

import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


ALLOWED_DIRECTIONS = {"bullish", "bearish", "neutral"}
ALLOWED_CONTROLLERS = {"L&M", "S"}
ALLOWED_RISK_STATES = {"normal", "caution"}
ALLOWED_GRADES = {"A", "B", "C", "D", "F"}


def clamp_int(value: float, minimum: int = 0, maximum: int = 100) -> int:
    return int(max(minimum, min(maximum, value)))


def normalize_direction(value: str) -> str:
    value = str(value or "").strip().lower()
    if value not in ALLOWED_DIRECTIONS:
        return "neutral"
    return value


def evaluate_black_layer(
    momentum: Dict[str, Any],
    liquidity: Dict[str, Any],
    volatility: Dict[str, Any],
    zones: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Layer 12: Protective Risk Layer
    Allowed Effects:
    - risk penalty
    - caution / protective context
    Forbidden Effects:
    - لا يغير direction
    - لا يقرر execution المباشر
    """

    risk = 0.0
    reasons: List[str] = []

    if volatility.get("state") == "high":
        risk += 0.3
        reasons.append("unstable_volatility")

    if liquidity.get("state") in ["sweep_up", "sweep_down", "low"]:
        risk += 0.2
        reasons.append("liquidity_event_detected")

    if zones.get("state") in ["resistance", "support"]:
        risk += 0.2
        reasons.append("zone_pressure")

    raw_score = max(0.0, min(risk, 1.0))
    penalty = clamp_int(raw_score * 100)
    state = "protective_block" if penalty >= 25 else "neutral_context"

    return {
        "layer_metadata": {
            "layer_name": "Layer 12: Protective Risk Layer",
            "version": "4.1-safe-test",
            "authority": "Risk Escalation Authority",
        },
        "black_layer_state": state,
        "black_layer_penalty": penalty,
        "reason": reasons,
    }


def evaluate_conflict(lm_direction: str, s_direction: str) -> Dict[str, Any]:
    """
    Layer 5.6: Participant Conflict
    Allowed Effects:
    - conflict penalty
    - quality context
    Forbidden Effects:
    - لا يغير direction
    """

    lm_direction = normalize_direction(lm_direction)
    s_direction = normalize_direction(s_direction)

    conflict = (
        lm_direction != "neutral"
        and s_direction != "neutral"
        and lm_direction != s_direction
    )

    penalty = 12 if conflict else 0

    return {
        "layer_metadata": {
            "layer_name": "Layer 5.6: Participant Conflict",
            "version": "4.1-safe-test",
            "authority": "Quality Context Authority",
        },
        "participant_conflict": conflict,
        "conflict_penalty": penalty,
        "summary": (
            f"Conflict Detected: L&M ({lm_direction}) vs S ({s_direction})"
            if conflict
            else "Aligned"
        ),
    }


def compute_decision_quality(
    base_confidence: int,
    conflict_penalty: int,
    black_layer_penalty: int,
) -> Dict[str, Any]:
    """
    Layer 13: Decision Quality Stack
    المصدر الوحيد للثقة النهائية داخل هذا الاختبار.
    """

    base_confidence = clamp_int(base_confidence)
    conflict_penalty = clamp_int(conflict_penalty)
    black_layer_penalty = clamp_int(black_layer_penalty)

    final_confidence = clamp_int(
        base_confidence - conflict_penalty - black_layer_penalty
    )

    if final_confidence >= 85:
        grade = "A"
    elif final_confidence >= 70:
        grade = "B"
    elif final_confidence >= 55:
        grade = "C"
    elif final_confidence >= 40:
        grade = "D"
    else:
        grade = "F"

    return {
        "layer_metadata": {
            "layer_name": "Layer 13: Decision Quality Stack",
            "version": "4.1-safe-test",
            "authority": "Confidence / Quality Authority",
        },
        "base_confidence": base_confidence,
        "final_confidence": final_confidence,
        "grade": grade,
        "quality_label": "Safe Stage Test",
        "confidence_breakdown": {
            "base_confidence": base_confidence,
            "conflict_penalty": conflict_penalty,
            "protective_risk_penalty": black_layer_penalty,
        },
    }


def resolve_timing_controller(now_utc: Optional[datetime] = None) -> str:
    """
    Layer 3: Timing Authority
    Monday/Friday = L&M
    Tue/Wed/Thu/Sat/Sun = S
    """

    now_utc = now_utc or datetime.now(timezone.utc)
    day_of_week = now_utc.weekday()
    return "L&M" if day_of_week in [0, 4] else "S"


def run_ndsp_v4_pipeline(
    symbol: str,
    mock_market_conditions: Dict[str, Any],
    now_utc: Optional[datetime] = None,
    base_confidence: int = 50,
    lm_direction: str = "bullish",
    s_direction: str = "bearish",
) -> Dict[str, Any]:
    """
    Master Orchestrator - Safe Test Version

    لا يقرأ مصادر حية.
    لا يكتب في Runtime.
    ينتج عقد اختبار فقط.
    """

    if not symbol or not str(symbol).strip():
        raise ValueError("symbol is required")

    now_utc = now_utc or datetime.now(timezone.utc)
    controller = resolve_timing_controller(now_utc)

    lm_dir = normalize_direction(lm_direction)
    s_dir = normalize_direction(s_direction)

    initial_direction = lm_dir if controller == "L&M" else s_dir

    conflict_res = evaluate_conflict(lm_dir, s_dir)

    black_layer_res = evaluate_black_layer(
        momentum={"state": "weak"},
        liquidity={
            "state": "low"
            if mock_market_conditions.get("low_liquidity")
            else "normal"
        },
        volatility={
            "state": "high"
            if mock_market_conditions.get("volatility_spike")
            else "normal"
        },
        zones={"state": "resistance"},
    )

    quality = compute_decision_quality(
        base_confidence=base_confidence,
        conflict_penalty=conflict_res["conflict_penalty"],
        black_layer_penalty=black_layer_res["black_layer_penalty"],
    )

    total_penalty = (
        conflict_res["conflict_penalty"]
        + black_layer_res["black_layer_penalty"]
    )

    risk_state = "caution" if total_penalty > 0 else "normal"

    # NDSP Governance: No direct execution in this test.
    execution_allowed = False
    execution_mode = "decision_support_only"

    final_direction = (
        initial_direction
        if quality["final_confidence"] > 30
        else "neutral"
    )

    contract = {
        "contract_id": f"NDSP-V4.1-SAFE-{uuid.uuid4().hex[:8].upper()}",
        "timestamp_utc": int(time.time() * 1000),
        "timestamp_iso": now_utc.isoformat(),
        "symbol": str(symbol).upper().strip(),
        "source_mode": "safe_structural_test",
        "runtime_mutation": False,
        "service_restart_required": False,
        "layers": {
            "timing": {
                "controller": controller,
                "authority": "Timing Authority",
            },
            "tdl_simulated": {
                "lm_direction": lm_dir,
                "s_direction": s_dir,
                "selected_direction": initial_direction,
                "note": "Simulated inputs for stage closure test only.",
            },
            "conflict": conflict_res,
            "protective_risk": black_layer_res,
            "quality": quality,
        },
        "decision": {
            "direction": final_direction,
            "timing_controller": controller,
            "confidence": quality["final_confidence"],
            "grade": quality["grade"],
            "risk_state": risk_state,
            "decision_state": f"ACTIVE_{risk_state.upper()}",
            "execution_allowed": execution_allowed,
            "execution_mode": execution_mode,
        },
        "governance_assertions": {
            "no_direct_execution": execution_allowed is False,
            "decision_support_only": execution_mode == "decision_support_only",
            "confidence_from_quality_stack": True,
            "risk_from_penalties": True,
            "runtime_mutation": False,
        },
    }

    validate_contract(contract)
    return contract


def validate_contract(contract: Dict[str, Any]) -> None:
    decision = contract.get("decision", {})
    layers = contract.get("layers", {})

    direction = decision.get("direction")
    controller = decision.get("timing_controller")
    confidence = decision.get("confidence")
    grade = decision.get("grade")
    risk_state = decision.get("risk_state")

    if direction not in ALLOWED_DIRECTIONS:
        raise AssertionError(f"invalid decision.direction: {direction}")

    if controller not in ALLOWED_CONTROLLERS:
        raise AssertionError(f"invalid timing_controller: {controller}")

    if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
        raise AssertionError(f"invalid confidence range: {confidence}")

    if grade not in ALLOWED_GRADES:
        raise AssertionError(f"invalid grade: {grade}")

    if risk_state not in ALLOWED_RISK_STATES:
        raise AssertionError(f"invalid risk_state: {risk_state}")

    if decision.get("execution_allowed") is not False:
        raise AssertionError("execution_allowed must be False")

    if decision.get("execution_mode") != "decision_support_only":
        raise AssertionError("execution_mode must be decision_support_only")

    if contract.get("runtime_mutation") is not False:
        raise AssertionError("runtime_mutation must be False")

    quality_conf = layers.get("quality", {}).get("final_confidence")
    if confidence != quality_conf:
        raise AssertionError("decision.confidence must equal quality.final_confidence")

    total_penalty = (
        layers.get("conflict", {}).get("conflict_penalty", 0)
        + layers.get("protective_risk", {}).get("black_layer_penalty", 0)
    )
    expected_risk = "caution" if total_penalty > 0 else "normal"
    if risk_state != expected_risk:
        raise AssertionError(
            f"risk_state mismatch: expected={expected_risk}, actual={risk_state}"
        )


def publish_decision_contract(
    contract_data: Dict[str, Any],
    stream_name: str = "ndsp.decision.stream",
    host: str = "127.0.0.1",
    port: int = 6379,
    db: int = 0,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """
    Redis publisher.
    الافتراضي dry_run=True حتى لا نضخ أحداث اختبار داخل Stream الإنتاج.
    """

    event_payload = json.dumps(contract_data, ensure_ascii=False, sort_keys=True)

    if dry_run:
        return {
            "redis_publish_attempted": False,
            "redis_publish_mode": "dry_run",
            "stream": stream_name,
            "payload_bytes": len(event_payload.encode("utf-8")),
        }

    try:
        import redis
    except ImportError:
        return {
            "redis_publish_attempted": True,
            "redis_publish_ok": False,
            "error": "redis package not installed",
        }

    try:
        r = redis.Redis(host=host, port=int(port), db=int(db))
        event_id = r.xadd(stream_name, {"payload": event_payload})
        return {
            "redis_publish_attempted": True,
            "redis_publish_ok": True,
            "stream": stream_name,
            "event_id": (
                event_id.decode("utf-8")
                if isinstance(event_id, bytes)
                else str(event_id)
            ),
        }
    except Exception as exc:
        return {
            "redis_publish_attempted": True,
            "redis_publish_ok": False,
            "stream": stream_name,
            "error": str(exc),
        }


def run_all_stage_tests() -> Dict[str, Any]:
    """
    يشغل سيناريوهات متعددة لإغلاق المرحلة:
    - يوم L&M
    - يوم S
    - سوق خطر
    - سوق طبيعي
    - انهيار ثقة يؤدي إلى neutral
    """

    scenarios = [
        {
            "name": "lm_controller_caution",
            "symbol": "XAUUSD",
            "now": datetime(2026, 5, 15, 12, 0, 0, tzinfo=timezone.utc),
            "conditions": {"volatility_spike": True, "low_liquidity": True},
            "base_confidence": 90,
            "lm_direction": "bullish",
            "s_direction": "bearish",
            "expected_controller": "L&M",
            "expected_risk": "caution",
        },
        {
            "name": "s_controller_caution",
            "symbol": "EURUSD",
            "now": datetime(2026, 5, 13, 12, 0, 0, tzinfo=timezone.utc),
            "conditions": {"volatility_spike": True, "low_liquidity": True},
            "base_confidence": 50,
            "lm_direction": "bullish",
            "s_direction": "bearish",
            "expected_controller": "S",
            "expected_risk": "caution",
        },
        {
            "name": "normal_aligned",
            "symbol": "BTCUSDT",
            "now": datetime(2026, 5, 16, 12, 0, 0, tzinfo=timezone.utc),
            "conditions": {"volatility_spike": False, "low_liquidity": False},
            "base_confidence": 80,
            "lm_direction": "bearish",
            "s_direction": "bearish",
            "expected_controller": "S",
            "expected_risk": "caution",
        },
        {
            "name": "low_confidence_neutralized",
            "symbol": "USOIL",
            "now": datetime(2026, 5, 14, 12, 0, 0, tzinfo=timezone.utc),
            "conditions": {"volatility_spike": True, "low_liquidity": True},
            "base_confidence": 50,
            "lm_direction": "bullish",
            "s_direction": "bearish",
            "expected_controller": "S",
            "expected_risk": "caution",
            "expected_direction": "neutral",
        },
    ]

    results: List[Dict[str, Any]] = []
    failed: List[str] = []

    for scenario in scenarios:
        try:
            contract = run_ndsp_v4_pipeline(
                symbol=scenario["symbol"],
                mock_market_conditions=scenario["conditions"],
                now_utc=scenario["now"],
                base_confidence=scenario["base_confidence"],
                lm_direction=scenario["lm_direction"],
                s_direction=scenario["s_direction"],
            )

            if contract["decision"]["timing_controller"] != scenario["expected_controller"]:
                raise AssertionError(
                    f"controller mismatch: expected={scenario['expected_controller']} "
                    f"actual={contract['decision']['timing_controller']}"
                )

            if contract["decision"]["risk_state"] != scenario["expected_risk"]:
                raise AssertionError(
                    f"risk mismatch: expected={scenario['expected_risk']} "
                    f"actual={contract['decision']['risk_state']}"
                )

            if "expected_direction" in scenario:
                if contract["decision"]["direction"] != scenario["expected_direction"]:
                    raise AssertionError(
                        f"direction mismatch: expected={scenario['expected_direction']} "
                        f"actual={contract['decision']['direction']}"
                    )

            results.append(
                {
                    "name": scenario["name"],
                    "ok": True,
                    "contract_id": contract["contract_id"],
                    "symbol": contract["symbol"],
                    "controller": contract["decision"]["timing_controller"],
                    "direction": contract["decision"]["direction"],
                    "confidence": contract["decision"]["confidence"],
                    "grade": contract["decision"]["grade"],
                    "risk_state": contract["decision"]["risk_state"],
                    "execution_allowed": contract["decision"]["execution_allowed"],
                    "execution_mode": contract["decision"]["execution_mode"],
                }
            )

        except Exception as exc:
            failed.append(scenario["name"])
            results.append(
                {
                    "name": scenario["name"],
                    "ok": False,
                    "error": str(exc),
                }
            )

    return {
        "ok": len(failed) == 0,
        "scenario_count": len(scenarios),
        "failed": failed,
        "results": results,
    }


if __name__ == "__main__":
    output = run_all_stage_tests()
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    if not output["ok"]:
        raise SystemExit(1)
