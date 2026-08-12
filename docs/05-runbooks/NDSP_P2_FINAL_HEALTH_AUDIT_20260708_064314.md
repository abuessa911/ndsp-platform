# NDSP P2 Final Health Audit + Release Package
DATE=2026-07-08T06:43:14+02:00
MODE=FINAL_P2_HEALTH_AUDIT_AND_PACKAGE
MODIFICATIONS=None_to_runtime
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1

## 1) Reality Lock P2 status checks
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=P2_FIX_A_REAL_FEEDS_PERMISSIONS_STATUS=OK
LOCK_KEY_OK=P2_FIX_B2_LOGROTATE_DUPLICATE_STATUS=OK
LOCK_KEY_OK=P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_STATUS=OK
LOCK_KEY_OK=P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_STATUS=OK
LOCK_KEY_OK=P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_STATUS=OK
REALITY_LOCK_P2_STATUS=1

## 2) Core runtime health
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
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.5%[39m | [1mram usage[22m: [32m10%[39m | [1mlo[22m: ⇓ [32m0.013mb/s[39m ⇑ [32m0.013mb/s[39m | [1meth0[22m: ⇓ [32m0.173mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.022mb/s[39m [90m/[39m [1m[33m81.98%[39m[22m |
PM2_TOTAL_PROCESS_COUNT=1
PM2_NDSP_PORTAL_COUNT=1
PM2_NDSP_PORTAL_ONLINE=1

## 3) Public endpoint health
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200

## 4) Logrotate health
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
switching euid from 0 to 0 and egid from 0 to 4 (pid 3658312)
considering log /var/log/alternatives.log
  Now: 2026-07-08 06:43
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3658312)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3658312)
considering log /var/log/apport.log
  Now: 2026-07-08 06:43
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3658312)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3658312)
considering log /var/log/apt/term.log
  Now: 2026-07-08 06:43
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3658312)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3658312)
considering log /var/log/apt/history.log
  Now: 2026-07-08 06:43
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3658312)

rotating pattern: /var/log/boot.log
 after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3658312)
considering log /var/log/boot.log
  log /var/log/boot.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3658312)

rotating pattern: /var/log/btmp  monthly (1 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3658312)
considering log /var/log/btmp
  Now: 2026-07-08 06:43
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3658312)

rotating pattern: /var/log/letsencrypt/*.log  weekly (12 rotations)
empty log files are rotated, old logs are removed
LOGROTATE_DEBUG_EXIT=0
LOGROTATE_DUPLICATE_PRESENT=0

## 5) Certbot renewal scope health
CERTBOT_TIMER_ACTIVE=active
CERTBOT_SERVICE_ACTIVE=inactive
total 28
drwxr-xr-x 2 root root 4096 يوليو   8 06:04 .
drwxr-xr-x 9 root root 4096 يوليو   8 06:05 ..
-rw-r--r-- 1 root root  543 يونيو  16 22:15 admin.ndsp.app.conf
-rw-r--r-- 1 root root  533 يونيو  28 19:30 api.ndsp.app.conf
-rw-r--r-- 1 root root  533 مايو   29 19:11 bot.ndsp.app.conf
-rw-r--r-- 1 root root  528 يونيو  21 22:01 my.ndsp.app.conf
-rw-r--r-- 1 root root  538 مايو   23 18:07 ndsp.app-0005.conf
NAWAFO_RENEWAL_CONFIGS_PRESENT=0

## 6) Data write and real-feed files
drwxrwxr-x 2 nawaf511 nawaf511 4096 يوليو   8 06:42 /var/www/ndsp-my/data
-rw-r--r-- nawaf511 nawaf511 711 2026-07-08 06:39 /var/www/ndsp-my/data/data-quality.json
-rw-r--r-- nawaf511 nawaf511 11169 2026-07-08 06:39 /var/www/ndsp-my/data/news-impact.json
-rw-r--r-- nawaf511 nawaf511 33079 2026-07-08 06:39 /var/www/ndsp-my/data/economic-calendar.json

## 7) Failed units final snapshot
  UNIT                         LOAD   ACTIVE SUB    DESCRIPTION
● ndip-api-new.service         loaded failed failed NDIP API - New Backend
● signal-engine.service        loaded failed failed Empire Core Signal Engine
● subscription-watcher.service loaded failed failed Subscription Expiry Watcher
● testapp.service              loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

4 loaded units listed.
FAILED_UNITS_COUNT=4

## 8) Package staging
STAGE=/tmp/NDSP_P2_RELEASE_PACKAGE_20260708_064314

## 9) Create package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz.sha256
f3a5f2fc49a939d56242116f870eff306fce1b1ac3f8df7cf815040073cc55b0  /home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz

## 10) Final evaluation
NGINX_ACTIVE_FINAL=active
PM2_ACTIVE_FINAL=active
PORTAL_ONLINE_FINAL=1
API_HTTP_FINAL=200
QUALITY_LIVE_HTTP_FINAL=200
MY_NDSP_HTTP_FINAL=200
P2_FINAL_HEALTH_STATUS=OK
P2_RELEASE_PACKAGE_STATUS=CREATED
FINAL_STATUS=P2_FINAL_HEALTH_AND_PACKAGE_OK
REALITY_LOCK_STATUS=UPDATED
