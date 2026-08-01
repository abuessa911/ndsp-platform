# PR-036 — P0 Remediation Batches

This package decomposes the 391 PR-035 P0 capabilities into deterministic,
executable batches of at most 25 capabilities.

The first deliverable is a ranked top-50 list based on missing SERVICE,
ENDPOINT, and REAL_DATA evidence. The package then groups every P0 capability
by gap signature and records the remediation action and closure condition.

This PR is planning-only. It does not modify product code, Traceability, or
runtime.
