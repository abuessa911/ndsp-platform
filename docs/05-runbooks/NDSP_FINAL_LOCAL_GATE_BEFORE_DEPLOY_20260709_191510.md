# NDSP Final Local Gate Before Deploy
DATE=2026-07-09T19:15:10+02:00
PROJECT_DIR=/home/nawaf511/empire-core-new
APP_DIR=/home/nawaf511/empire-core-new/frontend/user-portal-vite

== 1) GIT STATUS ==
 M README.md
 M backend/auth_api/ndsp_platform_gateway_9001.cjs
 M backend/data/raw_cot/current_disaggregated_futures_only_f_disagg.txt
 M backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt
 M backend/data/raw_cot/raw_cot_manifest.json
 M backend/server.js
 M frontend/user-portal-vite/src/main.jsx
 M frontend/user-portal-vite/src/styles.css
?? NDSP_CODEX_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_PROMPT.txt
?? backend/auth_api/ndsp_register_compat_gateway.cjs
?? backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260703_222221.txt
?? backend/data/raw_cot/tff_futures_only_FinFutWk_20260703_222221.txt
?? backend/password_reset_gateway/run_password_reset_gateway.sh
?? backups/
?? docs/00-build-catalog/
?? docs/01-build-control-pack/
?? docs/02-execution-ready-pack/
?? docs/03-final-transition/
?? docs/04-legal/
?? docs/05-runbooks/
?? docs/06-decision-room-contracts/
?? docs/README.md
?? docs/README_NDSP_GOVERNANCE_ENTRYPOINT.md
?? scripts/

== 2) P1 OLD HTML MENU LINKS CHECK ==
OK: no old .html menu links.

== 3) P2 OLD CURRENT CLOCK CHECK ==
OK: no rejected current-clock timestamp formatter.

== 4) REFERENCE LEVELS PAYLOAD CHECK ==
442:async function fetchScenarioLevels(symbol) {
443:  const endpoint = `/api/scenario/levels?symbol=${encodeURIComponent(symbol)}`;
476:  const [scenarioPayload, setScenarioPayload] = useState(null);
492:    () => getReferenceLevels(scenarioPayload || price, tr.locale, tr.waitingData),
493:    [scenarioPayload, price, tr.locale, tr.waitingData]
523:    fetchScenarioLevels(symbol).then((payload) => {
OK: reference levels prefer scenario payload.

== 5) ADAPTER PRICE KEYS CHECK ==
OK: found activation_price
OK: found arrival_price
OK: found review_price
OK: found cancel_price
OK: found invalidation_price
OK: found nmp_price

== 6) FAKE LEVEL LITERAL CHECK ==
OK: no rejected fake hard-coded levels.

== 7) LOCAL BUILD ONLY ==

> ndsp-user-portal-vite@1.0.0 build
> vite build

vite v6.4.3 building for production...
transforming...
✓ 27 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.44 kB │ gzip:  0.33 kB
dist/assets/index-CB5D1TQG.css    8.81 kB │ gzip:  2.62 kB
dist/assets/index-BX9FubtP.js   169.72 kB │ gzip: 53.47 kB
✓ built in 2.27s

== 8) DIFF STAT ==
 frontend/user-portal-vite/src/main.jsx   | 919 ++++++++++++++++++++++++++++---
 frontend/user-portal-vite/src/styles.css | 451 ++++++++++++++-
 2 files changed, 1261 insertions(+), 109 deletions(-)

FINAL_STATUS=LOCAL_GATE_OK_READY_FOR_SAFE_DEPLOY
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_LOCAL_GATE_BEFORE_DEPLOY_20260709_191510.md
