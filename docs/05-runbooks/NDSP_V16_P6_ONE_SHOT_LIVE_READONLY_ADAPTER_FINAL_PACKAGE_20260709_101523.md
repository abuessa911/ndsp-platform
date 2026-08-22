# NDSP V1.6 / P6 One-Shot — Live Read-only Completed Decisions Adapter + Final Package
DATE=2026-07-09T10:15:23+02:00
MODE=V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE
CONTROLLED_NGINX_CHANGE=conditional_only_if_source_proven
NO_BACKEND_ENGINE_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_DB_SCHEMA_CHANGE=1
NO_PROTECTED_ASSET_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE_20260709_101523.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_20260709_101523
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz

## 1) Required V1.5/P5 D2 final lock
V15_P5_D2_FINAL_LOCK=OK

## 2) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 10h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.4mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m8.6%[39m | [1mram usage[22m: [32m8%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.171mb/s[39m [90m/[39m [1m[33m82.43%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_BEFORE=active
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Baseline stable endpoints
HTTP_BASE_api_health=200
HTTP_BASE_v15_page=200
HTTP_BASE_quality_live=200
HTTP_BASE_my_home=200
HTTP_BASE_v15_completed=200
HTTP_BASE_v15_completed_latest=200
HTTP_BASE_v15_completed_v15=200
BASE_ENDPOINTS_OK=1

## 4) Backup targets
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/completed-decisions-v16-live-adapter.json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/v16-live-adapter.html
BACKUP_FILE=/home/nawaf511/ndsp_backups/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_20260709_101523/completed-decisions-v15-api.json.before
BACKUP_NGINX_DIR=/home/nawaf511/ndsp_backups/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_20260709_101523/etc-nginx.before

