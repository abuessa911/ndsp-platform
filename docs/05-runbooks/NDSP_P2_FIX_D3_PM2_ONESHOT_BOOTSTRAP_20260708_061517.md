# NDSP P2 Fix D3 — PM2 Oneshot Bootstrap
DATE=2026-07-08T06:15:17+02:00
MODE=CONTROLLED_PM2_SYSTEMD_ONESHOT_BOOTSTRAP_FIX
MODIFICATION=Replace failing Type=forking/PIDFile PM2 unit with Type=oneshot RemainAfterExit bootstrap
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_20260708_061517

## 1) Pre-check PM2 and service
LANG=ar_SA.UTF-8
TERM=xterm-256color
LC_CTYPE=ar_SA.UTF-8
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
MAIL=/var/mail/nawaf511
LOGNAME=nawaf511
USER=nawaf511
HOME=/home/nawaf511
SHELL=/bin/bash
SUDO_COMMAND=/usr/bin/env
SUDO_USER=root
SUDO_UID=0
SUDO_GID=0
TELEGRAM_BOT_TOKEN=<REDACTED_TOKEN>
TELEGRAM_CHAT_ID=302572192
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 10.4% | ram usage: 9.9% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.163mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.256mb/s / 82.01% |
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
