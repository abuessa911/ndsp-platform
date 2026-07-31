# PR-003 Canonical Service Map — Final

## Governance status

`PR003_READY_FOR_COMMIT`

- Schema version: `1.3.0`
- Total accepted services: `13`
- Running services: `10`
- Source-only services: `3`
- Ambiguous services: `0`
- Owner: `nawaf511`
- Runtime owner: `nawaf511`

All runtime evidence was collected read-only.

No service was started, stopped, restarted, enabled, disabled, or reconfigured.

## Canonical services

| Service | Status | Entrypoint | PID | Listener | Systemd | Exposure |
|---|---|---|---|---|---|---|
| `bot-execution` | `RUNNING` | `backend/services/bot_execution/main.cjs` | 2497949 | `127.0.0.1:9080` | `ndsp-bot_execution.service` | `LOOPBACK_ONLY` |
| `completed-decision` | `RUNNING` | `backend/services/completed_decision/main.cjs` | 2499820 | `127.0.0.1:9078` | `ndsp-completed_decision.service` | `LOOPBACK_ONLY` |
| `decision-governance-core` | `RUNNING` | `backend/services/decision_governance_core/main.cjs` | 2498024 | `127.0.0.1:9079` | `ndsp-decision_governance_core.service` | `LOOPBACK_ONLY` |
| `ndsp-launch-control-v167` | `RUNNING` | `backend/services/ndsp-launch-control-v167/server.py` | 2978939 | `127.0.0.1:9090` | `—` | `LOOPBACK_ONLY` |
| `ndsp-layers-api` | `SOURCE_ONLY` | `apps/ndsp-layers-api/app.py` | — | `—` | `—` | `NONE` |
| `ndsp-live-decision-quality` | `RUNNING` | `backend/ndsp-live-decision-quality/server.py` | 2978652 | `127.0.0.1:9057` | `—` | `LOOPBACK_ONLY` |
| `ndsp-platform-backend` | `SOURCE_ONLY` | `backend/server.js` | — | `—` | `—` | `NONE` |
| `ndsp-trial-clock-v163` | `SOURCE_ONLY` | `backend/services/ndsp-trial-clock-v163/server.py` | — | `—` | `—` | `NONE` |
| `ndsp-trial-clock-v164` | `RUNNING` | `backend/services/ndsp-trial-clock-v164/server.py` | 2978938 | `127.0.0.1:9089` | `—` | `LOOPBACK_ONLY` |
| `ndsp-trial-register-canonical-wrapper` | `RUNNING` | `backend/ndsp-trial-register-canonical-wrapper/server.js` | 2498156 | `127.0.0.1:9041` | `—` | `LOOPBACK_ONLY` |
| `ndsp-trial-seats-api` | `RUNNING` | `backend/ndsp-trial-seats-api/server.js` | 2498136 | `127.0.0.1:9064` | `—` | `LOOPBACK_ONLY` |
| `ndsp-user-alert-channels` | `RUNNING` | `backend/ndsp-user-alert-channels/server.js` | 2498159 | `127.0.0.1:9062` | `—` | `LOOPBACK_ONLY` |
| `password-reset-gateway` | `RUNNING` | `backend/password_reset_gateway/server.js` | 2498041 | `127.0.0.1:9027` | `—` | `LOOPBACK_ONLY` |

## Closure decision

PR-003 establishes the canonical repository and runtime service map for the thirteen accepted service candidates.

Ten services have exact entrypoint, PID, and socket evidence.

Three services are explicitly accepted as source-only:

- `ndsp-layers-api` — `apps/ndsp-layers-api/app.py`
- `ndsp-platform-backend` — `backend/server.js`
- `ndsp-trial-clock-v163` — `backend/services/ndsp-trial-clock-v163/server.py`

No unresolved or ambiguous service remains.
