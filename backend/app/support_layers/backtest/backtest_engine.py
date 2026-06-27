"""
NDSP V5.0 Backtest Engine

Purpose:
- Replay historical OHLCV records through simplified NDSP path:
  simulated direction -> DQS -> Scenario report.
- This is a first operational simulator, not final statistical research backtest.

Governance:
- Backtest does not execute trades.
- Backtest does not bypass Direction Authority in production.
- Simulated direction is explicitly marked as simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.support_layers.quality.decision_quality_stack import DQSInput, DecisionQualityStack
from app.support_layers.scenario.scenario_engine import ScenarioEngine, ScenarioInput


@dataclass(frozen=True)
class BacktestRecord:
    timestamp: int | str
    open: float
    high: float | None = None
    low: float | None = None
    close: float = 0.0
    volume: float | None = None
    symbol: str = "UNKNOWN"


@dataclass(frozen=True)
class BacktestResult:
    timestamp: int | str
    symbol: str
    price: float
    simulated_direction: str
    confidence: float
    grade: str
    decision_state: str
    risk_state: str
    scenario_summary: str
    execution_allowed: bool = False


class BacktestEngine:
    def __init__(self) -> None:
        self.dqs = DecisionQualityStack()
        self.scenario = ScenarioEngine()
        self.history_results: list[BacktestResult] = []

    def _simulate_direction(self, record: BacktestRecord) -> str:
        if record.close > record.open:
            return "BULLISH"
        if record.close < record.open:
            return "BEARISH"
        return "NEUTRAL"

    def _validate_record(self, record: BacktestRecord) -> None:
        if record.open <= 0 or record.close <= 0:
            raise ValueError(f"Invalid OHLC record: open/close must be positive: {record}")

        if record.high is not None and record.high < max(record.open, record.close):
            raise ValueError(f"Invalid OHLC record: high invariant failed: {record}")

        if record.low is not None and record.low > min(record.open, record.close):
            raise ValueError(f"Invalid OHLC record: low invariant failed: {record}")

    def run_on_data(
        self,
        historical_data: list[dict[str, Any]],
        *,
        symbol: str = "BTCUSDT",
        base_confidence: float = 75.0,
        macro_effect: float = 0.1,
        black_layer_penalty: float = 0.0,
        black_severity: str = "CLEAR",
    ) -> list[BacktestResult]:
        self.history_results = []

        for raw in historical_data:
            record = BacktestRecord(
                timestamp=raw.get("timestamp", raw.get("open_time_utc", "unknown")),
                open=float(raw["open"]),
                high=float(raw["high"]) if raw.get("high") is not None else None,
                low=float(raw["low"]) if raw.get("low") is not None else None,
                close=float(raw["close"]),
                volume=float(raw["volume"]) if raw.get("volume") is not None else None,
                symbol=str(raw.get("symbol", symbol)),
            )

            self._validate_record(record)

            simulated_direction = self._simulate_direction(record)

            quality = self.dqs.calculate_total_quality(
                DQSInput(
                    base_confidence=base_confidence,
                    macro_effect=macro_effect,
                    black_layer_penalty=black_layer_penalty,
                    black_severity=black_severity,
                    black_reasons=[],
                    notes={
                        "mode": "backtest",
                        "direction_source": "simulated_candle_direction",
                    },
                )
            )

            report = self.scenario.generate_report(
                ScenarioInput(
                    direction=simulated_direction,
                    grade=quality.grade,
                    confidence=quality.final_confidence,
                    decision_state=quality.decision_state,
                    risk_state=quality.risk_state,
                    execution_allowed=False,
                    execution_mode="decision_support_only",
                    reasons=quality.reasons,
                    macro_sentiment="NEUTRAL",
                    quality_label=quality.quality_label,
                    symbol=record.symbol,
                    timeframe="backtest",
                )
            )

            self.history_results.append(
                BacktestResult(
                    timestamp=record.timestamp,
                    symbol=record.symbol,
                    price=record.close,
                    simulated_direction=simulated_direction,
                    confidence=quality.final_confidence,
                    grade=quality.grade,
                    decision_state=quality.decision_state,
                    risk_state=quality.risk_state,
                    scenario_summary=report.summary,
                    execution_allowed=False,
                )
            )

        return self.history_results

    def summarize(self) -> dict[str, Any]:
        total = len(self.history_results)
        if total == 0:
            return {
                "total": 0,
                "bullish": 0,
                "bearish": 0,
                "neutral": 0,
                "blocked": 0,
                "avg_confidence": 0.0,
            }

        bullish = sum(1 for r in self.history_results if r.simulated_direction == "BULLISH")
        bearish = sum(1 for r in self.history_results if r.simulated_direction == "BEARISH")
        neutral = sum(1 for r in self.history_results if r.simulated_direction == "NEUTRAL")
        blocked = sum(1 for r in self.history_results if r.decision_state == "blocked")
        avg_conf = sum(r.confidence for r in self.history_results) / total

        return {
            "total": total,
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral,
            "blocked": blocked,
            "avg_confidence": round(avg_conf, 2),
        }
