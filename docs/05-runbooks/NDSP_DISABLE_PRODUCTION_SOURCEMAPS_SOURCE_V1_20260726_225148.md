============================================================
NDSP — DISABLE PRODUCTION SOURCEMAPS SOURCE V1
MODE=SOURCE_CONFIG_ATOMIC_REBUILD_PERMANENT_GATE
DATE=2026-07-26T22:51:49+02:00
SOURCE=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1
============================================================

== 1) Preconditions and backup ==
b60df47bbb4aab26b74906491593b26a3f20c15b7a7a7d8952ac8a2b408ba1c3  /home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1/vite.config.js
b71f00afdcfd73452eeed428903b47542f9ec205d33bd30d1bcba97093a0fa3d  /home/nawaf511/Downloads/ndsp_install_commercial_preview_no_nginx_v2.sh
BACKUP=/home/nawaf511/empire-core-new/backups/disable-production-sourcemaps-source-v1/20260726_225148
BACKUP_GATE=PASS
DIRECT_DIST_PATCH=NO
BACKEND_CHANGE_PLANNED=NO
NGINX_CHANGE_PLANNED=NO
SERVICE_RESTART_PLANNED=NO

== 2) Patch Vite source configuration ==
VITE_PATCH_ACTION=UPDATED_EXISTING_SOURCEMAP_SETTING
VITE_SOURCEMAP_POLICY=FALSE
VITE_SOURCE_PATCH_GATE=PASS

== 3) Add permanent installer no-map gate ==
INSTALLER_PATCH_ACTION=ADDED_INSTALLER_GATE
INSTALLER_SOURCEMAP_GATE=PASS
INSTALLER_BASH_SYNTAX_GATE=PASS

== 4) Refresh and verify source manifest ==
SOURCE_MANIFEST_FILE_COUNT=20
SOURCE_MANIFEST_REFRESH=PASS
SOURCE_MANIFEST_GATE=PASS

== 5) Atomic rebuild and preview installation ==
============================================================
NDSP — COMMERCIAL LIVE PREVIEW V2
MODE=PHYSICAL_SPA_ROUTES_NO_NGINX_CHANGE
DATE=2026-07-26T22:51:49+02:00
============================================================

== 1) Preconditions ==
PRECONDITION_GATE=PASS

== 2) Isolated source verification and build ==
SOURCE_LIVE_CONTRACT_GATE=PASS
FIXTURE=quality_eth_weekly.json
  price=1875.48
  activation=1775.67
  arrival=1630.48
  review=1937.77
  invalidation=2047.89
  time_horizon='متابعة كسر أسبوعي'
  decision_quality=84.0
  alignment=35.0
  confirmation=55.0
  macd=16.5561839611
  obv=14.680007
  cci=-54.612554
  usd=-5.327774
  blockers=1.0
FIXTURE=quality_btc_weekly.json
  price=64415.99
  activation=61652.96
  arrival=57634.0
  review=67902.8
  invalidation=69188.5
  time_horizon='متابعة كسر أسبوعي'
  decision_quality=87.0
  alignment=35.0
  confirmation=55.0
  macd=-28.6301257173
  obv=17.57139
  cci=-76.62275
  usd=-5.327774
  blockers=1.0
FIXTURE=quality_eth_15m.json
  price=1875.48
  activation=1877.18
  arrival=1879.65
  review=1871.2
  invalidation=1872.55
  time_horizon='متابعة اختراق 15 دقيقة'
  decision_quality=82.0
  alignment=82.0
  confirmation=55.0
  macd=0.221424832
  obv=19.308846
  cci=99.59919
  usd=-7.535293
  blockers=1.0
CANDLE_COUNT=100
CONTRACT_FIXTURE_GATE=PASS

> ndsp-user-portal-vite@1.0.0 build
> vite build

vite v6.4.3 building for production...
transforming...
✓ 28 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.62 kB │ gzip:  0.34 kB
dist/assets/index-DoraAm3r.css   42.66 kB │ gzip:  9.02 kB
dist/assets/index-BbNOtHX6.js   262.48 kB │ gzip: 80.44 kB
✓ built in 3.35s
PRODUCTION_SOURCEMAP_FILE_COUNT=0
PRODUCTION_SOURCEMAP_BUILD_GATE=PASS
BUILD_GATE=PASS
BUILT_JS=index-BbNOtHX6.js
BUILT_CSS=index-DoraAm3r.css

== 3) Create physical SPA route entrypoints ==
PHYSICAL_SPA_ROUTE_COUNT=19
PHYSICAL_SPA_ROUTE_GATE=PASS

== 4) Atomic preview installation ==
PREVIEW_INSTALL=PASS
NGINX_CHANGED=NO
NGINX_RELOADED=NO

