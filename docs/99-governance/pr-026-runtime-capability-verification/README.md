# PR-026 — Runtime Capability Verification

This package verifies all capability traceability records using read-only
repository and runtime evidence.

Safety boundaries:

- only local `GET` and `HEAD` HTTP requests are executed
- mutating HTTP methods are never executed
- services are never restarted or modified
- environment variable values are never read into artifacts
- ambiguous or missing evidence remains pending
- no capability is promoted to `UI_COMPLETE` automatically
