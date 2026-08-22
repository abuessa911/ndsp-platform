# NDSP P2 Failed Services Classification Read-only
DATE=2026-07-08T06:23:40+02:00
MODE=READ_ONLY_FAILED_SERVICES_CLASSIFICATION
MODIFICATIONS=None
NO_DISABLE=1
NO_STOP=1
NO_DELETE=1
NO_REBOOT=1

## 1) Current failed units
  UNIT                         LOAD   ACTIVE SUB    DESCRIPTION
● fanno-comments.service       loaded failed failed Fanno Comment Service
● marketpulse.service          loaded failed failed MarketPulse Backend Service
● ndip-api-new.service         loaded failed failed NDIP API - New Backend
● redis-replica.service        loaded failed failed Redis Replica
● redis-sentinel.service       loaded failed failed Redis Sentinel
● signal-engine.service        loaded failed failed Empire Core Signal Engine
● subscription-watcher.service loaded failed failed Subscription Expiry Watcher
● testapp.service              loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

8 loaded units listed.

## 2) Critical runtime safety before classification
nginx=active
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.5%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ [32m0.009mb/s[39m ⇑ [32m0.38mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 3) Service-by-service classification evidence

---- SERVICE=fanno-comments.service ----
DESCRIPTION=Fanno Comment Service
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/fanno-comments.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
RESTART_POLICY=always

### UNIT_FILE_REDACTED
# /etc/systemd/system/fanno-comments.service
[Unit]
Description=Fanno Comment Service
After=network.target

[Service]
User=nawaf511
WorkingDirectory=/opt/fanno_comments
ExecStart=/opt/fanno_comments/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started fanno-comments.service - Fanno Comment Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started fanno-comments.service - Fanno Comment Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started fanno-comments.service - Fanno Comment Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: fanno-comments.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started fanno-comments.service - Fanno Comment Service.
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started fanno-comments.service - Fanno Comment Service.
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Start request repeated too quickly.
يوليو 05 12:00:09 vmi2934783 systemd[1]: fanno-comments.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Failed to start fanno-comments.service - Fanno Comment Service.

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=LEGACY_CANDIDATE_IF_NO_ACTIVE_REFERENCES

---- SERVICE=marketpulse.service ----
DESCRIPTION=MarketPulse Backend Service
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/marketpulse.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
RESTART_POLICY=always

### UNIT_FILE_REDACTED
# /etc/systemd/system/marketpulse.service
[Unit]
Description=MarketPulse Backend Service
After=network.target

[Service]
User=nawaf511
WorkingDirectory=/home/nawaf511/marketpulse
Environment="MARKETPULSE_SECRET=[REDACTED]
Environment="TELEGRAM_BOT_TOKEN=[REDACTED]
ExecStart=/home/nawaf511/marketpulse/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          server:app

Restart=always

[Install]
WantedBy=multi-user.target

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started marketpulse.service - MarketPulse Backend Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started marketpulse.service - MarketPulse Backend Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started marketpulse.service - MarketPulse Backend Service.
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: marketpulse.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started marketpulse.service - MarketPulse Backend Service.
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started marketpulse.service - MarketPulse Backend Service.
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Main process exited, code=exited, status=203/EXEC
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Start request repeated too quickly.
يوليو 05 12:00:09 vmi2934783 systemd[1]: marketpulse.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Failed to start marketpulse.service - MarketPulse Backend Service.

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=LEGACY_CANDIDATE_IF_NO_ACTIVE_REFERENCES

---- SERVICE=ndip-api-new.service ----
DESCRIPTION=NDIP API - New Backend
ACTIVE=failed
ENABLED=disabled
FAILED=failed
FRAGMENT=/etc/systemd/system/ndip-api-new.service
RESULT=exit-code
EXEC_MAIN_STATUS=1
RESTART_POLICY=always

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

### RECENT_JOURNAL_REDACTED
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

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=2

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=NEEDS_REVIEW_HAS_REFERENCES

---- SERVICE=redis-replica.service ----
DESCRIPTION=Redis Replica
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/redis-replica.service
RESULT=start-limit-hit
EXEC_MAIN_STATUS=0
RESTART_POLICY=always

### UNIT_FILE_REDACTED
# /etc/systemd/system/redis-replica.service
[Unit]
Description=Redis Replica
After=network.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis/redis-replica.conf
Restart=always
User=redis
Group=redis

[Install]
WantedBy=multi-user.target

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started redis-replica.service - Redis Replica.
يوليو 05 12:00:08 vmi2934783 redis-server[1360]: 1360:C 05 Jul 2026 12:00:08.221 # systemd supervision error: NOTIFY_SOCKET not found!
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-replica.service: Deactivated successfully.
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-replica.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started redis-replica.service - Redis Replica.
يوليو 05 12:00:08 vmi2934783 redis-server[1478]: 1478:C 05 Jul 2026 12:00:08.718 # systemd supervision error: NOTIFY_SOCKET not found!
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-replica.service: Deactivated successfully.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-replica.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started redis-replica.service - Redis Replica.
يوليو 05 12:00:09 vmi2934783 redis-server[1595]: 1595:C 05 Jul 2026 12:00:09.145 # systemd supervision error: NOTIFY_SOCKET not found!
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-replica.service: Deactivated successfully.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-replica.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started redis-replica.service - Redis Replica.
يوليو 05 12:00:09 vmi2934783 redis-server[1701]: 1701:C 05 Jul 2026 12:00:09.462 # systemd supervision error: NOTIFY_SOCKET not found!
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-replica.service: Deactivated successfully.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-replica.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started redis-replica.service - Redis Replica.
يوليو 05 12:00:10 vmi2934783 redis-server[1782]: 1782:C 05 Jul 2026 12:00:09.996 # systemd supervision error: NOTIFY_SOCKET not found!
يوليو 05 12:00:10 vmi2934783 systemd[1]: redis-replica.service: Deactivated successfully.
يوليو 05 12:00:10 vmi2934783 systemd[1]: redis-replica.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:10 vmi2934783 systemd[1]: redis-replica.service: Start request repeated too quickly.
يوليو 05 12:00:10 vmi2934783 systemd[1]: redis-replica.service: Failed with result 'start-limit-hit'.
يوليو 05 12:00:10 vmi2934783 systemd[1]: Failed to start redis-replica.service - Redis Replica.

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=LEGACY_CANDIDATE_REDIS_SECONDARY_NOT_PRIMARY

---- SERVICE=redis-sentinel.service ----
DESCRIPTION=Redis Sentinel
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/redis-sentinel.service
RESULT=exit-code
EXEC_MAIN_STATUS=1
RESTART_POLICY=always

### UNIT_FILE_REDACTED
# /etc/systemd/system/redis-sentinel.service
[Unit]
Description=Redis Sentinel
After=network.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis/sentinel.conf --sentinel
Restart=always
User=redis
Group=redis

[Install]
WantedBy=multi-user.target

### RECENT_JOURNAL_REDACTED
يوليو 05 12:00:07 vmi2934783 systemd[1]: Started redis-sentinel.service - Redis Sentinel.
يوليو 05 12:00:08 vmi2934783 redis-server[1361]: 1361:X 05 Jul 2026 12:00:08.223 # Sentinel config file /etc/redis/sentinel.conf is not writable: Permission denied. Exiting...
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 redis-server[1484]: 1484:X 05 Jul 2026 12:00:08.652 # Sentinel config file /etc/redis/sentinel.conf is not writable: Permission denied. Exiting...
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Scheduled restart job, restart counter is at 1.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started redis-sentinel.service - Redis Sentinel.
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Failed with result 'exit-code'.
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Scheduled restart job, restart counter is at 2.
يوليو 05 12:00:08 vmi2934783 systemd[1]: Started redis-sentinel.service - Redis Sentinel.
يوليو 05 12:00:08 vmi2934783 redis-server[1560]: 1560:X 05 Jul 2026 12:00:08.962 # Sentinel config file /etc/redis/sentinel.conf is not writable: Permission denied. Exiting...
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 12:00:08 vmi2934783 systemd[1]: redis-sentinel.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Scheduled restart job, restart counter is at 3.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started redis-sentinel.service - Redis Sentinel.
يوليو 05 12:00:09 vmi2934783 redis-server[1597]: 1597:X 05 Jul 2026 12:00:09.160 # Sentinel config file /etc/redis/sentinel.conf is not writable: Permission denied. Exiting...
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Scheduled restart job, restart counter is at 4.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Started redis-sentinel.service - Redis Sentinel.
يوليو 05 12:00:09 vmi2934783 redis-server[1696]: 1696:X 05 Jul 2026 12:00:09.412 # Sentinel config file /etc/redis/sentinel.conf is not writable: Permission denied. Exiting...
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Scheduled restart job, restart counter is at 5.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Start request repeated too quickly.
يوليو 05 12:00:09 vmi2934783 systemd[1]: redis-sentinel.service: Failed with result 'exit-code'.
يوليو 05 12:00:09 vmi2934783 systemd[1]: Failed to start redis-sentinel.service - Redis Sentinel.

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=LEGACY_CANDIDATE_REDIS_SECONDARY_NOT_PRIMARY

---- SERVICE=signal-engine.service ----
DESCRIPTION=Empire Core Signal Engine
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/signal-engine.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
RESTART_POLICY=always

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

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=NEEDS_REVIEW

---- SERVICE=subscription-watcher.service ----
DESCRIPTION=Subscription Expiry Watcher
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/subscription-watcher.service
RESULT=exit-code
EXEC_MAIN_STATUS=2
RESTART_POLICY=always

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

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=0

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=NEEDS_REVIEW

---- SERVICE=testapp.service ----
DESCRIPTION=testapp Service
ACTIVE=failed
ENABLED=enabled
FAILED=failed
FRAGMENT=/etc/systemd/system/testapp.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
RESTART_POLICY=always

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

### PROJECT_REFERENCES
PROJECT_REFS_COUNT=8

### NGINX_REFERENCES
NGINX_REFS_COUNT=0
PRELIMINARY_CLASSIFICATION=LEGACY_CANDIDATE_IF_NO_ACTIVE_REFERENCES_HAS_REFERENCES

## 4) Summary table
service                       active  enabled   failed  fragment                                          project_refs  nginx_refs  classification
fanno-comments.service        failed  enabled   failed  /etc/systemd/system/fanno-comments.service        0             0           LEGACY_CANDIDATE_IF_NO_ACTIVE_REFERENCES
marketpulse.service           failed  enabled   failed  /etc/systemd/system/marketpulse.service           0             0           LEGACY_CANDIDATE_IF_NO_ACTIVE_REFERENCES
ndip-api-new.service          failed  disabled  failed  /etc/systemd/system/ndip-api-new.service          2             0           NEEDS_REVIEW_HAS_REFERENCES
redis-replica.service         failed  enabled   failed  /etc/systemd/system/redis-replica.service         0             0           LEGACY_CANDIDATE_REDIS_SECONDARY_NOT_PRIMARY
redis-sentinel.service        failed  enabled   failed  /etc/systemd/system/redis-sentinel.service        0             0           LEGACY_CANDIDATE_REDIS_SECONDARY_NOT_PRIMARY
signal-engine.service         failed  enabled   failed  /etc/systemd/system/signal-engine.service         0             0           NEEDS_REVIEW
subscription-watcher.service  failed  enabled   failed  /etc/systemd/system/subscription-watcher.service  0             0           NEEDS_REVIEW
testapp.service               failed  enabled   failed  /etc/systemd/system/testapp.service               8             0           LEGACY_CANDIDATE_IF_NO_ACTIVE_REFERENCES_HAS_REFERENCES

## 5) Final runtime safety after classification
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m15.9%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.017mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ [1m[31m22.243mb/s[39m[22m ⇑ [32m0.321mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

FINAL_STATUS=P2_FAILED_SERVICES_CLASSIFICATION_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_FAILED_SERVICES_CLASSIFICATION_READONLY_20260708_062340.md
