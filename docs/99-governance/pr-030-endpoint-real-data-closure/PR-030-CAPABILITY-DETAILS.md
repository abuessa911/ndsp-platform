# PR-030 — 20 Capability Endpoint and Data Details

| # | Capability | Missing | Declared contract | Service | Data source | Data state | Candidate routes |
|---:|---|---|---|---|---|---|---:|
| 1 | `CAP-4FF90CCC6DFE` — Tdl V2 Policy Admin | REAL_DATA | GET /policy | ndsp-governance-bridge.service | UNKNOWN | UNKNOWN | 10 |
| 2 | `CAP-8A9DD9B6E7D5` — Tdl V2 Policy Admin | REAL_DATA | GET /auth-debug | ndsp-governance-bridge.service | UNKNOWN | UNKNOWN | 10 |
| 3 | `CAP-15C56B60B4B0` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/logout | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 4 | `CAP-214521E6EBD1` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/login | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 5 | `CAP-242D8324FAD9` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/setup/skip | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 6 | `CAP-3A5ED3DB0C0D` — Risk Label | ENDPOINT | DISCOVERY_REQUIRED | ndsp-scenario-levels-adapter.service | UNKNOWN | REAL_LIVE | 10 |
| 7 | `CAP-3B89863B2015` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/setup/start | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 8 | `CAP-3D9086A829ED` — Ndsp Admin Ui Proxy | ENDPOINT | POST /api/admin-ui/action | ndsp-admin-ui-proxy.service | JSON | REAL_SNAPSHOT | 10 |
| 9 | `CAP-4B75FD38F852` — Ndsp Admin Ui Proxy | ENDPOINT | POST /api/admin-ui/alerts/test | ndsp-admin-ui-proxy.service | JSON | REAL_SNAPSHOT | 10 |
| 10 | `CAP-4FCAA631BA18` — Ndsp Admin Actions Bypass Old Middleware | ENDPOINT | POST /api/admin-actions/users/action | ndsp-admin-actions.service | JSON | REAL_SNAPSHOT | 10 |
| 11 | `CAP-644C81537AC6` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/status | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 12 | `CAP-6565FE804AF5` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/login/verify | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 13 | `CAP-8F78E58E5656` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/setup/confirm | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 14 | `CAP-98156F574B28` — Risk Warnings | ENDPOINT | DISCOVERY_REQUIRED | ndsp-scenario-levels-adapter.service | UNKNOWN | REAL_LIVE | 10 |
| 15 | `CAP-A61CF5BBAA01` — Ndsp Admin Ui Proxy | ENDPOINT | POST /api/admin-ui/alerts/channel | ndsp-admin-ui-proxy.service | JSON | REAL_SNAPSHOT | 10 |
| 16 | `CAP-C55DEBBD7CB7` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/disable | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 17 | `CAP-D054F1321201` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/setup/confirm-final | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 18 | `CAP-E6FFD507C6FA` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/setup/confirm-speakeasy | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 19 | `CAP-F139426B5341` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/setup | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
| 20 | `CAP-F56AB637F669` — Ndsp User Login Gateway | ENDPOINT | POST /api/auth/2fa/confirm | ndsp-user-login.service | JSON | REAL_SNAPSHOT | 10 |
