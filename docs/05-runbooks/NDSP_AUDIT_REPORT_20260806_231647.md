# NDSP Audit Report

DATE=20260806_231647
PROJECT_DIR=/home/nawaf511/empire-core-new
FRONTEND_DIR=/var/www/ndsp-my
BACKEND_DIR=/home/nawaf511/empire-core-new
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## 1) Directory Integrity
[OK] Found: /home/nawaf511/empire-core-new/docs/00-build-catalog
[OK] Found: /home/nawaf511/empire-core-new/docs/01-build-control-pack
[OK] Found: /home/nawaf511/empire-core-new/docs/02-execution-ready-pack
[OK] Found: /home/nawaf511/empire-core-new/docs/03-final-transition
[OK] Found: /home/nawaf511/empire-core-new/docs/04-legal
[OK] Found: /home/nawaf511/empire-core-new/docs/05-runbooks
[OK] Found: /home/nawaf511/empire-core-new/docs/06-decision-room-contracts
[OK] Found: /home/nawaf511/empire-core-new/scripts/audit
[OK] Found: /home/nawaf511/empire-core-new/scripts/backup
[OK] Found: /home/nawaf511/empire-core-new/scripts/tests

## 2) Official Frontend Files
[OK] index.html
[OK] decision-support.html
[WARN] Missing or not static: NDSP_Asset_View.html
[OK] NDSP_Command_Center.html
[WARN] Missing or not static: NDSP_Daily_Brief.html
[WARN] Missing or not static: NDSP_Settings_Alerts.html
[WARN] Missing or not static: login.html
[WARN] Missing or not static: register.html
[WARN] Missing or not static: disclaimer.html
[WARN] Missing or not static: admin.html

## 3) HTTP Page Checks
[200] https://my.ndsp.app/
[200] https://my.ndsp.app/index.html
[200] https://my.ndsp.app/decision-support.html
[200] https://my.ndsp.app/NDSP_Asset_View.html
[200] https://my.ndsp.app/NDSP_Command_Center.html
[200] https://my.ndsp.app/NDSP_Daily_Brief.html
[200] https://my.ndsp.app/NDSP_Settings_Alerts.html

## 4) API Checks
[200] https://api.ndsp.app/api/health
[200] https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT
[ALERT] decision_quality missing or API failed
[OK] scenario_state found
[OK] live_price found
API_SAMPLE_BEGIN
{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"weekly","live_price":1907.14,"provider_sources":[{"provider":"binance","priority":1,"scope":"intraday_and_daily","active":true},{"provider":"yahoo","priority":2,"scope":"intraday_and_daily_fallback","active":false}]},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,808.62","scenario_arrival_level":"1,665.31","scenario_review_zone":"1,929.89","scenario_invalidation_level":"2,077.32","scenario_confidence_band":"متوسط","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"تبقى القراءة الهابطة تحت المتابعة؛ لا يتفعّل السيناريو إلا بعد كسر مستوى التفعيل 1,808.62، بينما تستدعي العودة فوق منطقة المراجعة 1,929.89 إعادة تقييم القراءة.","scenario_last_updated":"2026-08-06T21:16:49Z","scenario_levels":{"activation":{"price":1808.62,"label_ar":"مستوى التفعيل","label_en":"Activation level","source":"computed","raw_value":"1,808.62"},"arrival":{"price":1665.31,"label_ar":"مستوى الوصول","label_en":"Arrival level","source":"computed","raw_value":"1,665.31"},"review":{"price":1929.89,"label_ar":"مستوى المراجعة","label_en":"Review level","source":"computed","raw_value":"1,929.89"},"invalidation":{"price":2077.32,"label_ar":"مستوى الإلغاء","label_en":"Invalidation level","source":"computed","raw_value":"2,077.32"}},"nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_outputs":{"directional_bias":"قراءة 
API_SAMPLE_END

## 5) Service Status
[OK] systemd nginx = active
[ALERT] systemd ndsp-api = inactive
unknown
[ALERT] systemd ndip-api-new = inactive
unknown
[INFO] systemd ndsp-next not found
[INFO] systemd market-bridge not found
### PM2 list
PM2: ┌────┬─────────────────────────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
PM2: │ id │ name                                │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
PM2: ├────┼─────────────────────────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
PM2: │ 2  │ ndsp-launch-control-v167            │ default     │ 1.0.0   │ fork    │ 4508     │ 3D     │ 0    │ online    │ 0%       │ 27.5mb   │ nawaf511 │ disabled │
PM2: │ 0  │ ndsp-portal                         │ default     │ 0.39.7  │ fork    │ 4474     │ 3D     │ 0    │ online    │ 0%       │ 78.0mb   │ root     │ disabled │
PM2: │ 3  │ ndsp-telegram-notifications-v182    │ default     │ 1.0.0   │ fork    │ 4521     │ 3D     │ 0    │ online    │ 0%       │ 24.1mb   │ nawaf511 │ disabled │
PM2: │ 1  │ ndsp-trial-clock-v164               │ default     │ 1.0.0   │ fork    │ 4498     │ 3D     │ 0    │ online    │ 0%       │ 21.6mb   │ nawaf511 │ disabled │
PM2: └────┴─────────────────────────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
PM2: host metrics | cpu: 15.7% | ram usage: 12.5% | lo: ⇓ 0.024mb/s ⇑ 0.024mb/s | eth0: ⇓ 0.024mb/s ⇑ 0.003mb/s | disk: ⇓ 1.079mb/s ⇑ 0.172mb/s / 74.76% |

## 6) Nginx / SSL
NGINX: 2026/08/06 23:17:33 [warn] 3400382#3400382: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
NGINX: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
NGINX: 2026/08/06 23:17:33 [emerg] 3400382#3400382: open() "/run/nginx.pid" failed (13: Permission denied)
NGINX: nginx: configuration file /etc/nginx/nginx.conf test failed

## 7) Protected UI Element Presence
RADAR_FILE_COUNT=19
SIDEBAR_FILE_COUNT=33
DISCLAIMER_FILE_COUNT=12

## 8) Forbidden Wording Scan
[OK] No obvious forbidden wording found in first scan.

## 9) Resource Snapshot
DF: Filesystem      Size  Used Avail Use% Mounted on
DF: tmpfs           2.4G  1.9M  2.4G   1% /run
DF: /dev/sda1       387G  289G   98G  75% /
DF: tmpfs            12G  1.1M   12G   1% /dev/shm
DF: tmpfs           5.0M     0  5.0M   0% /run/lock
DF: /dev/sda16      881M  117M  703M  15% /boot
DF: /dev/sda15      105M  6.2M   99M   6% /boot/efi
DF: overlay         387G  289G   98G  75% /var/lib/docker/rootfs/overlayfs/f1cd005aa4d48a8990a5e55950e350d693efb9265bed246c3fd7280754892b27
DF: tmpfs           2.4G   84K  2.4G   1% /run/user/1000
MEM:                total        used        free      shared  buff/cache   available
MEM: Mem:            23Gi       3.0Gi        18Gi        31Mi       2.3Gi        20Gi
MEM: Swap:          2.0Gi          0B       2.0Gi

FINAL_STATUS=AUDIT_DONE
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUDIT_REPORT_20260806_231647.md
