#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Mapping

from backend.layers.canonical_v1.runtime_bridge import apply_canonical_golden
from backend.layers.canonical_v1.direction.investment_policy import evaluate_investment_policy
from backend.layers.canonical_v1.quality.golden_signals import evaluate_golden_signals

CONTRACT_VERSION = "NDSP_COMMERCIAL_LAUNCH_V203"
GOVERNING_INPUTS_VERSION = "NDSP_GOVERNING_INPUTS_V201"
COMMERCIAL_SCORE_VERSION = "NDSP_COMMERCIAL_SCORE_V202"
RAW_COT_URL = "http://127.0.0.1:9076/api/admin/raw-cot/status"
USER_AGENT = "NDSP-Commercial-Launch-V203/1.0"
DEFAULT_MAX_COT_AGE_DAYS = 10


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(str(value).replace(",", "").replace("٬", "").strip())
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _normalize_direction(value: Any) -> str | None:
    raw = str(value or "").strip().lower()
    aliases = {
        "bullish": "bullish", "bull": "bullish", "up": "bullish",
        "positive": "bullish", "صاعد": "bullish",
        "bearish": "bearish", "bear": "bearish", "down": "bearish",
        "negative": "bearish", "هابط": "bearish",
        "neutral": "neutral", "flat": "neutral", "محايد": "neutral",
    }
    return aliases.get(raw)


def _direction_sign(direction: Any) -> float:
    normalized = _normalize_direction(direction)
    if normalized == "bullish":
        return 1.0
    if normalized == "bearish":
        return -1.0
    return 0.0


def _analysis_mode(value: Any, timeframe: Any) -> str:
    raw = str(value or "").lower()
    if any(token in raw for token in ("investment", "invest", "استثمار")):
        return "investment"
    if any(token in raw for token in ("speculative", "trade", "مضارب")):
        return "speculative"
    tf = str(timeframe or "").lower()
    return "investment" if tf in {"1w", "weekly", "1m", "monthly"} else "speculative"


def _http_json(url: str, timeout: int = 10) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = int(getattr(response, "status", 200))
        if status < 200 or status >= 300:
            raise RuntimeError(f"HTTP_{status}")
        return json.loads(response.read().decode("utf-8", "replace"))


def _fetch_raw_cot(symbol: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"asset": str(symbol or "").upper().strip()})
    try:
        payload = _http_json(f"{RAW_COT_URL}?{query}", timeout=10)
    except Exception as exc:
        return {
            "ok": False,
            "raw_cot_connected": False,
            "raw_cot_governing_inputs_complete": False,
            "error": f"RAW_COT_FETCH_FAILED:{type(exc).__name__}",
        }
    return payload if isinstance(payload, dict) else {
        "ok": False,
        "raw_cot_connected": False,
        "raw_cot_governing_inputs_complete": False,
        "error": "RAW_COT_INVALID_PAYLOAD",
    }


def _layer(data: dict[str, Any], layer_id: str) -> dict[str, Any] | None:
    layers = data.get("decision_layers")
    if not isinstance(layers, list):
        return None
    for item in layers:
        if isinstance(item, dict) and str(item.get("id") or "") == layer_id:
            return item
    return None


