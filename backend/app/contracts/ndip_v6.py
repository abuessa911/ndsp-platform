from __future__ import annotations
from typing import List, Literal, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field, field_validator

Direction = Literal["bullish", "bearish", "neutral"]
NmpSignal = Literal["TESTING_ZONE", "CONTINUATION_SIGNAL", "REVERSAL_SIGNAL", "NO_SIGNAL"]
SystemState = Literal["live", "blocked", "safe_mode", "error"]
RiskState = Literal["normal", "paused", "drawdown"]
PositionState = Literal["none", "active", "monitoring"]
Lifecycle = Literal["waiting", "signal", "executing", "monitoring", "closed"]
AlertType = Literal["info", "warning", "critical"]

SUPPORTED_VERSION = "1.0.0"

class Decision(BaseModel):
    direction: Direction
    confidence: int = Field(ge=0, le=100)

class MarketAlignment(BaseModel):
    signal: NmpSignal
    zone_context: str
    entry_effect: str
    explanation: Optional[str] = None

class Scenario(BaseModel):
    interest: str
    invalidation: str
    target: str

class States(BaseModel):
    system_state: SystemState
    risk_state: RiskState
    position_state: PositionState

class Execution(BaseModel):
    lifecycle: Lifecycle
    trade_id: str

class AlertItem(BaseModel):
    type: AlertType
    priority: int = Field(ge=1, le=5)
    message: str
    timestamp: datetime

class HistoryItem(BaseModel):
    direction: Direction
    confidence: int = Field(ge=0, le=100)
    timestamp: datetime

class Risk(BaseModel):
    state: RiskState
    reason: str

class Meta(BaseModel):
    timestamp: datetime
    latency_ms: int = Field(ge=0)
    symbol_id: str
    connection_status: Literal["connected", "degraded", "disconnected"] = "connected"

class NDSPDashboardPayloadV6(BaseModel):
    version: str
    symbol: str
    decision: Decision
    market_alignment: market_alignment
    scenario: Scenario
    states: States
    execution: Execution
    alerts: List[AlertItem]
    history: List[HistoryItem]
    risk: Risk
    meta: Meta

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        if v != SUPPORTED_VERSION:
            raise ValueError("unsupported version")
        return v

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("symbol is required")
        return v

    @field_validator("meta")
    @classmethod
    def validate_meta(cls, v: Meta) -> Meta:
        if not v.symbol_id:
            raise ValueError("symbol_id is required")
        now = datetime.now(timezone.utc)
        payload_ts = v.timestamp
        if payload_ts.tzinfo is None:
            payload_ts = payload_ts.replace(tzinfo=timezone.utc)
        if now - payload_ts > timedelta(minutes=15):
            raise ValueError("stale payload")
        return v

def make_invalid_payload_response(reason: str) -> dict:
    return {
        "status": "invalid_payload",
        "freeze_ui": True,
        "safe_mode": True,
        "reason": reason,
    }

def validate_payload_or_failsafe(payload: dict) -> dict:
    try:
        validated = NDSPDashboardPayloadV6.model_validate(payload)
        return {"status": "ok", "payload": validated.model_dump(mode="json")}
    except Exception as exc:
        return make_invalid_payload_response(str(exc))
