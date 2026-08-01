# PR-033 — Real-Data Runtime Proof

This package closes the two remaining TDL v2 policy capabilities using an
isolated FastAPI runtime loaded from the real application source.

The proof establishes:

- the canonical router prefix and endpoint contracts,
- a non-empty policy snapshot from `read_tdl_v2_policy`,
- live, masked process-environment presence metadata,
- response structure, size, and SHA-256 evidence.

No production service is restarted. The temporary admin key and payload values
are never committed.
