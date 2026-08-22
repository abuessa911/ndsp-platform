# NDSP P3 Final Clean Audit + Release Package
DATE=2026-07-08T23:32:09+02:00
MODE=P3_FINAL_CLEAN_AUDIT_AND_PACKAGE
MODIFICATIONS=None_to_runtime
NO_REBOOT=1
NO_RESTART=1
NO_START=1
NO_STOP=1
NO_ENABLE=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_PM2_CHANGE=1

## 1) Required Reality Lock chain
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=P2_POST_G_FINAL_CLEAN_HEALTH_STATUS=OK
LOCK_KEY_OK=P2_POST_G_FINAL_RELEASE_PACKAGE_STATUS=CREATED
LOCK_KEY_OK=P3_BOOT_READINESS_STATUS=READY_FOR_CONTROLLED_REBOOT_DRILL
LOCK_KEY_OK=P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_STATUS=OK
LOCK_KEY_OK=P3_CONTROLLED_REBOOT_AFTER_FIX_I_STATUS=OK

## 2) Final systemd state
SYSTEM_RUNNING_STATE=running
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT=0

## 3) Fix I target service state
ndip-api-new.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=no NRESTARTS=0
ndip-health-monitor.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=always NRESTARTS=0
ndip-telegram-decision-worker.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=always NRESTARTS=0
ndsp-market-prices-updater.service ENABLED=static ACTIVE=inactive FAILED=inactive RESTART=no NRESTARTS=0
ndsp-market-prices-updater.timer ENABLED=enabled ACTIVE=active FAILED=active RESTART= NRESTARTS=
NDIP_ACTIVE_FINAL=inactive
NDIP_FAILED_FINAL=inactive
NDIP_RESTART_POLICY_FINAL=no
MARKET_TIMER_ACTIVE_FINAL=active
MARKET_SERVICE_FAILED_FINAL=inactive

## 4) Core runtime health
NGINX_ACTIVE=active
NGINX_ENABLED=enabled
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE=active
PM2_ENABLED=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 10m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.3mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.4%[39m | [1mram usage[22m: [32m7.2%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.086mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.223mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
PM2_TOTAL_PROCESS_COUNT=1
PM2_NDSP_PORTAL_COUNT=1
PM2_NDSP_PORTAL_ONLINE=1

## 5) Public endpoints
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200

## 6) Gateway and feed files
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1328,fd=32))                                                                                                                                                                                                         
PORT_9001_LISTENING=1
drwxrwxr-x 2 nawaf511 nawaf511 4096 يوليو   8 23:32 /var/www/ndsp-my/data
-rw-r--r-- nawaf511 nawaf511 711 2026-07-08 23:32 /var/www/ndsp-my/data/data-quality.json
-rw-r--r-- nawaf511 nawaf511 11270 2026-07-08 23:32 /var/www/ndsp-my/data/news-impact.json
-rw-r--r-- nawaf511 nawaf511 33130 2026-07-08 23:32 /var/www/ndsp-my/data/economic-calendar.json
DATA_DIR_OWNER=nawaf511:nawaf511

## 7) Logrotate and certbot
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
switching euid from 0 to 0 and egid from 0 to 4 (pid 47801)
considering log /var/log/alternatives.log
  Now: 2026-07-08 23:32
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 47801)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 47801)
considering log /var/log/apport.log
  Now: 2026-07-08 23:32
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 47801)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 47801)
considering log /var/log/apt/term.log
  Now: 2026-07-08 23:32
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 47801)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 47801)
considering log /var/log/apt/history.log
  Now: 2026-07-08 23:32
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 47801)
LOGROTATE_DEBUG_EXIT=0
LOGROTATE_DUPLICATE_PRESENT=0
CERTBOT_TIMER_ACTIVE=active
CERTBOT_SERVICE_ACTIVE=inactive
NAWAFO_RENEWAL_CONFIGS_PRESENT=0

## 8) Disk and memory
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       387G  318G   70G  83% /
               total        used        free      shared  buff/cache   available
Mem:            23Gi       1.7Gi        20Gi        28Mi       1.4Gi        21Gi
Swap:          2.0Gi          0B       2.0Gi
ROOT_DISK_USAGE_PERCENT=83
DISK_ALERT=OK

## 9) Package staging
STAGE=/tmp/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209

## 10) Create package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz.sha256
0355c29a6b98aceff31967ea6c2b37482172c14175af14d00e3a75fe9828694c  /home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz

## 11) Final Evaluation
OK_EVALUATION=1
P3_FINAL_CLEAN_HEALTH_STATUS=OK
P3_FINAL_RELEASE_PACKAGE_STATUS=CREATED
FINAL_STATUS=P3_FINAL_CLEAN_AUDIT_AND_PACKAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P3_FINAL_CLEAN_AUDIT_20260708_233209.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz.sha256