def _update_public_layers(data: dict[str, Any], mode: str, directions: Mapping[str, Any]) -> None:
    overall = directions.get("asset_managers_overall")
    am_weekly = directions.get("asset_managers_weekly")
    lf_weekly = directions.get("leveraged_funds_weekly")

    investment = evaluate_investment_policy(
        asset_managers_overall=overall,
        asset_managers_weekly=am_weekly,
        leveraged_funds_weekly=lf_weekly,
    )
    golden = evaluate_golden_signals(
        asset_managers_overall=overall,
        asset_managers_weekly=am_weekly,
        leveraged_funds_weekly=lf_weekly,
    )

    l01 = _layer(data, "NDSP-CORE-L01")
    if l01 is not None:
        l01.update({
            "state": "ACTIVE" if _normalize_direction(overall) in {"bullish", "bearish"} else "UNDER_REVIEW",
            "state_ar": "نشطة" if _normalize_direction(overall) in {"bullish", "bearish"} else "قيد المراجعة",
            "score": 90 if investment["readiness_allowed"] else 65,
            "blocking": not investment["readiness_allowed"],
            "evidence": (
                f"governing={overall}; asset_managers_weekly={am_weekly}; "
                f"leveraged_funds_weekly={lf_weekly}; correction={investment['correction_state']}"
            ),
            "public_summary": (
                "اكتملت بيانات الاتجاه المؤسسي الحاكمة؛ "
                + ("انتهى التصحيح الأسبوعي." if investment["readiness_allowed"] else "التصحيح الأسبوعي ما زال قائمًا.")
            ),
        })

    if mode == "investment":
        l04 = _layer(data, "NDSP-CORE-L04")
        if l04 is not None:
            allowed = bool(investment["asset_managers_weekly_alignment"])
            l04.update({
                "state": "ALLOWED" if allowed else "MONITORING_ONLY",
                "state_ar": "مسموحة" if allowed else "للمتابعة فقط",
                "score": 88 if allowed else 55,
                "blocking": not allowed,
                "evidence": "investment weekly correction gate derived from current and weekly Asset Manager directions",
                "public_summary": "انتهى التصحيح الأسبوعي." if allowed else "التصحيح الأسبوعي لم ينتهِ بعد.",
            })

    l13 = _layer(data, "NDSP-CORE-L13")
    if l13 is not None:
        active = bool(golden["golden_active"])
        l13.update({
            "state": "ACTIVE" if active else "INACTIVE",
            "state_ar": "نشطة" if active else "غير نشطة",
            "score": 95 if active else 0,
            "blocking": False,
            "evidence": "AM_WEEKLY_EQUALS_LF_WEEKLY evaluated from current CFTC TFF inputs",
            "public_summary": "تم تقييم الإشارة من المدخلات الحاكمة الفعلية.",
        })

    l14 = _layer(data, "NDSP-CORE-L14")
    if l14 is not None:
        active = bool(golden["enhanced_active"])
        l14.update({
            "state": "ACTIVE" if active else "INACTIVE",
            "state_ar": "نشطة" if active else "غير نشطة",
            "score": 98 if active else 0,
            "blocking": False,
            "evidence": "AM_OVERALL_EQUALS_AM_WEEKLY_EQUALS_LF_WEEKLY evaluated from current CFTC TFF inputs",
            "public_summary": "تم تقييم الإشارة المعززة من المدخلات الحاكمة الفعلية.",
        })


def _refresh_public_golden(data: dict[str, Any]) -> None:
    golden = data.get("golden_alignment")
    if not isinstance(golden, dict):
        return

    status = str(golden.get("golden_status") or "inactive")
    direction = str(golden.get("direction") or "unknown")
    evaluated = not bool(golden.get("missing_inputs")) and golden.get("reason_code") in (None, "")
    active = bool(golden.get("golden_signal"))
    enhanced = bool(golden.get("enhanced_golden_signal"))

    if not evaluated:
        return

    if enhanced:
        label = "نشطة — محاذاة ذهبية معززة"
        summary = "اكتملت المحاذاة الكلية والأسبوعية بين الفئات المؤسسية الحاكمة."
    elif active:
        label = "نشطة — محاذاة ذهبية"
        summary = "تحققت المحاذاة الأسبوعية بين مدراء الأصول وصناديق الرافعة."
    else:
        label = "مقيّمة — غير نشطة"
        summary = "اكتملت المدخلات الحاكمة، لكن شروط المحاذاة الذهبية غير متحققة حاليًا."

    evidence = [
        {"label": "حالة التقييم", "value": "تم التقييم من بيانات CFTC TFF الفعلية"},
        {"label": "الاتجاه", "value": direction},
    ]

    data["golden_status"] = status
    data["golden_reason_public"] = summary
    data["golden_evidence_public"] = evidence

    spotlight = data.get("golden_spotlight")
    if not isinstance(spotlight, dict):
        spotlight = {}
        data["golden_spotlight"] = spotlight
    spotlight.update({
        "title": "إشارة نواف الذهبية",
        "status": status,
        "label": label,
        "summary": summary,
        "quality_effect": "تدخل الإشارة في جودة القراءة فقط، ولا تمنح أمر شراء أو بيع.",
        "evidence": evidence,
    })

    explainability = data.get("explainability")
    if not isinstance(explainability, dict):
        explainability = {}
        data["explainability"] = explainability
    explainability.update({
        "golden_signal_exposed": True,
        "golden_signal": active,
        "golden_status": status,
        "golden_reason_public": summary,
        "not_recommendation": True,
    })

    public = data.get("public_explainability")
    if not isinstance(public, dict):
        public = {}
        data["public_explainability"] = public
    pg = public.get("golden_alignment")
    if not isinstance(pg, dict):
        pg = {}
        public["golden_alignment"] = pg
    pg.update({
        "title": "إشارة نواف الذهبية",
        "status": status,
        "label": label,
        "reason": summary,
        "evidence": evidence,
        "notice": "هذه قراءة تفسيرية محكومة وليست توصية مالية.",
    })


