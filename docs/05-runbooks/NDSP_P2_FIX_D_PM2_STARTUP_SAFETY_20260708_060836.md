# NDSP P2 Fix D — PM2 Startup Safety
DATE=2026-07-08T06:08:36+02:00
MODE=CONTROLLED_PM2_STARTUP_SAVE_FIX
MODIFICATION=Ensure ndsp-portal PM2 process list is saved and pm2-nawaf511.service is configured
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D_PM2_STARTUP_SAFETY_20260708_060836

## 1) Pre-check PM2 as nawaf511
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.9%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.004mb/s[39m | [1meth0[22m: ⇓ [32m0.019mb/s[39m ⇑ [32m0.009mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.296mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
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

## 3) Ensure only expected PM2 app is present
