export type RemainingQuickWinState =
  | "loading"
  | "empty"
  | "stale"
  | "error"
  | "ready";

export interface RemainingQuickWinBinding {
  capabilityId: string;
  capabilityName: string;
  endpoint: string;
  screen: string;
  component: string;
  states: readonly RemainingQuickWinState[];
}
