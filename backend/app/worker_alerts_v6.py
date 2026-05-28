from __future__ import annotations

import json
import os
import time
import traceback

from app.core.governed_pipeline import run_governed
from app.engines.alerts_engine import process_alert
from app.pg_db import execute


SUPPORTED_VERSION = "1.0.0"


def _symbols() -> list[str]:
    raw = os.getenv("NDSP_ALERT_SYMBOLS", "BTCUSDT,ETHUSDT,SOLUSDT")
    return [x.strip().upper() for x in raw.split(",") if x.strip()]


def _interval() -> int:
    try:
        return max(30, int(os.getenv("NDSP_ALERT_INTERVAL_SECONDS", "300")))
    except Exception:
        return 300


def _alert_plan() -> str:
    return os.getenv("NDSP_ALERT_PLAN", "pro").strip().lower()


def _json_dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def _is_governed_contract(result: dict) -> bool:
    if not isinstance(result, dict):
        return False

    if result.get("version") != SUPPORTED_VERSION:
        return False

    required = (
        "symbol",
        "decision",
        "market_alignment",
        "scenario",
        "states",
        "execution",
        "alerts",
        "history",
        "risk",
        "meta",
    )

    return all(k in result for k in required)


def log_decision(result: dict, alert: dict | None = None) -> None:
    """
    Logs the governed decision-delivery contract.

    This does not create a broker-style signal.
    It does not write BUY/SELL/LONG/SHORT into signals.
    """
    try:
        alert = alert or {}

        decision = result.get("decision") or {}
        execution = result.get("execution") or {}
        risk = result.get("risk") or {}
        states = result.get("states") or {}
        meta = result.get("meta") or {}

        symbol = result.get("symbol") or alert.get("symbol")
        direction = decision.get("direction") or "neutral"
        confidence = decision.get("confidence")

        alert_status = alert.get("status")
        alert_reason = alert.get("reason")

        lifecycle = execution.get("lifecycle")
        trade_id = execution.get("trade_id")

        risk_state = risk.get("state") or states.get("risk_state")
        risk_reason = risk.get("reason")

        if not symbol:
            print("DECISION LOG SKIP missing symbol")
            return

        query = """
        INSERT INTO signal_decisions (
            symbol,
            direction,
            confidence,
            price,
            alert_status,
            alert_reason,
            lifecycle,
            trade_id,
            risk_state,
            risk_reason,
            raw_result,
            raw_alert
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s,
            %s, %s,
            %s, %s,
            %s::jsonb, %s::jsonb
        )
        """

        execute(
            query,
            (
                str(symbol).upper().strip(),
                str(direction).lower().strip(),
                confidence,
                None,
                alert_status,
                alert_reason,
                lifecycle,
                trade_id,
                risk_state,
                risk_reason,
                _json_dumps(result),
                _json_dumps(alert),
            ),
        )

        print(
            "GOVERNED DECISION LOGGED:",
            symbol,
            direction,
            confidence,
            states.get("system_state"),
            meta.get("momentum_alignment"),
            alert_status,
            alert_reason,
        )

    except Exception as exc:
        print("DECISION LOG ERROR:", str(exc))
        traceback.print_exc()


def run_worker() -> None:
    symbols = _symbols()
    interval = _interval()
    plan = _alert_plan()

    print("NDSP v6 governed alert worker started")
    print("symbols:", ",".join(symbols))
    print("interval_seconds:", interval)
    print("alert_plan:", plan)

    while True:
        for symbol in symbols:
            try:
                result = run_governed(symbol)

                if not _is_governed_contract(result):
                    print("SKIP invalid governed contract:", symbol, repr(result))
                    log_decision(
                        {
                            "version": SUPPORTED_VERSION,
                            "symbol": symbol,
                            "decision": {"direction": "neutral", "confidence": 0},
                            "market_alignment": {},
                            "scenario": {},
                            "states": {
                                "system_state": "blocked",
                                "risk_state": "paused",
                                "position_state": "none",
                            },
                            "execution": {"lifecycle": "waiting", "trade_id": ""},
                            "alerts": [],
                            "history": [],
                            "risk": {"state": "paused", "reason": "invalid_governed_contract"},
                            "meta": {},
                        },
                        {"status": "skipped", "reason": "invalid_governed_contract", "symbol": symbol},
                    )
                    continue

                try:
                    alert_result = process_alert(result, plan=plan)
                except Exception as alert_exc:
                    alert_result = {
                        "status": "skipped",
                        "reason": f"alert_error:{alert_exc}",
                        "symbol": symbol,
                    }
                    print("ALERT ERROR:", symbol, str(alert_exc))

                print("GOVERNED ALERT", symbol, alert_result)

                if isinstance(alert_result, dict):
                    log_decision(result, alert_result)
                else:
                    log_decision(result, {"status": "skipped", "reason": "non_dict_alert", "symbol": symbol})

            except Exception as exc:
                print("WORKER ERROR:", symbol, str(exc))
                traceback.print_exc()

        time.sleep(interval)


if __name__ == "__main__":
    run_worker()
