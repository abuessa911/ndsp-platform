# NDSP Optional API Loading Fix V56

- Date: 2026-07-16T11:05:18+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Portal: v50
- Mode: REMOVE_MISSING_SCENARIO_REQUEST_DEFER_PROTECTED_HISTORY_NO_AUTH_BYPASS
- Backup: /home/nawaf511/ndsp_launch_backups/fix_optional_api_loading_v56_20260716_110518
- Output: /home/nawaf511/ndsp_launch_reports/NDSP_FIX_OPTIONAL_API_LOADING_V56_20260716_110518
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_OPTIONAL_API_LOADING_V56_20260716_110518.md

== 1) Preserve protected public state ==
ROOT_STATUS=302
ROOT_LOCATION=https://www.ndsp.app/
LOGIN_STATUS=200
REGISTER_STATUS=200

== 2) Back up portal runtime and HTML aliases ==
BACKUP: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js
BACKUP: /var/www/ndsp-my/portal-v50/assets/ndsp-portal-v50.js
BACKUP: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/index.html
BACKUP: /var/www/ndsp-my/portal-v50/index.html
BACKUP: /var/www/ndsp-my/NDSP_Command_Center.html
BACKUP: /var/www/ndsp-my/analysis-center.html
BACKUP: /var/www/ndsp-my/asset-selector.html
BACKUP: /var/www/ndsp-my/command-center.html
BACKUP: /var/www/ndsp-my/completed-decisions-review.html
BACKUP: /var/www/ndsp-my/completed-decisions.html
BACKUP: /var/www/ndsp-my/dashboard.html
BACKUP: /var/www/ndsp-my/data-freshness.html
BACKUP: /var/www/ndsp-my/data-health.html
BACKUP: /var/www/ndsp-my/decision-center.html
BACKUP: /var/www/ndsp-my/decision-guide.html
BACKUP: /var/www/ndsp-my/decision-layers.html
BACKUP: /var/www/ndsp-my/decision-radar.html
BACKUP: /var/www/ndsp-my/decision-room.html
BACKUP: /var/www/ndsp-my/decision-support.html
BACKUP: /var/www/ndsp-my/governance.html
BACKUP: /var/www/ndsp-my/guide.html
BACKUP: /var/www/ndsp-my/market-assets.html
BACKUP: /var/www/ndsp-my/markets.html
BACKUP: /var/www/ndsp-my/my-watchlist.html
BACKUP: /var/www/ndsp-my/nmp.html
BACKUP: /var/www/ndsp-my/platform-capabilities.html
BACKUP: /var/www/ndsp-my/platform.html
BACKUP: /var/www/ndsp-my/portal-v50/capabilities/index.html
BACKUP: /var/www/ndsp-my/portal-v50/completed/index.html
BACKUP: /var/www/ndsp-my/portal-v50/data/index.html
BACKUP: /var/www/ndsp-my/portal-v50/decision/index.html
BACKUP: /var/www/ndsp-my/portal-v50/guide/index.html
BACKUP: /var/www/ndsp-my/portal-v50/home/index.html
BACKUP: /var/www/ndsp-my/portal-v50/index.html
BACKUP: /var/www/ndsp-my/portal-v50/layers/index.html
BACKUP: /var/www/ndsp-my/portal-v50/markets/index.html
BACKUP: /var/www/ndsp-my/portal-v50/risk/index.html
BACKUP: /var/www/ndsp-my/portal-v50/scenarios/index.html
BACKUP: /var/www/ndsp-my/portal-v50/selector/index.html
BACKUP: /var/www/ndsp-my/portal.html
BACKUP: /var/www/ndsp-my/radar.html
BACKUP: /var/www/ndsp-my/risk-governance.html
BACKUP: /var/www/ndsp-my/scenario-levels.html
ALIAS_HTML_COUNT=39

