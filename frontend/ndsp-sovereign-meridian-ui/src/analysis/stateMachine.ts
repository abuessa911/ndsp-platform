import type {
  AnalysisSelection,
  CapabilityState,
  GovernedAnalysisContext,
} from "./types";

export type ResultLifecycleState =
  | "loading"
  | "unavailable"
  | "stale"
  | "blocked"
  | "partial"
  | "ready";

export function sameCalculationContext(
  previous: GovernedAnalysisContext | null,
  selection: AnalysisSelection,
): boolean {
  return Boolean(
    previous &&
      previous.market === selection.market &&
      previous.symbol === selection.symbol &&
      previous.timeframe === selection.timeframe &&
      previous.analysisMode === selection.analysisMode,
  );
}

export function buildNextGovernedContext(
  previous: GovernedAnalysisContext | null,
  selection: AnalysisSelection,
  asOf: string | null,
): GovernedAnalysisContext {
  const calculationUnchanged = sameCalculationContext(previous, selection);
  return {
    ...selection,
    asOf,
    generation: calculationUnchanged
      ? previous?.generation ?? 1
      : (previous?.generation ?? 0) + 1,
  };
}

export type ResultLifecycleInput = {
  loading: boolean;
  hasError: boolean;
  hasCoverage: boolean;
  globalRegistryReconciled: boolean;
  decisionReady: boolean;
  officialState?: string | null;
  capabilityStates: CapabilityState[];
};

export function deriveResultLifecycleState(
  input: ResultLifecycleInput,
): ResultLifecycleState {
  if (input.loading) return "loading";
  if (input.hasError || !input.hasCoverage) return "unavailable";

  if (input.capabilityStates.includes("STALE")) return "stale";

  if (!input.globalRegistryReconciled) return "blocked";

  // Contradictory upstream evidence must fail closed. A READY boolean may never
  // override an explicit BLOCKED official state or capability contribution.
  if (
    String(input.officialState || "").toUpperCase() === "BLOCKED" ||
    input.capabilityStates.includes("BLOCKED")
  ) {
    return "blocked";
  }

  if (input.decisionReady) return "ready";

  if (
    input.capabilityStates.includes("PARTIAL") ||
    input.capabilityStates.includes("UNAVAILABLE")
  ) {
    return "partial";
  }

  return "blocked";
}
