# NDSP V18 P8 D12 Arabic / Mobile / Decision Room Fix

DATE=2026-07-09T18:17:31+02:00
TASK=NDSP_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX

## Patch Mode

- PATCH_MODE=SOURCE_LEVEL
- ACTIVE_SOURCE=/home/nawaf511/empire-core-new/frontend/user-portal-vite
- RUNTIME_TARGET_REQUESTED=/var/www/ndsp-my/approved-design/ndsp-full-ar-i18n-v18-d11.js
- RUNTIME_TARGET_AVAILABLE_IN_WORKSPACE=NO

## Files Modified

- `frontend/user-portal-vite/src/main.jsx`
- `frontend/user-portal-vite/src/styles.css`
- `scripts/rollback/ndsp_v18_p8_d12_rollback_20260709_181731.sh`
- `docs/05-runbooks/NDSP_V18_P8_D12_READONLY_AUDIT_20260709_181731.md`
- `docs/05-runbooks/NDSP_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_20260709_181731.md`

## Backups

- BACKUP_DIR=`/home/nawaf511/empire-core-new/backups/NDSP_V18_P8_D12_20260709_181731`
- BACKUP_FILES:
  - `main.jsx.before`
  - `styles.css.before`

## Rollback Path

- ROLLBACK_SCRIPT=`/home/nawaf511/empire-core-new/scripts/rollback/ndsp_v18_p8_d12_rollback_20260709_181731.sh`

## Package Path

- PACKAGE_PATH=`/home/nawaf511/empire-core-new/frontend/user-portal-vite`

## What Was Patched

### Language Button

- Added stable `localStorage`-backed language state using `ndsp_lang`
- Arabic is the default
- Toggle is deterministic: `ar -> en -> ar -> en`
- No `MutationObserver` introduced
- Button label is fixed as `AR | EN` so it does not translate itself into a broken state
- Only one language button is rendered

### Translation Layer

- Added visible Arabic/English dictionary for the current source-level portal shell
- Covered visible labels for:
  - nav links
  - section headers
  - buttons
  - select label
  - titles
  - card copy
  - scenario labels
  - seals
  - data freshness copy
- Preserved asset symbols and allowed terms such as `NDSP`, `NMP`, `UTC`, and market symbols

### Mobile Menu

- Added a mobile-only menu button
- Added a drawer with official production links:
  - `/`
  - `/asset-selector.html`
  - `/market-assets.html`
  - `/decision-radar.html`
  - `/decision-support.html`
  - `/nmp.html`
  - `/decision-guide.html`
  - `/completed-decisions.html`
  - `/daily-brief.html`
  - `/settings.html`
  - `/login.html`
  - `/register.html`
  - `/admin.html`
- Desktop nav remains intact

### Decision Room Content Added To Available Source

- reference levels
- NMP
- governing scenario
- alternative scenarios
- beginner explanation
- professional explanation
- reading styles
- decision guide
- risk radar legend
- USD/Macro panel before objection panel
- data freshness with `UTC`
- state seals
- beginner default with professional toggle

## Language Result

- LANGUAGE_BUTTON_RESULT=LOCAL_SOURCE_OK
- Persistence logic implemented
- No refresh required in source code path
- Not deployed from this session

## Mobile Menu Result

- MOBILE_MENU_RESULT=LOCAL_SOURCE_OK
- Button is hidden on desktop and visible on small screens by CSS
- Drawer close/backdrop behavior implemented
- Not browser-smoke-tested because no browser/runtime toolchain is available in this environment

## Translation Result

- TRANSLATION_RESULT=LOCAL_SOURCE_SUBSTANTIAL_COVERAGE_ADDED
- ENGLISH_REMAINING_VISIBLE_ITEMS_IN_LOCAL_AR_MODE=0_REQUIRED_ITEMS
- INTENTIONAL_NON_TRANSLATED_ITEMS:
  - `AR | EN`
  - `NDSP`
  - `NMP`
  - `UTC`
  - market symbols such as `XAUUSD`, `BTCUSDT`, `ETHUSDT`, `EURUSD`, `USOIL`, `SPX`

## 24-Point Decision Room Audit

Local source after patch:

1. Decision unit completion radar: PRESENT
2. Reference levels activation/arrival/review/invalidation: PRESENT
3. NMP / Nawaf Meet Point: PRESENT
4. Governing scenario and alternative scenarios: PRESENT
5. Beginner explanation: PRESENT
6. Professional explanation: PRESENT
7. Reading styles investment/speculative: PRESENT
8. Decision guide: PRESENT
9. Markets page link: PRESENT
10. Assets page link: PRESENT
11. Section sequence through final stage: PRESENT
12. Completed decisions: PRESENT
13. Landing page link: PRESENT
14. Register page link: PRESENT
15. Login page link: PRESENT
16. Admin page link: PRESENT
17. Disclaimer / not financial advice / support only: PRESENT
18. Beginner default + advanced toggle: PRESENT
19. Risk Radar legend: PRESENT
20. USD/Macro panel before objection: PRESENT
21. Data freshness / last update / UTC: PRESENT
22. Completed / Under Monitoring / Caution seals: PRESENT
23. No Buy/Sell/LONG/SHORT/NO TRADE in patched source: PASS
24. No internal provider names in patched source: PASS

