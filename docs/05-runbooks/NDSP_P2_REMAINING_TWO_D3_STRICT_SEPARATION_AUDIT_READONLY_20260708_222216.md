# NDSP P2 Remaining Two D3 Strict Separation Audit — Read-only
DATE=2026-07-08T22:22:16+02:00
MODE=READ_ONLY_D3_STRICT_SEPARATION_AUDIT
TARGETS=ndip-api-new.service,testapp.service
MODIFICATIONS=None
NO_STOP=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_RESTART=1
NO_REBOOT=1
ARTIFACT_DIR=/tmp/NDSP_P2_REMAINING_TWO_D3_STRICT_20260708_222216

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
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.9%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.061mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.159mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
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
ENABLED=disabled
ACTIVE=failed
FAILED=failed
FRAGMENT=/etc/systemd/system/ndip-api-new.service
RESULT=exit-code
EXEC_MAIN_STATUS=1

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

### UNIT_PATHS
PATH_OK=/home/nawaf511/empire-core-new/backend TYPE=directory OWNER=nawaf511 GROUP=nawaf511 MODE=drwxr-xr-x
PATH_OK=/home/nawaf511/empire-core-new/backend/.env TYPE=regular file OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-------
PATH_OK=/home/nawaf511/empire-core-new/backend/venv/bin/python TYPE=symbolic link OWNER=nawaf511 GROUP=nawaf511 MODE=lrwxrwxrwx
UNIT_PATHS_MISSING=PATH_OK=/home/nawaf511/empire-core-new/backend TYPE=directory OWNER=nawaf511 GROUP=nawaf511 MODE=drwxr-xr-x
PATH_OK=/home/nawaf511/empire-core-new/backend/.env TYPE=regular file OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-------
PATH_OK=/home/nawaf511/empire-core-new/backend/venv/bin/python TYPE=symbolic link OWNER=nawaf511 GROUP=nawaf511 MODE=lrwxrwxrwx
0

### STRICT_PROJECT_REFS
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:6:const PORT = Number(process.env.NDSP_PLATFORM_GATEWAY_PORT || 9001);
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:25:    'X-NDSP-Gateway': 'platform-9001'
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:53:      'x-ndsp-platform-gateway': '9001',
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:62:    headers['x-ndsp-gateway'] = 'platform-9001';
/home/nawaf511/empire-core-new/backend/ndsp_platform_gateway_9001.cjs:116:        platform_backend_port: 9001,
/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:44:PORT="9001"
/home/nawaf511/empire-core-new/backend/.env.bak.20260527_025723:8:PORT=9001
/home/nawaf511/empire-core-new/backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260618_100847.txt:78:"SONAT - TIER 1 POOL (ZONE 0) - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233C1,IFED,01,023 ,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -8224,    9001,   -5705,    -890,    -300,     -85,   -2832,       0,       0,     133,       0,       0,    5327,   -6090,  -13551,   -2134,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"2500 mmbtu","0233C1","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.json:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/nmp-lab-summary.txt:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260618_100847.txt:78:"SONAT - TIER 1 POOL (ZONE 0) - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233C1,IFED,01,023 ,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -8224,    9001,   -5705,    -890,    -300,     -85,   -2832,       0,       0,     133,       0,       0,    5327,   -6090,  -13551,   -2134,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"2500 mmbtu","0233C1","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/current_disaggregated_futures_only_f_disagg.txt:78:"SONAT - TIER 1 POOL (ZONE 0) - ICE FUTURES ENERGY DIV",260609,2026-06-09,0233C1,IFED,01,023 ,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,   88012,   59266,   71219,    6938,    7310,    4337,    6239,       0,       0,    2097,       0,     180,   79057,   83046,    8955,    4966,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,   -8224,    9001,   -5705,    -890,    -300,     -85,   -2832,       0,       0,     133,       0,       0,    5327,   -6090,  -13551,   -2134,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,   67.3,   80.9,    7.9,    8.3,    4.9,    7.1,    0.0,    0.0,    2.4,    0.0,    0.2,   89.8,   94.4,   10.2,    5.6,  100.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,     29,     13,     18,.,.,.,.,      0,      0,.,      0,.,     19,     24,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,    56.5,    56.2,    74.2,    70.8,    54.8,    52.6,    69.6,    67.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.0,"2500 mmbtu","0233C1","IFED","023 ","N13","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/nmp-lab/results/NDIP_MT4_CANDLES_ETHUSD_M30_nmp_lab_summary.csv:74:PRICE_BODY_ATR,open,2,1.0,0.5,1.0,0.5004,0.29001199999999994
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:6:const PORT = Number(process.env.NDSP_PLATFORM_GATEWAY_PORT || 9001);
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:25:    'X-NDSP-Gateway': 'platform-9001'
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:53:      'x-ndsp-platform-gateway': '9001',
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:62:    headers['x-ndsp-gateway'] = 'platform-9001';
/home/nawaf511/empire-core-new/backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_platform_gateway_9001.cjs:116:        platform_backend_port: 9001,
/home/nawaf511/empire-core-new/backend/architecture/registry/SERVICE_REGISTRY_V2.md:11:| SRV-003 | Platform Gateway | 9001 | NDSP Platform | Active |
/home/nawaf511/empire-core-new/backend/architecture/DEPLOYMENT_ARCHITECTURE.md:14:- 127.0.0.1:9001 Platform Gateway
/home/nawaf511/empire-core-new/backend/_archive_safe_cleanup_20260627_214310/server.jsy:27:const PORT = Number(process.env.PORT || 9001);
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs:6:const PORT = Number(process.env.NDSP_PLATFORM_GATEWAY_PORT || 9001);
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs:27:    'X-NDSP-Gateway': 'platform-9001'
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs:55:      'x-ndsp-platform-gateway': '9001',
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs:64:    headers['x-ndsp-gateway'] = 'platform-9001';
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs:118:        platform_backend_port: 9001,
/home/nawaf511/empire-core-new/backend/auth_api/.env:8:PORT=9001
/home/nawaf511/empire-core-new/backend/.env:8:PORT=9001
/home/nawaf511/empire-core-new/scripts/audit/ndsp_server_and_project_audit_EN.sh:76:  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
/home/nawaf511/empire-core-new/scripts/audit/ndsp_server_and_project_audit_AR.sh:76:  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
/home/nawaf511/empire-core-new/research/nmp-lab/results/NDIP_MT4_CANDLES_ETHUSD_M30_nmp_lab_summary.csv:74:PRICE_BODY_ATR,open,2,1.0,0.5,1.0,0.5004,0.29001199999999994
/home/nawaf511/empire-core-new/frontend/admin-console/nmp-lab-summary.json:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/frontend/admin-console/nmp-lab-summary.txt:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/apps/admin-console/nmp-lab-summary.json:950:      "score": 0.29001199999999994,
/home/nawaf511/empire-core-new/apps/admin-console/nmp-lab-summary.txt:950:      "score": 0.29001199999999994,
TRUE_PROJECT_REFS_COUNT=35

