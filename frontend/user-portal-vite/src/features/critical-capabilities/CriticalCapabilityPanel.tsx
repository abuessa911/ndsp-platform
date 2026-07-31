import { useEffect, useState } from "react";
import { loadCriticalCapability } from "./criticalCapabilityClient";
import type {
  CapabilityPayload,
  CapabilityViewState,
  CriticalCapabilityBinding,
} from "./types";

interface Props {
  binding: CriticalCapabilityBinding;
}

function inferState(payload: CapabilityPayload | null): CapabilityViewState {
  if (!payload) return "empty";
  if (payload.stale) return "stale";
  if (payload.value === null || payload.value === undefined) return "empty";
  if (Array.isArray(payload.value) && payload.value.length === 0) return "empty";
  return "ready";
}

export function CriticalCapabilityPanel({ binding }: Props) {
  const [state, setState] = useState<CapabilityViewState>("loading");
  const [payload, setPayload] = useState<CapabilityPayload | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    setState("loading");

    loadCriticalCapability(binding, controller.signal)
      .then((result) => {
        setPayload(result);
        setState(inferState(result));
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        setMessage(error instanceof Error ? error.message : "Unknown error");
        setState("error");
      });

    return () => controller.abort();
  }, [binding]);

  return (
    <article data-capability-id={binding.capabilityId} data-state={state}>
      <header>
        <span>{binding.screen}</span>
        <h2>{binding.capabilityName}</h2>
      </header>
      {state === "loading" && <p>Loading verified capability data…</p>}
      {state === "empty" && <p>No verified data is available.</p>}
      {state === "stale" && <p>Data is stale and awaiting refresh.</p>}
      {state === "error" && <p role="alert">{message}</p>}
      {state === "ready" && (
        <pre>{JSON.stringify(payload?.value, null, 2)}</pre>
      )}
      <footer>{binding.bindingStatus}</footer>
    </article>
  );
}
