# PR-064 — Canonical Direction Engine Correction

Implements `delta = long - short`; neutral only when long equals short.

Integration is shadow-only at `POST /api/governance/direction/shadow`.
No official result write, UTC/effective-week change, deployment, restart,
or public EXPANDED exposure occurs in this PR.