### STRICT_ACTIVE_NGINX_REFS
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:177:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
ACTIVE_NGINX_REFS_COUNT=2

### PORTS
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
PORT_HINT=PORT_9001_LISTENING

### STRICT_RECOMMENDATION
STRICT_RECOMMENDATION=DO_NOT_DISABLE_REVIEW_SERVICE_MAPPING_OR_RESET_FAILED_ONLY

---- SERVICE=testapp.service ----
ENABLED=enabled
ACTIVE=failed
FAILED=failed
FRAGMENT=/etc/systemd/system/testapp.service
RESULT=exit-code
EXEC_MAIN_STATUS=203

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

### UNIT_PATHS
PATH_OK=/srv/testapp TYPE=directory OWNER=testapp GROUP=testapp MODE=drwxr-xr-x
PATH_MISSING=/srv/testapp/app.py
PATH_MISSING=/srv/testapp/venv/bin/streamlit
UNIT_PATHS_MISSING=PATH_OK=/srv/testapp TYPE=directory OWNER=testapp GROUP=testapp MODE=drwxr-xr-x
PATH_MISSING=/srv/testapp/app.py
PATH_MISSING=/srv/testapp/venv/bin/streamlit
2

### STRICT_PROJECT_REFS
/home/nawaf511/empire-core-new/backend/data/raw_cot/tff_futures_only_FinFutWk_20260618_100847.txt:46:"ULTRA UST 10Y - CHICAGO BOARD OF TRADE",260609,2026-06-09,043607,CBT ,00,043 , 2428052,   68078,  309109,    9431, 1244293,  648550,  578135,  150112,  410242,   34668,  150222,  132900,     300, 2235239, 2123335,  192813,  304717,    8326,    5525,  -18521,   -3206,    5942,   73353,   -7673,   12950,  -12243,   -5679,   49003,   -1243,     300,   57162,   25088,  -48836,  -16762,  100.0,    2.8,   12.7,    0.4,   51.2,   26.7,   23.8,    6.2,   16.9,    1.4,    6.2,    5.5,    0.0,   92.1,   87.5,    7.9,   12.5,    240,      8,     21,      6,     65,     71,     73,     18,     41,     23,      7,      9,.,    162,    181,    25.3,    21.3,    38.2,    31.5,    15.7,    14.0,    27.0,    22.0,"(CONTRACTS OF $100,000 FACE VALUE)","043607","CBT ","043 ","F30","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt:46:"ULTRA UST 10Y - CHICAGO BOARD OF TRADE",260609,2026-06-09,043607,CBT ,00,043 , 2428052,   68078,  309109,    9431, 1244293,  648550,  578135,  150112,  410242,   34668,  150222,  132900,     300, 2235239, 2123335,  192813,  304717,    8326,    5525,  -18521,   -3206,    5942,   73353,   -7673,   12950,  -12243,   -5679,   49003,   -1243,     300,   57162,   25088,  -48836,  -16762,  100.0,    2.8,   12.7,    0.4,   51.2,   26.7,   23.8,    6.2,   16.9,    1.4,    6.2,    5.5,    0.0,   92.1,   87.5,    7.9,   12.5,    240,      8,     21,      6,     65,     71,     73,     18,     41,     23,      7,      9,.,    162,    181,    25.3,    21.3,    38.2,    31.5,    15.7,    14.0,    27.0,    22.0,"(CONTRACTS OF $100,000 FACE VALUE)","043607","CBT ","043 ","F30","FutOnly"
/home/nawaf511/empire-core-new/backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/data/raw_cot/tff_futures_only_FinFutWk_20260618_100847.txt:46:"ULTRA UST 10Y - CHICAGO BOARD OF TRADE",260609,2026-06-09,043607,CBT ,00,043 , 2428052,   68078,  309109,    9431, 1244293,  648550,  578135,  150112,  410242,   34668,  150222,  132900,     300, 2235239, 2123335,  192813,  304717,    8326,    5525,  -18521,   -3206,    5942,   73353,   -7673,   12950,  -12243,   -5679,   49003,   -1243,     300,   57162,   25088,  -48836,  -16762,  100.0,    2.8,   12.7,    0.4,   51.2,   26.7,   23.8,    6.2,   16.9,    1.4,    6.2,    5.5,    0.0,   92.1,   87.5,    7.9,   12.5,    240,      8,     21,      6,     65,     71,     73,     18,     41,     23,      7,      9,.,    162,    181,    25.3,    21.3,    38.2,    31.5,    15.7,    14.0,    27.0,    22.0,"(CONTRACTS OF $100,000 FACE VALUE)","043607","CBT ","043 ","F30","FutOnly"
TRUE_PROJECT_REFS_COUNT=3

