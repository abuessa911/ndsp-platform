export type DirectionContext = "bullish" | "bearish" | "neutral";
export type RiskState = "normal" | "paused" | "drawdown";
export type SystemState = "live" | "blocked" | "safe_mode" | "error";

export interface DecisionObject {
  version: string;
  governance_version: string;
  system: "NDSP";
  symbol: string;
  decision: {
    direction: DirectionContext;
    confidence: number;
  };
  states: {
    system_state: SystemState;
    risk_state: RiskState;
    position_state: "none" | "active" | "monitoring";
  };
  meta: {
    timestamp: string;
    request_id?: string;
    latency_ms?: number;
  };
}
