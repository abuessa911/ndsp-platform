============================================================
NDSP — READING SEPARATION SOURCE V1.1
MODE=CANONICAL_COMPONENT_ALL_RELEVANT_PAGES_SOURCE_ONLY
DATE=2026-07-26T12:31:56+02:00
PROJECT=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1
============================================================

== 1) Strict preflight ==
2e316cda3f90c18bf3bc09bab25b985a61d526e50bd284862cc1761e033c8b97  /home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1/src/main.jsx
758d34fc2fda1b307abcae13b8237738f2922f1811a4e1de3a367bfcec8ab005  /home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1/src/styles.css
BACKUP=/home/nawaf511/empire-core-new/backups/reading-separation-source-v1-1/20260726_123156
BACKUP_GATE=PASS
BACKEND_PATCH_PLANNED=NO
NGINX_PATCH_PLANNED=NO
CANONICAL_PORTAL_PATCH_PLANNED=NO

== 2) Authoritative weekly mode contract gate ==
PUBLIC_WEEKLY_SPECULATIVE_HTTP=200
PUBLIC_WEEKLY_INVESTMENT_HTTP=200
PUBLIC_WEEKLY_SPECULATIVE={"direction": "bearish", "mode": "speculative", "scenario": "قراءة أسبوعي · ضغط هابط", "score": 75.91, "status": "CALCULATED_GOVERNED", "timeframe": "weekly"}
PUBLIC_WEEKLY_INVESTMENT={"direction": "bullish", "mode": "investment", "scenario": "قراءة أسبوعي · ضغط هابط", "score": 64.34, "status": "CALCULATED_GOVERNED", "timeframe": "weekly"}
AUTHORITATIVE_WEEKLY_MODE_CONTRACT_GATE=PASS

== 3) Build canonical source change ==
LAYERS_TDL_MULTILINE_ANCHOR=PASS
CANONICAL_READING_COMPONENT_REPLACEMENT=PASS
COMMAND_CENTER_TECHNICAL_HEADING=CLARIFIED
DECISION_ROOM_TECHNICAL_HEADING=CLARIFIED
TDL_LAYER_TECHNICAL_TEXT=CLARIFIED
MODE_CONTEXT_VISIBLE_USAGES=7
MODE_CONTEXT_VISIBLE_PAGES=command-center,prices-chart,decision-room,scenarios,layers,risk
READING_SEPARATION_CSS=CANONICAL
SOURCE_STAGE_GATE=PASS

== 4) Install staged source and run gates ==
READING_SEPARATION_SOURCE_GATE=PASS
PROHIBITED_WORD_GATE=PASS
SOURCE_LIVE_CONTRACT_GATE=PASS
SOURCE_GATE=PASS

== 5) Refresh source manifest ==
SOURCE_MANIFEST_FILE_COUNT=20
SOURCE_MANIFEST_REFRESH=PASS

== 6) Governed build and preview installation ==
============================================================
NDSP — COMMERCIAL LIVE PREVIEW V2
MODE=PHYSICAL_SPA_ROUTES_NO_NGINX_CHANGE
DATE=2026-07-26T12:32:04+02:00
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
dist/assets/index-BbNOtHX6.js   262.53 kB │ gzip: 80.47 kB │ map: 687.53 kB
✓ built in 4.28s
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
QUALITY_PRICE=1883.8
QUALITY_ACTIVATION=1,779.14
QUALITY_LIVE_SMOKE_GATE=PASS

FINAL_STATUS=NDSP_COMMERCIAL_LIVE_PREVIEW_V2_INSTALLED
PREVIEW_URL=https://my.ndsp.app/portal-commercial-preview/command-center/?lang=ar
CANONICAL_PORTAL_CHANGED=NO
NGINX_CHANGED=NO
BACKUP_STATE=/home/nawaf511/empire-core-new/backups/commercial-live-preview-no-nginx/20260726_123204

== 7) Post-install preview identity ==
PREVIEW_HTTP=200
PREVIEW_JS=/portal-commercial-preview/assets/index-BbNOtHX6.js
PREVIEW_CSS=/portal-commercial-preview/assets/index-DoraAm3r.css
PREVIEW_READING_SEPARATION_IDENTITY=PASS

FINAL_STATUS=NDSP_READING_SEPARATION_SOURCE_V1_1_INSTALLED
PREVIEW_URL=https://my.ndsp.app/portal-commercial-preview/command-center/?lang=ar&market=CRYPTO&symbol=BTCUSDT&timeframe=weekly&mode=speculative&readingseparationv11=20260726_123156
CHANGED_SOURCE_FILES=src/main.jsx,src/styles.css
MODE_CONTEXT_VISIBLE_USAGES=7
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
CANONICAL_PORTAL_CHANGED=NO
SERVICE_RESTARTED=NO
BACKUP=/home/nawaf511/empire-core-new/backups/reading-separation-source-v1-1/20260726_123156
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_READING_SEPARATION_SOURCE_V1_1_20260726_123156.md
