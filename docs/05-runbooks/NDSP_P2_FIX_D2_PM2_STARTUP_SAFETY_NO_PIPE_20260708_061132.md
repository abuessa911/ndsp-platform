# NDSP P2 Fix D2 — PM2 Startup Safety No Pipe
DATE=2026-07-08T06:11:32+02:00
MODE=CONTROLLED_PM2_STARTUP_SAVE_FIX_NO_PIPE
MODIFICATION=Fix PM2 startup/save without pipeline heredoc EPIPE
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D2_PM2_STARTUP_SAFETY_NO_PIPE_20260708_061132

PM2_BIN=/usr/local/bin/pm2

## 1) Pre-check PM2 as nawaf511
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.2%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.015mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.232mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
PM2_DUMP_BEFORE_SIZE=11196 PM2_DUMP_BEFORE_UPDATED=2026-07-07 09:26:49.733544741 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

## 2) Existing pm2 systemd unit
PM2_SERVICE_ENABLED_BEFORE=enabled
PM2_SERVICE_ACTIVE_BEFORE=inactive
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

## 3) Safe PM2 jlist to file — no pipe/heredoc
PM2_JLIST_WRITE_STATUS=OK
PM2_TOTAL_PROCESS_COUNT=1
PM2_NDSP_PORTAL_COUNT=1
PM2_NDSP_PORTAL_ONLINE=1

## 4) Refresh PM2 startup service
[PM2] Init System found: systemd
Platform systemd
Template
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

Target path
/etc/systemd/system/pm2-nawaf511.service
Command list
[ 'systemctl enable pm2-nawaf511' ]
[PM2] Writing init configuration in /etc/systemd/system/pm2-nawaf511.service
[PM2] Making script booting at startup...
[PM2] [-] Executing: systemctl enable pm2-nawaf511...
[PM2] [v] Command successfully executed.
+---------------------------------------+
[PM2] Freeze a process list on reboot via:
$ pm2 save

[PM2] Remove init script via:
$ pm2 unstartup systemd
PM2_STARTUP_EXIT=0

## 5) Save PM2 process list as nawaf511
[32m[PM2] [39mSaving current process list...
[32m[PM2] [39mSuccessfully saved in /home/nawaf511/.pm2/dump.pm2
PM2_SAVE_STATUS=OK

## 6) Enable and start pm2-nawaf511.service
PM2_SERVICE_ACTIVE_BEFORE_START=inactive
Job for pm2-nawaf511.service failed because the service did not take the steps required by its unit configuration.
See "systemctl status pm2-nawaf511.service" and "journalctl -xeu pm2-nawaf511.service" for details.

## 7) Post-check PM2 startup
PM2_SERVICE_ENABLED_AFTER=enabled
PM2_SERVICE_ACTIVE_AFTER=activating
● pm2-nawaf511.service - PM2 process manager
     Loaded: loaded (/etc/systemd/system/pm2-nawaf511.service; enabled; preset: enabled)
     Active: activating (auto-restart) (Result: protocol) since Wed 2026-07-08 06:11:40 CEST; 57ms ago
       Docs: https://pm2.keymetrics.io/
    Process: 3525925 ExecStart=/usr/local/lib/node_modules/pm2/bin/pm2 resurrect (code=exited, status=0/SUCCESS)
        CPU: 394ms

يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Scheduled restart job, restart counter is at 5.
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Start request repeated too quickly.
يوليو 08 06:11:40 vmi2934783 systemd[1]: pm2-nawaf511.service: Failed with result 'protocol'.
يوليو 08 06:11:40 vmi2934783 systemd[1]: Failed to start pm2-nawaf511.service - PM2 process manager.
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 3895     │ 0s     │ 0    │ online    │ 0%       │ 40.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 3883     │ 0s     │ 0    │ online    │ 0%       │ 19.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: └────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 05 12:00:16 vmi2934783 systemd[1]: Started pm2-nawaf511.service - PM2 process manager.
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] Applying action deleteProcessId on app [all](ids: [ 0, 1 ])
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-portal](0) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-backend](1) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] All Applications Stopped
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] PM2 Daemon Stopped
يوليو 05 14:32:49 vmi2934783 systemd[1]: pm2-nawaf511.service: Deactivated successfully.
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

## 8) PM2 app list after service start
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.2%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.015mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.232mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
PM2_TOTAL_PROCESS_COUNT_AFTER=1
PM2_NDSP_PORTAL_COUNT_AFTER=1
PM2_NDSP_PORTAL_ONLINE_AFTER=1
PM2_DUMP_AFTER_SIZE=11196 PM2_DUMP_AFTER_UPDATED=2026-07-08 06:11:36.688832622 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

## 9) Critical runtime still OK
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 10) Final Evaluation
PM2_ENABLED_FINAL=enabled
PM2_ACTIVE_FINAL=failed
NDSP_PORTAL_ONLINE_FINAL=1
P2_FIX_D2_PM2_STARTUP_SAFETY_STATUS=CHECK_ALERTS
FINAL_STATUS=P2_FIX_D2_PM2_STARTUP_SAFETY_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_P2_FIX_D2_PM2_STARTUP_SAFETY_NO_PIPE_20260708_061132.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D2_PM2_STARTUP_SAFETY_NO_PIPE_20260708_061132