def attach_v201_governing_inputs(
    payload: Any,
    *,
    symbol: Any = None,
    timeframe: Any = None,
    analysis_mode: Any = None,
    max_cot_age_days: int = DEFAULT_MAX_COT_AGE_DAYS,
    raw_cot_override: Mapping[str, Any] | None = None,
) -> Any:
    if not isinstance(payload, dict):
        return payload

    data = deepcopy(payload)
    instrument = data.get("instrument") if isinstance(data.get("instrument"), Mapping) else {}
    normalized_symbol = str(symbol or instrument.get("symbol") or data.get("symbol") or "").upper().strip()
    normalized_tf = str(timeframe or instrument.get("timeframe") or "weekly").strip()
    mode = _analysis_mode(analysis_mode, normalized_tf)
    raw = dict(raw_cot_override) if isinstance(raw_cot_override, Mapping) else _fetch_raw_cot(normalized_symbol)

    directions = {
        "asset_managers_overall": _normalize_direction(
            raw.get("asset_managers_overall_direction") or raw.get("asset_managers_bias")
        ),
        "asset_managers_weekly": _normalize_direction(raw.get("asset_managers_weekly_direction")),
        "leveraged_funds_overall": _normalize_direction(
            raw.get("leveraged_funds_overall_direction")
            or raw.get("leveraged_funds_bias")
        ),
        "leveraged_funds_weekly": _normalize_direction(raw.get("leveraged_funds_weekly_direction")),
    }
    missing = [name for name, value in directions.items() if value not in {"bullish", "bearish", "neutral"}]
    age = _safe_float(raw.get("report_age_days"))

    # Canonical freshness fallback:
    # report_age_days may be derived only from a real report_date.
    # Missing report_date remains missing; no synthetic freshness.
    if age is None:
        report_date_value = raw.get("report_date")
        if report_date_value:
            try:
                from datetime import date, datetime, timezone

                text = str(report_date_value).strip()
                parsed = datetime.fromisoformat(
                    text.replace("Z", "+00:00")
                )

                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)

                age = float(
                    (datetime.now(timezone.utc).date() - parsed.date()).days
                )
            except Exception:
                try:
                    parsed_date = date.fromisoformat(
                        str(report_date_value).strip()[:10]
                    )
                    age = float(
                        (datetime.now(timezone.utc).date() - parsed_date).days
                    )
                except Exception:
                    age = None

    fresh = age is not None and age <= float(max_cot_age_days)
    complete = (
        raw.get("raw_cot_connected") is True
        and raw.get("raw_cot_governing_inputs_complete") is True
        and not missing
        and fresh
    )

    data["governing_inputs"] = {
        "contract_version": GOVERNING_INPUTS_VERSION,
        "status": "COMPLETE" if complete else "INCOMPLETE",
        "source": "CFTC_TFF_FUTURES_ONLY",
        "source_family": raw.get("source_family"),
        "source_market": raw.get("market_name"),
        "report_date": raw.get("report_date"),
        "report_age_days": age,
        "max_age_days": int(max_cot_age_days),
        "fresh": fresh,
        "symbol": normalized_symbol,
        "source_timeframe": "weekly",
        "analysis_timeframe": normalized_tf,
        "analysis_mode": mode,
        "directions": directions,
        "missing_inputs": missing,
        "raw_cot_connected": raw.get("raw_cot_connected") is True,
        "raw_cot_status": raw.get("raw_cot_status"),
        "not_recommendation": True,
    }

    if not complete:
        data["governing_inputs_reason_code"] = (
            "COT_STALE" if age is not None and not fresh
            else "COT_GOVERNING_INPUTS_INCOMPLETE"
        )
        return data

    data.update(directions)
    data["asset_managers_overall_direction"] = directions["asset_managers_overall"]
    data["asset_managers_weekly_direction"] = directions["asset_managers_weekly"]
    data["leveraged_funds_overall_direction"] = directions["leveraged_funds_overall"]
    data["leveraged_funds_weekly_direction"] = directions["leveraged_funds_weekly"]
    data["canonical_cot_directions"] = dict(directions)

    data = apply_canonical_golden(data)
    golden = data.get("golden_alignment")
    if isinstance(golden, dict):
        golden.update({
            "governing_inputs_complete": True,
            "governing_inputs_contract_version": GOVERNING_INPUTS_VERSION,
            "source_report_date": raw.get("report_date"),
            "source_report_age_days": age,
            "source_fresh": fresh,
            "source_family": raw.get("source_family"),
            "decision_authority": False,
            "not_recommendation": True,
            "no_buy_sell": True,
        })

    _update_public_layers(data, mode, directions)
    _refresh_public_golden(data)
    data["governing_inputs_reason_code"] = None
    data["governing_inputs_contract_version"] = GOVERNING_INPUTS_VERSION
    return data