Live production over HTTP at audit time:

- Many URLs returned `HTTP 200`
- However `/approved-design/ndsp-full-ar-i18n-v18-d11.js` and protected asset URLs responded with the same HTML shell content instead of JS payloads
- Therefore live runtime integrity cannot be considered healthy solely from status code

## Forbidden Terms Result

Patched local source grep:

- `Buy`: 0
- `Sell`: 0
- `LONG`: 0
- `SHORT`: 0
- `NO TRADE`: 0
- `CFTC`: 0
- `FRED`: 0
- `Glassnode`: 0
- `CryptoQuant`: 0
- `TradingEconomics`: 0
- `Provider Manager`: 0
- `Failover Controller`: 0
- `Data Ingest`: 0
- `On-Chain Adapter`: 0
- `NDIP`: 0
- `Empire Core`: 0

## HTTP Result

Verified outside sandbox with live requests:

- `https://ndsp.app/` -> `200`
- `https://ndsp.app/asset-selector.html` -> `200`
- `https://ndsp.app/market-assets.html` -> `200`
- `https://ndsp.app/decision-radar.html` -> `200`
- `https://ndsp.app/decision-support.html` -> `200`
- `https://ndsp.app/nmp.html` -> `200`
- `https://ndsp.app/decision-guide.html` -> `200`
- `https://ndsp.app/completed-decisions.html` -> `200`
- `https://ndsp.app/login.html` -> `200`
- `https://ndsp.app/register.html` -> `200`
- `https://ndsp.app/admin.html` -> `200`
- `https://ndsp.app/approved-design/ndsp-full-ar-i18n-v18-d11.js` -> `200`

Important note:

- The D11 path above returned HTML shell content, not confirmed JS runtime content

## API Result

- `https://api.ndsp.app/api/health` -> `200`
- `https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT` -> `200`

## Protected Assets Checksums

Local filesystem under `/var/www/ndsp-my`:

- `/var/www/ndsp-my` not present in this workspace session
- Local checksum verification against filesystem copy: NOT_POSSIBLE

Remote HTTP payload hashes observed during audit:

- `https://ndsp.app/approved-design/ndsp-full-ar-i18n-v18-d11.js`
  - `sha256=8dcb99e7ed342250703ee352351a3970e41fc50dbf37ef7dfc08dd733f423df3`
- `https://ndsp.app/assets/ndsp-radar-safe-clean.js`
  - `sha256=8dcb99e7ed342250703ee352351a3970e41fc50dbf37ef7dfc08dd733f423df3`
- `https://ndsp.app/assets/ndsp-global-menu.js`
  - `sha256=8dcb99e7ed342250703ee352351a3970e41fc50dbf37ef7dfc08dd733f423df3`
- `https://ndsp.app/assets/ndsp-disclaimer-gate.js`
  - `sha256=8dcb99e7ed342250703ee352351a3970e41fc50dbf37ef7dfc08dd733f423df3`

Interpretation:

- All remote asset URLs above returned the same payload hash
- That payload is the HTML shell fallback, not distinct JS files
- Therefore protected runtime assets could not be confirmed as valid JS artifacts from the live surface

## Tests

Completed:

- source diff review
- local forbidden-terms scan
- remote HTTP status verification
- remote API status verification
- remote content sanity check showing HTML fallback on asset URLs

Not completed in this environment:

- `npm run build`
  - blocked because `node` / `npm` are not installed in this session
- Playwright / browser smoke
  - blocked because browser toolchain is unavailable here
- local `/var/www/ndsp-my` checksum verification
  - blocked because that path does not exist in this workspace session
- production deploy
  - not attempted from this session

## Outcome

- LOCAL_SOURCE_PATCH=COMPLETE
- PRODUCTION_RUNTIME_PATCH=NOT_EXECUTED
- DEPLOYMENT=NOT_EXECUTED
- RUNTIME_D11_FILE_IN_WORKSPACE=NO

## Remaining Items

1. The requested production runtime file `/var/www/ndsp-my/approved-design/ndsp-full-ar-i18n-v18-d11.js` is not available in this workspace, so the runtime single-file path could not be edited here.
2. The live asset endpoints currently behave like HTML fallback routes even when returning `HTTP 200`, so runtime asset validity remains unresolved.
3. Local build and browser verification could not run because `node`, `npm`, and browser tooling are absent from this environment.
4. Source-of-truth documentation is inconsistent between `apps/user-portal` and `frontend/user-portal-vite`.

FINAL_STATUS=V18_P8_D12_WITH_REMAINING_TRANSLATION_ITEMS
