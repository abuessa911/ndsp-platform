import type {
  CapabilityPayload,
  CriticalCapabilityBinding,
} from "./types";

export class CapabilityBindingError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CapabilityBindingError";
  }
}

export async function loadCriticalCapability(
  binding: CriticalCapabilityBinding,
  signal?: AbortSignal,
): Promise<CapabilityPayload> {
  if (!binding.endpoint) {
    throw new CapabilityBindingError(
      `No verified endpoint exists for ${binding.capabilityId}`,
    );
  }

  const response = await fetch(binding.endpoint, {
    credentials: "include",
    headers: { Accept: "application/json" },
    signal,
  });

  if (!response.ok) {
    throw new CapabilityBindingError(
      `${binding.capabilityId} returned HTTP ${response.status}`,
    );
  }

  const value: unknown = await response.json();
  const updatedAt =
    response.headers.get("last-modified") ??
    response.headers.get("date") ??
    undefined;

  return { value, updatedAt, stale: false };
}
