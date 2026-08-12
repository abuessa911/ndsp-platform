# NDSP P2 Hold-Review Services Deep Audit — Read-only
DATE=2026-07-08T06:52:26+02:00
MODE=READ_ONLY_HOLD_REVIEW_DEEP_AUDIT
MODIFICATIONS=None
NO_STOP=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_RESTART=1
NO_REBOOT=1
ARTIFACT_DIR=/tmp/NDSP_P2_HOLD_REVIEW_DEEP_AUDIT_20260708_065226

## 1) Critical runtime baseline
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
pm2-nawaf511-enabled=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.9%[39m | [1mram usage[22m: [32m10%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.204mb/s[39m [90m/[39m [1m[33m81.99%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Failed units baseline
  UNIT                         LOAD   ACTIVE SUB    DESCRIPTION
● ndip-api-new.service         loaded failed failed NDIP API - New Backend
● signal-engine.service        loaded failed failed Empire Core Signal Engine
● subscription-watcher.service loaded failed failed Subscription Expiry Watcher
● testapp.service              loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

4 loaded units listed.

## 3) Deep audit per hold-review service

---- SERVICE=ndip-api-new.service ----
DESCRIPTION=NDIP API - New Backend
ACTIVE=failed
ENABLED=disabled
FAILED=failed
FRAGMENT=/etc/systemd/system/ndip-api-new.service
RESULT=exit-code
EXEC_MAIN_STATUS=1
RESTART_POLICY=always
N_RESTARTS=754

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

### UNIT_SHOW_REDACTED
Restart=always
Result=exit-code
NRestarts=754
ExecMainStatus=1
ExecStart={ path=/home/nawaf511/empire-core-new/backend/venv/bin/python ; argv[]=/home/nawaf511/empire-core-new/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 9000 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
WorkingDirectory=/home/nawaf511/empire-core-new/backend
User=nawaf511
Id=ndip-api-new.service
Names=ndip-api-new.service
Description=NDIP API - New Backend
LoadState=loaded
ActiveState=failed
SubState=failed
FragmentPath=/etc/systemd/system/ndip-api-new.service
UnitFileState=disabled

### RECENT_JOURNAL_REDACTED
يوليو 05 13:06:46 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:06:51 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 735.
يوليو 05 13:06:51 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:06:51 vmi2934783 python[485447]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:06:51 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:06:51 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:06:56 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 736.
يوليو 05 13:06:56 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:06:57 vmi2934783 python[485886]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:06:57 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:06:57 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:02 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 737.
يوليو 05 13:07:02 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:02 vmi2934783 python[486263]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:02 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:02 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:07 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 738.
يوليو 05 13:07:07 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:08 vmi2934783 python[486702]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:08 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:08 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:13 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 739.
يوليو 05 13:07:13 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:13 vmi2934783 python[487994]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:13 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:13 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:18 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 740.
يوليو 05 13:07:18 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:18 vmi2934783 python[488388]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:18 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:18 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:23 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 741.
يوليو 05 13:07:23 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:24 vmi2934783 python[488789]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:24 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:24 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:29 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 742.
يوليو 05 13:07:29 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:29 vmi2934783 python[489206]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:29 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:29 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:34 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 743.
يوليو 05 13:07:34 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:34 vmi2934783 python[490608]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:34 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:34 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:39 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 744.
يوليو 05 13:07:39 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:40 vmi2934783 python[491034]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:40 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:40 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:45 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 745.
يوليو 05 13:07:45 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:45 vmi2934783 python[491415]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:45 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:45 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:50 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 746.
يوليو 05 13:07:50 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:50 vmi2934783 python[491820]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:50 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:50 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:07:55 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 747.
يوليو 05 13:07:55 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:07:56 vmi2934783 python[493131]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:07:56 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:07:56 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:01 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 748.
يوليو 05 13:08:01 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:08:01 vmi2934783 python[493504]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:08:01 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:08:01 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:06 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 749.
يوليو 05 13:08:06 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:08:07 vmi2934783 python[493938]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:08:07 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:08:07 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:12 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 750.
يوليو 05 13:08:12 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:08:12 vmi2934783 python[495234]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:08:12 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:08:12 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:17 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 751.
يوليو 05 13:08:17 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:08:17 vmi2934783 python[495632]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:08:17 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:08:17 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:23 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 752.
يوليو 05 13:08:23 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:08:23 vmi2934783 python[496036]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:08:23 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:08:23 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:28 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 753.
يوليو 05 13:08:28 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 05 13:08:28 vmi2934783 python[496467]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 05 13:08:28 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 13:08:28 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:33 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 754.
يوليو 05 13:08:33 vmi2934783 systemd[1]: ndip-api-new.service: Start request repeated too quickly.
يوليو 05 13:08:33 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 05 13:08:33 vmi2934783 systemd[1]: Failed to start ndip-api-new.service - NDIP API - New Backend.

### PATH_EXISTENCE_CHECK
PATH_OK=/home/nawaf511/empire-core-new/backend TYPE=directory OWNER=nawaf511 GROUP=nawaf511 MODE=drwxr-xr-x
PATH_OK=/home/nawaf511/empire-core-new/backend/.env TYPE=regular file OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-------
PATH_OK=/home/nawaf511/empire-core-new/backend/venv/bin/python TYPE=symbolic link OWNER=nawaf511 GROUP=nawaf511 MODE=lrwxrwxrwx
PATHS_MISSING_COUNT=0

### PROJECT_REFERENCES_CONTEXT
/home/nawaf511/empire-core-new/scripts/audit/ndsp_server_and_project_audit_EN.sh:76:  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
/home/nawaf511/empire-core-new/scripts/audit/ndsp_server_and_project_audit_AR.sh:76:  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
PROJECT_REFS_COUNT=2

### NGINX_REFERENCES_CONTEXT
NGINX_REFS_COUNT=0

### PORT_AND_PROCESS_EVIDENCE
LISTEN 0      511        127.0.0.1:9041      0.0.0.0:*    users:(("node",pid=2676,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9044      0.0.0.0:*    users:(("node",pid=1345,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9047      0.0.0.0:*    users:(("python3",pid=3532117,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9024      0.0.0.0:*    users:(("node",pid=2632,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9027      0.0.0.0:*    users:(("node",pid=2655,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9030      0.0.0.0:*    users:(("node",pid=2633,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9031      0.0.0.0:*    users:(("node",pid=2636,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9033      0.0.0.0:*    users:(("node",pid=1388,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9034      0.0.0.0:*    users:(("node",pid=1400,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9074      0.0.0.0:*    users:(("uvicorn",pid=3532176,fd=6))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9076      0.0.0.0:*    users:(("uvicorn",pid=3532178,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9077      0.0.0.0:*    users:(("node",pid=1335,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1339,fd=33))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1343,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1337,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1340,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=3532132,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9083      0.0.0.0:*    users:(("python3",pid=3532150,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9084      0.0.0.0:*    users:(("python3",pid=3532154,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=3532223,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9061      0.0.0.0:*    users:(("uvicorn",pid=3532173,fd=6))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9062      0.0.0.0:*    users:(("node",pid=2680,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9064      0.0.0.0:*    users:(("node",pid=2679,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9065      0.0.0.0:*    users:(("uvicorn",pid=3532165,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9066      0.0.0.0:*    users:(("python3",pid=3532200,fd=13))                                                                                                                                                                                                                           
LISTEN 0      5          127.0.0.1:9067      0.0.0.0:*    users:(("python3",pid=3532131,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9068      0.0.0.0:*    users:(("python3",pid=3532221,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9069      0.0.0.0:*    users:(("uvicorn",pid=3532162,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9070      0.0.0.0:*    users:(("node",pid=2669,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9017      0.0.0.0:*    users:(("node",pid=2634,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2682,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9021      0.0.0.0:*    users:(("node",pid=1352,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9022      0.0.0.0:*    users:(("node",pid=2643,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9023      0.0.0.0:*    users:(("node",pid=2649,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=3532115,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=3532119,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9093      0.0.0.0:*    users:(("python3",pid=3532143,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511          0.0.0.0:3000      0.0.0.0:*    users:(("MainThread",pid=1099167,fd=21))                                                                                                                                                                                                                        
LISTEN 0      511        127.0.0.1:8097      0.0.0.0:*    users:(("node",pid=1389,fd=32))                                                                                                                                                                                                                                 
3532162 postgres       39:26 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
3532165 nawaf511       39:26 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
3532173 root           39:26 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
3532176 postgres       39:25 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
3532178 nawaf511       39:25 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
3532200 root           39:24 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
3532221 root           39:24 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
3697407 root           00:00 grep -E ndip-api-new|uvicorn|gunicorn|streamlit|signal_engine|run_watcher|app.main|server:app
3697408 root           00:00 tee /tmp/NDSP_P2_HOLD_REVIEW_DEEP_AUDIT_20260708_065226/ndip-api-new/process_matches.txt

### PRELIMINARY_DECISION
PRELIMINARY_DECISION=REVIEW_IMPORT_PATH_OR_LEGACY_BACKEND

---- SERVICE=signal-engine.service ----
DESCRIPTION=Empire Core Signal Engine
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/signal-engine.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
RESTART_POLICY=always
N_RESTARTS=5

### UNIT_FILE_REDACTED
# /etc/systemd/system/signal-engine.service
[Unit]
Description=Empire Core Signal Engine
After=network.target

[Service]
User=nawaf511
WorkingDirectory=/opt/empire-core/backend
ExecStart=/opt/empire-core/backend/venv/bin/python /opt/empire-core/backend/app/signal_engine.py
Restart=always

[Install]
WantedBy=multi-user.target

### UNIT_SHOW_REDACTED
Restart=always
Result=exit-code
NRestarts=5
ExecMainStatus=203
ExecStart={ path=/opt/empire-core/backend/venv/bin/python ; argv[]=/opt/empire-core/backend/venv/bin/python /opt/empire-core/backend/app/signal_engine.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
WorkingDirectory=/opt/empire-core/backend
User=nawaf511
Id=signal-engine.service
Names=signal-engine.service
Description=Empire Core Signal Engine
LoadState=loaded
ActiveState=failed
SubState=failed
FragmentPath=/etc/systemd/system/signal-engine.service
UnitFileState=enabled

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started signal-engine.service - Empire Core Signal Engine.
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started signal-engine.service - Empire Core Signal Engine.
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started signal-engine.service - Empire Core Signal Engine.
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: signal-engine.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started signal-engine.service - Empire Core Signal Engine.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started signal-engine.service - Empire Core Signal Engine.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Start request repeated too quickly.
يوليو 05 12:00:09 vmi2934783 systemd[1]: signal-engine.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Failed to start signal-engine.service - Empire Core Signal Engine.

### PATH_EXISTENCE_CHECK
PATH_MISSING=/opt/empire-core/backend
PATH_MISSING=/opt/empire-core/backend/app/signal_engine.py
PATH_MISSING=/opt/empire-core/backend/venv/bin/python
PATHS_MISSING_COUNT=3

### PROJECT_REFERENCES_CONTEXT
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES_CONTEXT
NGINX_REFS_COUNT=0

### PORT_AND_PROCESS_EVIDENCE
LISTEN 0      511        127.0.0.1:9041      0.0.0.0:*    users:(("node",pid=2676,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9044      0.0.0.0:*    users:(("node",pid=1345,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9047      0.0.0.0:*    users:(("python3",pid=3532117,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9024      0.0.0.0:*    users:(("node",pid=2632,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9027      0.0.0.0:*    users:(("node",pid=2655,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9030      0.0.0.0:*    users:(("node",pid=2633,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9031      0.0.0.0:*    users:(("node",pid=2636,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9033      0.0.0.0:*    users:(("node",pid=1388,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9034      0.0.0.0:*    users:(("node",pid=1400,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9074      0.0.0.0:*    users:(("uvicorn",pid=3532176,fd=6))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9076      0.0.0.0:*    users:(("uvicorn",pid=3532178,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9077      0.0.0.0:*    users:(("node",pid=1335,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1339,fd=33))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1343,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1337,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1340,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=3532132,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9083      0.0.0.0:*    users:(("python3",pid=3532150,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9084      0.0.0.0:*    users:(("python3",pid=3532154,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=3532223,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9061      0.0.0.0:*    users:(("uvicorn",pid=3532173,fd=6))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9062      0.0.0.0:*    users:(("node",pid=2680,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9064      0.0.0.0:*    users:(("node",pid=2679,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9065      0.0.0.0:*    users:(("uvicorn",pid=3532165,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9066      0.0.0.0:*    users:(("python3",pid=3532200,fd=13))                                                                                                                                                                                                                           
LISTEN 0      5          127.0.0.1:9067      0.0.0.0:*    users:(("python3",pid=3532131,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9068      0.0.0.0:*    users:(("python3",pid=3532221,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9069      0.0.0.0:*    users:(("uvicorn",pid=3532162,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9070      0.0.0.0:*    users:(("node",pid=2669,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9017      0.0.0.0:*    users:(("node",pid=2634,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2682,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9021      0.0.0.0:*    users:(("node",pid=1352,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9022      0.0.0.0:*    users:(("node",pid=2643,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9023      0.0.0.0:*    users:(("node",pid=2649,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=3532115,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=3532119,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9093      0.0.0.0:*    users:(("python3",pid=3532143,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511          0.0.0.0:3000      0.0.0.0:*    users:(("MainThread",pid=1099167,fd=21))                                                                                                                                                                                                                        
LISTEN 0      511        127.0.0.1:8097      0.0.0.0:*    users:(("node",pid=1389,fd=32))                                                                                                                                                                                                                                 
3532162 postgres       39:28 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
3532165 nawaf511       39:28 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
3532173 root           39:28 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
3532176 postgres       39:28 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
3532178 nawaf511       39:28 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
3532200 root           39:27 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
3532221 root           39:27 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
3697552 nawaf511       00:00 /home/nawaf511/empire-core-new/backend/venv/bin/python /home/nawaf511/empire-core-new/backend/venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:9002 --workers 4 --timeout 120
3697592 root           00:00 grep -E signal-engine|uvicorn|gunicorn|streamlit|signal_engine|run_watcher|app.main|server:app
3697593 root           00:00 tee /tmp/NDSP_P2_HOLD_REVIEW_DEEP_AUDIT_20260708_065226/signal-engine/process_matches.txt

### PRELIMINARY_DECISION
PRELIMINARY_DECISION=LIKELY_LEGACY_EXEC_PATH_MISSING_REVIEW_BEFORE_DISABLE

---- SERVICE=subscription-watcher.service ----
DESCRIPTION=Subscription Expiry Watcher
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/subscription-watcher.service
RESULT=exit-code
EXEC_MAIN_STATUS=2
RESTART_POLICY=always
N_RESTARTS=5

### UNIT_FILE_REDACTED
# /etc/systemd/system/subscription-watcher.service
[Unit]
Description=Subscription Expiry Watcher
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/empire-core/backend/app/engine/run_watcher.py
Restart=always

[Install]
WantedBy=multi-user.target

### UNIT_SHOW_REDACTED
Restart=always
Result=exit-code
NRestarts=5
ExecMainStatus=2
ExecStart={ path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/empire-core/backend/app/engine/run_watcher.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
Id=subscription-watcher.service
Names=subscription-watcher.service
Description=Subscription Expiry Watcher
LoadState=loaded
ActiveState=failed
SubState=failed
FragmentPath=/etc/systemd/system/subscription-watcher.service
UnitFileState=enabled

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started subscription-watcher.service - Subscription Expiry Watcher.
يوليو 05 12:00:08 vmi2934783 python3[1366]: /usr/bin/python3: can't open file '/opt/empire-core/backend/app/engine/run_watcher.py': [Errno 2] No such file or directory
يوليو 05 12:00:08 vmi2934783 systemd[1]: subscription-watcher.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
يوليو 05 12:00:08 vmi2934783 systemd[1]: subscription-watcher.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: subscription-watcher.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started subscription-watcher.service - Subscription Expiry Watcher.
يوليو 05 12:00:08 vmi2934783 python3[1501]: /usr/bin/python3: can't open file '/opt/empire-core/backend/app/engine/run_watcher.py': [Errno 2] No such file or directory
يوليو 05 12:00:08 vmi2934783 systemd[1]: subscription-watcher.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
يوليو 05 12:00:08 vmi2934783 systemd[1]: subscription-watcher.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: subscription-watcher.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started subscription-watcher.service - Subscription Expiry Watcher.
يوليو 05 12:00:09 vmi2934783 python3[1572]: /usr/bin/python3: can't open file '/opt/empire-core/backend/app/engine/run_watcher.py': [Errno 2] No such file or directory
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started subscription-watcher.service - Subscription Expiry Watcher.
يوليو 05 12:00:09 vmi2934783 python3[1698]: /usr/bin/python3: can't open file '/opt/empire-core/backend/app/engine/run_watcher.py': [Errno 2] No such file or directory
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started subscription-watcher.service - Subscription Expiry Watcher.
يوليو 05 12:00:09 vmi2934783 python3[1761]: /usr/bin/python3: can't open file '/opt/empire-core/backend/app/engine/run_watcher.py': [Errno 2] No such file or directory
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
يوليو 05 12:00:09 vmi2934783 systemd[1]: subscription-watcher.service: Failed with result 'exit-code'.
يوليو 05 12:00:10 vmi2934783 systemd[1]: subscription-watcher.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:10 vmi2934783 systemd[1]: subscription-watcher.service: Start request repeated too quickly.
يوليو 05 12:00:10 vmi2934783 systemd[1]: subscription-watcher.service: Failed with result 'exit-code'.
يوليو 05 12:00:10 vmi2934783 systemd[1]: Failed to start subscription-watcher.service - Subscription Expiry Watcher.

### PATH_EXISTENCE_CHECK
PATH_MISSING=/opt/empire-core/backend/app/engine/run_watcher.py
PATH_OK=/usr/bin/python3 TYPE=symbolic link OWNER=root GROUP=root MODE=lrwxrwxrwx
PATHS_MISSING_COUNT=1

### PROJECT_REFERENCES_CONTEXT
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES_CONTEXT
NGINX_REFS_COUNT=0

### PORT_AND_PROCESS_EVIDENCE
LISTEN 0      511        127.0.0.1:9041      0.0.0.0:*    users:(("node",pid=2676,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9044      0.0.0.0:*    users:(("node",pid=1345,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9047      0.0.0.0:*    users:(("python3",pid=3532117,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9024      0.0.0.0:*    users:(("node",pid=2632,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9027      0.0.0.0:*    users:(("node",pid=2655,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9030      0.0.0.0:*    users:(("node",pid=2633,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9031      0.0.0.0:*    users:(("node",pid=2636,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9033      0.0.0.0:*    users:(("node",pid=1388,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9034      0.0.0.0:*    users:(("node",pid=1400,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9074      0.0.0.0:*    users:(("uvicorn",pid=3532176,fd=6))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9076      0.0.0.0:*    users:(("uvicorn",pid=3532178,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9077      0.0.0.0:*    users:(("node",pid=1335,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1339,fd=33))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1343,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1337,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1340,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=3532132,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9083      0.0.0.0:*    users:(("python3",pid=3532150,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9084      0.0.0.0:*    users:(("python3",pid=3532154,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=3532223,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9061      0.0.0.0:*    users:(("uvicorn",pid=3532173,fd=6))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9062      0.0.0.0:*    users:(("node",pid=2680,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9064      0.0.0.0:*    users:(("node",pid=2679,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9065      0.0.0.0:*    users:(("uvicorn",pid=3532165,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9066      0.0.0.0:*    users:(("python3",pid=3532200,fd=13))                                                                                                                                                                                                                           
LISTEN 0      5          127.0.0.1:9067      0.0.0.0:*    users:(("python3",pid=3532131,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9068      0.0.0.0:*    users:(("python3",pid=3532221,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9069      0.0.0.0:*    users:(("uvicorn",pid=3532162,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9070      0.0.0.0:*    users:(("node",pid=2669,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9017      0.0.0.0:*    users:(("node",pid=2634,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2682,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9021      0.0.0.0:*    users:(("node",pid=1352,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9022      0.0.0.0:*    users:(("node",pid=2643,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9023      0.0.0.0:*    users:(("node",pid=2649,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=3532115,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=3532119,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9093      0.0.0.0:*    users:(("python3",pid=3532143,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511          0.0.0.0:3000      0.0.0.0:*    users:(("MainThread",pid=1099167,fd=21))                                                                                                                                                                                                                        
LISTEN 0      511        127.0.0.1:8097      0.0.0.0:*    users:(("node",pid=1389,fd=32))                                                                                                                                                                                                                                 
3532162 postgres       39:31 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
3532165 nawaf511       39:31 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
3532173 root           39:31 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
3532176 postgres       39:31 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
3532178 nawaf511       39:31 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
3532200 root           39:30 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
3532221 root           39:30 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
3697552 nawaf511       00:02 /home/nawaf511/empire-core-new/backend/venv/bin/python /home/nawaf511/empire-core-new/backend/venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:9002 --workers 4 --timeout 120
3697800 root           00:00 grep -E subscription-watcher|uvicorn|gunicorn|streamlit|signal_engine|run_watcher|app.main|server:app
3697801 root           00:00 tee /tmp/NDSP_P2_HOLD_REVIEW_DEEP_AUDIT_20260708_065226/subscription-watcher/process_matches.txt

### PRELIMINARY_DECISION
PRELIMINARY_DECISION=LIKELY_LEGACY_MISSING_FILE_REVIEW_BEFORE_DISABLE

---- SERVICE=testapp.service ----
DESCRIPTION=testapp Service
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/testapp.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
RESTART_POLICY=always
N_RESTARTS=5

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

### UNIT_SHOW_REDACTED
Restart=always
Result=exit-code
NRestarts=5
ExecMainStatus=203
ExecStart={ path=/srv/testapp/venv/bin/streamlit ; argv[]=/srv/testapp/venv/bin/streamlit run /srv/testapp/app.py --server.port=8521 --server.address=127.0.0.1 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
WorkingDirectory=/srv/testapp
User=testapp
Id=testapp.service
Names=testapp.service
Description=testapp Service
LoadState=loaded
ActiveState=failed
SubState=failed
FragmentPath=/etc/systemd/system/testapp.service
UnitFileState=enabled

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started testapp.service - testapp Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started testapp.service - testapp Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started testapp.service - testapp Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: testapp.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started testapp.service - testapp Service.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started testapp.service - testapp Service.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Start request repeated too quickly.
يوليو 05 12:00:09 vmi2934783 systemd[1]: testapp.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Failed to start testapp.service - testapp Service.

### PATH_EXISTENCE_CHECK
PATH_OK=/srv/testapp TYPE=directory OWNER=testapp GROUP=testapp MODE=drwxr-xr-x
PATH_MISSING=/srv/testapp/app.py
PATH_MISSING=/srv/testapp/venv/bin/streamlit
PATHS_MISSING_COUNT=2

### PROJECT_REFERENCES_CONTEXT
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

### NGINX_REFERENCES_CONTEXT
NGINX_REFS_COUNT=0

### PORT_AND_PROCESS_EVIDENCE
LISTEN 0      511        127.0.0.1:9041      0.0.0.0:*    users:(("node",pid=2676,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9044      0.0.0.0:*    users:(("node",pid=1345,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9047      0.0.0.0:*    users:(("python3",pid=3532117,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9024      0.0.0.0:*    users:(("node",pid=2632,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9027      0.0.0.0:*    users:(("node",pid=2655,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9030      0.0.0.0:*    users:(("node",pid=2633,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9031      0.0.0.0:*    users:(("node",pid=2636,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9033      0.0.0.0:*    users:(("node",pid=1388,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9034      0.0.0.0:*    users:(("node",pid=1400,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9074      0.0.0.0:*    users:(("uvicorn",pid=3532176,fd=6))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9076      0.0.0.0:*    users:(("uvicorn",pid=3532178,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9077      0.0.0.0:*    users:(("node",pid=1335,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1339,fd=33))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1343,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1337,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1340,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=3532132,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9083      0.0.0.0:*    users:(("python3",pid=3532150,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9084      0.0.0.0:*    users:(("python3",pid=3532154,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=3532223,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9061      0.0.0.0:*    users:(("uvicorn",pid=3532173,fd=6))                                                                                                                                                                                                                            
LISTEN 0      511        127.0.0.1:9062      0.0.0.0:*    users:(("node",pid=2680,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9064      0.0.0.0:*    users:(("node",pid=2679,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      2048       127.0.0.1:9065      0.0.0.0:*    users:(("uvicorn",pid=3532165,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9066      0.0.0.0:*    users:(("python3",pid=3532200,fd=13))                                                                                                                                                                                                                           
LISTEN 0      5          127.0.0.1:9067      0.0.0.0:*    users:(("python3",pid=3532131,fd=3))                                                                                                                                                                                                                            
LISTEN 0      2048       127.0.0.1:9068      0.0.0.0:*    users:(("python3",pid=3532221,fd=13))                                                                                                                                                                                                                           
LISTEN 0      2048       127.0.0.1:9069      0.0.0.0:*    users:(("uvicorn",pid=3532162,fd=13))                                                                                                                                                                                                                           
LISTEN 0      511        127.0.0.1:9070      0.0.0.0:*    users:(("node",pid=2669,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9017      0.0.0.0:*    users:(("node",pid=2634,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2664,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2682,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9021      0.0.0.0:*    users:(("node",pid=1352,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9022      0.0.0.0:*    users:(("node",pid=2643,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9023      0.0.0.0:*    users:(("node",pid=2649,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=3532115,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=3532119,fd=3))                                                                                                                                                                                                                            
LISTEN 0      5          127.0.0.1:9093      0.0.0.0:*    users:(("python3",pid=3532143,fd=3))                                                                                                                                                                                                                            
LISTEN 0      511          0.0.0.0:3000      0.0.0.0:*    users:(("MainThread",pid=1099167,fd=21))                                                                                                                                                                                                                        
LISTEN 0      511        127.0.0.1:8097      0.0.0.0:*    users:(("node",pid=1389,fd=32))                                                                                                                                                                                                                                 
3532162 postgres       39:34 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
3532165 nawaf511       39:34 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
3532173 root           39:34 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
3532176 postgres       39:34 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
3532178 nawaf511       39:33 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
3532200 root           39:33 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
3532221 root           39:32 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
3697982 root           00:00 grep -E testapp|uvicorn|gunicorn|streamlit|signal_engine|run_watcher|app.main|server:app
3697983 root           00:00 tee /tmp/NDSP_P2_HOLD_REVIEW_DEEP_AUDIT_20260708_065226/testapp/process_matches.txt

### PRELIMINARY_DECISION
PRELIMINARY_DECISION=HAS_PROJECT_REFS_DEEP_REVIEW_REQUIRED

## 4) Hold-review summary
service                       enabled   active  failed  result     exec_status  project_refs  nginx_refs  paths_missing  preliminary_decision
ndip-api-new.service          disabled  failed  failed  exit-code  1            2             0           0              REVIEW_IMPORT_PATH_OR_LEGACY_BACKEND
signal-engine.service         enabled   failed  failed  exit-code  203          0             0           3              LIKELY_LEGACY_EXEC_PATH_MISSING_REVIEW_BEFORE_DISABLE
subscription-watcher.service  enabled   failed  failed  exit-code  2            0             0           1              LIKELY_LEGACY_MISSING_FILE_REVIEW_BEFORE_DISABLE
testapp.service               enabled   failed  failed  exit-code  203          28            0           2              HAS_PROJECT_REFS_DEEP_REVIEW_REQUIRED

## 5) Critical runtime safety after audit
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.9%[39m | [1mram usage[22m: [32m10%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.204mb/s[39m [90m/[39m [1m[33m81.99%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

FINAL_STATUS=P2_HOLD_REVIEW_SERVICES_DEEP_AUDIT_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_HOLD_REVIEW_SERVICES_DEEP_AUDIT_READONLY_20260708_065226.md
ARTIFACT_DIR=/tmp/NDSP_P2_HOLD_REVIEW_DEEP_AUDIT_20260708_065226
