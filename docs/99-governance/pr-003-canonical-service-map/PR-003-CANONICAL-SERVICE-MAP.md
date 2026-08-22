# PR-003 Canonical Service Map

## Governance status

`BLOCKED_PENDING_RUNTIME_VERIFICATION`

- Schema version: `1.1.0`
- Clean service candidates: `13`
- Candidates with direct listener evidence: `1`
- Confirmed canonical services: `0`

Backup, archive, documentation, and private-governance snapshot paths were excluded.

Systemd units are treated as launch evidence and not as independent services.

Referenced ports are not automatically classified as listener ports.

No process, database, proxy, or runtime component was changed.

## Service candidates

| Service | Entrypoint | Listener ports | Environment | Referenced ports | Systemd | Status |
|---|---|---|---|---|---|---|
| `bot-execution` | `backend/services/bot_execution/main.cjs` | TBD | — | 9078 | `backend/services/bot_execution/systemd/ndsp-bot_execution.service` | `PORT_VERIFICATION_REQUIRED` |
| `completed-decision` | `backend/services/completed_decision/main.cjs` | TBD | — | — | `backend/services/completed_decision/systemd/ndsp-completed_decision.service` | `PORT_VERIFICATION_REQUIRED` |
| `decision-governance-core` | `backend/services/decision_governance_core/main.cjs` | TBD | — | 9078 | `backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-launch-control-v167` | `backend/services/ndsp-launch-control-v167/server.py` | TBD | — | 9001, 9020, 9028 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-layers-api` | `apps/ndsp-layers-api/app.py` | TBD | — | 9057, 9076 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-live-decision-quality` | `backend/ndsp-live-decision-quality/server.py` | 9057 | — | — | `—` | `REVIEW_REQUIRED` |
| `ndsp-platform-backend` | `backend/server.js` | TBD | — | — | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-trial-clock-v163` | `backend/services/ndsp-trial-clock-v163/server.py` | TBD | — | 9001, 9028 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-trial-clock-v164` | `backend/services/ndsp-trial-clock-v164/server.py` | TBD | — | 9001, 9028 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-trial-register-canonical-wrapper` | `backend/ndsp-trial-register-canonical-wrapper/server.js` | TBD | — | 9019 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-trial-seats-api` | `backend/ndsp-trial-seats-api/server.js` | TBD | — | 9064 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `ndsp-user-alert-channels` | `backend/ndsp-user-alert-channels/server.js` | TBD | — | 9062 | `—` | `PORT_VERIFICATION_REQUIRED` |
| `password-reset-gateway` | `backend/password_reset_gateway/server.js` | TBD | — | 9027 | `—` | `PORT_VERIFICATION_REQUIRED` |

## Remaining verification

Each accepted service requires read-only evidence for:

1. Effective launch command.
2. Effective listening address and port.
3. Public, internal, or loopback-only exposure.
4. Process owner and business owner.
5. Upstream and downstream dependencies.

PR-003 remains blocked until these fields are confirmed.
