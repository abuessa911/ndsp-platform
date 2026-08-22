#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import tempfile
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(os.environ.get("NDSP_PROJECT_ROOT", "/home/nawaf511/empire-core-new"))
UPSTREAM_BASE = os.environ.get("NDSP_UPSTREAM_BASE", "http://127.0.0.1:9082").rstrip("/")
HOST = os.environ.get("NDSP_CANONICAL_HOST", "127.0.0.1")
PORT = int(os.environ.get("NDSP_CANONICAL_PORT", "9085"))
RUNTIME_DIR = Path(os.environ.get(
    "NDSP_CANONICAL_RUNTIME_DIR",
    str(PROJECT_ROOT / "var/runtime/canonical-live-v30"),
))
WEB_DATA_DIR = Path(os.environ.get("NDSP_WEB_DATA_DIR", "/var/www/ndsp-my/data"))
VERSION = "ndsp-canonical-live-runtime-v30.0.0"
CONTRACT_VERSION = "ndsp-canonical-live-contract-v30"
SUPPORTED_MODES = {"investment", "speculative"}
SYMBOL_RE = re.compile(r"^[A-Z0-9._=-]{2,32}$")
TIMEFRAME_RE = re.compile(r"^(daily|weekly|monthly)$")
LOCK = threading.RLock()

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.layers.canonical_v1.runtime_bridge import run_canonical_layers  # noqa: E402
from backend.layers.canonical_v1.registry_lock import validate_registry_lock  # noqa: E402

REGISTRY_PATH = PROJECT_ROOT / "docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json"
PACKAGE_ROOT = PROJECT_ROOT / "backend/layers/canonical_v1"
EXPECTED_LAYER_IDS = [f"NDSP-CORE-L{i:02d}" for i in range(1, 17)]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def normalize_direction(value: Any) -> str:
    raw = str(value or "").strip().lower()
    aliases = {
        "bullish": "bullish", "bull": "bullish", "up": "bullish",
        "positive": "bullish", "صاعد": "bullish",
        "bearish": "bearish", "bear": "bearish", "down": "bearish",
        "negative": "bearish", "هابط": "bearish",
        "neutral": "neutral", "flat": "neutral", "محايد": "neutral",
    }
    return aliases.get(raw, "unknown")


def parse_iso(value: Any) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, path)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass


def append_ledger(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
    with LOCK:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(encoded + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(path, 0o600)


def sha256_json(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fetch_json(url: str, timeout: int = 40) -> tuple[int, dict[str, Any]]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": f"NDSP/{VERSION}",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            status = int(response.status)
    except HTTPError as exc:
        body = exc.read()
        status = int(exc.code)
    except (URLError, TimeoutError, OSError) as exc:
        return 0, {"ok": False, "error": type(exc).__name__, "detail": str(exc)}
    try:
        parsed = json.loads(body.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return status, {
            "ok": False,
            "error": "UPSTREAM_NON_JSON",
            "body_prefix": body[:240].decode("utf-8", errors="replace"),
        }
    return status, parsed if isinstance(parsed, dict) else {"data": parsed}


def read_json_file(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def walk_items(value: Any):
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key), child
            yield from walk_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_items(child)


DIRECTION_CANDIDATES = {
    "asset_managers_overall": {
        "asset_managers_overall", "asset_managers_overall_direction",
        "am_overall", "am_overall_direction", "tdl_medium_long_direction",
        "tdl_ml_direction",
    },
    "asset_managers_weekly": {
        "asset_managers_weekly", "asset_managers_weekly_direction",
        "am_weekly", "am_weekly_direction", "asset_manager_weekly_direction",
    },
    "leveraged_funds_weekly": {
        "leveraged_funds_weekly", "leveraged_funds_weekly_direction",
        "lf_weekly", "lf_weekly_direction", "leveraged_weekly_direction",
    },
}


def extract_direction(value: Mapping[str, Any], candidates: set[str]) -> str | None:
    lowered = {item.lower() for item in candidates}
    for key, child in walk_items(value):
        if key.lower() not in lowered:
            continue
        if isinstance(child, Mapping):
            for nested in ("direction", "value", "state", "signal"):
                direction = normalize_direction(child.get(nested))
                if direction in {"bullish", "bearish", "neutral"}:
                    return direction
        direction = normalize_direction(child)
        if direction in {"bullish", "bearish", "neutral"}:
            return direction
    return None


def discover_cot() -> dict[str, Any]:
    runtime = PROJECT_ROOT / "backend/runtime"
    candidates = [
        runtime / "tdl_active_direction.json",
        runtime / "tdl_ml_direction.json",
        runtime / "cot_canonical.json",
        runtime / "cftc_cot_canonical.json",
    ]
    if runtime.is_dir():
        candidates.extend(sorted(runtime.glob("*cot*.json"))[:20])

    merged: dict[str, Any] = {}
    files_used: list[str] = []
    for path in candidates:
        if not path.is_file():
            continue
        data = read_json_file(path)
        if data is None:
            continue
        merged[path.name] = data
        files_used.append(str(path))

    directions = {
        name: extract_direction(merged, keys)
        for name, keys in DIRECTION_CANDIDATES.items()
    }
    report_date = None
    generated_at = None
    for key, value in walk_items(merged):
        low = key.lower()
        if report_date is None and low in {
            "report_as_of_date", "report_date", "as_of_date", "cot_report_date"
        }:
            report_date = str(value or "").strip() or None
        if generated_at is None and low in {
            "generated_at", "updated_at", "fetched_at", "received_at"
        }:
            generated_at = str(value or "").strip() or None

    complete = all(
        directions[name] in {"bullish", "bearish"}
        for name in DIRECTION_CANDIDATES
    )
    timestamp = parse_iso(generated_at)
    age_hours = None
    if timestamp is not None:
        age_hours = round((utc_now() - timestamp).total_seconds() / 3600, 2)

    # Conservative: direction files alone are not enough for decision authority.
    verified = bool(complete and report_date and timestamp and age_hours is not None and age_hours <= 168)
    return {
        "status": "CURRENT_VERIFIED" if verified else "INPUTS_INCOMPLETE",
        "decision_use_allowed": verified,
        "monitoring_use_allowed": bool(files_used),
        "directions": directions,
        "report_as_of_date": report_date,
        "generated_at": generated_at,
        "age_hours": age_hours,
        "files_used": files_used,
        "reason_code": None if verified else "CANONICAL_COT_NOT_VERIFIED",
    }


def level_value(value: Any) -> float | None:
    if isinstance(value, Mapping):
        return finite_number(value.get("price"))
    return finite_number(value)


def normalize_levels(upstream: Mapping[str, Any]) -> dict[str, float]:
    raw = upstream.get("scenario_levels")
    if not isinstance(raw, Mapping):
        raw = (upstream.get("scenario") or {}).get("scenario_levels")
    raw = raw if isinstance(raw, Mapping) else {}
    result: dict[str, float] = {}
    for name in ("activation", "arrival", "review", "invalidation"):
        number = level_value(raw.get(name))
        if number is not None:
            result[name] = number
    return result


def load_context_file(name: str, max_age_minutes: int = 30) -> dict[str, Any]:
    path = WEB_DATA_DIR / name
    data = read_json_file(path)
    if data is None:
        return {
            "available": False,
            "fresh": False,
            "path": str(path),
            "reason": "FILE_MISSING_OR_INVALID",
            "items": [],
        }
    generated = parse_iso(data.get("generated_at"))
    age_minutes = None
    if generated is not None:
        age_minutes = round((utc_now() - generated).total_seconds() / 60, 2)
    fresh = bool(age_minutes is not None and 0 <= age_minutes <= max_age_minutes)
    items = data.get("items") if isinstance(data.get("items"), list) else []
    return {
        "available": True,
        "fresh": fresh,
        "path": str(path),
        "source": data.get("source"),
        "provider": data.get("provider"),
        "generated_at": data.get("generated_at"),
        "age_minutes": age_minutes,
        "item_count": len(items),
        "items": items,
    }


def high_impact_count(calendar: Mapping[str, Any]) -> int:
    count = 0
    for item in calendar.get("items") or []:
        impact = str((item or {}).get("impact") or "").strip().lower()
        if impact in {"high", "عالي", "مرتفع", "3"}:
            count += 1
    return count


def build_payload(
    upstream: Mapping[str, Any],
    symbol: str,
    timeframe: str,
    mode: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    instrument = upstream.get("instrument") if isinstance(upstream.get("instrument"), Mapping) else {}
    market = upstream.get("live_market_analysis")
    market = market if isinstance(market, Mapping) else {}
    scenario = upstream.get("scenario") if isinstance(upstream.get("scenario"), Mapping) else {}
    nmp = upstream.get("nmp") if isinstance(upstream.get("nmp"), Mapping) else {}
    levels = normalize_levels(upstream)

    selected_direction = normalize_direction(
        market.get("selected_timeframe_direction")
        or market.get("direction")
    )
    weekly_direction = selected_direction
    timing_eligible = bool(
        selected_direction in {"bullish", "bearish"}
        and len(levels) == 4
        and upstream.get("ok", False)
    )

    selected_rsi = finite_number(market.get("selected_timeframe_rsi"))
    atr_pct = finite_number(market.get("atr_4h_pct"))
    price = finite_number(instrument.get("live_price") or market.get("price"))
    cross_divergence = upstream.get("cross_timeframe_divergence")

    if cross_divergence is True:
        divergence_result = {
            "status": "CONFLICT_DETECTED",
            "confidence": 65,
            "regular_or_hidden": "NOT_CLASSIFIED",
            "reason": "cross_timeframe_divergence_flag",
            "input_quality": "PARTIAL",
        }
    else:
        divergence_result = {
            "status": "NOT_EVALUATED",
            "confidence": 0,
            "regular_or_hidden": "NOT_CLASSIFIED",
            "reason": "RSI_MACD_OBV_CCI_DIVERGENCE_SET_NOT_BOUND",
            "input_quality": "MISSING_GOVERNED_INDICATOR_SET",
        }

    momentum_status = "NOT_EVALUATED"
    momentum_confidence = 0
    if selected_rsi is not None and selected_direction in {"bullish", "bearish"}:
        momentum_status = "PARTIAL_AVAILABLE"
        momentum_confidence = int(min(85, 45 + abs(selected_rsi - 50)))
    momentum_result = {
        "status": momentum_status,
        "confidence": momentum_confidence,
        "rsi": selected_rsi,
        "direction": selected_direction,
        "reason": (
            "RSI_AND_DIRECTION_BOUND_MACD_OBV_CCI_PENDING"
            if momentum_status != "NOT_EVALUATED"
            else "NO_DIRECTIONAL_RSI_INPUT"
        ),
        "input_quality": "PARTIAL" if momentum_status != "NOT_EVALUATED" else "MISSING",
    }

    structure_complete = len(levels) == 4 and price is not None
    liquidity_structure_result = {
        "status": "PARTIAL_AVAILABLE" if structure_complete else "NOT_EVALUATED",
        "confidence": 55 if structure_complete else 0,
        "price": price,
        "scenario_levels": levels,
        "liquidity_verified": False,
        "structure_verified": structure_complete,
        "reason": (
            "STRUCTURE_BOUND_LIQUIDITY_FEED_PENDING"
            if structure_complete
            else "SCENARIO_STRUCTURE_INPUT_INCOMPLETE"
        ),
        "input_quality": "PARTIAL" if structure_complete else "MISSING",
    }

    calendar = load_context_file("economic-calendar.json", 30)
    news = load_context_file("news-impact.json", 30)
    macro_fresh = bool(calendar["fresh"] and news["fresh"])
    macro_status = "PARTIAL_AVAILABLE" if macro_fresh else "DEGRADED"
    usd_macro_result = {
        "status": macro_status,
        "confidence": 60 if macro_fresh else 25,
        "economic_calendar": {
            key: calendar.get(key)
            for key in ("available", "fresh", "source", "provider", "generated_at", "age_minutes", "item_count")
        },
        "news_context": {
            key: news.get(key)
            for key in ("available", "fresh", "source", "provider", "generated_at", "age_minutes", "item_count")
        },
        "high_impact_event_count": high_impact_count(calendar),
        "usd_direction_verified": False,
        "reason": (
            "LIVE_CALENDAR_AND_NEWS_BOUND_USD_INDEX_PENDING"
            if macro_fresh
            else "MACRO_CONTEXT_STALE_OR_UNAVAILABLE"
        ),
        "input_quality": "PARTIAL",
    }

    risk_reasons: list[str] = []
    risk_score = 20
    if atr_pct is None:
        risk_score += 25
        risk_reasons.append("ATR_PERCENT_MISSING")
    elif atr_pct >= 4:
        risk_score += 35
        risk_reasons.append("HIGH_ATR_VOLATILITY")
    elif atr_pct >= 2:
        risk_score += 20
        risk_reasons.append("ELEVATED_ATR_VOLATILITY")
    if not macro_fresh:
        risk_score += 20
        risk_reasons.append("MACRO_CONTEXT_NOT_FRESH")
    if len(levels) != 4:
        risk_score += 35
        risk_reasons.append("SCENARIO_LEVELS_INCOMPLETE")
    risk_score = min(100, risk_score)
    risk_blocked = bool(risk_score >= 80 or not upstream.get("ok", False))
    risk_result = {
        "status": "BLOCKED" if risk_blocked else "ACTIVE",
        "confidence": 75 if atr_pct is not None else 45,
        "blocked": risk_blocked,
        "risk_score": risk_score,
        "atr_pct": atr_pct,
        "reasons": risk_reasons,
        "input_quality": "PARTIAL",
    }

    cot = discover_cot()
    cot_directions = cot["directions"]

    nmp_candle = nmp.get("momentum_candle")
    nmp_candle = nmp_candle if isinstance(nmp_candle, Mapping) else {}
    nmp_open = finite_number(nmp_candle.get("open") or nmp.get("value"))
    nmp_indicator = finite_number(nmp.get("rsi"))
    nmp_direction = normalize_direction(nmp.get("direction") or selected_direction)
    candles = [{"open": nmp_open}] if nmp_open is not None else []
    indicator_values = [nmp_indicator] if nmp_open is not None and nmp_indicator is not None else []

    objections: list[str] = []
    if mode == "investment" and not cot["decision_use_allowed"]:
        objections.append("CANONICAL_COT_NOT_VERIFIED")
    if divergence_result["status"] == "NOT_EVALUATED":
        objections.append("DIVERGENCE_ENGINE_INPUT_SET_NOT_BOUND")
    if momentum_result["status"] != "AVAILABLE":
        objections.append("MOMENTUM_INDICATOR_SET_PARTIAL")
    if not liquidity_structure_result["liquidity_verified"]:
        objections.append("LIQUIDITY_FEED_NOT_VERIFIED")
    if not usd_macro_result["usd_direction_verified"]:
        objections.append("USD_DIRECTION_FEED_NOT_VERIFIED")
    if risk_blocked:
        objections.extend(risk_reasons or ["RISK_ENGINE_BLOCKED"])

    payload = {
        "analysis_mode": mode,
        "symbol": symbol,
        "market": instrument.get("market"),
        "timeframe": timeframe,
        "direction": nmp_direction if nmp_direction != "unknown" else selected_direction,
        "asset_managers_overall": cot_directions.get("asset_managers_overall"),
        "asset_managers_weekly": cot_directions.get("asset_managers_weekly"),
        "leveraged_funds_overall": cot_directions.get("leveraged_funds_overall"),
        "leveraged_funds_weekly": cot_directions.get("leveraged_funds_weekly"),
        "weekly_tdl_direction": weekly_direction,
        "timing_eligible": timing_eligible,
        "divergence_result": divergence_result,
        "scenario_levels": levels,
        "candles": candles,
        "indicator_values": indicator_values,
        "indicator_name": "RSI",
        "momentum_result": momentum_result,
        "liquidity_structure_result": liquidity_structure_result,
        "usd_macro_result": usd_macro_result,
        "risk_result": risk_result,
        "devils_advocate_blocked": bool(risk_blocked),
        "devils_advocate_reasons": objections,
        "_runtime_evidence": {
            "upstream_contract": upstream.get("public_contract_version"),
            "upstream_generated_at": upstream.get("generated_at"),
            "upstream_source_mode": upstream.get("source_mode"),
            "cot": cot,
        },
    }

    critical_blockers = list(dict.fromkeys(objections))
    input_matrix = {
        "L01": {"state": "LIVE" if cot["decision_use_allowed"] else "BLOCKED", "source": "CFTC_COT"},
        "L02": {"state": "LIVE" if timing_eligible else "PARTIAL", "source": "quality-live technical context"},
        "L03": {"state": "RUNTIME_DERIVED"},
        "L04": {"state": "RUNTIME_DERIVED"},
        "L05": {"state": "PARTIAL" if divergence_result["status"] != "NOT_EVALUATED" else "NOT_BOUND"},
        "L06": {"state": "RUNTIME_DERIVED"},
        "L07": {"state": "LIVE" if len(levels) == 4 else "BLOCKED"},
        "L08": {"state": "LIVE" if candles and indicator_values else "BLOCKED"},
        "L09": {"state": "PARTIAL" if momentum_status != "NOT_EVALUATED" else "NOT_BOUND"},
        "L10": {"state": "PARTIAL" if structure_complete else "NOT_BOUND"},
        "L11": {"state": "PARTIAL" if macro_fresh else "DEGRADED"},
        "L12": {"state": "PARTIAL"},
        "L13": {"state": "LIVE" if cot["decision_use_allowed"] else "BLOCKED"},
        "L14": {"state": "LIVE" if cot["decision_use_allowed"] else "BLOCKED"},
        "L15": {"state": "RUNTIME_DERIVED"},
        "L16": {"state": "REAL_ORCHESTRATOR"},
    }
    evidence = {
        "cot": cot,
        "input_matrix": input_matrix,
        "critical_blockers": critical_blockers,
        "upstream_generated_at": upstream.get("generated_at"),
        "upstream_provider": market.get("provider") or upstream.get("data_provider"),
        "upstream_contract": upstream.get("public_contract_version"),
        "scenario_state": scenario.get("scenario_state"),
    }
    return payload, evidence


def execute(symbol: str, timeframe: str, mode: str) -> tuple[int, dict[str, Any]]:
    query = urlencode({"symbol": symbol, "timeframe": timeframe})
    upstream_url = f"{UPSTREAM_BASE}/api/decision/quality-live?{query}"
    upstream_http, upstream = fetch_json(upstream_url)

    if upstream_http != 200 or upstream.get("ok") is not True:
        return 502, {
            "ok": False,
            "contract_version": CONTRACT_VERSION,
            "runtime_version": VERSION,
            "error": "UPSTREAM_QUALITY_LIVE_UNAVAILABLE",
            "upstream_http": upstream_http,
            "upstream": upstream,
        }

    payload, evidence = build_payload(upstream, symbol, timeframe, mode)
    canonical = run_canonical_layers(payload)

    layer_ids = [
        item.get("layer_id")
        for item in canonical.get("layers") or []
        if isinstance(item, Mapping)
    ]
    actual_execution = bool(
        canonical.get("ok")
        and canonical.get("total_layers_executed") == 16
        and layer_ids == EXPECTED_LAYER_IDS
    )

    blockers = list(evidence["critical_blockers"])
    if not actual_execution:
        blockers.append("CANONICAL_16_LAYER_EXECUTION_FAILED")
    blockers = list(dict.fromkeys(blockers))

    orchestrator_state = canonical.get("single_truth_state") or "UNDER_REVIEW"
    if not actual_execution:
        governed_state = "DATA_BLOCKED"
    elif mode == "investment" and not evidence["cot"]["decision_use_allowed"]:
        governed_state = "DATA_BLOCKED"
    elif "RISK_ENGINE_BLOCKED" in blockers or orchestrator_state == "BLOCKED_BY_DEVILS_ADVOCATE":
        governed_state = "BLOCKED_BY_DEVILS_ADVOCATE"
    elif blockers:
        governed_state = "MONITORING_ONLY"
    else:
        governed_state = orchestrator_state

    decision_use_allowed = bool(
        actual_execution
        and not blockers
        and governed_state in {"READY", "COMPLETED"}
    )

    generated_at = iso_now()
    request_id = hashlib.sha256(
        f"{symbol}|{timeframe}|{mode}|{generated_at}".encode("utf-8")
    ).hexdigest()[:24]

    public_layers = []
    for item in canonical.get("layers") or []:
        if not isinstance(item, Mapping):
            continue
        public_layers.append({
            "id": item.get("layer_id"),
            "canonical_name": item.get("canonical_name"),
            "state": item.get("status"),
            "confidence": item.get("confidence"),
            "blocking": item.get("blocking"),
            "reasons": item.get("reasons") or [],
            "output": item.get("output") or {},
            "binding_mode": "REAL_CANONICAL_ORCHESTRATOR_V30",
        })

    response = {
        "ok": actual_execution,
        "contract_version": CONTRACT_VERSION,
        "runtime_version": VERSION,
        "request_id": request_id,
        "generated_at": generated_at,
        "instrument": {
            "symbol": symbol,
            "timeframe": timeframe,
            "analysis_mode": mode,
            "market": (upstream.get("instrument") or {}).get("market"),
            "live_price": (upstream.get("instrument") or {}).get("live_price"),
        },
        "execution": {
            "actual_canonical_execution": actual_execution,
            "total_layers_expected": 16,
            "total_layers_executed": canonical.get("total_layers_executed", 0),
            "ordered_layer_ids": layer_ids,
            "orchestrator_state": orchestrator_state,
            "governed_single_truth_state": governed_state,
            "decision_use_allowed": decision_use_allowed,
            "monitoring_use_allowed": actual_execution,
            "publishable_completed_decision": decision_use_allowed,
            "decision_authority_boundary": "ONLY_NDSP_CORE_L01_TO_L16",
            "blockers": blockers,
        },
        "input_evidence": evidence,
        "decision_layers": public_layers,
        "scenario": upstream.get("scenario"),
        "nmp": upstream.get("nmp"),
        "golden_alignment": upstream.get("golden_alignment"),
        "upstream": {
            "http": upstream_http,
            "contract_version": upstream.get("public_contract_version"),
            "generated_at": upstream.get("generated_at"),
            "source_mode": upstream.get("source_mode"),
        },
        "not_recommendation": True,
        "no_execution_authority": True,
    }
    response["evidence_sha256"] = sha256_json(response)

    safe_key = re.sub(r"[^A-Z0-9_.-]", "_", symbol)
    latest = RUNTIME_DIR / f"latest_{safe_key}_{timeframe}_{mode}.json"
    raw = RUNTIME_DIR / "raw" / f"{request_id}.json"
    atomic_json(raw, {"upstream": upstream, "canonical_payload": payload, "response": response})
    atomic_json(latest, response)
    append_ledger(
        RUNTIME_DIR / "decision_evidence_ledger.jsonl",
        {
            "request_id": request_id,
            "generated_at": generated_at,
            "symbol": symbol,
            "timeframe": timeframe,
            "mode": mode,
            "actual_canonical_execution": actual_execution,
            "governed_single_truth_state": governed_state,
            "decision_use_allowed": decision_use_allowed,
            "blockers": blockers,
            "evidence_sha256": response["evidence_sha256"],
            "raw_evidence": str(raw),
        },
    )
    return 200 if actual_execution else 503, response


def health() -> tuple[int, dict[str, Any]]:
    lock = validate_registry_lock(REGISTRY_PATH, PACKAGE_ROOT)
    upstream_http, upstream = fetch_json(f"{UPSTREAM_BASE}/health", timeout=10)
    return (200 if lock.get("ok") else 503), {
        "ok": bool(lock.get("ok")),
        "service": "ndsp-canonical-live-runtime-v30",
        "runtime_version": VERSION,
        "contract_version": CONTRACT_VERSION,
        "host": HOST,
        "port": PORT,
        "canonical_registry_ok": bool(lock.get("ok")),
        "canonical_layer_count": lock.get("layer_count"),
        "upstream_health_http": upstream_http,
        "upstream_health_ok": upstream.get("ok"),
        "runtime_dir": str(RUNTIME_DIR),
        "publicly_exposed": False,
        "generated_at": iso_now(),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "NDSPCanonicalLive/30"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write(
            f"{iso_now()} client={self.client_address[0]} {fmt % args}\n"
        )

    def write_json(self, status: int, payload: Mapping[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-NDSP-Contract", CONTRACT_VERSION)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/health", "/api/health"}:
            status, payload = health()
            self.write_json(status, payload)
            return
        if parsed.path != "/api/decision/canonical-live":
            self.write_json(404, {"ok": False, "error": "NOT_FOUND"})
            return

        params = parse_qs(parsed.query)
        symbol = str((params.get("symbol") or ["ETHUSDT"])[0]).strip().upper()
        timeframe = str((params.get("timeframe") or ["weekly"])[0]).strip().lower()
        mode = str((params.get("mode") or ["speculative"])[0]).strip().lower()

        if not SYMBOL_RE.fullmatch(symbol):
            self.write_json(400, {"ok": False, "error": "INVALID_SYMBOL"})
            return
        if not TIMEFRAME_RE.fullmatch(timeframe):
            self.write_json(400, {"ok": False, "error": "INVALID_TIMEFRAME"})
            return
        if mode not in SUPPORTED_MODES:
            self.write_json(400, {"ok": False, "error": "INVALID_ANALYSIS_MODE"})
            return

        try:
            status, payload = execute(symbol, timeframe, mode)
        except Exception as exc:
            self.write_json(500, {
                "ok": False,
                "error": "CANONICAL_RUNTIME_EXCEPTION",
                "exception_type": type(exc).__name__,
                "detail": str(exc),
                "runtime_version": VERSION,
            })
            return
        self.write_json(status, payload)


def main() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(RUNTIME_DIR, 0o700)
    lock = validate_registry_lock(REGISTRY_PATH, PACKAGE_ROOT)
    if not lock.get("ok"):
        raise SystemExit(f"canonical registry invalid: {lock.get('errors')}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(json.dumps({
        "ok": True,
        "service": "ndsp-canonical-live-runtime-v30",
        "host": HOST,
        "port": PORT,
        "runtime_version": VERSION,
        "registry_layers": lock.get("layer_count"),
    }, ensure_ascii=False), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