== 5) Public route identity verification ==
ROOT_HTTP_CODE=200
ROOT_JS=/portal-commercial-preview/assets/index-BbNOtHX6.js
ROOT_CSS=/portal-commercial-preview/assets/index-DoraAm3r.css
ROUTE_PASS=command-center/
ROUTE_PASS=command-center
ROUTE_PASS=markets/
ROUTE_PASS=markets
ROUTE_PASS=prices-chart/
ROUTE_PASS=prices-chart
ROUTE_PASS=opportunities/
ROUTE_PASS=opportunities
ROUTE_PASS=decision-room/
ROUTE_PASS=decision-room
ROUTE_PASS=portfolio/
ROUTE_PASS=portfolio
ROUTE_PASS=scenarios/
ROUTE_PASS=scenarios
ROUTE_PASS=layers/
ROUTE_PASS=layers
ROUTE_PASS=risk/
ROUTE_PASS=risk
ROUTE_PASS=completed/
ROUTE_PASS=completed
ROUTE_PASS=data-health/
ROUTE_PASS=data-health
ROUTE_PASS=alerts/
ROUTE_PASS=alerts
ROUTE_PASS=guide/
ROUTE_PASS=guide
ROUTE_PASS=support/
ROUTE_PASS=support
ROUTE_PASS=account/
ROUTE_PASS=account
ROUTE_PASS=plans/
ROUTE_PASS=plans
ROUTE_PASS=settings/
ROUTE_PASS=settings
ROUTE_PASS=context/
ROUTE_PASS=context
ROUTE_PASS=trial-expired/
ROUTE_PASS=trial-expired
ROUTE_VARIANTS_TESTED=38
ALL_PREVIEW_ROUTES=PASS

== 6) Live API smoke check ==
QUALITY_LIVE_HTTP_CODE=200
QUALITY_SYMBOL=ETHUSDT
QUALITY_PRICE=1914.2
QUALITY_ACTIVATION=1,809.54
QUALITY_LIVE_SMOKE_GATE=PASS

FINAL_STATUS=NDSP_COMMERCIAL_LIVE_PREVIEW_V2_INSTALLED
PREVIEW_URL=https://my.ndsp.app/portal-commercial-preview/command-center/?lang=ar
CANONICAL_PORTAL_CHANGED=NO
NGINX_CHANGED=NO
BACKUP_STATE=/home/nawaf511/empire-core-new/backups/commercial-live-preview-no-nginx/20260726_225149

== 6) Verify current public bundle has no real source map ==
PUBLIC_JS=/portal-commercial-preview/assets/index-BbNOtHX6.js
MAP_HTTP_CODE=200
PUBLIC_MAP_ACTUAL=FALSE
PUBLIC_MAP_SOURCE_COUNT=0
PUBLIC_MAP_HAS_SOURCES_CONTENT=FALSE
PUBLIC_MAP_RESPONSE_IS_HTML=TRUE
PUBLIC_SOURCEMAP_CLOSURE_GATE=PASS

== 7) Final route and API closure gates ==
ROUTE_PASS=command-center FINAL_HTTP=200
ROUTE_PASS=markets FINAL_HTTP=200
ROUTE_PASS=prices-chart FINAL_HTTP=200
ROUTE_PASS=opportunities FINAL_HTTP=200
ROUTE_PASS=decision-room FINAL_HTTP=200
ROUTE_PASS=portfolio FINAL_HTTP=200
ROUTE_PASS=scenarios FINAL_HTTP=200
ROUTE_PASS=layers FINAL_HTTP=200
ROUTE_PASS=risk FINAL_HTTP=200
ROUTE_PASS=completed FINAL_HTTP=200
ROUTE_PASS=data-health FINAL_HTTP=200
ROUTE_PASS=alerts FINAL_HTTP=200
ROUTE_PASS=guide FINAL_HTTP=200
ROUTE_PASS=support FINAL_HTTP=200
ROUTE_PASS=account FINAL_HTTP=200
ROUTE_PASS=plans FINAL_HTTP=200
ROUTE_PASS=settings FINAL_HTTP=200
ROUTE_PASS=context FINAL_HTTP=200
ROUTE_PASS=trial-expired FINAL_HTTP=200
ALL_38_ROUTE_VARIANTS_ALREADY_ENFORCED_BY_INSTALLER=YES
TRIAL_HTTP=200
RAW_COT_HTTP=200
QUALITY_SPEC_HTTP=200
QUALITY_INV_HTTP=200
SPECULATIVE={'mode': 'speculative', 'score': 75.91, 'direction': 'bearish', 'status': 'CALCULATED_GOVERNED'}
INVESTMENT={'mode': 'investment', 'score': 64.34, 'direction': 'bullish', 'status': 'CALCULATED_GOVERNED'}
MODE_CONTRACT_GATE=PASS

COMMERCIAL_LAUNCH_READY=YES
FINAL_STATUS=PRODUCTION_SOURCEMAP_REMOVED_AND_LAUNCH_GATES_PASSED
SOURCE_CHANGED=YES:vite.config.js
INSTALLER_CHANGED=YES:permanent_no_map_gate
DIRECT_DIST_PATCH=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
SERVICE_RESTARTED=NO
BACKUP=/home/nawaf511/empire-core-new/backups/disable-production-sourcemaps-source-v1/20260726_225148
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_DISABLE_PRODUCTION_SOURCEMAPS_SOURCE_V1_20260726_225148.md
