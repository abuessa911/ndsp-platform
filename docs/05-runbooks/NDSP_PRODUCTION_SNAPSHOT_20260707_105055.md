# NDSP Production Snapshot
DATE=2026-07-07T10:50:55+02:00
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/var/www/ndsp-my
PUBLIC=https://my.ndsp.app
API=https://api.ndsp.app

## 1) Live frontend archive
-rw-rw-r-- 1 nawaf511 nawaf511 96K يوليو   7 10:50 /home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055/frontend/var_www_ndsp-my_20260707_105055.tar.gz

## 2) Copy locked runbooks
[OK] copied docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md
[OK] copied docs/05-runbooks/NDSP_FINAL_RELEASE_SWEEP_20260707_103944.md
[OK] copied docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_103951.md
[OK] copied docs/05-runbooks/NDSP_RELEASE_HANDOFF_20260707_104741.md
[OK] copied docs/05-runbooks/NDSP_PATCH_COMMAND_CENTER_RADAR_BIND_V24_20260707_100000.md
[OK] copied docs/05-runbooks/NDSP_PATCH_DECISION_SUPPORT_BIND_V1_20260707_100626.md
[OK] copied docs/05-runbooks/NDSP_PATCH_ASSET_VIEW_LIVE_BIND_V1_20260707_101304.md
[OK] copied docs/05-runbooks/NDSP_PATCH_DAILY_BRIEF_LIVE_BIND_V1_20260707_102950.md
[OK] copied docs/05-runbooks/NDSP_PATCH_SETTINGS_ALERTS_BIND_V1_20260707_103642.md

## 3) Runtime evidence
[OK] runtime evidence saved

## 4) Live HTTP verification
[200] size=884 https://my.ndsp.app/
[200] size=884 https://my.ndsp.app/index.html
[200] size=2610 https://my.ndsp.app/decision-support.html
[200] size=2854 https://my.ndsp.app/NDSP_Asset_View.html
[200] size=3310 https://my.ndsp.app/NDSP_Command_Center.html
[200] size=2611 https://my.ndsp.app/NDSP_Daily_Brief.html
[200] size=2579 https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] size=4677 https://my.ndsp.app/disclaimer.html
[200] size=9846 https://my.ndsp.app/assets/ndsp-radar-safe-clean.js?v=24-command-bind
[200] size=6709 https://my.ndsp.app/assets/ndsp-decision-support-bind.js?v=1
[200] size=10160 https://my.ndsp.app/assets/ndsp-asset-view-live-bind.js?v=1
[200] size=9632 https://my.ndsp.app/assets/ndsp-daily-brief-live-bind.js?v=1
[200] size=11545 https://my.ndsp.app/assets/ndsp-settings-alerts-bind.js?v=1

## 5) API verification
--- ETHUSDT ---
ok= True
symbol= ETHUSDT
live_price= 1771.24
quality= 86
scenario= UNDER_MONITORING
nmp= AVAILABLE 1583.4
--- BTCUSDT ---
ok= True
symbol= BTCUSDT
live_price= 63083.18
quality= 86
scenario= UNDER_MONITORING
nmp= AVAILABLE 61056.47
--- XAUUSD ---
ok= True
symbol= XAUUSD
live_price= 4143.5
quality= 60
scenario= UNDER_MONITORING
nmp= UNAVAILABLE None
--- USOIL ---
ok= True
symbol= USOIL
live_price= 69.33000183105469
quality= 56
scenario= UNDER_MONITORING
nmp= UNAVAILABLE None

## 6) Checksums

## 7) Package
SNAPSHOT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz
-rw-rw-r-- 1 nawaf511 nawaf511 112K يوليو   7 10:51 /home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz

SHA256:
ab006cc5201bbde45da508366a78a23b7ec66cbc78db10fcaad881f43a6118ef  /home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz

FINAL_STATUS=PRODUCTION_SNAPSHOT_CREATED
REPORT=docs/05-runbooks/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.md