## 5) Discover live/read-only source candidates
State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                                                                                                                                                                                                                                                          
LISTEN 0      65535  127.0.0.53%lo:53        0.0.0.0:*    users:(("systemd-resolve",pid=912,fd=15))                                                                                                                                                                                                                       
LISTEN 0      511          0.0.0.0:443       0.0.0.0:*    users:(("nginx",pid=2482391,fd=9),("nginx",pid=2482390,fd=9),("nginx",pid=2482389,fd=9),("nginx",pid=2482387,fd=9),("nginx",pid=2482385,fd=9),("nginx",pid=2482384,fd=9),("nginx",pid=2482383,fd=9),("nginx",pid=2482382,fd=9),("nginx",pid=1478,fd=9))         
LISTEN 0      100          0.0.0.0:25        0.0.0.0:*    users:(("master",pid=3416,fd=13))                                                                                                                                                                                                                               
LISTEN 0      65535        0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=1410,fd=3),("systemd",pid=1,fd=333))                                                                                                                                                                                                         
LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=2482391,fd=7),("nginx",pid=2482390,fd=7),("nginx",pid=2482389,fd=7),("nginx",pid=2482387,fd=7),("nginx",pid=2482385,fd=7),("nginx",pid=2482384,fd=7),("nginx",pid=2482383,fd=7),("nginx",pid=2482382,fd=7),("nginx",pid=1478,fd=7))         
LISTEN 0      511          0.0.0.0:3000      0.0.0.0:*    users:(("MainThread",pid=3788,fd=21))                                                                                                                                                                                                                           
LISTEN 0      65535     127.0.0.54:53        0.0.0.0:*    users:(("systemd-resolve",pid=912,fd=17))                                                                                                                                                                                                                       
LISTEN 0      65535        0.0.0.0:5433      0.0.0.0:*    users:(("docker-proxy",pid=3959,fd=8))                                                                                                                                                                                                                          
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=1358,fd=13))                                                                                                                                                                                                                              
LISTEN 0      511        127.0.0.1:9062      0.0.0.0:*    users:(("node",pid=2716,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9061      0.0.0.0:*    users:(("uvicorn",pid=1323,fd=6))                                                                                                                                                                                                                               
LISTEN 0      5          127.0.0.1:9067      0.0.0.0:*    users:(("python3",pid=1329,fd=3))                                                                                                                                                                                                                               
LISTEN 0      2048       127.0.0.1:9066      0.0.0.0:*    users:(("python3",pid=1332,fd=13))                                                                                                                                                                                                                              
LISTEN 0      2048       127.0.0.1:9065      0.0.0.0:*    users:(("uvicorn",pid=1327,fd=13))                                                                                                                                                                                                                              
LISTEN 0      511        127.0.0.1:9064      0.0.0.0:*    users:(("node",pid=2715,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9070      0.0.0.0:*    users:(("node",pid=2703,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9069      0.0.0.0:*    users:(("uvicorn",pid=2672,fd=13))                                                                                                                                                                                                                              
LISTEN 0      2048       127.0.0.1:9068      0.0.0.0:*    users:(("python3",pid=2658,fd=13))                                                                                                                                                                                                                              
LISTEN 0      2048       127.0.0.1:9074      0.0.0.0:*    users:(("uvicorn",pid=2682,fd=6))                                                                                                                                                                                                                               
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1324,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1319,fd=33))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9077      0.0.0.0:*    users:(("node",pid=1311,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9076      0.0.0.0:*    users:(("uvicorn",pid=1331,fd=13))                                                                                                                                                                                                                              
LISTEN 0      5          127.0.0.1:9083      0.0.0.0:*    users:(("python3",pid=1336,fd=3))                                                                                                                                                                                                                               
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=1330,fd=3))                                                                                                                                                                                                                               
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1322,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1317,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9084      0.0.0.0:*    users:(("python3",pid=1337,fd=3))                                                                                                                                                                                                                               
LISTEN 0      511        127.0.0.1:9027      0.0.0.0:*    users:(("node",pid=2689,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9024      0.0.0.0:*    users:(("node",pid=2647,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9031      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9030      0.0.0.0:*    users:(("node",pid=2653,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2691,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9034      0.0.0.0:*    users:(("node",pid=1364,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9033      0.0.0.0:*    users:(("node",pid=1361,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9041      0.0.0.0:*    users:(("node",pid=2705,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9047      0.0.0.0:*    users:(("python3",pid=2690,fd=3))                                                                                                                                                                                                                               
LISTEN 0      511        127.0.0.1:9044      0.0.0.0:*    users:(("node",pid=1326,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=1363,fd=3))                                                                                                                                                                                                                               
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1328,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2702,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9017      0.0.0.0:*    users:(("node",pid=2655,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9023      0.0.0.0:*    users:(("node",pid=2669,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9022      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9021      0.0.0.0:*    users:(("node",pid=1334,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2720,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9093      0.0.0.0:*    users:(("python3",pid=1335,fd=3))                                                                                                                                                                                                                               
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=1338,fd=3))                                                                                                                                                                                                                               
LISTEN 0      200        127.0.0.1:5432      0.0.0.0:*    users:(("postgres",pid=1462,fd=7))                                                                                                                                                                                                                              
LISTEN 0      511        127.0.0.1:8097      0.0.0.0:*    users:(("node",pid=1362,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:6379      0.0.0.0:*    users:(("redis-server",pid=1340,fd=6))                                                                                                                                                                                                                          
LISTEN 0      65535      127.0.0.1:631       0.0.0.0:*    users:(("cupsd",pid=162749,fd=7))                                                                                                                                                                                                                               
LISTEN 0      511            [::1]:6379         [::]:*    users:(("redis-server",pid=1340,fd=7))                                                                                                                                                                                                                          
LISTEN 0      511             [::]:443          [::]:*    users:(("nginx",pid=2482391,fd=10),("nginx",pid=2482390,fd=10),("nginx",pid=2482389,fd=10),("nginx",pid=2482387,fd=10),("nginx",pid=2482385,fd=10),("nginx",pid=2482384,fd=10),("nginx",pid=2482383,fd=10),("nginx",pid=2482382,fd=10),("nginx",pid=1478,fd=10))
LISTEN 0      100             [::]:25           [::]:*    users:(("master",pid=3416,fd=14))                                                                                                                                                                                                                               
LISTEN 0      65535           [::]:22           [::]:*    users:(("sshd",pid=1410,fd=4),("systemd",pid=1,fd=335))                                                                                                                                                                                                         
LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=2482391,fd=8),("nginx",pid=2482390,fd=8),("nginx",pid=2482389,fd=8),("nginx",pid=2482387,fd=8),("nginx",pid=2482385,fd=8),("nginx",pid=2482384,fd=8),("nginx",pid=2482383,fd=8),("nginx",pid=2482382,fd=8),("nginx",pid=1478,fd=8))         
LISTEN 0      200            [::1]:5432         [::]:*    users:(("postgres",pid=1462,fd=6))                                                                                                                                                                                                                              
LISTEN 0      2                  *:3389            *:*    users:(("xrdp",pid=1487,fd=11))                                                                                                                                                                                                                                 
LISTEN 0      2              [::1]:3350         [::]:*    users:(("xrdp-sesman",pid=1398,fd=11))                                                                                                                                                                                                                          
LISTEN 0      65535           [::]:5433         [::]:*    users:(("docker-proxy",pid=3966,fd=8))                                                                                                                                                                                                                          
LISTEN 0      65535          [::1]:631          [::]:*    users:(("cupsd",pid=162749,fd=6))                                                                                                                                                                                                                               
2612168 root     bash            bash /tmp/ndsp_v16_p6_one_shot_live_readonly_adapter_final_package.sh
2612398 root     bash            bash /tmp/ndsp_v16_p6_one_shot_live_readonly_adapter_final_package.sh
   1310 root     fail2ban-server /usr/bin/python3 /usr/bin/fail2ban-server -xf start
   3788 nawaf511 MainThread      node server.js
   1056 root     networkd-dispat /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
   1311 nawaf511 node            /usr/bin/node /opt/ndsp16-api/server.js
   1317 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/services/bot_execution/main.cjs
   1319 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs
   1322 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/main.cjs
   1324 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/services/decision_governance_core/main.cjs
   1326 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/apps/ndsp-governance-bridge/server.mjs
   1328 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs
   1334 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_dashboard_gateway.cjs
   1361 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp_live_market_adapter.cjs
   1362 nawaf511 node            /usr/bin/node /opt/ndsp-news-ticker/server.js
   1364 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp_scenario_levels_adapter.cjs
   2647 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-access-guard-9024/server.js
   2653 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-access-guard-final/server.js
   2655 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_actions_gateway.cjs
   2661 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/admin_users_official_api/server.js
   2664 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_api_compat_gateway.cjs
   2669 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_ui_proxy.cjs
   2689 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/password_reset_gateway/server.js
   2691 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_register_compat_gateway.cjs
   2702 root     node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_register_gateway.cjs
   2703 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_fingerprint_guard_proxy.cjs
   2705 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-trial-register-canonical-wrapper/server.js
   2715 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-trial-seats-api/server.js
   2716 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-user-alert-channels/server.js
   2717 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-telegram-link-listener/server.js
   2720 nawaf511 node            /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs
   2937 nawaf511 PM2 v7.0.3: God PM2 v7.0.3: God Daemon (/home/nawaf511/.pm2)
   1329 root     python3         /usr/bin/python3 /home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_golden_wrapper.py
   1330 root     python3         /usr/bin/python3 /home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
   1332 root     python3         /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
   1335 www-data python3         /usr/bin/python3 /opt/ndsp-v3-portal-gateway/app.py
   1336 root     python3         /usr/bin/python3 /opt/ndsp-v52-contract/app.py
   1337 root     python3         /usr/bin/python3 /opt/ndsp-v53-bridge/app.py
   1338 nawaf511 python3         /usr/bin/python3 /opt/ndsp-public-summary-v548/app.py
   1358 nawaf511 python3         /usr/bin/python3 /home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
   1363 www-data python3         /usr/bin/python3 /opt/ndsp-platform-gateway-9002/app.py
   2658 root     python3         /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
   2690 postgres python3         /usr/bin/python3 /home/nawaf511/empire-core-new/backend/ndsp-portal-real-data-api/server.py
   3784 nawaf511 sh              sh -c node server.js
2611846 root     sudo            sudo bash /tmp/ndsp_v16_p6_one_shot_live_readonly_adapter_final_package.sh
2612167 root     sudo            sudo bash /tmp/ndsp_v16_p6_one_shot_live_readonly_adapter_final_package.sh
2612399 root     tee             tee /tmp/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523/live_source_process_candidates.txt
2612400 root     tee             tee -a docs/05-runbooks/NDSP_V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE_20260709_101523.md
   1323 root     uvicorn         /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
   1327 nawaf511 uvicorn         /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
   1331 nawaf511 uvicorn         /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
   2672 postgres uvicorn         /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
   2682 postgres uvicorn         /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
LOCAL_PORTS_SCANNED=3000 3001 8000 8001 8097 9001 9002 9017 9019 9020 9021 9022 9023 9024 9027 9028 9030 9031 9033 9034 9041 9044 9047 9057 9061 9062 9064 9065 9066 9067 9068 9069 9070 9074 9076 9077 9078 9079 9080 9081 9082 9083 9084 9092 9093
LIVE_HTTP_SOURCE=http://127.0.0.1:9078/api/completed/latest
LIVE_HTTP_OUT=/tmp/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523/probes/local_9078_api_completed_latest.out
LOCAL_HTTP_MATRIX=/tmp/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523/live_source_local_http_matrix.tsv
2026-07-09 01:34 2119 nawaf511:nawaf511 /var/www/ndsp-my/data/completed-decisions-viewer-config.json
2026-07-09 09:07 3576 nawaf511:nawaf511 /var/www/ndsp-my/data/completed-decisions-v14-adapter.json
2026-07-09 09:41 2747 nawaf511:nawaf511 /var/www/ndsp-my/data/completed-decisions-v15-api.json
LIVE_FILE_SOURCE=NONE

## 6) Build V16 adapter payload
V16_JSON_CREATED=1
V16_PAGE_CREATED=1
V16_SOURCE_PROVEN=1
V16_SOURCE_MODE=live_http_local_source
V16_ITEMS_COUNT=1
FILE=/var/www/ndsp-my/data/completed-decisions-v16-live-adapter.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=2429
FILE=/var/www/ndsp-my/v16-live-adapter.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=1493
V16_SOURCE_PROVEN=1
V16_SOURCE_MODE=live_http_local_source
V16_ITEMS_COUNT=1

## 7) Patch Nginx for V16 live adapter routes
API_SERVER_BLOCKS_TARGETED=6
MODIFIED_NGINX_FILES_COUNT=4
MODIFIED_NGINX_FILE=/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf
MODIFIED_NGINX_FILE=/etc/nginx/conf.d/000-my.ndsp.app-final.conf
MODIFIED_NGINX_FILE=/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf
MODIFIED_NGINX_FILE=/etc/nginx/sites-enabled/bot.ndsp.app
NGINX_PATCH_PYTHON_EXIT=0
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
NGINX_TEST_AFTER_PATCH=OK
NGINX_RELOAD=OK

## 8) Post-patch endpoint tests
HTTP_completed_live=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_v15_completed=200
HTTP_completed_live_latest=200
HTTP_v16_page=200
HTTP_v16_json=200
HTTP_v16_completed=200
LINK_INTEGRITY_OK=1

## 9) Runtime and governance after patch
FAILED_UNITS_COUNT_AFTER=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_AFTER=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
PM2_ENABLED_AFTER=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 10h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.4mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m17%[39m | [1mram usage[22m: [32m7.9%[39m | [1mlo[22m: ⇓ [32m0.017mb/s[39m ⇑ [32m0.017mb/s[39m | [1meth0[22m: ⇓ [32m0.183mb/s[39m ⇑ [32m0.008mb/s[39m | [1mdisk[22m: ⇓ [32m0.01mb/s[39m ⇑ [32m0.235mb/s[39m [90m/[39m [1m[33m82.43%[39m[22m |
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V16_FILES=0
GLOBAL_SCRIPT_HITS_V16_PAGE=0
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz.sha256
0bde32a6567610dd1364b1d37a76d0454cc631b19e399cdf75d1b9d790138ae2  /home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz

## 10) Final Evaluation
OK_EVALUATION=1
V16_P6_LIVE_READONLY_ADAPTER_STATUS=OK
V16_P6_NGINX_LIVE_ROUTE_STATUS=OK
V16_P6_FINAL_AUDIT_PACKAGE_STATUS=CREATED
FINAL_STATUS=V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE_20260709_101523.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz.sha256
