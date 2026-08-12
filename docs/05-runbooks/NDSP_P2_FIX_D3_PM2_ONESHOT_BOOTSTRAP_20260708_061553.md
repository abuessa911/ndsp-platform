# NDSP P2 Fix D3 — PM2 Oneshot Bootstrap
DATE=2026-07-08T06:15:53+02:00
MODE=CONTROLLED_PM2_SYSTEMD_ONESHOT_BOOTSTRAP_FIX
MODIFICATION=Replace failing Type=forking/PIDFile PM2 unit with Type=oneshot RemainAfterExit bootstrap
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_20260708_061553

## 1) Pre-check PM2 and service
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.9%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.009mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.223mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
PM2_DUMP_BEFORE_SIZE=11196 PM2_DUMP_BEFORE_UPDATED=2026-07-08 06:11:36.688832622 +0200 PATH=/home/nawaf511/.pm2/dump.pm2
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
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
Environment=PM2_HOME=/home/nawaf511/.pm2
PIDFile=/home/nawaf511/.pm2/pm2.pid
Restart=on-failure

ExecStart=/usr/local/lib/node_modules/pm2/bin/pm2 resurrect
ExecReload=/usr/local/lib/node_modules/pm2/bin/pm2 reload all
ExecStop=/usr/local/lib/node_modules/pm2/bin/pm2 kill

[Install]
WantedBy=multi-user.target

## 2) Validate current PM2 process list
PM2_TOTAL_PROCESS_COUNT=1
PM2_NDSP_PORTAL_COUNT=1
PM2_NDSP_PORTAL_ONLINE=1