def _scenario_levels_complete(data: Mapping[str, Any]) -> bool:
    levels = data.get("scenario_levels")
    if not isinstance(levels, Mapping):
        scenario = data.get("scenario")
        levels = scenario.get("scenario_levels") if isinstance(scenario, Mapping) else None
    if not isinstance(levels, Mapping):
        return False
    for key in ("activation", "arrival", "review", "invalidation"):
        item = levels.get(key)
        if not isinstance(item, Mapping) or _safe_float(item.get("price")) is None:
            return False
    return True


def _score_band(score: float) -> str:
    if score >= 90:
        return "EXCEPTIONAL"
    if score >= 80:
        return "STRONG"
    if score >= 70:
        return "QUALIFIED"
    if score >= 60:
        return "CAUTIOUS"
    return "WEAK"


def _momentum_score(data: Mapping[str, Any], score_inputs: Mapping[str, Any], direction: str) -> float | None:
    momentum = score_inputs.get("momentum")
    if not isinstance(momentum, Mapping):
        return None
    sign = _direction_sign(direction)
    if sign == 0:
        return 50.0

    live = data.get("live_market_analysis") if isinstance(data.get("live_market_analysis"), Mapping) else {}
    instrument = data.get("instrument") if isinstance(data.get("instrument"), Mapping) else {}
    rsi = _safe_float(live.get("selected_timeframe_rsi") or live.get("rsi_4h"))
    price = _safe_float(instrument.get("live_price") or live.get("price"))
    macd = _safe_float(momentum.get("macd_histogram"))
    obv = _safe_float(momentum.get("obv_slope"))
    cci = _safe_float(momentum.get("cci_value"))
    if None in (rsi, price, macd, obv, cci) or price is None or price <= 0:
        return None

    rsi_score = _clamp(50.0 + sign * (rsi - 50.0) * 2.0)
    macd_scale = max(price * 0.001, 1e-9)
    macd_score = _clamp(50.0 + 50.0 * math.tanh(sign * macd / macd_scale))
    obv_score = _clamp(50.0 + sign * obv / 2.0)
    cci_score = _clamp(50.0 + sign * cci / 4.0)
    return round((rsi_score + macd_score + obv_score + cci_score) / 4.0, 6)


