import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import type { AnalysisSelection, GovernedAnalysisContext } from "./types";

const STORAGE_KEY = "ndsp.governed-analysis-context.v1";

type AnalysisContextValue = {
  context: GovernedAnalysisContext | null;
  complete: boolean;
  setValidatedContext: (selection: AnalysisSelection, asOf: string | null) => void;
  clearContext: () => void;
};

const AnalysisContext = createContext<AnalysisContextValue | null>(null);

function loadStoredContext(): GovernedAnalysisContext | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<GovernedAnalysisContext>;
    if (
      !parsed.market ||
      !parsed.symbol ||
      !parsed.timeframe ||
      !parsed.analysisMode ||
      !parsed.presentationMode
    ) {
      return null;
    }
    return {
      market: String(parsed.market),
      symbol: String(parsed.symbol),
      timeframe: parsed.timeframe,
      analysisMode: parsed.analysisMode,
      presentationMode: parsed.presentationMode,
      asOf: parsed.asOf ? String(parsed.asOf) : null,
      generation: Number(parsed.generation || 1),
    } as GovernedAnalysisContext;
  } catch {
    return null;
  }
}

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const [context, setContext] = useState<GovernedAnalysisContext | null>(() => loadStoredContext());

  const persist = useCallback((next: GovernedAnalysisContext | null) => {
    if (typeof window === "undefined") return;
    if (!next) {
      window.sessionStorage.removeItem(STORAGE_KEY);
      return;
    }
    window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  }, []);

  const setValidatedContext = useCallback(
    (selection: AnalysisSelection, asOf: string | null) => {
      setContext((previous) => {
        const sameCalculationContext =
          previous?.market === selection.market &&
          previous?.symbol === selection.symbol &&
          previous?.timeframe === selection.timeframe &&
          previous?.analysisMode === selection.analysisMode;

        const next: GovernedAnalysisContext = {
          ...selection,
          asOf,
          generation: sameCalculationContext
            ? previous?.generation ?? 1
            : (previous?.generation ?? 0) + 1,
        };
        persist(next);
        return next;
      });
    },
    [persist],
  );

  const clearContext = useCallback(() => {
    persist(null);
    setContext(null);
  }, [persist]);

  const complete = Boolean(
    context?.market &&
      context?.symbol &&
      context?.timeframe &&
      context?.analysisMode &&
      context?.presentationMode,
  );

  const value = useMemo(
    () => ({ context, complete, setValidatedContext, clearContext }),
    [clearContext, complete, context, setValidatedContext],
  );

  return <AnalysisContext.Provider value={value}>{children}</AnalysisContext.Provider>;
}

export function useAnalysisContext(): AnalysisContextValue {
  const value = useContext(AnalysisContext);
  if (!value) throw new Error("useAnalysisContext must be used inside AnalysisProvider");
  return value;
}
