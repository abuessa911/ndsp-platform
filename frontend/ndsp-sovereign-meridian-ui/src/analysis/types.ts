export type AnalysisMode = "investment" | "speculative";
export type PresentationMode = "beginner" | "professional";
export type AnalysisTimeframe = "daily" | "weekly" | "monthly";

export type AnalysisSelection = {
  market: string;
  symbol: string;
  timeframe: AnalysisTimeframe;
  analysisMode: AnalysisMode;
  presentationMode: PresentationMode;
};

export type GovernedAnalysisContext = AnalysisSelection & {
  asOf: string | null;
  generation: number;
};

export type CapabilityState =
  | "CONTRIBUTED"
  | "BLOCKED"
  | "NOT_APPLICABLE"
  | "UNAVAILABLE"
  | "STALE"
  | "PARTIAL"
  | "GOVERNANCE_PROTECTED";

export type CapabilityCoverageItem = {
  id: string;
  public_label: string;
  protected: boolean;
  state: CapabilityState;
  effect: "supports" | "weakens" | "conflicts" | "blocks" | "informational" | string;
  safe_detail: string;
  freshness: string | null;
};

export type LayerCoverageItem = {
  layer: number;
  public_label: string;
  state: CapabilityState;
  protected: boolean;
};