## 3) Save PM2 process list
[32m[PM2] [39mSaving current process list...
[32m[PM2] [39mSuccessfully saved in /home/nawaf511/.pm2/dump.pm2

## 4) Write oneshot bootstrap systemd unit
UNIT_WRITTEN=/etc/systemd/system/pm2-nawaf511.service
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

## 5) Reload systemd and start service

## 6) Post-check service
PM2_SERVICE_ENABLED_AFTER=enabled
PM2_SERVICE_ACTIVE_AFTER=active
● pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511
     Loaded: loaded (/etc/systemd/system/pm2-nawaf511.service; enabled; preset: enabled)
     Active: active (exited) since Wed 2026-07-08 06:15:57 CEST; 2s ago
       Docs: https://pm2.keymetrics.io/
    Process: 3545845 ExecStart=/usr/local/bin/pm2 resurrect (code=exited, status=0/SUCCESS)
   Main PID: 3545845 (code=exited, status=0/SUCCESS)
        CPU: 391ms

يوليو 08 06:15:57 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511...
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: [PM2] Resurrecting
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: host metrics | cpu: 14% | ram usage: 10% | lo: ⇓ 0.014mb/s ⇑ 0.014mb/s | eth0: ⇓ 0.166mb/s ⇑ 0.007mb/s | disk: ⇓ 0mb/s ⇑ 0.282mb/s / 82.01% |
يوليو 08 06:15:57 vmi2934783 systemd[1]: Finished pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511.
يوليو 05 14:32:49 vmi2934783 systemd[1]: pm2-nawaf511.service: Consumed 2h 59min 421ms CPU time.
يوليو 08 06:11:37 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager...
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: [PM2] Resurrecting
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:11:38 vmi2934783 pm2[3525770]: host metrics | cpu: 9.2% | ram usage: 10.1% | lo: ⇓ 0.003mb/s ⇑ 0.003mb/s | eth0: ⇓ 0.015mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.232mb/s / 82.01% |
يوليو 08 06:11:38 vmi2934783 systemd[1]: pm2-nawaf511.service: New main PID 1094061 does not belong to service, and PID file is not owned by root. Refusing.
يوليو 08 06:11:38 vmi2934783 systemd[1]: pm2-nawaf511.service: New main PID 1094061 does not belong to service, and PID file is not owned by root. Refusing.
يوليو 08 06:11:38 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:38 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 08 06:11:38 vmi2934783 systemd[1]: pm2-nawaf511.service: Scheduled restart job, restart counter is at 1.
يوليو 08 06:11:38 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager...
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: [PM2] Resurrecting
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:11:39 vmi2934783 pm2[3525794]: host metrics | cpu: 9.2% | ram usage: 10.1% | lo: ⇓ 0.003mb/s ⇑ 0.003mb/s | eth0: ⇓ 0.015mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.232mb/s / 82.01% |
يوليو 08 06:11:39 vmi2934783 systemd[1]: pm2-nawaf511.service: Can't open PID file /home/nawaf511/.pm2/pm2.pid (yet?) after start: No such file or directory
يوليو 08 06:11:39 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:39 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 08 06:11:39 vmi2934783 systemd[1]: pm2-nawaf511.service: Scheduled restart job, restart counter is at 2.
يوليو 08 06:11:39 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager...
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: [PM2] Resurrecting
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:11:39 vmi2934783 pm2[3525822]: host metrics | cpu: 9.2% | ram usage: 10.1% | lo: ⇓ 0.003mb/s ⇑ 0.003mb/s | eth0: ⇓ 0.015mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.232mb/s / 82.01% |
يوليو 08 06:11:39 vmi2934783 systemd[1]: pm2-nawaf511.service: Can't open PID file /home/nawaf511/.pm2/pm2.pid (yet?) after start: No such file or directory
يوليو 08 06:11:39 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:39 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 08 06:11:39 vmi2934783 systemd[1]: pm2-nawaf511.service: Scheduled restart job, restart counter is at 3.
يوليو 08 06:11:39 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager...
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: [PM2] Resurrecting
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:11:40 vmi2934783 pm2[3525878]: host metrics | cpu: 9.2% | ram usage: 10.1% | lo: ⇓ 0.003mb/s ⇑ 0.003mb/s | eth0: ⇓ 0.015mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.232mb/s / 82.01% |
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Can't open PID file /home/nawaf511/.pm2/pm2.pid (yet?) after start: No such file or directory
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:40 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Scheduled restart job, restart counter is at 4.
يوليو 08 06:11:40 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager...
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: [PM2] Resurrecting
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:11:40 vmi2934783 pm2[3525925]: host metrics | cpu: 9.2% | ram usage: 10.1% | lo: ⇓ 0.003mb/s ⇑ 0.003mb/s | eth0: ⇓ 0.015mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.232mb/s / 82.01% |
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Can't open PID file /home/nawaf511/.pm2/pm2.pid (yet?) after start: No such file or directory
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:40 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Scheduled restart job, restart counter is at 5.
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Start request repeated too quickly.
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:40 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 08 06:15:57 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511...
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: [PM2] Resurrecting
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: ┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: │ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: ├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: │ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: └────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 08 06:15:57 vmi2934783 pm2[3545845]: host metrics | cpu: 14% | ram usage: 10% | lo: ⇓ 0.014mb/s ⇑ 0.014mb/s | eth0: ⇓ 0.166mb/s ⇑ 0.007mb/s | disk: ⇓ 0mb/s ⇑ 0.282mb/s / 82.01% |
يوليو 08 06:15:57 vmi2934783 systemd[1]: Finished pm2-nawaf511.service - PM2 process manager bootstrap for nawaf511.

## 7) PM2 app list after oneshot start
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m14%[39m | [1mram usage[22m: [32m10%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.166mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.282mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
PM2_TOTAL_PROCESS_COUNT_AFTER=1
PM2_NDSP_PORTAL_COUNT_AFTER=1
PM2_NDSP_PORTAL_ONLINE_AFTER=1
PM2_DUMP_AFTER_SIZE=11196 PM2_DUMP_AFTER_UPDATED=2026-07-08 06:15:55.268814088 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

## 8) Critical runtime still OK
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 9) Failed units snapshot
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

## 10) Final Evaluation
PM2_ENABLED_FINAL=enabled
PM2_ACTIVE_FINAL=active
NDSP_PORTAL_ONLINE_FINAL=1
P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_STATUS=OK
FINAL_STATUS=P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_20260708_061553.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_20260708_061553
