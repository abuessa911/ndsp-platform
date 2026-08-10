#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs, urlparse

HOST = os.environ.get("NDSP_COMPLETED_EVIDENCE_HOST", "127.0.0.1")
PORT = int(os.environ.get("NDSP_COMPLETED_EVIDENCE_PORT", "9087"))
V33_RUNTIME_DIR = Path(os.environ.get(
    "NDSP_V33_RUNTIME_DIR",
    "/home/nawaf511/empire-core-new/var/runtime/canonical-live-v33",
))
VERSION = "ndsp-completed-decisions-evidence-v35.0.0"
CONTRACT_VERSION = "ndsp-completed-decisions-current-v35"
SYMBOL_RE = re.compile(r"^[A-Z0-9._=-]{2,32}$")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def layer_by_id(response: Mapping[str, Any], layer_id: str) -> Mapping[str, Any]:
    for item in response.get("decision_layers") or []:
        if isinstance(item, Mapping) and item.get("id") == layer_id:
            return item
    return {}


def stable_fingerprint(response: Mapping[str, Any]) -> str:
    execution = response.get("execution") or {}
    instrument = response.get("instrument") or {}
    layers = []
    for item in response.get("decision_layers") or []:
        if not isinstance(item, Mapping):
            continue
        layers.append({
            "id": item.get("id"),
            "state": item.get("state"),
            "confidence": item.get("confidence"),
            "blocking": item.get("blocking"),
            "reasons": item.get("reasons") or [],
            "output": item.get("output") or {},
        })

    stable = {
        "symbol": instrument.get("symbol"),
        "timeframe": instrument.get("timeframe"),
        "analysis_mode": instrument.get("analysis_mode"),
        "market": instrument.get("market"),
        "governed_state": execution.get("governed_single_truth_state"),
        "decision_use_allowed": execution.get("decision_use_allowed"),
        "publishable": execution.get("publishable_completed_decision"),
        "blockers": execution.get("blockers") or [],
        "scenario": response.get("scenario"),
        "nmp": response.get("nmp"),
        "layers": layers,
    }
    encoded = json.dumps(
        stable,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_publishable(response: Mapping[str, Any]) -> bool:
    execution = response.get("execution") or {}
    return bool(
        response.get("ok") is True
        and response.get("runtime_version") == "ndsp-canonical-live-runtime-v33.0.0"
        and execution.get("actual_canonical_execution") is True
        and execution.get("total_layers_executed") == 16
        and execution.get("decision_use_allowed") is True
        and execution.get("publishable_completed_decision") is True
        and execution.get("governed_single_truth_state") in {"READY", "COMPLETED"}
        and not (execution.get("blockers") or [])
    )


def scenario_levels(response: Mapping[str, Any]) -> dict[str, Any]:
    scenario = response.get("scenario") or {}
    l07 = layer_by_id(response, "NDSP-CORE-L07")
    layer_levels = ((l07.get("output") or {}).get("levels") or {})
    return {
        "activation": (
            layer_levels.get("activation")
            or scenario.get("scenario_activation_level")
            or scenario.get("activation_level")
        ),
        "arrival": (
            layer_levels.get("arrival")
            or scenario.get("scenario_arrival_level")
            or scenario.get("arrival_level")
        ),
        "review": (
            layer_levels.get("review")
            or scenario.get("scenario_review_zone")
            or scenario.get("review_zone")
        ),
        "invalidation": (
            layer_levels.get("invalidation")
            or scenario.get("scenario_invalidation_level")
            or scenario.get("invalidation_level")
        ),
    }


def decision_from_response(response: Mapping[str, Any], source_file: Path) -> dict[str, Any]:
    instrument = response.get("instrument") or {}
    execution = response.get("execution") or {}
    scenario = response.get("scenario") or {}
    l03 = layer_by_id(response, "NDSP-CORE-L03")
    l08 = layer_by_id(response, "NDSP-CORE-L08")
    l12 = layer_by_id(response, "NDSP-CORE-L12")
    l15 = layer_by_id(response, "NDSP-CORE-L15")
    l16 = layer_by_id(response, "NDSP-CORE-L16")

    fingerprint = stable_fingerprint(response)
    decision_id = "CD-" + fingerprint[:20].upper()
    l03_output = l03.get("output") or {}
    l08_output = l08.get("output") or {}
    l12_output = l12.get("output") or {}
    l15_output = l15.get("output") or {}
    l16_output = l16.get("output") or {}

    confidence_values = [
        finite_number(item.get("confidence"))
        for item in response.get("decision_layers") or []
        if isinstance(item, Mapping)
    ]
    confidence_values = [value for value in confidence_values if value is not None]
    evidence_confidence = (
        round(sum(confidence_values) / len(confidence_values), 2)
        if confidence_values else None
    )

    return {
        "decision_id": decision_id,
        "decision_status": "complete",
        "decision_state": execution.get("governed_single_truth_state"),
        "publishable": True,
        "symbol": instrument.get("symbol"),
        "asset_id": instrument.get("symbol"),
        "asset_name": instrument.get("symbol"),
        "market": instrument.get("market"),
        "timeframe": instrument.get("timeframe"),
        "analysis_mode": instrument.get("analysis_mode"),
        "trend_context": (
            l03_output.get("direction")
            or scenario.get("scenario_directional_context")
            or scenario.get("directional_context")
        ),
        "scenario_state": scenario.get("scenario_state"),
        "levels": scenario_levels(response),
        "nmp": {
            "status": l08.get("state"),
            "value": l08_output.get("value"),
            "direction": l08_output.get("direction"),
            "timeframe": l08_output.get("timeframe"),
            "indicator_name": l08_output.get("indicator_name"),
            "indicator_value": l08_output.get("indicator_value"),
        },
        "risk": {
            "status": l12.get("state"),
            "blocked": bool(l12_output.get("blocked")),
            "risk_score": l12_output.get("risk_score"),
            "atr_pct": l12_output.get("atr_pct"),
            "reasons": l12_output.get("reasons") or [],
        },
        "devils_advocate": {
            "status": l15.get("state"),
            "blocked": bool(l15_output.get("blocked")),
            "reasons": l15_output.get("reasons") or [],
            "authority": l15_output.get("authority"),
        },
        "readiness": {
            "status": l16.get("state"),
            "allowed": bool(l16_output.get("allowed")),
            "single_truth_state": l16_output.get("single_truth_state"),
            "reason_code": l16_output.get("reason_code"),
        },
        "decision_quality": None,
        "decision_quality_note": "No independent numeric quality score is fabricated by V35.",
        "evidence_confidence_average": evidence_confidence,
        "actual_layers_executed": execution.get("total_layers_executed"),
        "layer_states": [
            {
                "id": item.get("id"),
                "name": item.get("canonical_name"),
                "state": item.get("state"),
                "confidence": item.get("confidence"),
                "blocking": item.get("blocking"),
            }
            for item in response.get("decision_layers") or []
            if isinstance(item, Mapping)
        ],
        "follow_up_horizon": None,
        "updated_at": None,
        "generated_at": response.get("generated_at"),
        "source_runtime": response.get("runtime_version"),
        "contract_version": response.get("contract_version"),
        "evidence_sha256": response.get("evidence_sha256"),
        "semantic_fingerprint": fingerprint,
        "not_recommendation": True,
        "no_execution_authority": True,
        "disclaimer": (
            "NDSP provides explanatory decision support only. "
            "This is not financial advice, not a buy/sell recommendation, "
            "and not an execution instruction."
        ),
        "_source_file_name": source_file.name,
    }


def load_current_decisions() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: dict[tuple[str, str, str], dict[str, Any]] = {}
    rejected: list[dict[str, Any]] = []

    for path in sorted(V33_RUNTIME_DIR.glob("latest_*.json")):
        response = read_json(path)
        if response is None:
            rejected.append({"file": path.name, "reason": "INVALID_JSON"})
            continue

        instrument = response.get("instrument") or {}
        key = (
            str(instrument.get("symbol") or ""),
            str(instrument.get("timeframe") or ""),
            str(instrument.get("analysis_mode") or ""),
        )

        if not is_publishable(response):
            execution = response.get("execution") or {}
            rejected.append({
                "file": path.name,
                "symbol": key[0],
                "timeframe": key[1],
                "analysis_mode": key[2],
                "state": execution.get("governed_single_truth_state"),
                "blockers": execution.get("blockers") or [],
                "reason": "NOT_PUBLISHABLE",
            })
            continue

        decision = decision_from_response(response, path)
        previous = accepted.get(key)
        if previous is None or str(decision.get("generated_at") or "") > str(previous.get("generated_at") or ""):
            accepted[key] = decision

    decisions = sorted(
        accepted.values(),
        key=lambda item: str(item.get("generated_at") or ""),
        reverse=True,
    )
    return decisions, rejected


class Handler(BaseHTTPRequestHandler):
    server_version = "NDSPCompletedEvidence/35"

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def write_json(self, status: int, payload: Mapping[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-NDSP-Contract", CONTRACT_VERSION)
        self.send_header("X-NDSP-Decision-Authority", "explanatory-only")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        self.write_json(405, {
            "ok": False,
            "error": "READ_ONLY_REGISTRY",
            "message": "V35 does not accept manual decision ingestion.",
        })

    def do_PUT(self) -> None:
        self.do_POST()

    def do_DELETE(self) -> None:
        self.do_POST()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        decisions, rejected = load_current_decisions()

        if parsed.path in {"/health", "/api/health"}:
            self.write_json(200, {
                "ok": True,
                "service": "ndsp-completed-decisions-evidence-v35",
                "runtime_version": VERSION,
                "contract_version": CONTRACT_VERSION,
                "port": PORT,
                "v33_runtime_dir": str(V33_RUNTIME_DIR),
                "v33_runtime_dir_exists": V33_RUNTIME_DIR.is_dir(),
                "current_publishable_count": len(decisions),
                "current_blocked_or_rejected_count": len(rejected),
                "read_only": True,
                "database_backed_history": False,
                "generated_at": iso_now(),
            })
            return

        if parsed.path == "/api/completed-decisions":
            params = parse_qs(parsed.query)
            symbol = str((params.get("symbol") or [""])[0]).strip().upper()
            mode = str((params.get("mode") or [""])[0]).strip().lower()
            timeframe = str((params.get("timeframe") or [""])[0]).strip().lower()
            try:
                limit = max(1, min(100, int((params.get("limit") or ["25"])[0])))
            except ValueError:
                limit = 25

            filtered = decisions
            if symbol:
                filtered = [item for item in filtered if item.get("symbol") == symbol]
            if mode:
                filtered = [item for item in filtered if item.get("analysis_mode") == mode]
            if timeframe:
                filtered = [item for item in filtered if item.get("timeframe") == timeframe]

            self.write_json(200, {
                "ok": True,
                "source": "v33_evidence_backed_current_registry",
                "contract_version": CONTRACT_VERSION,
                "current_only": True,
                "database_backed_history": False,
                "decision_authority_boundary": "ONLY_V33_PUBLISHABLE_CANONICAL_DECISIONS",
                "count": len(filtered[:limit]),
                "decisions": filtered[:limit],
                "generated_at": iso_now(),
            })
            return

        if parsed.path == "/api/completed-decisions/latest":
            self.write_json(200, {
                "ok": True,
                "source": "v33_evidence_backed_current_registry",
                "decision": decisions[0] if decisions else None,
                "generated_at": iso_now(),
            })
            return

        prefix = "/api/completed-decisions/"
        if parsed.path.startswith(prefix):
            symbol = parsed.path[len(prefix):].strip().upper()
            if not SYMBOL_RE.fullmatch(symbol):
                self.write_json(400, {"ok": False, "error": "INVALID_SYMBOL"})
                return
            found = next((item for item in decisions if item.get("symbol") == symbol), None)
            if found is None:
                self.write_json(404, {
                    "ok": False,
                    "error": "NO_CURRENT_PUBLISHABLE_COMPLETED_DECISION",
                    "symbol": symbol,
                })
                return
            self.write_json(200, {
                "ok": True,
                "source": "v33_evidence_backed_current_registry",
                "decision": found,
                "generated_at": iso_now(),
            })
            return

        self.write_json(404, {"ok": False, "error": "NOT_FOUND"})


def main() -> None:
    if not V33_RUNTIME_DIR.is_dir():
        raise SystemExit(f"V33 runtime directory not found: {V33_RUNTIME_DIR}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(
        f"[NDSP] Completed Decisions Evidence V35 listening on "
        f"http://{HOST}:{PORT}",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
