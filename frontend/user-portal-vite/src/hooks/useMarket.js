import { useEffect, useState, useCallback } from "react";

/*
  مهم:
  BASE_URL فارغ لأن Vite Proxy سيحوّل:
  /api/...  --->  https://api.ndsp.app/api/...
*/
const BASE_URL = "";

export function useMarket(symbol) {
  const [price, setPrice] = useState(null);
  const [scenario, setScenario] = useState(null);
  const [allPrices, setAllPrices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchJson = async (url) => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    try {
      const res = await fetch(url, {
        signal: controller.signal,
        cache: "no-store",
        headers: {
          Accept: "application/json"
        }
      });

      if (!res.ok) {
        throw new Error(`HTTP_${res.status}`);
      }

      return await res.json();
    } finally {
      clearTimeout(timeout);
    }
  };

  const fetchPrice = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const normalizedSymbol = String(symbol || "").trim().toUpperCase();
      const url = `${BASE_URL}/api/market/prices?symbol=${encodeURIComponent(normalizedSymbol)}`;

      const data = await fetchJson(url);
      const rows = Array.isArray(data?.prices) ? data.prices : [];

      const current = rows.find((r) => {
        const rowSymbol = String(r?.symbol || "").trim().toUpperCase();
        return rowSymbol === normalizedSymbol;
      });

      setAllPrices(rows);
      setPrice(current || null);

      if (!current) {
        setError(`NO_MATCH_FOR_${normalizedSymbol}`);
      }
    } catch (err) {
      console.error("PRICE FETCH ERROR:", err);

      setPrice(null);
      setAllPrices([]);
      setError(err?.message || "PRICE_FETCH_ERROR");
    } finally {
      setLoading(false);
    }
  }, [symbol]);

  const fetchScenario = useCallback(async () => {
    try {
      const normalizedSymbol = String(symbol || "").trim().toUpperCase();
      const url = `${BASE_URL}/api/scenario/levels?symbol=${encodeURIComponent(normalizedSymbol)}`;

      const data = await fetchJson(url);
      setScenario(data || null);
    } catch (err) {
      console.warn("SCENARIO FETCH ERROR:", err?.message);
      setScenario(null);
    }
  }, [symbol]);

  useEffect(() => {
    fetchPrice();
    fetchScenario();

    const id = setInterval(() => {
      fetchPrice();
      fetchScenario();
    }, 30000);

    return () => clearInterval(id);
  }, [fetchPrice, fetchScenario]);

  const refresh = async () => {
    await Promise.all([
      fetchPrice(),
      fetchScenario()
    ]);
  };

  return {
    price,
    scenario,
    allPrices,
    loading,
    error,
    refresh
  };
}
