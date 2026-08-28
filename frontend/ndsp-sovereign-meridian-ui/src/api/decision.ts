import type {
  AnalysisMode,
  AnalysisSelection,
  AnalysisTimeframe,
  CapabilityCoverageItem,
  LayerCoverageItem,
  PresentationMode,
} from "../analysis/types";

const API_ORIGIN = (import.meta.env.VITE_NDSP_DECISION_API_ORIGIN as string | undefined)?.replace(/\/$/, "") ?? "https://api.ndsp.app";
const BASE = `${API_ORIGIN}/api/ui-bridge/analysis`;

type Option = { id: string; label_ar: string; label_en: string };
export type SetupAsset = { symbol: string; market: string; label: string; source: string };
export type SetupMarket = { id: string; label_ar: string; label_en: string; assets_count: number };

export type AnalysisSetupOptions = {
  ok: boolean;
  generated_at: string;
  markets: SetupMarket[];
  assets: SetupAsset[];
  timeframes: Array<Option & { id: AnalysisTimeframe }>;
  analysis_modes: Array<Option & { id: AnalysisMode }>;
  presentation_modes: Array<Option & { id: PresentationMode }>;
  sources?: Record<string, string>;
  error?: string;
  message?: string;
};

export type ContextValidation = {
  ok: boolean;
  valid_context: boolean;
  decision_ready: boolean;
  errors: string[];
  context: {
    market: string;
    actual_market: string;
    symbol: string;
    timeframe: AnalysisTimeframe;
    analysis_mode: AnalysisMode;
    presentation_mode: PresentationMode;
    presentation_only: boolean;
    analysis_mode_binding: string;
    as_of: string | null;
  };
  governance_note: string;
};

export type CapabilityCoverage = {
  ok: boolean;
  contract: string;
  context: ContextValidation["context"];
  validation_errors: string[];
  decision_ready: boolean;
  official_state: "READY" | "BLOCKED" | string;
  silent_omission_count: number;
  silent_omissions: string[];
  capability_counts: Record<string, number>;
  capabilities: CapabilityCoverageItem[];
  layer_coverage: LayerCoverageItem[];
  decision_summary: {
    directional_bias: string | null;
    decision_quality: number | string | null;
    reading_horizon: string | null;
    market_state: string | null;
    caution_reason: string | null;
    sanitized_summary: string | null;
    scenario_state: string | null;
    activation: string | number | null;
    arrival: string | number | null;
    review: string | number | null;
    invalidation: string | number | null;
    generated_at: string | null;
  };
  governance: {
    frontend_recomputes_protected_logic: boolean;
    protected_formulas_exposed: boolean;
    presentation_mode_changes_calculation: boolean;
    no_silent_omission: boolean;
    fail_closed: boolean;
  };
  generated_at: string;
};

async function readJson<T>(url: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(url, {
    method: "GET",
    credentials: "include",
    headers: { Accept: "application/json" },
    signal,
  });

  let payload: unknown = null;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`INVALID_JSON:${response.status}`);
  }

  if (!response.ok) {
    const message =
      payload && typeof payload === "object" && "message" in payload
        ? String((payload as { message?: unknown }).message ?? response.status)
        : String(response.status);
    throw new Error(`REQUEST_FAILED:${message}`);
  }

  return payload as T;
}

function contextQuery(selection: AnalysisSelection): string {
  const params = new URLSearchParams({
    market: selection.market,
    symbol: selection.symbol,
    timeframe: selection.timeframe,
    analysis_mode: selection.analysisMode,
    presentation_mode: selection.presentationMode,
  });
  return params.toString();
}

export function getAnalysisSetupOptions(signal?: AbortSignal): Promise<AnalysisSetupOptions> {
  return readJson<AnalysisSetupOptions>(`${BASE}/setup/options`, signal);
}

export function validateAnalysisContext(selection: AnalysisSelection, signal?: AbortSignal): Promise<ContextValidation> {
  return readJson<ContextValidation>(`${BASE}/context/validate?${contextQuery(selection)}`, signal);
}

export function getCapabilityCoverage(selection: AnalysisSelection, signal?: AbortSignal): Promise<CapabilityCoverage> {
  return readJson<CapabilityCoverage>(`${BASE}/capability-coverage?${contextQuery(selection)}`, signal);
}
