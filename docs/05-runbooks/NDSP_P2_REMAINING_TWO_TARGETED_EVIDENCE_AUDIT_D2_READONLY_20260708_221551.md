# NDSP P2 Remaining Two Targeted Evidence Audit D2 — Read-only
DATE=2026-07-08T22:15:51+02:00
MODE=READ_ONLY_TARGETED_EVIDENCE_AUDIT_D2
TARGETS=ndip-api-new.service,testapp.service
MODIFICATIONS=None
NO_STOP=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_RESTART=1
NO_REBOOT=1
ARTIFACT_DIR=/tmp/NDSP_P2_REMAINING_TWO_EVIDENCE_D2_20260708_221551

## 1) Runtime baseline
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m14.8%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.132mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.234mb/s[39m [90m/[39m [1m[33m82.05%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Current failed units
  UNIT                 LOAD   ACTIVE SUB    DESCRIPTION
● ndip-api-new.service loaded failed failed NDIP API - New Backend
● testapp.service      loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

2 loaded units listed.

---- SERVICE=ndip-api-new.service ----
DESCRIPTION=NDIP API - New Backend
ENABLED=disabled
ACTIVE=failed
FAILED=failed
FRAGMENT=/etc/systemd/system/ndip-api-new.service
RESULT=exit-code
EXEC_MAIN_STATUS=1
WORKING_DIRECTORY=/home/nawaf511/empire-core-new/backend

### UNIT_FILE_REDACTED
# /etc/systemd/system/ndip-api-new.service
[Unit]
Description=NDIP API - New Backend
After=network.target

[Service]
Type=simple
User=nawaf511
WorkingDirectory=/home/nawaf511/empire-core-new/backend
EnvironmentFile=/home/nawaf511/empire-core-new/backend/.env
ExecStart=/home/nawaf511/empire-core-new/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 9000
Restart=always
RestartSec=5
TimeoutStopSec=20
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/ndip-api-new.service.d/10-mt4-dir.conf
[Service]
Environment=NDIP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4
Environment=NDSP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4

### UNIT_EXEC_LINES
9:WorkingDirectory=/home/nawaf511/empire-core-new/backend
10:EnvironmentFile=/home/nawaf511/empire-core-new/backend/.env
11:ExecStart=/home/nawaf511/empire-core-new/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 9000
22:Environment=NDIP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4
23:Environment=NDSP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4

### RECENT_JOURNAL_REDACTED
-- No entries --

### PROJECT_REFERENCES
/home/nawaf511/empire-core-new/scripts/audit/ndsp_server_and_project_audit_EN.sh:76:  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
/home/nawaf511/empire-core-new/scripts/audit/ndsp_server_and_project_audit_AR.sh:76:  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
PROJECT_REFS_COUNT=2

### BROADER_PROJECT_REFERENCES
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:6:const PORT = Number(process.env.NDSP_PLATFORM_GATEWAY_PORT || 9001);
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:11:  { prefix: '/api/auth/', target: 'http://127.0.0.1:9020' },
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:13:  { prefix: '/api/trial/', target: 'http://127.0.0.1:9019' },
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:25:    'X-NDSP-Gateway': 'platform-9001'
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:53:      'x-ndsp-platform-gateway': '9001',
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:62:    headers['x-ndsp-gateway'] = 'platform-9001';
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:116:        platform_backend_port: 9001,
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:119:        legacy_services_behind_gateway: [9017, 9019, 9020, 9021]
/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:28:DATABASE_URL=postgresql://ndip_user:498e6aae274b0f3c57c0e1ec516741d7080cfce43221db69f6cb2630e2346055@localhost:5433/ndip
/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:29:NDIP_MT4_CSV_DIR=/home/nawaf511/ndip-backend/data/mt4
/home/nawaf511/empire-core-new/backend/ndsp_user_login_gateway.cjs:31:const PORT = Number(process.env.NDSP_USER_LOGIN_PORT || process.env.PORT || 9020)
/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:44:PORT="9001"
/home/nawaf511/empire-core-new/backend/runtime/private_governance/source_snapshot/ndsp_trial_register_gateway.cjs:49:const PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);
/home/nawaf511/empire-core-new/backend/runtime/private_governance/final_extra_snapshot/ndsp_trial_register_gateway.cjs:49:const PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);
/home/nawaf511/empire-core-new/backend/.env.bak.20260527_025723:8:PORT=9001
/home/nawaf511/empire-core-new/backend/migrations/001_postgres_core.sql:66:    source TEXT DEFAULT 'ndip',
/home/nawaf511/empire-core-new/backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260618_100847.txt:78:"SONAT - TIER 1 POOL (ZONE 0) - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233C1,IFED,01,023 ,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -8224,    9001,   -5705,    -890,    -300,     -85,   -2832,       0,       0,     133,       0,       0,    5327,   -6090,  -13551,   -2134,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"2500 mmbtu","0233C1","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260618_100847.txt:85:"TRANSCO ZONE 6 MONTHLY INDEX - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233CV,IFED,01,023 ,   92907,   34870,   88993,   57737,    1288,       0,       0,       0,       0,       0,       0,       0,   92607,   90281,     300,    2626,   92907,   34870,   88993,   57737,    1288,       0,       0,       0,       0,       0,       0,       0,   92607,   90281,     300,    2626,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -9308,   -6231,   -8874,   -2550,       0,       0,       0,       0,       0,       0,       0,       0,   -8781,   -8874,    -527,    -434,  100.0,   37.5,   95.8,   62.1,    1.4,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,   99.7,   97.2,    0.3,    2.8,  100.0,   37.5,   95.8,   62.1,    1.4,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,   99.7,   97.2,    0.3,    2.8,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     25,      9,     12,      4,.,      0,      0,      0,      0,      0,      0,      0,     13,     13,     25,      9,     12,      4,.,      0,      0,      0,      0,      0,      0,      0,     13,     13,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"mmbtu","0233CV","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/data/raw_cot/tff_futures_only_FinFutWk_20260618_100847.txt:22:"E-MINI S&P HEALTH CARE INDEX - CHICAGO MERCANTILE EXCHANGE",260609,2026-06-09,13874E,CME ,00,138 ,   22690,    8500,   19019,      21,   10471,       0,       0,    1046,    2372,       0,       0,       0,       0,   20038,   21412,    2652,    1278,     677,    1359,     327,       1,    -581,       0,       0,     328,     243,       0,       0,       0,       0,    1107,     571,    -430,     106,  100.0,   37.5,   83.8,    0.1,   46.1,    0.0,    0.0,    4.6,   10.5,    0.0,    0.0,    0.0,    0.0,   88.3,   94.4,   11.7,    5.6,     27,      7,      5,.,     10,      0,      0,.,.,      0,      0,      0,      0,     21,      7,    47.5,    83.6,    68.1,    94.4,    47.5,    83.6,    68.1,    94.3,"($100 x S&P Select Sector Health Care Index price)","13874E","CME ","138 ","F20","FutOnly"
/home/nawaf511/empire-core-new/backend/data/raw_cot/tff_futures_only_FinFutWk_20260618_100847.txt:58:"10 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE",260609,2026-06-09,343603,CBT ,00,343 ,  257039,   28375,   10683,   37215,   18157,    9021,       0,    7235,  136968,   27088,  138857,   35930,     112,  257039,  257017,       0,      22,   10389,    1190,     417,    3151,    2690,     730,       0,     -35,    3706,   -1500,   84681,   26320,     112,   90289,   32936,  -79900,  -22547,  100.0,   11.0,    4.2,   14.5,    7.1,    3.5,    0.0,    2.8,   53.3,   10.5,   54.0,   14.0,    0.0,  100.0,  100.0,    0.0,    0.0,     57,      6,      4,      4,      5,.,      0,.,      8,.,     22,      6,.,     39,     25,    43.2,    73.8,    66.8,    91.8,    37.6,    62.8,    53.5,    73.3,"(100,000 USD notional principal)","343603","CBT ","343 ","F50","FutOnly"
/home/nawaf511/empire-core-new/backend/ndsp-trial-register-canonical-wrapper/server.js:9:const UPSTREAM = process.env.NDSP_REGISTER_UPSTREAM || "http://127.0.0.1:9019";
/home/nawaf511/empire-core-new/backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp-trial-register-canonical-wrapper/server.js:9:const UPSTREAM = process.env.NDSP_REGISTER_UPSTREAM || "http://127.0.0.1:9019";
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.json:690:      "score": 0.4902885,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.json:703:      "score": 0.4902885,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.json:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.txt:690:      "score": 0.4902885,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.txt:703:      "score": 0.4902885,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.txt:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-raw-cot-gateway/.venv/lib64/python3.12/site-packages/pip/_vendor/certifi/cacert.pem:3781:# Serial: 156256931880233212765902055439220583700
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-raw-cot-gateway/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/_cell_widths.py:168:    (9001, 9002, 2),
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-raw-cot-gateway/.venv/lib/python3.12/site-packages/pip/_vendor/certifi/cacert.pem:3781:# Serial: 156256931880233212765902055439220583700
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-raw-cot-gateway/.venv/lib/python3.12/site-packages/pip/_vendor/rich/_cell_widths.py:168:    (9001, 9002, 2),
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-layers-api/.venv/lib64/python3.12/site-packages/pip/_vendor/certifi/cacert.pem:3781:# Serial: 156256931880233212765902055439220583700
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-layers-api/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/_cell_widths.py:168:    (9001, 9002, 2),
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-layers-api/.venv/lib/python3.12/site-packages/pip/_vendor/certifi/cacert.pem:3781:# Serial: 156256931880233212765902055439220583700
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-layers-api/.venv/lib/python3.12/site-packages/pip/_vendor/rich/_cell_widths.py:168:    (9001, 9002, 2),
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260618_100847.txt:78:"SONAT - TIER 1 POOL (ZONE 0) - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233C1,IFED,01,023 ,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -8224,    9001,   -5705,    -890,    -300,     -85,   -2832,       0,       0,     133,       0,       0,    5327,   -6090,  -13551,   -2134,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"2500 mmbtu","0233C1","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260618_100847.txt:85:"TRANSCO ZONE 6 MONTHLY INDEX - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233CV,IFED,01,023 ,   92907,   34870,   88993,   57737,    1288,       0,       0,       0,       0,       0,       0,       0,   92607,   90281,     300,    2626,   92907,   34870,   88993,   57737,    1288,       0,       0,       0,       0,       0,       0,       0,   92607,   90281,     300,    2626,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -9308,   -6231,   -8874,   -2550,       0,       0,       0,       0,       0,       0,       0,       0,   -8781,   -8874,    -527,    -434,  100.0,   37.5,   95.8,   62.1,    1.4,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,   99.7,   97.2,    0.3,    2.8,  100.0,   37.5,   95.8,   62.1,    1.4,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,   99.7,   97.2,    0.3,    2.8,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     25,      9,     12,      4,.,      0,      0,      0,      0,      0,      0,      0,     13,     13,     25,      9,     12,      4,.,      0,      0,      0,      0,      0,      0,      0,     13,     13,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"mmbtu","0233CV","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/current_disaggregated_futures_only_f_disagg.txt:78:"SONAT - TIER 1 POOL (ZONE 0) - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233C1,IFED,01,023 ,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -8224,    9001,   -5705,    -890,    -300,     -85,   -2832,       0,       0,     133,       0,       0,    5327,   -6090,  -13551,   -2134,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"2500 mmbtu","0233C1","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/current_disaggregated_futures_only_f_disagg.txt:85:"TRANSCO ZONE 6 MONTHLY INDEX - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233CV,IFED,01,023 ,   92907,   34870,   88993,   57737,    1288,       0,       0,       0,       0,       0,       0,       0,   92607,   90281,     300,    2626,   92907,   34870,   88993,   57737,    1288,       0,       0,       0,       0,       0,       0,       0,   92607,   90281,     300,    2626,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -9308,   -6231,   -8874,   -2550,       0,       0,       0,       0,       0,       0,       0,       0,   -8781,   -8874,    -527,    -434,  100.0,   37.5,   95.8,   62.1,    1.4,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,   99.7,   97.2,    0.3,    2.8,  100.0,   37.5,   95.8,   62.1,    1.4,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,   99.7,   97.2,    0.3,    2.8,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     25,      9,     12,      4,.,      0,      0,      0,      0,      0,      0,      0,     13,     13,     25,      9,     12,      4,.,      0,      0,      0,      0,      0,      0,      0,     13,     13,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,    75.9,    76.5,    96.4,    93.1,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"mmbtu","0233CV","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt:22:"E-MINI S&P HEALTH CARE INDEX - CHICAGO MERCANTILE EXCHANGE",260609,2026-06-09,13874E,CME ,00,138 ,   22690,    8500,   19019,      21,   10471,       0,       0,    1046,    2372,       0,       0,       0,       0,   20038,   21412,    2652,    1278,     677,    1359,     327,       1,    -581,       0,       0,     328,     243,       0,       0,       0,       0,    1107,     571,    -430,     106,  100.0,   37.5,   83.8,    0.1,   46.1,    0.0,    0.0,    4.6,   10.5,    0.0,    0.0,    0.0,    0.0,   88.3,   94.4,   11.7,    5.6,     27,      7,      5,.,     10,      0,      0,.,.,      0,      0,      0,      0,     21,      7,    47.5,    83.6,    68.1,    94.4,    47.5,    83.6,    68.1,    94.3,"($100 x S&P Select Sector Health Care Index price)","13874E","CME ","138 ","F20","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt:58:"10 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE",260609,2026-06-09,343603,CBT ,00,343 ,  257039,   28375,   10683,   37215,   18157,    9021,       0,    7235,  136968,   27088,  138857,   35930,     112,  257039,  257017,       0,      22,   10389,    1190,     417,    3151,    2690,     730,       0,     -35,    3706,   -1500,   84681,   26320,     112,   90289,   32936,  -79900,  -22547,  100.0,   11.0,    4.2,   14.5,    7.1,    3.5,    0.0,    2.8,   53.3,   10.5,   54.0,   14.0,    0.0,  100.0,  100.0,    0.0,    0.0,     57,      6,      4,      4,      5,.,      0,.,      8,.,     22,      6,.,     39,     25,    43.2,    73.8,    66.8,    91.8,    37.6,    62.8,    53.5,    73.3,"(100,000 USD notional principal)","343603","CBT ","343 ","F50","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/tff_futures_only_FinFutWk_20260618_100847.txt:22:"E-MINI S&P HEALTH CARE INDEX - CHICAGO MERCANTILE EXCHANGE",260609,2026-06-09,13874E,CME ,00,138 ,   22690,    8500,   19019,      21,   10471,       0,       0,    1046,    2372,       0,       0,       0,       0,   20038,   21412,    2652,    1278,     677,    1359,     327,       1,    -581,       0,       0,     328,     243,       0,       0,       0,       0,    1107,     571,    -430,     106,  100.0,   37.5,   83.8,    0.1,   46.1,    0.0,    0.0,    4.6,   10.5,    0.0,    0.0,    0.0,    0.0,   88.3,   94.4,   11.7,    5.6,     27,      7,      5,.,     10,      0,      0,.,.,      0,      0,      0,      0,     21,      7,    47.5,    83.6,    68.1,    94.4,    47.5,    83.6,    68.1,    94.3,"($100 x S&P Select Sector Health Care Index price)","13874E","CME ","138 ","F20","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/tff_futures_only_FinFutWk_20260618_100847.txt:58:"10 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE",260609,2026-06-09,343603,CBT ,00,343 ,  257039,   28375,   10683,   37215,   18157,    9021,       0,    7235,  136968,   27088,  138857,   35930,     112,  257039,  257017,       0,      22,   10389,    1190,     417,    3151,    2690,     730,       0,     -35,    3706,   -1500,   84681,   26320,     112,   90289,   32936,  -79900,  -22547,  100.0,   11.0,    4.2,   14.5,    7.1,    3.5,    0.0,    2.8,   53.3,   10.5,   54.0,   14.0,    0.0,  100.0,  100.0,    0.0,    0.0,     57,      6,      4,      4,      5,.,      0,.,      8,.,     22,      6,.,     39,     25,    43.2,    73.8,    66.8,    91.8,    37.6,    62.8,    53.5,    73.3,"(100,000 USD notional principal)","343603","CBT ","343 ","F50","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/nmp-lab/results/NDIP_MT4_CANDLES_ETHUSD_M30_nmp_lab_summary.csv:54:ROC14,open,2,1.0,0.5,0.5,3.84295,0.4902885
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/nmp-lab/results/NDIP_MT4_CANDLES_ETHUSD_M30_nmp_lab_summary.csv:55:MOM14,open,2,1.0,0.5,0.5,3.84295,0.4902885
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/nmp-lab/results/NDIP_MT4_CANDLES_ETHUSD_M30_nmp_lab_summary.csv:74:PRICE_BODY_ATR,open,2,1.0,0.5,1.0,0.5004,0.29001199999999994
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/migrations/001_postgres_core.sql:66:    source TEXT DEFAULT 'ndip',
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:6:const PORT = Number(process.env.NDSP_PLATFORM_GATEWAY_PORT || 9001);
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:11:  { prefix: '/api/auth/', target: 'http://127.0.0.1:9020' },
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:13:  { prefix: '/api/trial/', target: 'http://127.0.0.1:9019' },
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:25:    'X-NDSP-Gateway': 'platform-9001'
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:53:      'x-ndsp-platform-gateway': '9001',
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:62:    headers['x-ndsp-gateway'] = 'platform-9001';
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:116:        platform_backend_port: 9001,
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:119:        legacy_services_behind_gateway: [9017, 9019, 9020, 9021]
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_user_login_gateway.cjs:31:const PORT = Number(process.env.NDSP_USER_LOGIN_PORT || process.env.PORT || 9020)
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_trial_fingerprint_guard_proxy.cjs:9:const TARGET_PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_trial_register_gateway.cjs:49:const PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);
/home/nawaf511/empire-core-new/backend/ndsp_trial_register_gateway.cjs:49:const PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);
/home/nawaf511/empire-core-new/backend/architecture/registry/SERVICE_REGISTRY_V2.md:9:| SRV-001 | Auth Service | 9020 | NDSP Platform | Active |
/home/nawaf511/empire-core-new/backend/architecture/registry/SERVICE_REGISTRY_V2.md:10:| SRV-002 | Trial Service | 9019 | NDSP Platform | Active |
/home/nawaf511/empire-core-new/backend/architecture/registry/SERVICE_REGISTRY_V2.md:11:| SRV-003 | Platform Gateway | 9001 | NDSP Platform | Active |
/home/nawaf511/empire-core-new/backend/architecture/DEPLOYMENT_ARCHITECTURE.md:14:- 127.0.0.1:9001 Platform Gateway
/home/nawaf511/empire-core-new/backend/architecture/DEPLOYMENT_ARCHITECTURE.md:15:- 127.0.0.1:9019 Trial Service
/home/nawaf511/empire-core-new/backend/architecture/DEPLOYMENT_ARCHITECTURE.md:16:- 127.0.0.1:9020 Auth Service
/home/nawaf511/empire-core-new/backend/_archive_safe_cleanup_20260627_214310/server.jsy:27:const PORT = Number(process.env.PORT || 9001);
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/pip/_vendor/certifi/cacert.pem:4477:# Serial: 156256931880233212765902055439220583700
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/pip/_vendor/rich/_cell_widths.py:176:    (9001, 9002, 2),
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/ecdsa/ecdsa.py:850:    925BE9FB01AFC6FB4D3E7D4990010F813408AB106C4F09CB7EE07868CC136F
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/ecdsa/test_pyecdsa.py:2464:                "230E18E1BCC88A362FA54E4EA3902009292F7F8033624FD471B5D8ACE49"
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/curl_cffi/requests/impersonate.py:341:    # 19019-23129:"Unassigned
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/psycopg2/_range.py:351:        if conn.info.server_version < 90200:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/psycopg2/errorcodes.py:301:INVALID_SQLSTATE_RETURNED = '39001'
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/test_umath_complex.py:384:            0.35812203996480685 + 0.6097119028618724j,
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/test_umath_complex.py:404:            0.35812203996480685 + 0.6097119028618724j,
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-tanh.csv:1084:np.float64,0xbfed290014fa5200,0xbfe71871f7e859ed,2
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cos.csv:1089:np.float64,0xbfd030e2902061c6,0x3feefb3f811e024f,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cos.csv:1299:np.float64,0xffccbc9728397930,0x3fc53cbc59020704,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arcsinh.csv:1325:np.float64,0x7fe16c6c7ea2d8d8,0x40862ef18d90201f,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arccos.csv:1040:np.float64,0x3fe061291160c252,0x3ff0890010199bbc,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:886:np.float64,0x355be5fc6ab7e,0xc090010ca315b50b,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:900:np.float64,0x30c6c2ae618d9,0xc09001914b30381b,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:915:np.float64,0x324e59ce649cc,0xc0900163ad091c76,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:995:np.float64,0x33fe2b0667fc6,0xc0900132f3fab55e,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:1092:np.float64,0x340d1e6a681a5,0xc09001314b68a0a2,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:1095:np.float64,0x329a0e9e65343,0xc090015b044e3270,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:1373:np.float64,0x3fe2c79f80a58f3f,0xbfe89ac33f990289,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:1403:np.float64,0x2d9c65925b38e,0xc09001f46bcd3bc5,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:1460:np.float64,0x34159bc2682b4,0xc09001305a885f94,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv:1565:np.float64,0x2d78ec5a5af1e,0xc09001f8ea8601e0,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log1p.csv:1139:np.float64,0x80cad1b90195a,0x80cad1b90195a,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log10.csv:805:np.float32,0x3f5dbdc9,0xbd7f9019,4
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-expm1.csv:856:np.float64,0x3fee8c48ae7d1892,0x3ff9902899480526,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-expm1.csv:922:np.float64,0xbfe4800b11e90016,0xbfde4648c6f29ce5,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-exp2.csv:760:np.float64,0x7fcc81073d39020d,0x7ff0000000000000,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-sin.csv:1023:np.float64,0x3fe3f9a61ae7f34c,0x3fe2b3f701b79028,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cosh.csv:906:np.float64,0x7fb4800c4a290018,0x7ff0000000000000,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cosh.csv:1262:np.float64,0xbfe48e5728e91cae,0x3ff36a9020bf9d20,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arctanh.csv:383:np.float32,0x3f28bc48,0x3f4a9019,2
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arctanh.csv:460:np.float32,0xbf091018,0xbf190208,2
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arcsin.csv:486:np.float32,0xbe576138,0xbe590012,4
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-tan.csv:962:np.float64,0x800c810250d90205,0x800c810250d90205,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-tan.csv:1304:np.float64,0x1a90209e35205,0x1a90209e35205,1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/typing/tests/data/fail/random.pyi:59:np.random.Generator(12333283902830213)  # type: ignore[arg-type]
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/lib/_nanfunctions_impl.py:1839:        # so this used to work by serendipity.
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/test_random.py:1019:        desired = np.array([[2.28567572673902042, 2.89163838442285037],
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/test_random.py:1087:        desired = np.array([2.2129019979039612,
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/pcg64dxsm-testset-2.csv:424:422, 0x911210e154690191
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/philox-testset-2.csv:299:297, 0xbac15d1190014aad
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/pcg64-testset-2.csv:80:78, 0xf2edf9019a8fd343
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/pcg64-testset-2.csv:703:701, 0x3b900172045e25d
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/sfc64-testset-1.csv:369:367, 0x127d756ca4779001
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/pcg64-testset-1.csv:110:108, 0x5d4d9eda16e90286
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/philox-testset-1.csv:88:86, 0x5af2d239ff9028b1
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/philox-testset-1.csv:635:633, 0xf05a9b1900174c18
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/data/mt19937-testset-2.csv:374:372, 0x9001724a
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/test_randomstate.py:1265:        desired = np.array([[2.28567572673902042, 2.89163838442285037],
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/test_randomstate.py:1344:        desired = np.array([2.2129019979039612,
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/random/tests/test_generator_mt19937.py:1321:        desired = np.array([[ 5.03850858902096,  7.9228656732049 ],  # noqa: E202
BROADER_PROJECT_REFS_COUNT=131

### NGINX_REFERENCES
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:9:# - Platform backend: 127.0.0.1:9001
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:19:    server 127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:177:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:99:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:77:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:77:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:150:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:159:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:168:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:54:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:86:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:98:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:110:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:86:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:98:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:110:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:63:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:75:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:87:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:33:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:46:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:219:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:232:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:110:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:123:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:364:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:377:        proxy_pass http://127.0.0.1:9028/api/auth/register;
NGINX_REFS_COUNT=61

### PATH_EXISTENCE_FROM_UNIT
PATH_OK=/home/nawaf511/empire-core-new/backend TYPE=directory OWNER=nawaf511 GROUP=nawaf511 MODE=drwxr-xr-x
PATH_OK=/home/nawaf511/empire-core-new/backend/.env TYPE=regular file OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-------
PATH_OK=/home/nawaf511/empire-core-new/backend/venv/bin/python TYPE=symbolic link OWNER=nawaf511 GROUP=nawaf511 MODE=lrwxrwxrwx
UNIT_PATHS_MISSING=0

### PORTS_AND_PROCESSES
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2682,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
3157209 nawaf511       00:00 /home/nawaf511/empire-core-new/backend/venv/bin/python /home/nawaf511/empire-core-new/backend/venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:9002 --workers 4 --timeout 120
3532162 postgres    16:02:53 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
3532165 nawaf511    16:02:53 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
3532173 root        16:02:52 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
3532176 postgres    16:02:52 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
3532178 nawaf511    16:02:52 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
3532200 root        16:02:51 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
3532221 root        16:02:51 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
PORTS_HINT=API_PORTS_PRESENT

### PRELIMINARY_RECOMMENDATION
PRELIMINARY_RECOMMENDATION=DO_NOT_TOUCH_NGINX_OR_API_REFERENCED

---- SERVICE=testapp.service ----
DESCRIPTION=testapp Service
ENABLED=enabled
ACTIVE=failed
FAILED=failed
FRAGMENT=/etc/systemd/system/testapp.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
WORKING_DIRECTORY=/srv/testapp

### UNIT_FILE_REDACTED
# /etc/systemd/system/testapp.service
[Unit]
Description=testapp Service
After=network.target

[Service]
User=testapp
WorkingDirectory=/srv/testapp
ExecStart=/srv/testapp/venv/bin/streamlit run /srv/testapp/app.py --server.port=8521 --server.address=127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target

### UNIT_EXEC_LINES
8:WorkingDirectory=/srv/testapp
9:ExecStart=/srv/testapp/venv/bin/streamlit run /srv/testapp/app.py --server.port=8521 --server.address=127.0.0.1

### RECENT_JOURNAL_REDACTED
-- No entries --

### PROJECT_REFERENCES
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:35:import testapp
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:45:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:46:        open(os.path.join(self.path, "testapp/__init__.py"), "w").close()
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:47:        with open(os.path.join(self.path, "testapp/__main__.py"), "w") as f:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:57:            [sys.executable, "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:75:import testapp
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:95:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:96:        init_file = os.path.join(self.path, "testapp", "__init__.py")
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:98:        main_file = os.path.join(self.path, "testapp", "__main__.py")
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:109:            [sys.executable, "-m", "tornado.autoreload", "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi-0.19.2.dist-info/RECORD:1849:jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi,sha256=O0O2-rhExeAFHWIryQcjWpQhGPQfkkU8SuV0uLbbpco,226
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:15:    testapp,
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:30:test_app = testapp.test_app
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi:9:def render_testapp(req): ...
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:35:import testapp
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:45:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:46:        open(os.path.join(self.path, "testapp/__init__.py"), "w").close()
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:47:        with open(os.path.join(self.path, "testapp/__main__.py"), "w") as f:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:57:            [sys.executable, "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:75:import testapp
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:95:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:96:        init_file = os.path.join(self.path, "testapp", "__init__.py")
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:98:        main_file = os.path.join(self.path, "testapp", "__main__.py")
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:109:            [sys.executable, "-m", "tornado.autoreload", "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi-0.19.2.dist-info/RECORD:1849:jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi,sha256=O0O2-rhExeAFHWIryQcjWpQhGPQfkkU8SuV0uLbbpco,226
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:15:    testapp,
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:30:test_app = testapp.test_app
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi:9:def render_testapp(req): ...
PROJECT_REFS_COUNT=28

### BROADER_PROJECT_REFERENCES
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/ma/tests/test_extras.py:880:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/ma/tests/test_extras.py:902:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/testing/tests/test_utils.py:874:class TestApproxEqual:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:136:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:302:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:576:class TestAppendFields:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:1026:class TestAppendFieldsObj:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/pandas/tests/indexes/categorical/test_append.py:10:class TestAppend:
/home/nawaf511/empire-core-new/backend/venv/lib64/python3.12/site-packages/pandas/tests/reshape/concat/test_append.py:20:class TestAppend:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/ma/tests/test_extras.py:880:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/ma/tests/test_extras.py:902:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/testing/tests/test_utils.py:874:class TestApproxEqual:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:136:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:302:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:576:class TestAppendFields:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:1026:class TestAppendFieldsObj:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/pandas/tests/indexes/categorical/test_append.py:10:class TestAppend:
/home/nawaf511/empire-core-new/backend/venv/lib/python3.12/site-packages/pandas/tests/reshape/concat/test_append.py:20:class TestAppend:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:35:import testapp
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:45:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:46:        open(os.path.join(self.path, "testapp/__init__.py"), "w").close()
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:47:        with open(os.path.join(self.path, "testapp/__main__.py"), "w") as f:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:57:            [sys.executable, "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:75:import testapp
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:95:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:96:        init_file = os.path.join(self.path, "testapp", "__init__.py")
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:98:        main_file = os.path.join(self.path, "testapp", "__main__.py")
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/tornado/test/autoreload_test.py:109:            [sys.executable, "-m", "tornado.autoreload", "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/scipy/optimize/tests/test__numdiff.py:156:class TestApproxDerivativesDense:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/scipy/optimize/tests/test__numdiff.py:570:class TestApproxDerivativeSparse:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/scipy/optimize/tests/test__numdiff.py:665:class TestApproxDerivativeLinearOperator:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/ipywidgets/widgets/tests/test_widget_templates.py:246:class TestAppLayout(TestCase):
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/ma/tests/test_extras.py:880:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/ma/tests/test_extras.py:902:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/testing/tests/test_utils.py:874:class TestApproxEqual:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:136:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:302:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:576:class TestAppendFields:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:1026:class TestAppendFieldsObj:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi-0.19.2.dist-info/RECORD:1849:jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi,sha256=O0O2-rhExeAFHWIryQcjWpQhGPQfkkU8SuV0uLbbpco,226
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:15:    testapp,
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:30:test_app = testapp.test_app
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi:9:def render_testapp(req): ...
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/pandas/tests/indexes/categorical/test_append.py:10:class TestAppend:
/home/nawaf511/empire-core-new/venv/lib64/python3.12/site-packages/pandas/tests/reshape/concat/test_append.py:20:class TestAppend:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:35:import testapp
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:45:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:46:        open(os.path.join(self.path, "testapp/__init__.py"), "w").close()
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:47:        with open(os.path.join(self.path, "testapp/__main__.py"), "w") as f:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:57:            [sys.executable, "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:75:import testapp
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:95:        os.mkdir(os.path.join(self.path, "testapp"))
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:96:        init_file = os.path.join(self.path, "testapp", "__init__.py")
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:98:        main_file = os.path.join(self.path, "testapp", "__main__.py")
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/tornado/test/autoreload_test.py:109:            [sys.executable, "-m", "tornado.autoreload", "-m", "testapp"],
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/scipy/optimize/tests/test__numdiff.py:156:class TestApproxDerivativesDense:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/scipy/optimize/tests/test__numdiff.py:570:class TestApproxDerivativeSparse:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/scipy/optimize/tests/test__numdiff.py:665:class TestApproxDerivativeLinearOperator:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/ipywidgets/widgets/tests/test_widget_templates.py:246:class TestAppLayout(TestCase):
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/ma/tests/test_extras.py:880:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/ma/tests/test_extras.py:902:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/testing/tests/test_utils.py:874:class TestApproxEqual:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:136:class TestApplyAlongAxis:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/lib/tests/test_shape_base.py:302:class TestApplyOverAxes:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:576:class TestAppendFields:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/numpy/lib/tests/test_recfunctions.py:1026:class TestAppendFieldsObj:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi-0.19.2.dist-info/RECORD:1849:jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi,sha256=O0O2-rhExeAFHWIryQcjWpQhGPQfkkU8SuV0uLbbpco,226
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:15:    testapp,
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/__init__.pyi:30:test_app = testapp.test_app
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/jedi/third_party/typeshed/third_party/2and3/werkzeug/testapp.pyi:9:def render_testapp(req): ...
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/pandas/tests/indexes/categorical/test_append.py:10:class TestAppend:
/home/nawaf511/empire-core-new/venv/lib/python3.12/site-packages/pandas/tests/reshape/concat/test_append.py:20:class TestAppend:
BROADER_PROJECT_REFS_COUNT=72

### NGINX_REFERENCES
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:9:# - Platform backend: 127.0.0.1:9001
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:19:    server 127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:177:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:99:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:77:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:77:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:150:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:159:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:168:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:54:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:86:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:98:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:110:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:86:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:98:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:110:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:63:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:75:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:87:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:33:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:46:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:219:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:232:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:110:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:123:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:364:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:377:        proxy_pass http://127.0.0.1:9028/api/auth/register;
NGINX_REFS_COUNT=61

### PATH_EXISTENCE_FROM_UNIT
PATH_OK=/srv/testapp TYPE=directory OWNER=testapp GROUP=testapp MODE=drwxr-xr-x
PATH_MISSING=/srv/testapp/app.py
PATH_MISSING=/srv/testapp/venv/bin/streamlit
UNIT_PATHS_MISSING=2

### PORTS_AND_PROCESSES
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2682,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
3532162 postgres    16:03:00 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
3532165 nawaf511    16:03:00 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
3532173 root        16:03:00 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
3532176 postgres    16:02:59 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
3532178 nawaf511    16:02:59 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
3532200 root        16:02:58 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
3532221 root        16:02:58 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
PORTS_HINT=API_PORTS_PRESENT

### PRELIMINARY_RECOMMENDATION
PRELIMINARY_RECOMMENDATION=DO_NOT_TOUCH_NGINX_REFERENCED

## 3) Summary
service               enabled   active  failed  project_refs  broader_refs  nginx_refs  unit_paths_missing  ports_hint         preliminary_recommendation
ndip-api-new.service  disabled  failed  failed  2             131           61          0                   API_PORTS_PRESENT  DO_NOT_TOUCH_NGINX_OR_API_REFERENCED
testapp.service       enabled   failed  failed  28            72            61          2                   API_PORTS_PRESENT  DO_NOT_TOUCH_NGINX_REFERENCED

## 4) Runtime safety after read-only audit
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

FINAL_STATUS=P2_REMAINING_TWO_TARGETED_EVIDENCE_AUDIT_D2_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_REMAINING_TWO_TARGETED_EVIDENCE_AUDIT_D2_READONLY_20260708_221551.md
ARTIFACT_DIR=/tmp/NDSP_P2_REMAINING_TWO_EVIDENCE_D2_20260708_221551