== 3) Patch route-scoped API loading ==
PATCHED_JS_SYNTAX=PASS
1:const OPTIONAL_API_LOADING_V56 = "NDSP_OPTIONAL_API_LOADING_V56";
329:async function fetchCompletedRecords(ctx){
423:  const content=`${pageHero(tx("completedTitle"),tx("completedDesc"))}<div class="infoBox" style="margin-bottom:16px">${protectedText}</div><section class="card"><div class="cardHead"><div><h2>${tx("completedTitle")}</h2><p>${lang==="ar"?"يعرض السجل القرارات المطابقة للسوق والأصل والفريم ونوع القراءة فقط.":"Only records matching the locked market, asset, timeframe and reading type are shown."}</p></div><button class="btn btnGold" id="loadProtectedHistory">${lang==="ar"?"تحميل السجل المحمي":"Load protected history"}</button></div><div id="completedRecordsState">${noData(lang==="ar"?"لم يتم طلب بيانات السجل المحمي بعد.":"Protected history has not been requested yet.")}</div></section>`;
425:  document.getElementById("loadProtectedHistory")?.addEventListener("click",async event=>{
430:    const payload=await fetchCompletedRecords(ctx);
UPDATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js
UPDATED: /var/www/ndsp-my/portal-v50/assets/ndsp-portal-v50.js

== 4) Break the portal module cache ==
CACHE_TOKEN=v56-20260716_110518

== 5) Static and public contract checks ==
HTTP 200: /analysis-center.html
HTTP 200: /portal.html
HTTP 200: /market-assets.html
HTTP 200: /decision-support.html
HTTP 200: /decision-layers.html
HTTP 200: /platform-capabilities.html
HTTP 200: /scenario-levels.html
HTTP 200: /risk-governance.html
HTTP 200: /completed-decisions.html
HTTP 200: /data-health.html
HTTP 200: /decision-guide.html
QUALITY_HTTP=200
QUALITY_JSON=YES
ASSETS_HTTP=200
ASSETS_JSON=YES
LAYERS_HTTP=200
LAYERS_JSON=YES
CAPABILITIES_HTTP=200
CAPABILITIES_JSON=YES

== 6) Locate Playwright ==
PLAYWRIGHT_NODE_MODULES=/home/nawaf511/playwright-tools/node_modules
PLAYWRIGHT_RESOLVE=PASS
CHROMIUM_AVAILABLE=YES

== 7) Comprehensive browser and network gate ==
BROWSER_JS_SYNTAX=PASS
PAGE_HOME=PASS HTTP=200 LOCKED=1 MARKER=home BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_MARKETS=PASS HTTP=200 LOCKED=1 MARKER=markets BAD_LINKS=0 NEW_CONTEXT_LINKS=56 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_DECISION=PASS HTTP=200 LOCKED=1 MARKER=decision BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_LAYERS=PASS HTTP=200 LOCKED=1 MARKER=layers BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_CAPABILITIES=PASS HTTP=200 LOCKED=1 MARKER=capabilities BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_SCENARIOS=PASS HTTP=200 LOCKED=1 MARKER=scenarios BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_RISK=PASS HTTP=200 LOCKED=1 MARKER=risk BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_COMPLETED=PASS HTTP=200 LOCKED=1 MARKER=completed BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=1
PAGE_DATA=PASS HTTP=200 LOCKED=1 MARKER=data BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PAGE_GUIDE=PASS HTTP=200 LOCKED=1 MARKER=guide BAD_LINKS=0 NEW_CONTEXT_LINKS=0 BAD_NEW_CONTEXT_LINKS=0 PROTECTED_BUTTON=0
PROTECTED_REQUESTS_BEFORE_CLICK=0
PROTECTED_HISTORY_STATUSES=401,401
PROTECTED_HISTORY_GATE=PASS
DESKTOP_DECISION=PASS
EXPECTED_PROTECTED_401_403_COUNT=0
UNEXPECTED_HTTP_ERROR_COUNT=0
REQUEST_FAILED_COUNT=0
PAGE_ERROR_COUNT=0
TRUE_CONSOLE_ERROR_COUNT=0
GENERIC_NETWORK_CONSOLE_COUNT=0
COMPREHENSIVE_GATE=PASS
ERROR: Missing successful browser result: PAGE_HOME=PASS
