# PR-004 Non-Canonical Local Component Edges

These local targets are represented in source evidence but are not members of the PR-003 canonical 13-service map.

- Edge count: `8`
- Runtime changes: `none`

| Source | Component | Port | Confidence | Evidence |
|---|---|---:|---|---|
| `ndsp-launch-control-v167` | `ndsp-platform-gateway-9001` | `9001` | `HIGH` | `backend/services/ndsp-launch-control-v167/server.py:41` |
| `ndsp-launch-control-v167` | `ndsp-register-compat-gateway` | `9028` | `HIGH` | `backend/services/ndsp-launch-control-v167/server.py:37` |
| `ndsp-layers-api` | `raw-cot-service` | `9076` | `HIGH` | `apps/ndsp-layers-api/app.py:289` |
| `ndsp-trial-clock-v163` | `ndsp-platform-gateway-9001` | `9001` | `HIGH` | `backend/services/ndsp-trial-clock-v163/server.py:25` |
| `ndsp-trial-clock-v163` | `ndsp-register-compat-gateway` | `9028` | `HIGH` | `backend/services/ndsp-trial-clock-v163/server.py:21` |
| `ndsp-trial-clock-v164` | `ndsp-platform-gateway-9001` | `9001` | `HIGH` | `backend/services/ndsp-trial-clock-v164/server.py:25` |
| `ndsp-trial-clock-v164` | `ndsp-register-compat-gateway` | `9028` | `HIGH` | `backend/services/ndsp-trial-clock-v164/server.py:21` |
| `ndsp-trial-register-canonical-wrapper` | `ndsp-trial-register-gateway` | `9019` | `HIGH` | `backend/ndsp-trial-register-canonical-wrapper/server.js:9` |
