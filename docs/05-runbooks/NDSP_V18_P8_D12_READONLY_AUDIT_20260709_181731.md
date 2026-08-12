# NDSP V18 P8 D12 Read-only Audit

DATE=2026-07-09T18:17:31+02:00
TASK=NDSP_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX
MODE=READ_ONLY_AUDIT

## Scope

This audit was limited to files available inside the current workspace at:

- `/home/nawaf511/empire-core-new`

No production file was edited during this phase.

## Current Source Resolution

Findings:

- `apps/NDSP_FRONTEND_SOURCE_OF_TRUTH.md` and `frontend/NDSP_FRONTEND_SOURCE_OF_TRUTH.md` still declare:
  - `apps/user-portal -> /var/www/ndsp-my`
- `apps/user-portal` is not an active frontend source in this workspace. It contains only:
  - `apps/user-portal/data/command-center-real.json`
- `frontend/user-portal.README_AFTER_VITE.txt` states the active source is:
  - `/home/nawaf511/empire-core-new/frontend/user-portal-vite`
- `deploy_frontend_from_apps.sh` still deploys from `apps/user-portal`, which conflicts with the Vite README.

Conclusion:

- The workspace contains a source-of-truth conflict.
- The only locally available editable frontend source for the member portal is `frontend/user-portal-vite`.
- The runtime file requested by the task is not present in the workspace.

## Runtime / Production Resolution

Requested runtime target:

- `/var/www/ndsp-my/approved-design/ndsp-full-ar-i18n-v18-d11.js`

Observed in this environment:

- `/var/www/ndsp-my` is not available in the current sandboxed workspace.
- `find /home/nawaf511 -name 'ndsp-full-ar-i18n-v18-d11.js'` did not surface a local editable copy inside the repository.
- The repository contains references to that path in prompts and runbooks, but not the file itself.

Conclusion:

- Runtime single-file patching against the requested D11 file cannot be executed from this workspace as-is.

## Available Frontend Source

Available portal source:

- `frontend/user-portal-vite/src/main.jsx`
- `frontend/user-portal-vite/src/styles.css`
- `frontend/user-portal-vite/src/hooks/useMarket.js`
- `frontend/user-portal-vite/src/pages/*`

Observed product shape:

- Single Vite app with one `dist/index.html`
- No local multi-page static source matching the production route list in the task
- No local `approved-design/` directory

## Design / UX Baseline

The available Vite portal already has:

- NDSP shell styling
- decision-radar visual block
- asset selector
- decision quality panel
- decision state panel
- visible engine cards
- completed decisions section

Missing or incomplete in the available source:

- persistent Arabic/English toggle
- mobile-only menu drawer for official production links
- full visible-text translation coverage
- explicit audit instrumentation for the 24 required decision-room checks
- route-complete static pages matching the requested production list

## Decision Path

Preferred path requested by the task:

- Source-level patch if the authoritative source is available

Audit decision:

- Proceed with a source-level patch only against `frontend/user-portal-vite`, because it is the only locally editable member-portal frontend source.
- Do not claim a production runtime fix for `/var/www/ndsp-my/approved-design/ndsp-full-ar-i18n-v18-d11.js` from this environment.

## Risks / Constraints

- Production runtime file unavailable in workspace
- `/var/www/ndsp-my` unavailable in workspace
- Source-of-truth documents are inconsistent
- The locally available Vite source does not fully match the production route contract named in the task

## Next Step

Patch the available source-level Vite portal without changing the visual identity:

- add deterministic i18n state with `localStorage`
- add a stable language toggle
- add a mobile-only menu button and drawer
- preserve current visual design direction
- generate backup, rollback script, build output, and final report