### STRICT_ACTIVE_NGINX_REFS
ACTIVE_NGINX_REFS_COUNT=0

### PORTS
PORT_HINT=NONE

### STRICT_RECOMMENDATION
STRICT_RECOMMENDATION=DISABLE_CANDIDATE_REQUIRES_APPROVAL

## 3) Summary
service                                                                                                                          enabled              active                                                      failed  true_project_refs  active_nginx_refs  unit_paths_missing                                                                                           port_hint  strict_recommendation
ndip-api-new.service                                                                                                             disabled             failed                                                      failed  35                 2                  PATH_OK=/home/nawaf511/empire-core-new/backend TYPE=directory OWNER=nawaf511 GROUP=nawaf511 MODE=drwxr-xr-x             
PATH_OK=/home/nawaf511/empire-core-new/backend/.env TYPE=regular file OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-------                                                                                                                                                                                                                                                                     
PATH_OK=/home/nawaf511/empire-core-new/backend/venv/bin/python TYPE=symbolic link OWNER=nawaf511 GROUP=nawaf511 MODE=lrwxrwxrwx                                                                                                                                                                                                                                                         
0                                                                                                                                PORT_9001_LISTENING  DO_NOT_DISABLE_REVIEW_SERVICE_MAPPING_OR_RESET_FAILED_ONLY                                                                                                                                                                        
testapp.service                                                                                                                  enabled              failed                                                      failed  3                  0                  PATH_OK=/srv/testapp TYPE=directory OWNER=testapp GROUP=testapp MODE=drwxr-xr-x                                         
PATH_MISSING=/srv/testapp/app.py                                                                                                                                                                                                                                                                                                                                                        
PATH_MISSING=/srv/testapp/venv/bin/streamlit                                                                                                                                                                                                                                                                                                                                            
2                                                                                                                                NONE                 DISABLE_CANDIDATE_REQUIRES_APPROVAL                                                                                                                                                                                               

## 4) Runtime safety after read-only audit
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

FINAL_STATUS=P2_REMAINING_TWO_D3_STRICT_SEPARATION_AUDIT_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_REMAINING_TWO_D3_STRICT_SEPARATION_AUDIT_READONLY_20260708_222216.md
ARTIFACT_DIR=/tmp/NDSP_P2_REMAINING_TWO_D3_STRICT_20260708_222216
