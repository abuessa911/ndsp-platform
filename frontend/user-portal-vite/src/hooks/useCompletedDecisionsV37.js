import { useCallback, useEffect, useState } from "react";

const ENDPOINTS = {
  current: "/api/completed-decisions",
  history: "/api/completed-decisions/history?limit=100",
  integrity: "/api/completed-decisions/history/integrity"
};

async function fetchJson(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);

  try {
    const response = await fetch(url, {
      signal: controller.signal,
      cache: "no-store",
      headers: { Accept: "application/json" }
    });

    if (!response.ok) {
      throw new Error(`${url}:HTTP_${response.status}`);
    }

    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

export function useCompletedDecisionsV37() {
  const [current, setCurrent] = useState(null);
  const [history, setHistory] = useState(null);
  const [integrity, setIntegrity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastLoadedAt, setLastLoadedAt] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);

    const settled = await Promise.allSettled([
      fetchJson(ENDPOINTS.current),
      fetchJson(ENDPOINTS.history),
      fetchJson(ENDPOINTS.integrity)
    ]);

    const failures = [];

    if (settled[0].status === "fulfilled") {
      setCurrent(settled[0].value);
    } else {
      failures.push(settled[0].reason?.message || "CURRENT_FETCH_FAILED");
    }

    if (settled[1].status === "fulfilled") {
      setHistory(settled[1].value);
    } else {
      failures.push(settled[1].reason?.message || "HISTORY_FETCH_FAILED");
    }

    if (settled[2].status === "fulfilled") {
      setIntegrity(settled[2].value);
    } else {
      failures.push(settled[2].reason?.message || "INTEGRITY_FETCH_FAILED");
    }

    if (failures.length) {
      setError(failures.join(" | "));
    }

    const currentPayload =
      settled[0].status === "fulfilled" ? settled[0].value : null;
    const historyPayload =
      settled[1].status === "fulfilled" ? settled[1].value : null;

    const currentDecisionTimes = Array.isArray(currentPayload?.decisions)
      ? currentPayload.decisions.map((decision) => decision?.generated_at)
      : [];

    const historyRecords = Array.isArray(historyPayload?.records)
      ? historyPayload.records
      : [];

    const fallbackTimes = historyRecords.flatMap((record) => [
      record?.captured_at,
      record?.decision?.generated_at
    ]);

    const authoritativeTimes = currentDecisionTimes.length
      ? currentDecisionTimes
      : fallbackTimes;

    const validTimes = authoritativeTimes
      .map((value) => {
        if (!value) return null;
        const date = new Date(value);
        return Number.isNaN(date.getTime()) ? null : date;
      })
      .filter(Boolean);

    setLastLoadedAt(
      validTimes.length
        ? new Date(Math.max(...validTimes.map((date) => date.getTime())))
        : null
    );
    setLoading(false);
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 60000);
    return () => clearInterval(id);
  }, [refresh]);

  return {
    current,
    history,
    integrity,
    loading,
    error,
    lastLoadedAt,
    refresh
  };
}

