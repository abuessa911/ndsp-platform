# NDSP P3 Boot Readiness Audit — Read-only
DATE=2026-07-08T22:43:26+02:00
MODE=P3_BOOT_READINESS_AUDIT_READONLY
MODIFICATIONS=None
NO_REBOOT=1
NO_SERVICE_START=1
NO_RESTART=1
NO_STOP=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1

## 1) Reality Lock readiness
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=P2_FIX_A_REAL_FEEDS_PERMISSIONS_STATUS=OK
LOCK_KEY_OK=P2_FIX_B2_LOGROTATE_DUPLICATE_STATUS=OK
LOCK_KEY_OK=P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_STATUS=OK
LOCK_KEY_OK=P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_STATUS=OK
LOCK_KEY_OK=P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_STATUS=OK
LOCK_KEY_OK=P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_STATUS=OK
LOCK_KEY_OK=P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_STATUS=OK
LOCK_KEY_OK=P2_POST_G_FINAL_CLEAN_HEALTH_STATUS=OK
LOCK_KEY_OK=P2_POST_G_FINAL_RELEASE_PACKAGE_STATUS=CREATED

## 2) systemd failed units
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT=0

## 3) Core services readiness
nginx_active=active
nginx_enabled=enabled
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2_nawaf511_active=active
pm2_nawaf511_enabled=enabled
# /etc/systemd/system/pm2-nawaf511.service
[Unit]
Description=PM2 process manager bootstrap for nawaf511
Documentation=https://pm2.keymetrics.io/
Wants=network-online.target
After=network.target network-online.target

[Service]
Type=oneshot
User=nawaf511
WorkingDirectory=/home/nawaf511
Environment=HOME=/home/nawaf511
Environment=USER=nawaf511
Environment=PM2_HOME=/home/nawaf511/.pm2
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RemainAfterExit=yes
ExecStart=/usr/local/bin/pm2 resurrect
ExecReload=/usr/local/bin/pm2 reload all
ExecStop=/usr/local/bin/pm2 kill
TimeoutStartSec=120
TimeoutStopSec=120

[Install]
WantedBy=multi-user.target

## 4) PM2 process and dump readiness
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.3%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.009mb/s[39m ⇑ [32m0.009mb/s[39m | [1meth0[22m: ⇓ [32m0.137mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.117mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
PM2_TOTAL_PROCESS_COUNT=1
PM2_NDSP_PORTAL_COUNT=1
PM2_NDSP_PORTAL_ONLINE=1
PM2_DUMP_EXISTS=1 SIZE=11196 UPDATED=2026-07-08 06:15:55.268814088 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

## 5) Public endpoints readiness
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200

## 6) Disabled legacy services remain clean
ndip-api-new.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
testapp.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
signal-engine.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
subscription-watcher.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
fanno-comments.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
marketpulse.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
redis-replica.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
redis-sentinel.service ENABLED=disabled ACTIVE=inactive FAILED=inactive

## 7) Platform gateway 9001 mapping check
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
PORT_9001_LISTENING=1
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

## 8) Data directory and feed files
drwxrwxr-x 2 nawaf511 nawaf511 4096 يوليو   8 22:42 /var/www/ndsp-my/data
-rw-r--r-- nawaf511 nawaf511 711 2026-07-08 22:40 /var/www/ndsp-my/data/data-quality.json
-rw-r--r-- nawaf511 nawaf511 11264 2026-07-08 22:40 /var/www/ndsp-my/data/news-impact.json
-rw-r--r-- nawaf511 nawaf511 33087 2026-07-08 22:40 /var/www/ndsp-my/data/economic-calendar.json
DATA_DIR_OWNER=nawaf511:nawaf511

## 9) logrotate and certbot readiness
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

reading config file /etc/logrotate.conf
including /etc/logrotate.d
reading config file alternatives
reading config file apport
reading config file apt
reading config file bootlog
reading config file btmp
reading config file certbot
reading config file cloud-init
reading config file cups-daemon
reading config file dpkg
reading config file fail2ban
reading config file ndip
reading config file nginx
reading config file postgresql-common
reading config file ppp
reading config file preload
reading config file redis-server
reading config file rsyslog
reading config file sane-utils
reading config file ubuntu-pro-client
reading config file ufw
reading config file unattended-upgrades
reading config file vsftpd
reading config file wtmp
reading config file xrdp
Reading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state

Handling 25 logs

rotating pattern: /var/log/alternatives.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3271548)
considering log /var/log/alternatives.log
  Now: 2026-07-08 22:43
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3271548)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3271548)
considering log /var/log/apport.log
  Now: 2026-07-08 22:43
  Last rotated at 2026-07-01 00:00
LOGROTATE_DEBUG_EXIT=0
LOGROTATE_DUPLICATE_PRESENT=0
CERTBOT_TIMER_ACTIVE=active
CERTBOT_SERVICE_ACTIVE=inactive
NAWAFO_RENEWAL_CONFIGS_PRESENT=0

## 10) Disk and memory snapshot
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       387G  318G   70G  83% /
               total        used        free      shared  buff/cache   available
Mem:            23Gi       2.4Gi        19Gi        29Mi       1.5Gi        21Gi
Swap:          2.0Gi          0B       2.0Gi
ROOT_DISK_USAGE_PERCENT=83
DISK_ALERT=OK

## 11) Final Evaluation
P3_BOOT_READINESS_STATUS=READY_FOR_CONTROLLED_REBOOT_DRILL
FINAL_STATUS=P3_BOOT_READINESS_AUDIT_READONLY_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P3_BOOT_READINESS_AUDIT_READONLY_20260708_224326.md
