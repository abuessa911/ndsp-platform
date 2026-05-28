#!/usr/bin/env python3
import sys
from typing import List

from pydantic import BaseModel, Field


class NDSPDecisionContract(BaseModel):
    trace_id: str
    symbol: str
    timestamp: str
    session_state: str
    dominant_direction: str = Field(..., pattern="^(bullish|bearish|neutral)$")
    direction_source: str
    timing_controller: str
    confidence_score: float = Field(default=0.0, ge=0, le=100)
    grade: str = "D"
    applied_effects: List[str] = Field(default_factory=list)
    risk_state: str = "Normal"
    decision_state: str = "Blocked"
    execution_allowed: bool = False


if __name__ == "__main__":
    example_data = {
        "trace_id": "NDSP-V4.1-STABLE",
        "symbol": "BTCUSDT",
        "timestamp": "2023-10-27T10:00:00Z",
        "session_state": "Open",
        "dominant_direction": "bullish",
        "direction_source": "Weekly_LM",
        "timing_controller": "L&M",
        "confidence_score": 88.5,
        "grade": "A",
        "applied_effects": ["Golden_Alignment"],
        "risk_state": "Normal",
        "decision_state": "Ready",
        "execution_allowed": False,
    }

    try:
        contract = NDSPDecisionContract(**example_data)
        print("\n[SUCCESS] Contract Integrity Validated:")
        print(contract.model_dump_json(indent=2))
    except Exception as exc:
        print(f"\n[ERROR] Validation Failed: {exc}")
        sys.exit(1)
