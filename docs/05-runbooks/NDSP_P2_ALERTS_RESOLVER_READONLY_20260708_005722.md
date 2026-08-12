# NDSP P2 Alerts Resolver Read-only
DATE=2026-07-08T00:57:22+02:00
MODE=READ_ONLY_ALERTS_RESOLUTION
MODIFICATIONS=None

## 1) Failed Units Classification
certbot.service
fanno-comments.service
logrotate.service
marketpulse.service
ndip-api-new.service
ndsp-real-feeds-sync.service
ndsp-tradingview-calendar.service
redis-replica.service
redis-sentinel.service
signal-engine.service
subscription-watcher.service
testapp.service
FAILED_UNITS_COUNT=12

## 2) Failed Units Details

### FAILED_SERVICE=certbot.service
ENABLED=static
ACTIVE=failed
× certbot.service - Certbot
     Loaded: loaded (/usr/lib/systemd/system/certbot.service; static)
     Active: failed (Result: exit-code) since Tue 2026-07-07 14:36:44 CEST; 10h ago
TriggeredBy: ● certbot.timer
       Docs: file:///usr/share/doc/python-certbot-doc/html/index.html
             https://certbot.eff.org/docs
   Main PID: 3951735 (code=exited, status=1/FAILURE)
        CPU: 10.925s

