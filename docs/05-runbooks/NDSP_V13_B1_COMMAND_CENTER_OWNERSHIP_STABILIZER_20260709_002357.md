# NDSP V1.3-B1 Command Center Data Ownership Stabilizer
DATE=2026-07-09T00:23:57+02:00
MODE=CONTROLLED_SYSTEMD_DROPIN_AND_DATA_OWNERSHIP_PATCH
PATCH=V13-B1
TARGET=/var/www/ndsp-my/data/command-center-real.json
SERVICE=ndsp-market-prices-updater.service
DROPIN=/etc/systemd/system/ndsp-market-prices-updater.service.d/50-ndsp-v13-command-center-owner.conf
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_PROTECTED_ASSET_CHANGE=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_B1_COMMAND_CENTER_OWNERSHIP_STABILIZER_20260709_002357

## 1) V13-B prerequisite
V13_B_LOCK=OK

## 2) Preflight runtime health
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 62m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12%[39m | [1mram usage[22m: [32m7.3%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ [32m0.317mb/s[39m ⇑ [32m0.24mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200
DATA_FRESHNESS_HTTP_BEFORE=200
DATA_FRESHNESS_JSON_HTTP_BEFORE=200

## 3) Backup
617567f3451d1163becf522871f62e4f58543707d5117a9848beba384d0cd42a  /var/www/ndsp-my/data/command-center-real.json
TARGET_BEFORE=/var/www/ndsp-my/data/command-center-real.json OWNER=root GROUP=root MODE=-rw-r--r-- SIZE=46316
BACKUP_FRESHNESS_JSON=/home/nawaf511/ndsp_backups/NDSP_V13_B1_COMMAND_CENTER_OWNERSHIP_STABILIZER_20260709_002357/data-freshness-panel.json.before
BACKUP_EXISTING_DROPIN=NO_EXISTING_DROPIN

## 4) Install systemd drop-in
DROPIN_INSTALLED=/etc/systemd/system/ndsp-market-prices-updater.service.d/50-ndsp-v13-command-center-owner.conf
[Service]
ExecStartPost=/usr/bin/test ! -f /var/www/ndsp-my/data/command-center-real.json || /usr/bin/chown nawaf511:nawaf511 /var/www/ndsp-my/data/command-center-real.json
ExecStartPost=/usr/bin/test ! -f /var/www/ndsp-my/data/command-center-real.json || /usr/bin/chmod 0644 /var/www/ndsp-my/data/command-center-real.json

## 5) daemon-reload
DAEMON_RELOAD=OK

## 6) Run market updater once to verify persistent ownership
MARKET_UPDATER_START_EXIT=1
FINAL_STATUS=V13_B1_ABORTED_MARKET_UPDATER_START_FAILED
