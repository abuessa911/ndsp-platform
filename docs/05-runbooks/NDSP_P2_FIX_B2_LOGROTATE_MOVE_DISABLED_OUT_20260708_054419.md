# NDSP P2 Fix B2 — Move Disabled Logrotate Duplicate Out
DATE=2026-07-08T05:44:19+02:00
MODE=CONTROLLED_LOGROTATE_FIX_B2
MODIFICATION=Move nawafo duplicate logrotate configs out of /etc/logrotate.d
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_B2_LOGROTATE_MOVE_DISABLED_OUT_20260708_054419

## 1) Pre-check
/etc/logrotate.d/nawafo.disabled_p2_fix_b_20260708_053339

## 2) Move duplicate nawafo configs out of /etc/logrotate.d
MOVED_OUT=/etc/logrotate.d/nawafo.disabled_p2_fix_b_20260708_053339 -> /home/nawaf511/ndsp_backups/NDSP_P2_FIX_B2_LOGROTATE_MOVE_DISABLED_OUT_20260708_054419/moved_out_of_logrotate_d/nawafo.disabled_p2_fix_b_20260708_053339.moved_20260708_054419
MOVED_COUNT=1

## 3) Confirm /etc/logrotate.d no longer has nawafo duplicate config
REMAINING_NAWAFO_MATCHES_IN_LOGROTATE_D=0

## 4) logrotate debug test
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

Handling 25 logs

rotating pattern: /var/log/alternatives.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/alternatives.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/apport.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/apt/term.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/apt/history.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/boot.log
 after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/boot.log
  log /var/log/boot.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/btmp  monthly (1 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/btmp
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/letsencrypt/*.log  weekly (12 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/letsencrypt/letsencrypt.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/cloud-init*.log
 1048576 bytes (6 rotations)
empty log files are not rotated, old logs are removed
considering log /var/log/cloud-init.log
  Now: 2026-07-08 05:44
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)
considering log /var/log/cloud-init-output.log
  Now: 2026-07-08 05:44
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)

rotating pattern: /var/log/cups/*log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/cups/access_log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/cups/error_log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-03 00:00
  log does not need rotating (log is empty)
not running postrotate script, since no logs were rotated
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/dpkg.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/dpkg.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/fail2ban.log  weekly (4 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/fail2ban.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /opt/empire-core/backend/logs/*.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /opt/empire-core/backend/logs/*.log
  log /opt/empire-core/backend/logs/*.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 3411811)

rotating pattern: /var/log/nginx/*.log  after 1 days (14 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 3411811)
considering log /var/log/nginx/access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/nginx/api.access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-03-06 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api_access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-03-30 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api.error.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-03-06 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api_error.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-03-30 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api.nawafo.shop.access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-03-09 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/api.nawafo.shop.error.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-03-08 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/bot.ndsp.app.access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/nginx/bot.ndsp.app.error.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-06-28 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/cr7.access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-01-16 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/cr7.error.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-01-14 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/dashboard_access.log
  Now: 2026-07-08 05:44
  Last rotated at 2026-01-25 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/dashboard.nawaf.website.access.log
LOGROTATE_DEBUG_EXIT=0
DUPLICATE_STILL_PRESENT=0

## 5) Controlled real service test
LOGROTATE_SERVICE_START_EXIT=0
LOGROTATE_TIMER_ACTIVE=active
LOGROTATE_SERVICE_ACTIVE=inactive
○ logrotate.service - Rotate log files
     Loaded: loaded (/usr/lib/systemd/system/logrotate.service; static)
     Active: inactive (dead) since Wed 2026-07-08 05:44:19 CEST; 40ms ago
TriggeredBy: ● logrotate.timer
       Docs: man:logrotate(8)
             man:logrotate.conf(5)
    Process: 3411827 ExecStart=/usr/sbin/logrotate /etc/logrotate.conf (code=exited, status=0/SUCCESS)
   Main PID: 3411827 (code=exited, status=0/SUCCESS)
        CPU: 82ms

يوليو 08 05:44:19 vmi2934783 systemd[1]: Starting logrotate.service - Rotate log files...
يوليو 08 05:44:19 vmi2934783 systemd[1]: logrotate.service: Deactivated successfully.
يوليو 08 05:44:19 vmi2934783 systemd[1]: Finished logrotate.service - Rotate log files.

## 6) Runtime safety
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
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.5%[39m | [1mram usage[22m: [32m10%[39m | [1mlo[22m: ⇓ [32m0.005mb/s[39m ⇑ [32m0.005mb/s[39m | [1meth0[22m: ⇓ [32m0.084mb/s[39m ⇑ [32m0.003mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.186mb/s[39m [90m/[39m [1m[33m82%[39m[22m |

## 7) Final Evaluation
P2_FIX_B2_LOGROTATE_DUPLICATE_STATUS=OK
FINAL_STATUS=P2_FIX_B2_LOGROTATE_DUPLICATE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_B2_LOGROTATE_MOVE_DISABLED_OUT_20260708_054419.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_B2_LOGROTATE_MOVE_DISABLED_OUT_20260708_054419
