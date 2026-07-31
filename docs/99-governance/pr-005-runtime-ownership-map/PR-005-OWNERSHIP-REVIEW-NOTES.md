# PR-005 Ownership Review Notes

## Scope

This appendix records accepted runtime ownership exceptions.

## `ndsp-launch-control-v167`

- Ownership: `RUNNING_SHARED_SUPERVISOR`
- Governance: `ACCEPTED_WITH_WARNING`
- Supervisor: `PM2`
- Unit: `pm2-nawaf511.service`
- Entrypoint: `python3 /home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/server.py`
- Working directory: `/home/nawaf511`
- Note: Runtime entrypoint confirmed; lifecycle is governed through the shared PM2 systemd supervisor.

## `ndsp-platform-backend`

- Ownership: `RUNNING_MANAGED_ALIAS`
- Governance: `ACCEPTED_WITH_WARNING`
- Supervisor: `SYSTEMD`
- Unit: `ndsp-user-login.service`
- Entrypoint: `/usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs`
- Working directory: `/home/nawaf511/empire-core-new/backend/auth_api`
- Note: Port 9020 is owned by ndsp-user-login.service running backend/auth_api/ndsp_user_login_gateway.cjs. The canonical service name and deployed unit name differ.

## `ndsp-trial-clock-v164`

- Ownership: `RUNNING_SHARED_SUPERVISOR`
- Governance: `ACCEPTED_WITH_WARNING`
- Supervisor: `PM2`
- Unit: `pm2-nawaf511.service`
- Entrypoint: `python3 /home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/server.py`
- Working directory: `/home/nawaf511`
- Note: Runtime entrypoint confirmed; lifecycle is governed through the shared PM2 systemd supervisor.
