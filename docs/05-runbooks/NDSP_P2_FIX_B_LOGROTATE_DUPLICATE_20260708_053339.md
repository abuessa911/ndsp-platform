# NDSP P2 Fix B — Logrotate Duplicate Entry
DATE=2026-07-08T05:33:39+02:00
MODE=CONTROLLED_LOGROTATE_FIX
MODIFICATION=Resolve duplicate logrotate entry for /var/log/nginx/nawafo_access.log
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_B_LOGROTATE_DUPLICATE_20260708_053339

## 1) Pre-check duplicate sources
/etc/logrotate.d/nawafo:1:/var/log/nginx/nawafo_*.log {
MATCH_COUNT=1

## 2) Backup relevant logrotate files
[OK] Backed up /etc/logrotate.d/nginx
[OK] Backed up /etc/logrotate.d/nawafo
[OK] Backed up /etc/logrotate.conf

## 3) Show current files

### FILE=/etc/logrotate.d/nginx
     1	/var/log/nginx/*.log {
     2		daily
     3		missingok
     4		rotate 14
     5		compress
     6		delaycompress
     7		notifempty
     8		create 0640 www-data adm
     9		sharedscripts
    10		prerotate
    11			if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
    12				run-parts /etc/logrotate.d/httpd-prerotate; \
    13			fi \
    14		endscript
    15		postrotate
    16			invoke-rc.d nginx rotate >/dev/null 2>&1
    17		endscript
    18	}

### FILE=/etc/logrotate.d/nawafo
     1	/var/log/nginx/nawafo_*.log {
     2	    daily
     3	    rotate 14
     4	    compress
     5	    delaycompress
     6	    missingok
     7	    notifempty
     8	    create 0640 www-data adm
     9	    sharedscripts
    10	    postrotate
    11	        systemctl reload nginx >/dev/null 2>&1 || true
    12	    endscript
    13	}

## 4) Apply controlled fix
DISABLED_FILE=/etc/logrotate.d/nawafo.disabled_p2_fix_b_20260708_053339
FIX_APPLIED=1

## 5) Post-fix debug test
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
reading config file nawafo.disabled_p2_fix_b_20260708_053339
reading config file ndip
reading config file nginx
error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
error: found error in file nginx, skipping
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

Handling 26 logs

rotating pattern: /var/log/alternatives.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/alternatives.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/apport.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/apt/term.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/apt/history.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/boot.log
 after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/boot.log
  log /var/log/boot.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/btmp  monthly (1 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/btmp
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/letsencrypt/*.log  weekly (12 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/letsencrypt/letsencrypt.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/cloud-init*.log
 1048576 bytes (6 rotations)
empty log files are not rotated, old logs are removed
considering log /var/log/cloud-init.log
  Now: 2026-07-08 05:33
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)
considering log /var/log/cloud-init-output.log
  Now: 2026-07-08 05:33
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)

rotating pattern: /var/log/cups/*log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/cups/access_log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/cups/error_log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-03 00:00
  log does not need rotating (log is empty)
not running postrotate script, since no logs were rotated
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/dpkg.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/dpkg.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/fail2ban.log  weekly (4 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/fail2ban.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/nginx/nawafo_*.log  after 1 days (14 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/nginx/nawafo_access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_api_access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_api_error.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-08 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_error.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
not running postrotate script, since no logs were rotated
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /opt/empire-core/backend/logs/*.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /opt/empire-core/backend/logs/*.log
  log /opt/empire-core/backend/logs/*.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369163)

rotating pattern: /var/log/nginx/*.log  after 1 days (14 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369163)
considering log /var/log/nginx/access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/nginx/api.access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-03-06 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api_access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-03-30 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api.error.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-03-06 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api_error.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-03-30 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api.nawafo.shop.access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-03-09 00:00
  log does not need rotating (log is empty)
LOGROTATE_DEBUG_EXIT=1
DUPLICATE_STILL_PRESENT=1

## 6) Safe verbose test
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
reading config file nawafo.disabled_p2_fix_b_20260708_053339
reading config file ndip
reading config file nginx
error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
error: found error in file nginx, skipping
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
acquired lock on state file /var/lib/logrotate/statusReading state from file: /var/lib/logrotate/status
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

Handling 26 logs

rotating pattern: /var/log/alternatives.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/alternatives.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/apport.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/apt/term.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/apt/history.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/boot.log
 after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/boot.log
  log /var/log/boot.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/btmp  monthly (1 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/btmp
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/letsencrypt/*.log  weekly (12 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/letsencrypt/letsencrypt.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/cloud-init*.log
 1048576 bytes (6 rotations)
empty log files are not rotated, old logs are removed
considering log /var/log/cloud-init.log
  Now: 2026-07-08 05:33
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)
considering log /var/log/cloud-init-output.log
  Now: 2026-07-08 05:33
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)

rotating pattern: /var/log/cups/*log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/cups/access_log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/cups/error_log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-03 00:00
  log does not need rotating (log is empty)
not running postrotate script, since no logs were rotated
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/dpkg.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/dpkg.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/fail2ban.log  weekly (4 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/fail2ban.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3369176)

rotating pattern: /var/log/nginx/nawafo_*.log  after 1 days (14 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3369176)
considering log /var/log/nginx/nawafo_access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_api_access.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_api_error.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-08 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_error.log
  Now: 2026-07-08 05:33
  Last rotated at 2026-01-10 00:00
LOGROTATE_VERBOSE_EXIT=1

## 7) Reset failed state and check service
LOGROTATE_TIMER_ACTIVE=active
LOGROTATE_SERVICE_ACTIVE=inactive
  UNIT                         LOAD   ACTIVE SUB    DESCRIPTION
● certbot.service              loaded failed failed Certbot
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

9 loaded units listed.

## 8) Critical runtime still OK
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.8%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.108mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.221mb/s[39m [90m/[39m [1m[33m82%[39m[22m |

## 9) Final Evaluation
P2_FIX_B_LOGROTATE_DUPLICATE_STATUS=CHECK_ALERTS
FINAL_STATUS=P2_FIX_B_LOGROTATE_DUPLICATE_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_P2_FIX_B_LOGROTATE_DUPLICATE_20260708_053339.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_B_LOGROTATE_DUPLICATE_20260708_053339
