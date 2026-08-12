# PR-006 Final Runtime Network Exposure Map

## Final status

`FINALIZED_WITH_OWNERSHIP_WARNINGS`

- Listener records: `79`
- Canonical listener records: `11`
- Wildcard-bound listener records: `16`
- Ownership-warning records: `42`
- Unresolved listener records: `0`
- Runtime changes: `none`

## Governance conclusion

All PR-005 canonical service listeners observed in this audit are restricted to loopback bindings.

Wildcard bindings were identified for host infrastructure, edge proxy, container infrastructure, and non-canonical application components. A wildcard binding is documented as network-bound but is not treated as proof of internet reachability without firewall, routing, and upstream network evidence.

Non-canonical NDSP application listeners are retained with ownership warnings. They require a future ownership decision but are not unresolved at the process or supervisor level.

## Ownership categories

- `CANONICAL_SERVICE`: `11`
- `CONTAINER_INFRASTRUCTURE`: `2`
- `DATA_INFRASTRUCTURE`: `4`
- `EDGE_PROXY`: `4`
- `HOST_INFRASTRUCTURE`: `16`
- `NON_CANONICAL_APPLICATION`: `42`

## Governance statuses

- `ACCEPTED`: `11`
- `ACCEPTED_EXTERNAL_DEPENDENCY`: `26`
- `ACCEPTED_WITH_OWNERSHIP_WARNING`: `42`

## Network-bound listeners

| Protocol | Binding | Port | Process | Unit | Canonical service | Category | Status |
|---|---|---:|---|---|---|---|---|
| `tcp` | `0.0.0.0` | `22` | `-` | `-` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `::` | `22` | `-` | `-` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `0.0.0.0` | `25` | `master` | `postfix@-.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `::` | `25` | `master` | `postfix@-.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `0.0.0.0` | `80` | `-` | `-` | `-` | `EDGE_PROXY` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `::` | `80` | `-` | `-` | `-` | `EDGE_PROXY` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `0.0.0.0` | `443` | `-` | `-` | `-` | `EDGE_PROXY` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `::` | `443` | `-` | `-` | `-` | `EDGE_PROXY` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `0.0.0.0` | `3000` | `node` | `pm2-nawaf511.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `*` | `3389` | `xrdp` | `xrdp.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `udp` | `0.0.0.0` | `5353` | `avahi-daemon` | `avahi-daemon.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `udp` | `::` | `5353` | `avahi-daemon` | `avahi-daemon.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `0.0.0.0` | `5433` | `docker-proxy` | `docker.service` | `-` | `CONTAINER_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `tcp` | `::` | `5433` | `docker-proxy` | `docker.service` | `-` | `CONTAINER_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `udp` | `::` | `34533` | `avahi-daemon` | `avahi-daemon.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |
| `udp` | `0.0.0.0` | `57534` | `avahi-daemon` | `avahi-daemon.service` | `-` | `HOST_INFRASTRUCTURE` | `ACCEPTED_EXTERNAL_DEPENDENCY` |

## Canonical service listeners

| Protocol | Binding | Port | Process | Unit | Canonical service | Category | Status |
|---|---|---:|---|---|---|---|---|
| `tcp` | `127.0.0.1` | `9020` | `node` | `ndsp-user-login.service` | `ndsp-platform-backend` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9027` | `node` | `ndsp-password-reset.service` | `password-reset-gateway` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9041` | `node` | `ndsp-trial-register-canonical-wrapper.service` | `ndsp-trial-register-canonical-wrapper` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9057` | `python3` | `ndsp-live-decision-quality.service` | `ndsp-live-decision-quality` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9062` | `node` | `ndsp-user-alert-channels.service` | `ndsp-user-alert-channels` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9064` | `node` | `ndsp-trial-seats-api.service` | `ndsp-trial-seats-api` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9078` | `node` | `ndsp-completed_decision.service` | `completed-decision` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9079` | `node` | `ndsp-decision_governance_core.service` | `decision-governance-core` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9080` | `node` | `ndsp-bot_execution.service` | `bot-execution` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9089` | `python3` | `pm2-nawaf511.service` | `ndsp-trial-clock-v164` | `CANONICAL_SERVICE` | `ACCEPTED` |
| `tcp` | `127.0.0.1` | `9090` | `python3` | `pm2-nawaf511.service` | `ndsp-launch-control-v167` | `CANONICAL_SERVICE` | `ACCEPTED` |

## Non-canonical application listeners

| Protocol | Binding | Port | Process | Unit | Canonical service | Category | Status |
|---|---|---:|---|---|---|---|---|
| `tcp` | `0.0.0.0` | `3000` | `node` | `pm2-nawaf511.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `8097` | `node` | `ndsp-news-ticker.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9001` | `node` | `ndsp-platform-gateway.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9002` | `python3` | `ndsp-platform-gateway-9002.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9017` | `node` | `ndsp-admin-actions.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9019` | `node` | `ndsp-trial-register.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9021` | `node` | `ndsp-user-dashboard.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9022` | `node` | `ndsp-api-compat.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9023` | `node` | `ndsp-admin-ui-proxy.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9024` | `node` | `ndsp-access-guard-9024.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9028` | `node` | `ndsp-register-compat-gateway.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9029` | `node` | `ndsp-registration-consent-v42.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9030` | `node` | `ndsp-access-guard-final.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9031` | `node` | `ndsp-admin-users-official.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9033` | `node` | `ndsp-live-market-adapter.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9034` | `node` | `ndsp-scenario-levels-adapter.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9044` | `node` | `ndsp-governance-bridge.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9047` | `python3` | `ndsp-portal-real-data-api.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9061` | `uvicorn` | `ndsp-decision-package-v1.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9065` | `uvicorn` | `ndsp-layers-api.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9066` | `python3` | `ndsp-ui-bridge-api.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9067` | `python3` | `ndsp-quality-live-golden-wrapper.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9068` | `python3` | `ndsp-admin-user-ops.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9069` | `uvicorn` | `ndsp-change-password-gateway.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9070` | `node` | `ndsp-trial-fingerprint-guard.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9074` | `uvicorn` | `ndsp-current-user-display.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9076` | `uvicorn` | `ndsp-raw-cot-gateway.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9077` | `node` | `ndsp-16-layers.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9081` | `node` | `ndsp-ctl-001-workspace-identity.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9082` | `python3` | `ndsp-quality-live-nmp-wrapper.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9083` | `python3` | `ndsp-v52-contract.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9084` | `python3` | `ndsp-v53-bridge.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9085` | `python3` | `ndsp-canonical-live-runtime-v30.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9086` | `python3` | `ndsp-canonical-live-runtime-v33.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9087` | `python3` | `ndsp-completed-decisions-evidence-v35.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9088` | `python3` | `ndsp-completed-decisions-history-v36.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9091` | `python3` | `pm2-nawaf511.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9092` | `python3` | `ndsp-public-summary-v548.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9093` | `python3` | `ndsp-v3-portal-gateway.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9094` | `python3` | `ndsp-business-ops.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `9095` | `python3` | `ndsp-market-data-bridge-v2.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |
| `tcp` | `127.0.0.1` | `19091` | `nsolid` | `ndsp-auth-core-clean.service` | `-` | `NON_CANONICAL_APPLICATION` | `ACCEPTED_WITH_OWNERSHIP_WARNING` |

## Scope

This map records runtime listener state, process ownership, supervisor evidence, and bind-address classification.

It does not modify services, firewall rules, proxy configuration, containers, routing, or application code.
