import { useCallback, useEffect, useState } from "react";

const BASE_URL = "";
const MODES = ["speculative", "investment"];

async function fetchJson(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);

  try {
    const response = await fetch(url, {
      signal: controller.signal,
      cache: "no-store",
      headers: { Accept: "application/json" }
    });

    if (!response.ok) {
      throw new Error(`HTTP_${response.status}`);
    }

    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

export function useCanonicalDecision(symbol, timeframe = "weekly") {
  const [payloads, setPayloads] = useState({
    speculative: null,
    investment: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    const normalizedSymbol = String(symbol || "").trim().toUpperCase();
    const normalizedTimeframe = String(timeframe || "weekly").trim().toLowerCase();

    setLoading(true);
    setError(null);

    try {
      const settled = await Promise.allSettled(
        MODES.map(async (mode) => {
          const endpoint = `${BASE_URL}/api/decision/canonical-live?symbol=${encodeURIComponent(normalizedSymbol)}&timeframe=${encodeURIComponent(normalizedTimeframe)}&mode=${mode}`;
          const payload = await fetchJson(endpoint);
          return [mode, payload];
        })
      );

      const next = {};
      const failures = [];

      settled.forEach((result, index) => {
        const mode = MODES[index];
        if (result.status === "fulfilled") {
          next[mode] = result.value[1];
        } else {
          failures.push(`${mode}:${result.reason?.message || "FETCH_FAILED"}`);
        }
      });

      setPayloads((current) => ({ ...current, ...next }));

      if (failures.length === MODES.length) {
        throw new Error(failures.join("|"));
      }

      if (failures.length) {
        setError(failures.join("|"));
      }
    } catch (err) {
      setError(err?.message || "CANONICAL_FETCH_ERROR");
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
    speculative: payloads.speculative,
    investment: payloads.investment,
    loading,
    error,
    refresh
  };
}

