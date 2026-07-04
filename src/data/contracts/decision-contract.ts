/**
 * NDSP Phase 4 — Normalized Decision Contract
 * Public frontend contract only. It does not expose protected internals.
 */

export type NDSPDisplayMode = 'beginner' | 'professional';
export type NDSPReadingHorizon = 'investor' | 'tactical';

export interface NDSPDecisionContract {
  identity: { symbol: string; market: string; timeframe: string; updated_at: string };
  modes: { display_mode: NDSPDisplayMode; reading_horizon: NDSPReadingHorizon };
  decision: { scenario_state: string; decision_quality: string; directional_context: string; sanitized_summary: string; caution_reason: string };
  levels: { activation: string; arrival: string; review_zone: string; invalidation: string };
  nmp: { state: string; zone: string; note: string };
  radar: { market_state: string; risk_state: string; levels_state: string; nmp_state: string; horizon_state: string; devil_state: string };
  usd_macro: { usd_state: string; usd_impact: string; macro_events: string[]; metals_impact: string; fx_impact: string; crypto_impact: string; indices_commodities_impact: string };
  daily_brief: { headline: string; bullets: string[]; next_watch: string };
  monitoring: { watchlist: string[]; alerts: string[]; completed_readings: string[] };
  disclaimers: { decision_support_only: string };
}

export const NDSP_CONTRACT_VERSION = 'NDSP_PHASE4_DATA_CONTRACT_V1';