### FAILED_SERVICE=fanno-comments.service
ENABLED=enabled
ACTIVE=failed
× fanno-comments.service - Fanno Comment Service
     Loaded: loaded (/etc/systemd/system/fanno-comments.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-07-05 12:00:09 CEST; 2 days ago
   Duration: 14ms
   Main PID: 1619 (code=exited, status=203/EXEC)
        CPU: 2ms

### FAILED_SERVICE=logrotate.service
ENABLED=static
ACTIVE=failed
× logrotate.service - Rotate log files
     Loaded: loaded (/usr/lib/systemd/system/logrotate.service; static)
     Active: failed (Result: exit-code) since Wed 2026-07-08 00:00:05 CEST; 57min ago
TriggeredBy: ● logrotate.timer
       Docs: man:logrotate(8)
             man:logrotate.conf(5)
   Main PID: 2029717 (code=exited, status=1/FAILURE)
        CPU: 1.173s

### FAILED_SERVICE=marketpulse.service
ENABLED=enabled
ACTIVE=failed
× marketpulse.service - MarketPulse Backend Service
     Loaded: loaded (/etc/systemd/system/marketpulse.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-07-05 12:00:09 CEST; 2 days ago
   Duration: 68ms
   Main PID: 1620 (code=exited, status=203/EXEC)
        CPU: 18ms

### FAILED_SERVICE=ndip-api-new.service
ENABLED=disabled
ACTIVE=failed
× ndip-api-new.service - NDIP API - New Backend
     Loaded: loaded (/etc/systemd/system/ndip-api-new.service; disabled; preset: enabled)
    Drop-In: /etc/systemd/system/ndip-api-new.service.d
             └─10-mt4-dir.conf
     Active: failed (Result: exit-code) since Sun 2026-07-05 13:08:33 CEST; 2 days ago
   Duration: 280ms
   Main PID: 496467 (code=exited, status=1/FAILURE)
        CPU: 269ms

### FAILED_SERVICE=ndsp-real-feeds-sync.service
ENABLED=static
ACTIVE=failed
× ndsp-real-feeds-sync.service - NDSP Real Feeds Sync
     Loaded: loaded (/etc/systemd/system/ndsp-real-feeds-sync.service; static)
     Active: failed (Result: exit-code) since Wed 2026-07-08 00:54:01 CEST; 3min 22s ago
TriggeredBy: ● ndsp-real-feeds-sync.timer
    Process: 2256333 ExecStart=/usr/bin/python3 /home/nawaf511/ndsp-portal-real-data-sync/sync_real_feeds.py (code=exited, status=1/FAILURE)
   Main PID: 2256333 (code=exited, status=1/FAILURE)
        CPU: 225ms

يوليو 08 00:54:01 vmi2934783 python3[2256333]:     write("news-impact.json", {
يوليو 08 00:54:01 vmi2934783 python3[2256333]:   File "/home/nawaf511/ndsp-portal-real-data-sync/sync_real_feeds.py", line 16, in write
يوليو 08 00:54:01 vmi2934783 python3[2256333]:     (DATA / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
يوليو 08 00:54:01 vmi2934783 python3[2256333]:   File "/usr/lib/python3.12/pathlib.py", line 1049, in write_text
يوليو 08 00:54:01 vmi2934783 python3[2256333]:     with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
يوليو 08 00:54:01 vmi2934783 python3[2256333]:          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
يوليو 08 00:54:01 vmi2934783 python3[2256333]:   File "/usr/lib/python3.12/pathlib.py", line 1015, in open
يوليو 08 00:54:01 vmi2934783 python3[2256333]:     return io.open(self, mode, buffering, encoding, errors, newline)
يوليو 08 00:54:01 vmi2934783 python3[2256333]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
يوليو 08 00:54:01 vmi2934783 python3[2256333]: PermissionError: [Errno 13] Permission denied: '/var/www/ndsp-my/data/news-impact.json'

### FAILED_SERVICE=ndsp-tradingview-calendar.service
ENABLED=static
ACTIVE=failed
× ndsp-tradingview-calendar.service - NDSP TradingView Live Economic Calendar
     Loaded: loaded (/etc/systemd/system/ndsp-tradingview-calendar.service; static)
     Active: failed (Result: exit-code) since Wed 2026-07-08 00:54:01 CEST; 3min 22s ago
TriggeredBy: ● ndsp-tradingview-calendar.timer
    Process: 2256335 ExecStart=/usr/bin/python3 /home/nawaf511/ndsp-portal-real-data-sync/tradingview_live_calendar.py (code=exited, status=1/FAILURE)
   Main PID: 2256335 (code=exited, status=1/FAILURE)
        CPU: 293ms

يوليو 08 00:54:01 vmi2934783 python3[2256335]: During handling of the above exception, another exception occurred:
يوليو 08 00:54:01 vmi2934783 python3[2256335]: Traceback (most recent call last):
يوليو 08 00:54:01 vmi2934783 python3[2256335]:   File "/home/nawaf511/ndsp-portal-real-data-sync/tradingview_live_calendar.py", line 99, in <module>
يوليو 08 00:54:01 vmi2934783 python3[2256335]:     main()
يوليو 08 00:54:01 vmi2934783 python3[2256335]:   File "/home/nawaf511/ndsp-portal-real-data-sync/tradingview_live_calendar.py", line 87, in main
يوليو 08 00:54:01 vmi2934783 python3[2256335]:     write(OUT,{
يوليو 08 00:54:01 vmi2934783 python3[2256335]:   File "/home/nawaf511/ndsp-portal-real-data-sync/tradingview_live_calendar.py", line 16, in write
يوليو 08 00:54:01 vmi2934783 python3[2256335]:     with open(tmp,"w",encoding="utf-8") as f:
يوليو 08 00:54:01 vmi2934783 python3[2256335]:          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
يوليو 08 00:54:01 vmi2934783 python3[2256335]: PermissionError: [Errno 13] Permission denied: '/var/www/ndsp-my/data/economic-calendar.json.tmp'

### FAILED_SERVICE=redis-replica.service
ENABLED=enabled
ACTIVE=failed
× redis-replica.service - Redis Replica
     Loaded: loaded (/etc/systemd/system/redis-replica.service; enabled; preset: enabled)
     Active: failed (Result: start-limit-hit) since Sun 2026-07-05 12:00:10 CEST; 2 days ago
   Duration: 79ms
   Main PID: 1782 (code=exited, status=0/SUCCESS)
        CPU: 33ms

### FAILED_SERVICE=redis-sentinel.service
ENABLED=enabled
ACTIVE=failed
× redis-sentinel.service - Redis Sentinel
     Loaded: loaded (/etc/systemd/system/redis-sentinel.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-07-05 12:00:09 CEST; 2 days ago
   Duration: 127ms
   Main PID: 1696 (code=exited, status=1/FAILURE)
        CPU: 60ms

### FAILED_SERVICE=signal-engine.service
ENABLED=enabled
ACTIVE=failed
× signal-engine.service - Empire Core Signal Engine
     Loaded: loaded (/etc/systemd/system/signal-engine.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-07-05 12:00:09 CEST; 2 days ago
   Duration: 179ms
   Main PID: 1692 (code=exited, status=203/EXEC)
        CPU: 33ms

### FAILED_SERVICE=subscription-watcher.service
ENABLED=enabled
ACTIVE=failed
× subscription-watcher.service - Subscription Expiry Watcher
     Loaded: loaded (/etc/systemd/system/subscription-watcher.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-07-05 12:00:10 CEST; 2 days ago
   Duration: 200ms
   Main PID: 1761 (code=exited, status=2)
        CPU: 96ms

### FAILED_SERVICE=testapp.service
ENABLED=enabled
ACTIVE=failed
× testapp.service - testapp Service
     Loaded: loaded (/etc/systemd/system/testapp.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-07-05 12:00:09 CEST; 2 days ago
   Duration: 45ms
   Main PID: 1699 (code=exited, status=203/EXEC)
        CPU: 16ms

## 3) PM2 Startup Deep Check
### pm2 list as nawaf511
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m8.7%[39m | [1mram usage[22m: [32m9.7%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.114mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.129mb/s[39m [90m/[39m [1m[33m81.99%[39m[22m |

### pm2 dump
PM2_DUMP_EXISTS=1
PM2_DUMP_SIZE=11196 PM2_DUMP_UPDATED=2026-07-07 09:26:49.733544741 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

### pm2 systemd unit
PM2_SERVICE_ENABLED=enabled
PM2_SERVICE_ACTIVE=inactive
# /etc/systemd/system/pm2-nawaf511.service
[Unit]
Description=PM2 process manager
Documentation=https://pm2.keymetrics.io/
After=network.target

[Service]
Type=forking
User=nawaf511
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/bin:/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
Environment=PM2_HOME=/home/nawaf511/.pm2
PIDFile=/home/nawaf511/.pm2/pm2.pid
Restart=on-failure

ExecStart=/home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/pm2/bin/pm2 resurrect
ExecReload=/home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/pm2/bin/pm2 reload all
ExecStop=/home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/pm2/bin/pm2 kill

[Install]
WantedBy=multi-user.target
○ pm2-nawaf511.service - PM2 process manager
     Loaded: loaded (/etc/systemd/system/pm2-nawaf511.service; enabled; preset: enabled)
     Active: inactive (dead) since Sun 2026-07-05 14:32:49 CEST; 2 days ago
   Duration: 2h 32min 32.986s
       Docs: https://pm2.keymetrics.io/
   Main PID: 3004 (code=exited, status=0/SUCCESS)
        CPU: 2h 59min 421ms

يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: ├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 3895     │ 0s     │ 0    │ online    │ 0%       │ 40.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 3883     │ 0s     │ 0    │ online    │ 0%       │ 19.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: └────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] Applying action deleteProcessId on app [all](ids: [ 0, 1 ])
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-portal](0) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-backend](1) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] All Applications Stopped
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] PM2 Daemon Stopped

## 4) Nginx Runtime Check
NGINX_ACTIVE=active
NGINX_ENABLED=enabled
NGINX_NOTE=sudo nginx -t required later if approved; prior non-sudo nginx -t hit permission denied on /run/nginx.pid

## 5) Certbot and Logrotate Snapshot

### SERVICE=certbot.service
ENABLED=static
ACTIVE=failed
× certbot.service - Certbot
     Loaded: loaded (/usr/lib/systemd/system/certbot.service; static)
     Active: failed (Result: exit-code) since Tue 2026-07-07 14:36:44 CEST; 10h ago
TriggeredBy: ● certbot.timer
       Docs: file:///usr/share/doc/python-certbot-doc/html/index.html
             https://certbot.eff.org/docs
   Main PID: 3951735 (code=exited, status=1/FAILURE)
        CPU: 10.925s

### SERVICE=logrotate.service
ENABLED=static
ACTIVE=failed
× logrotate.service - Rotate log files
     Loaded: loaded (/usr/lib/systemd/system/logrotate.service; static)
     Active: failed (Result: exit-code) since Wed 2026-07-08 00:00:05 CEST; 57min ago
TriggeredBy: ● logrotate.timer
       Docs: man:logrotate(8)
             man:logrotate.conf(5)
   Main PID: 2029717 (code=exited, status=1/FAILURE)
        CPU: 1.173s

## 6) Critical Public Health Still OK
https://my.ndsp.app/index.html HTTP_CODE=200
https://api.ndsp.app/api/health HTTP_CODE=200
https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT HTTP_CODE=200

## 7) Final Evaluation
FINAL_STATUS=P2_ALERTS_RESOLVER_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_ALERTS_RESOLVER_READONLY_20260708_005722.md