def attach_v202_commercial_score(
    payload: Any,
    *,
    symbol: Any = None,
    timeframe: Any = None,
    analysis_mode: Any = None,
) -> Any:
    if not isinstance(payload, dict):
        return payload

    data = payload
    score_inputs = data.get("score_inputs")
    if not isinstance(score_inputs, dict):
        data["commercial_score"] = {
            "contract_version": COMMERCIAL_SCORE_VERSION,
            "status": "WITHHELD_INPUT_CONTRACT_MISSING",
            "score": None,
            "public_allowed": False,
            "not_recommendation": True,
        }
        return data

    instrument = data.get("instrument") if isinstance(data.get("instrument"), Mapping) else {}
    normalized_tf = str(timeframe or instrument.get("timeframe") or score_inputs.get("timeframe") or "weekly")
    mode = _analysis_mode(analysis_mode or score_inputs.get("analysis_mode"), normalized_tf)
    governing = data.get("governing_inputs") if isinstance(data.get("governing_inputs"), Mapping) else {}
    directions = governing.get("directions") if isinstance(governing.get("directions"), Mapping) else {}
    direction = (
        directions.get("asset_managers_overall")
        if mode == "investment"
        else directions.get("leveraged_funds_weekly")
    )
    direction = _normalize_direction(direction) or "neutral"
    sign = _direction_sign(direction)

    tdl_block = score_inputs.get("tdl") if isinstance(score_inputs.get("tdl"), Mapping) else {}
    correction_block = score_inputs.get("correction") if isinstance(score_inputs.get("correction"), Mapping) else {}
    macro_block = score_inputs.get("macro") if isinstance(score_inputs.get("macro"), Mapping) else {}
    blocker_block = score_inputs.get("blockers") if isinstance(score_inputs.get("blockers"), dict) else {}

    golden = data.get("golden_alignment") if isinstance(data.get("golden_alignment"), Mapping) else {}
    golden_complete = not bool(golden.get("missing_inputs")) and golden.get("reason_code") in (None, "")
    if golden_complete:
        codes = [
            str(code) for code in (blocker_block.get("codes") or [])
            if str(code) != "GOLDEN_GOVERNING_INPUTS_INCOMPLETE"
        ]
        blocker_block["codes"] = list(dict.fromkeys(codes))
        blocker_block["count"] = len(blocker_block["codes"])

    tdl = _safe_float(tdl_block.get("alignment_score"))
    correction = _safe_float(correction_block.get("confirmation_score"))
    momentum = _momentum_score(data, score_inputs, direction)
    usd_pressure = _safe_float(macro_block.get("usd_pressure_score"))
    macro = _clamp(50.0 + sign * usd_pressure / 2.0) if usd_pressure is not None else None
    scenario = 100.0 if _scenario_levels_complete(data) else 0.0
    nmp_obj = data.get("nmp") if isinstance(data.get("nmp"), Mapping) else {}
    nmp = 100.0 if nmp_obj.get("status") == "AVAILABLE" and _safe_float(nmp_obj.get("value")) is not None else 0.0
    golden_component = (
        100.0 if golden.get("enhanced_golden_signal") is True
        else 85.0 if golden.get("golden_signal") is True
        else 50.0 if golden_complete
        else 0.0
    )

    components = {
        "tdl": tdl,
        "correction": correction,
        "momentum": momentum,
        "macro_usd": macro,
        "scenario_structure": scenario,
        "nmp": nmp,
        "golden_evaluation": golden_component,
    }
    missing = [key for key, value in components.items() if _safe_float(value) is None]
    weights = {
        "tdl": 0.25,
        "correction": 0.15,
        "momentum": 0.20,
        "macro_usd": 0.10,
        "scenario_structure": 0.10,
        "nmp": 0.10,
        "golden_evaluation": 0.10,
    }

    raw_score = None
    if not missing:
        raw_score = round(sum(float(components[key]) * weights[key] for key in weights), 2)

    governance_summary = data.get("governance_summary") if isinstance(data.get("governance_summary"), Mapping) else {}
    capabilities = data.get("platform_capabilities")
    capability_count = len(capabilities) if isinstance(capabilities, list) else int(governance_summary.get("capability_total") or 0)
    layer_count = len(data.get("decision_layers")) if isinstance(data.get("decision_layers"), list) else 0
    blockers_count = int(_safe_float(blocker_block.get("count")) or 0)

    gates = {
        "score_input_contract_complete": score_inputs.get("contract_complete") is True,
        "score_input_missing_components_empty": not bool(score_inputs.get("missing_components")),
        "same_timeframe_enforced": score_inputs.get("same_timeframe_enforced") is True,
        "static_fallback_unused": score_inputs.get("static_fallback_used") is False,
        "cross_timeframe_fallback_unused": score_inputs.get("cross_timeframe_fallback_used") is False,
        "governing_inputs_complete": governing.get("status") == "COMPLETE",
        "governing_inputs_fresh": governing.get("fresh") is True,
        "golden_evaluated": golden_complete,
        "runtime_blockers_clear": blockers_count == 0,
        "scenario_levels_complete": scenario == 100.0,
        "nmp_available": nmp == 100.0,
        "governance_evidence_fresh": governance_summary.get("evidence_fresh") is True,
        "sixteen_layers_exposed": layer_count == 16,
        "twenty_eight_capabilities_exposed": capability_count == 28,
        "commercial_components_complete": not missing,
        "score_finite": raw_score is not None and math.isfinite(raw_score),
    }
    public_allowed = all(gates.values())
    status = "CALCULATED_GOVERNED" if public_allowed else "WITHHELD_GOVERNANCE_GATE"

    score_inputs["commercial_score_calculated"] = raw_score is not None
    score_inputs["commercial_score_status"] = status
    score_inputs["commercial_score_contract_version"] = COMMERCIAL_SCORE_VERSION
    score_inputs["blockers"] = blocker_block

    score_payload = {
        "contract_version": COMMERCIAL_SCORE_VERSION,
        "status": status,
        "score": raw_score if public_allowed else None,
        "raw_score_internal_available": raw_score is not None,
        "band": _score_band(raw_score) if public_allowed and raw_score is not None else None,
        "public_allowed": public_allowed,
        "governing_direction": direction,
        "analysis_mode": mode,
        "timeframe": normalized_tf,
        "blockers_count": blockers_count,
        "missing_components": missing,
        "gates": gates,
        "calculated_at": _now_iso(),
        "decision_authority": False,
        "not_recommendation": True,
        "no_buy_sell": True,
    }
    data["commercial_score"] = score_payload
    data["commercial_score_contract_version"] = COMMERCIAL_SCORE_VERSION

    allowed = data.get("allowed_public_outputs")
    if not isinstance(allowed, dict):
        allowed = {}
        data["allowed_public_outputs"] = allowed
    allowed["commercial_score_status"] = status
    allowed["commercial_score"] = score_payload["score"]
    allowed["commercial_score_band"] = score_payload["band"]
    allowed["commercial_score_notice"] = "مؤشر جودة تفسيري محكوم، وليس أمر شراء أو بيع."

    data["launch_readiness"] = {
        "contract_version": CONTRACT_VERSION,
        "status": "READY_FOR_COMMERCIAL_LAUNCH" if public_allowed else "BLOCKED_BY_GOVERNANCE_GATE",
        "ready": public_allowed,
        "gates": gates,
        "checked_at": _now_iso(),
        "decision_authority": False,
        "not_recommendation": True,
    }
    data["commercial_launch_contract_version"] = CONTRACT_VERSION
    return data

