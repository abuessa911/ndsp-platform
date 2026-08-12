import { useCallback, useEffect, useState } from "react";

const BASE_URL = "";
const MODES = ["speculative", "investment"];

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Decision request failed: ${response.status}`);
  }

  return response.json();
}

function toPublicDecision(input, mode) {
  const src = input?.decision || input?.data || input?.result || input || {};

  return {
    ok: input?.ok !== false,
    mode,
    symbol: src.symbol ?? input?.symbol ?? null,
    timeframe: src.timeframe ?? input?.timeframe ?? null,
    generatedAt: src.generated_at ?? src.generatedAt ?? input?.generated_at ?? input?.generatedAt ?? null,
    decisionState: src.decision_state ?? src.decisionState ?? src.state ?? null,
    direction: src.direction ?? src.bias ?? null,
    readiness: src.readiness ?? null,
    scenarioState: src.scenario_state ?? src.scenarioState ?? null,
    riskFinalState: src.risk_final_state ?? src.riskFinalState ?? src.risk?.final_state ?? null,
  };
}

export function useCanonicalDecision(symbol, timeframe = "weekly") {
  const [results, setResults] = useState({
    speculative: null,
    investment: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    const normalizedSymbol = symbol || "XAUUSD";
    const normalizedTimeframe = timeframe || "weekly";

    setLoading(true);
    setError(null);

    try {
      const entries = await Promise.all(
        MODES.map(async (mode) => {
          const endpoint = `${BASE_URL}/api/decision/canonical-live?symbol=${encodeURIComponent(normalizedSymbol)}&timeframe=${encodeURIComponent(normalizedTimeframe)}&mode=${mode}`;
          const body = await fetchJson(endpoint);
          return [mode, toPublicDecision(body, mode)];
        })
      );

      setResults(Object.fromEntries(entries));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Decision request failed");
    } finally {
      setLoading(false);
    }
  }, [symbol, timeframe]);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 30000);
    return () => clearInterval(id);
  }, [refresh]);

  return {
    speculative: results.speculative,
    investment: results.investment,
    loading,
    error,
    refresh,
  };
}
