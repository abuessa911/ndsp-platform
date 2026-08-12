import { useEffect, useState } from "react";
import type {
  RemainingQuickWinBinding,
  RemainingQuickWinState,
} from "./types";

interface Props {
  binding: RemainingQuickWinBinding;
}

export function RemainingQuickWinPanel({ binding }: Props) {
  const [state, setState] =
    useState<RemainingQuickWinState>("loading");
  const [payload, setPayload] = useState<unknown>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    setState("loading");

    fetch(binding.endpoint, {
      credentials: "include",
      headers: { Accept: "application/json" },
      signal: controller.signal,
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data: unknown = await response.json();
        setPayload(data);

        if (data === null || data === undefined) {
          setState("empty");
        } else if (Array.isArray(data) && data.length === 0) {
          setState("empty");
        } else {
          setState("ready");
        }
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        setMessage(
          error instanceof Error ? error.message : "Unknown error",
        );
        setState("error");
      });

    return () => controller.abort();
  }, [binding]);

  return (
    <article
      data-capability-id={binding.capabilityId}
      data-state={state}
    >
      <h2>{binding.capabilityName}</h2>
      {state === "loading" && <p>Loading…</p>}
      {state === "empty" && <p>No verified data is available.</p>}
      {state === "stale" && <p>Data is stale.</p>}
      {state === "error" && <p role="alert">{message}</p>}
      {state === "ready" && (
        <pre>{JSON.stringify(payload, null, 2)}</pre>
      )}
    </article>
  );
}
