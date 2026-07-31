export type CapabilityViewState =
  | "loading"
  | "empty"
  | "stale"
  | "error"
  | "ready";

export interface CriticalCapabilityBinding {
  capabilityId: string;
  capabilityName: string;
  screen: string;
  feature: string;
  endpoint: string | null;
  sourcePath: string;
  dataState: string;
  bindingStatus: "ENDPOINT_AVAILABLE" | "ENDPOINT_REQUIRED";
}

export interface CapabilityPayload {
  value: unknown;
  updatedAt?: string;
  stale?: boolean;
}
