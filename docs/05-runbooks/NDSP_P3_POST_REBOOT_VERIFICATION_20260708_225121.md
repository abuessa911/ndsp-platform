# NDSP P3 Post-Reboot Verification
DATE=2026-07-08T22:51:21+02:00
MODE=POST_REBOOT_VERIFICATION
MODIFICATIONS=None
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
NO_RESTART=1
NO_DISABLE=1
NO_MASK=1

## 1) Boot identity
up 1 minute
         system boot  2026-07-08 22:50
SYSTEM_RUNNING_STATE=degraded

## 2) Failed units after reboot
  UNIT                               LOAD   ACTIVE SUB    DESCRIPTION
● ndsp-market-prices-updater.service loaded failed failed NDSP Live Market Prices Updater

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
FAILED_UNITS_COUNT_AFTER_REBOOT=1

## 3) Core services after reboot
nginx_active_after_reboot=active
nginx_enabled_after_reboot=enabled
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2_nawaf511_active_after_reboot=active
pm2_nawaf511_enabled_after_reboot=enabled
● pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511
     Loaded: loaded (/etc/systemd/system/pm2-nawaf511.service; enabled; preset: enabled)
     Active: active (exited) since Wed 2026-07-08 22:50:41 CEST; 39s ago
       Docs: https://pm2.keymetrics.io/
    Process: 1380 ExecStart=/usr/local/bin/pm2 resurrect (code=exited, status=0/SUCCESS)
   Main PID: 1380 (code=exited, status=0/SUCCESS)
      Tasks: 31 (limit: 28792)
     Memory: 132.4M (peak: 138.6M)
        CPU: 3.551s
     CGroup: /system.slice/pm2-nawaf511.service
             ├─2660 "PM2 v7.0.3: God Daemon (/home/nawaf511/.pm2)"
             ├─3351 "npm run start"
             ├─3787 sh -c "node server.js"
             └─3788 node server.js

يوليو 08 22:50:41 vmi2934783 pm2[1380]: [PM2] PM2 Successfully daemonized
يوليو 08 22:50:41 vmi2934783 pm2[1380]: [PM2] Resurrecting
يوليو 08 22:50:41 vmi2934783 pm2[1380]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 22:50:41 vmi2934783 pm2[1380]: [PM2] Process /home/nawaf511/.nvm/versions/node/v24.15.0/bin/npm restored
يوليو 08 22:50:41 vmi2934783 pm2[1380]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 22:50:41 vmi2934783 pm2[1380]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 22:50:41 vmi2934783 pm2[1380]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 22:50:41 vmi2934783 pm2[1380]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 3351     │ 0s     │ 0    │ online    │ 0%       │ 3.4mb    │ nawaf511 │ disabled │
يوليو 08 22:50:41 vmi2934783 pm2[1380]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 22:50:41 vmi2934783 systemd[1]: Finished pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511.

## 4) PM2 process after reboot
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3351     │ 40s    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 70.9mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m22.6%[39m | [1mram usage[22m: [32m7.6%[39m | [1mlo[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.004mb/s[39m | [1meth0[22m: ⇓ [32m0.033mb/s[39m ⇑ [32m0.008mb/s[39m | [1mdisk[22m: ⇓ [32m5.312mb/s[39m ⇑ [32m0.757mb/s[39m [90m/[39m [1m[33m82.04%[39m[22m |
PM2_TOTAL_PROCESS_COUNT_AFTER_REBOOT=1
PM2_NDSP_PORTAL_COUNT_AFTER_REBOOT=1
PM2_NDSP_PORTAL_ONLINE_AFTER_REBOOT=1

## 5) Public endpoints after reboot
API_HEALTH_HTTP_AFTER_REBOOT=200
QUALITY_LIVE_HTTP_AFTER_REBOOT=200
MY_NDSP_HTTP_AFTER_REBOOT=200
ADMIN_NDSP_HTTP_AFTER_REBOOT=200

## 6) Disabled legacy services after reboot
ndip-api-new.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=activating FAILED_AFTER_REBOOT=activating
testapp.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive
signal-engine.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive
subscription-watcher.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive
fanno-comments.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive
marketpulse.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive
redis-replica.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive
redis-sentinel.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive

## 7) Gateway and feeds after reboot
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1318,fd=32))                                                                                                                                                                                                         
PORT_9001_LISTENING_AFTER_REBOOT=1
drwxrwxr-x 2 nawaf511 nawaf511 4096 يوليو   8 22:50 /var/www/ndsp-my/data
-rw-r--r-- nawaf511 nawaf511 711 2026-07-08 22:50 /var/www/ndsp-my/data/data-quality.json
-rw-r--r-- nawaf511 nawaf511 11270 2026-07-08 22:50 /var/www/ndsp-my/data/news-impact.json
-rw-r--r-- nawaf511 nawaf511 33088 2026-07-08 22:50 /var/www/ndsp-my/data/economic-calendar.json

## 8) logrotate/certbot after reboot
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
switching euid from 0 to 0 and egid from 0 to 4 (pid 8730)
considering log /var/log/alternatives.log
  Now: 2026-07-08 22:51
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 8730)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 8730)
considering log /var/log/apport.log
  Now: 2026-07-08 22:51
  Last rotated at 2026-07-01 00:00
LOGROTATE_DEBUG_EXIT_AFTER_REBOOT=0
LOGROTATE_DUPLICATE_PRESENT_AFTER_REBOOT=0
CERTBOT_TIMER_ACTIVE_AFTER_REBOOT=active
CERTBOT_SERVICE_ACTIVE_AFTER_REBOOT=inactive
NAWAFO_RENEWAL_CONFIGS_PRESENT_AFTER_REBOOT=0

## 9) Final Evaluation
P3_CONTROLLED_REBOOT_DRILL_STATUS=CHECK_ALERTS
FINAL_STATUS=P3_CONTROLLED_REBOOT_DRILL_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_P3_POST_REBOOT_VERIFICATION_20260708_225121.md
