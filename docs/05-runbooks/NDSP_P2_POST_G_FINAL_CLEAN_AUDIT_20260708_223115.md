# NDSP P2 Post-G Final Clean Audit + Release Package
DATE=2026-07-08T22:31:15+02:00
MODE=POST_G_FINAL_CLEAN_AUDIT_AND_PACKAGE
MODIFICATIONS=None_to_runtime
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_SERVICE_START=1
NO_RESTART=1
NO_DISABLE=1
NO_MASK=1
NO_REBOOT=1

## 1) Reality Lock P2 chain checks
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=P2_FIX_A_REAL_FEEDS_PERMISSIONS_STATUS=OK
LOCK_KEY_OK=P2_FIX_B2_LOGROTATE_DUPLICATE_STATUS=OK
LOCK_KEY_OK=P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_STATUS=OK
LOCK_KEY_OK=P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_STATUS=OK
LOCK_KEY_OK=P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_STATUS=OK
LOCK_KEY_OK=P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_STATUS=OK
LOCK_KEY_OK=P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_STATUS=OK
REALITY_LOCK_CHAIN_OK=1

## 2) Core runtime health
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
pm2-nawaf511-enabled=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11%[39m | [1mram usage[22m: [32m10.2%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.083mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.177mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
PM2_TOTAL_PROCESS_COUNT=1
PM2_NDSP_PORTAL_COUNT=1
PM2_NDSP_PORTAL_ONLINE=1

## 3) Public endpoint health
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200

## 4) Service cleanup final state
ndip-api-new.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
testapp.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
signal-engine.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
subscription-watcher.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
fanno-comments.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
marketpulse.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
redis-replica.service ENABLED=disabled ACTIVE=inactive FAILED=inactive
redis-sentinel.service ENABLED=disabled ACTIVE=inactive FAILED=inactive

## 5) Failed units final snapshot
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT=0

## 6) Logrotate final health
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
switching euid from 0 to 0 and egid from 0 to 4 (pid 3221413)
considering log /var/log/alternatives.log
  Now: 2026-07-08 22:31
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3221413)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3221413)
considering log /var/log/apport.log
  Now: 2026-07-08 22:31
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3221413)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3221413)
considering log /var/log/apt/term.log
  Now: 2026-07-08 22:31
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3221413)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3221413)
considering log /var/log/apt/history.log
  Now: 2026-07-08 22:31
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3221413)

rotating pattern: /var/log/boot.log
 after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3221413)
considering log /var/log/boot.log
  log /var/log/boot.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3221413)

rotating pattern: /var/log/btmp  monthly (1 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3221413)
considering log /var/log/btmp
  Now: 2026-07-08 22:31
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3221413)

rotating pattern: /var/log/letsencrypt/*.log  weekly (12 rotations)
empty log files are rotated, old logs are removed
LOGROTATE_DEBUG_EXIT=0
LOGROTATE_DUPLICATE_PRESENT=0

## 7) Certbot renewal scope
CERTBOT_TIMER_ACTIVE=active
CERTBOT_SERVICE_ACTIVE=inactive
NAWAFO_RENEWAL_CONFIGS_PRESENT=0

## 8) Package staging
STAGE=/tmp/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115

## 9) Create release package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz.sha256
8837dfa7379f5868e79a7298186aceacd3cca45f70706ac4c3fbea5b3876407f  /home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz

## 10) Final Evaluation
LOCK_OK_FINAL=1
FAILED_UNITS_COUNT_FINAL=0
NGINX_ACTIVE_FINAL=active
PM2_ACTIVE_FINAL=active
PORTAL_ONLINE_FINAL=1
TESTAPP_ENABLED_FINAL=disabled
TESTAPP_FAILED_FINAL=inactive
NDIP_ENABLED_FINAL=disabled
NDIP_FAILED_FINAL=inactive
API_HTTP_FINAL=200
QUALITY_LIVE_HTTP_FINAL=200
MY_NDSP_HTTP_FINAL=200
LOGROTATE_DEBUG_EXIT_FINAL=0
P2_POST_G_FINAL_CLEAN_HEALTH_STATUS=OK
P2_POST_G_FINAL_RELEASE_PACKAGE_STATUS=CREATED
FINAL_STATUS=P2_POST_G_FINAL_CLEAN_AUDIT_AND_PACKAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_POST_G_FINAL_CLEAN_AUDIT_20260708_223115.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz.sha256
