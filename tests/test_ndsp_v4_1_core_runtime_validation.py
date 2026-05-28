#!/usr/bin/env python3
import json
import sys
import urllib.request
from datetime import datetime, timezone

RUNTIME_ENDPOINT = "http://127.0.0.1:9001/decision"

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "EURUSD",
    "XAUUSD",
    "USOIL",
    "US30",
]

FORBIDDEN_PUBLIC_FIELDS = [
    "cot",
    "tff",
    "disaggregated",
    "legacy",
    "tdl_v2",
    "raw_score",
    "layer_score",
    "weights",
    "institutional_mapping",
    "participant_mapping",
    "execution_logic",
    "scoring_formula",
]

def fetch_decision(symbol: str) -> tuple[int, dict]:
    url = f"{RUNTIME_ENDPOINT}?symbol={symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": "NDSP-V4.1-Official-Runtime-Test"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            code = int(resp.status)
            body = resp.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
            except Exception:
                data = {"_raw": body[:1000]}
            return code, data
    except Exception as exc:
        return 0, {"error": str(exc)}

def deep_keys(obj):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.append(str(k))
            found.extend(deep_keys(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(deep_keys(item))
    return found

def get_nested(d, path, default=None):
    cur = d
    for part in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part)
    return cur

def main() -> int:
    results = {
        "source_mode": "http_decision",
        "runtime_endpoint": RUNTIME_ENDPOINT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "symbols": {},
        "failed_symbols": [],
        "assertions": {},
    }

    for symbol in SYMBOLS:
        code, data = fetch_decision(symbol)
        keys = [k.lower() for k in deep_keys(data)]
        forbidden_hits = sorted(set(k for k in keys if k in FORBIDDEN_PUBLIC_FIELDS))

        decision = data.get("decision", data if isinstance(data, dict) else {})
        execution_allowed = get_nested(data, ["decision", "execution_allowed"], data.get("execution_allowed"))
        execution_mode = get_nested(data, ["decision", "execution_mode"], data.get("execution_mode"))
        direct_execution = data.get("direct_execution", None)

        symbol_result = {
            "http_code": code,
            "ok_http": code in (200, 201),
            "has_json": isinstance(data, dict) and "_raw" not in data,
            "has_decision_like_payload": isinstance(data, dict) and len(data.keys()) > 0,
            "execution_allowed": execution_allowed,
            "execution_mode": execution_mode,
            "direct_execution": direct_execution,
            "forbidden_public_field_hits": forbidden_hits,
        }

        # Governance acceptance:
        # - runtime reachable
        # - JSON response exists
        # - no direct execution language/state exposed as allowed true
        # - no forbidden sensitive public fields
        symbol_ok = True
        if not symbol_result["ok_http"]:
            symbol_ok = False
        if not symbol_result["has_json"]:
            symbol_ok = False
        if forbidden_hits:
            symbol_ok = False
        if execution_allowed is True:
            symbol_ok = False
        if isinstance(execution_mode, str) and "auto_execution" in execution_mode.lower():
            symbol_ok = False
        if direct_execution is True:
            symbol_ok = False

        symbol_result["assert_ok"] = symbol_ok
        results["symbols"][symbol] = symbol_result

        if not symbol_ok:
            results["failed_symbols"].append(symbol)

    results["assertions"]["SOURCE_MODE_HTTP_DECISION"] = results["source_mode"] == "http_decision"
    results["assertions"]["FAILED_SYMBOLS_EMPTY"] = len(results["failed_symbols"]) == 0
    results["assertions"]["NO_DIRECT_EXECUTION"] = all(
        r.get("execution_allowed") is not True and r.get("direct_execution") is not True
        for r in results["symbols"].values()
    )
    results["assertions"]["NO_FORBIDDEN_PUBLIC_FIELDS"] = all(
        not r.get("forbidden_public_field_hits")
        for r in results["symbols"].values()
    )

    results["overall_assert_ok"] = all(results["assertions"].values())

    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if results["overall_assert_ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
