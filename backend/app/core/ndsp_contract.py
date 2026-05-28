from pydantic import BaseModel, Field
from typing import List, Optional

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
    applied_effects: List[str] = []
    risk_state: str = "Normal"
    decision_state: str = "Blocked"
    execution_allowed: bool = False
    source_mode: str = "http_decision"
