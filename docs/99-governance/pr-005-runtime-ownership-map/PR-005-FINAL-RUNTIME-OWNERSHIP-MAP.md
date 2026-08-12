# PR-005 Final Runtime Ownership Map

## Status

`FINAL`

- Canonical services: `13`
- Runtime changes: `none`
- Evidence basis: listener PID, `/proc`, process command line, working directory, cgroup and systemd properties.

## Ownership summary

- `RUNNING_DIRECTLY_MANAGED`: `7`
- `RUNNING_MANAGED_ALIAS`: `2`
- `RUNNING_SHARED_SUPERVISOR`: `2`
- `SOURCE_ONLY`: `2`

## Governance summary

- `ACCEPTED`: `10`
- `ACCEPTED_WITH_WARNING`: `3`

## Canonical map

| Service | Port | Supervisor | Unit | Ownership | Governance |
|---|---:|---|---|---|---|
| `bot-execution` | `9080` | `SYSTEMD` | `ndsp-bot_execution.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `completed-decision` | `9078` | `SYSTEMD` | `ndsp-completed_decision.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `decision-governance-core` | `9079` | `SYSTEMD` | `ndsp-decision_governance_core.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `ndsp-launch-control-v167` | `9090` | `PM2` | `pm2-nawaf511.service` | `RUNNING_SHARED_SUPERVISOR` | `ACCEPTED_WITH_WARNING` |
| `ndsp-layers-api` | `-` | `NONE` | `-` | `SOURCE_ONLY` | `ACCEPTED` |
| `ndsp-live-decision-quality` | `9057` | `SYSTEMD` | `ndsp-live-decision-quality.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `ndsp-platform-backend` | `9020` | `SYSTEMD` | `ndsp-user-login.service` | `RUNNING_MANAGED_ALIAS` | `ACCEPTED_WITH_WARNING` |
| `ndsp-trial-clock-v163` | `-` | `NONE` | `-` | `SOURCE_ONLY` | `ACCEPTED` |
| `ndsp-trial-clock-v164` | `9089` | `PM2` | `pm2-nawaf511.service` | `RUNNING_SHARED_SUPERVISOR` | `ACCEPTED_WITH_WARNING` |
| `ndsp-trial-register-canonical-wrapper` | `9041` | `SYSTEMD` | `ndsp-trial-register-canonical-wrapper.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `ndsp-trial-seats-api` | `9064` | `SYSTEMD` | `ndsp-trial-seats-api.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `ndsp-user-alert-channels` | `9062` | `SYSTEMD` | `ndsp-user-alert-channels.service` | `RUNNING_DIRECTLY_MANAGED` | `ACCEPTED` |
| `password-reset-gateway` | `9027` | `SYSTEMD` | `ndsp-password-reset.service` | `RUNNING_MANAGED_ALIAS` | `ACCEPTED` |

## Interpretation

- `RUNNING_DIRECTLY_MANAGED`: dedicated systemd ownership.
- `RUNNING_SHARED_SUPERVISOR`: entrypoint confirmed under shared PM2.
- `RUNNING_MANAGED_ALIAS`: runtime ownership confirmed with a different deployed unit name.
- `SOURCE_ONLY`: canonical source exists with no confirmed listener.
