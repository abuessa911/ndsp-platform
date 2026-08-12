# NDSP Audit Report

DATE=20260707_090724
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
[WARN] Missing or not static: decision-support.html
[WARN] Missing or not static: NDSP_Asset_View.html
[WARN] Missing or not static: NDSP_Command_Center.html
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
[OK] decision_quality found
[OK] scenario_state found
[OK] live_price found
API_SAMPLE_BEGIN
{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1779.11},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,678.69","scenario_arrival_level":"1,532.63","scenario_review_zone":"1,960.54","scenario_invalidation_level":"1,952.56","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون منطقة المراجعة.","scenario_last_updated":"2026-07-07T07:07:25Z","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_outputs":{"directional_bias":"قراءة أسبوعي · ضغط هابط","reading_horizon":"متابعة كسر أسبوعي","horizon_strength":"عالية جدًا","market_state":"قراءة أسبوعي · ضغط هابط","decision_quality":86,"caution_reason":"انتظار ثبات السعر دون منطقة المراجعة.","sanitized_summary":"قراءة أسبوعي على ETHUSDT: السعر 1,779.11، جودة القراءة 86، الحالة قراءة أسبوعي · ضغط هابط.","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة."},"live_market_analysis":{"provider":"binance","price":1779.11,"price_change_24h_pct":0.5357052039126705,"atr_4h":28.891428571428587,"atr_4h_pct":1.6239259276508249,"rsi_4h":43.717138299757785,"momentum_price_4h":1771.56,"momentum_close_time_4h":1783396799999,"direction":"neutral","market_state":"تذبذب بيني · قرب المتوسط","ho
API_SAMPLE_END

## 5) Service Status
[OK] systemd nginx = active
[ALERT] systemd ndsp-api = activating
unknown
[ALERT] systemd ndip-api-new = failed
unknown
[INFO] systemd ndsp-next not found
[INFO] systemd market-bridge not found
### PM2 list
PM2: ┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
PM2: │ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
PM2: ├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
PM2: │ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 2600731  │ 0s     │ 370… │ online    │ 0%       │ 23.9mb   │ nawaf511 │ disabled │
PM2: │ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
PM2: └────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
PM2: host metrics | cpu: 26.3% | ram usage: 9.3% | lo: ⇓ 0.009mb/s ⇑ 0.009mb/s | eth0: ⇓ 0.147mb/s ⇑ 0.005mb/s | disk: ⇓ 0mb/s ⇑ 0.224mb/s / 81.32% |

## 6) Nginx / SSL
NGINX: 2026/07/07 09:07:42 [warn] 2600742#2600742: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
NGINX: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
NGINX: 2026/07/07 09:07:42 [emerg] 2600742#2600742: open() "/run/nginx.pid" failed (13: Permission denied)
NGINX: nginx: configuration file /etc/nginx/nginx.conf test failed

## 7) Protected UI Element Presence
RADAR_FILE_COUNT=24
SIDEBAR_FILE_COUNT=24
DISCLAIMER_FILE_COUNT=17

## 8) Forbidden Wording Scan
[OK] No obvious forbidden wording found in first scan.

## 9) Resource Snapshot
DF: Filesystem      Size  Used Avail Use% Mounted on
DF: tmpfs           2.4G  1.5M  2.4G   1% /run
DF: /dev/sda1       387G  315G   73G  82% /
DF: tmpfs            12G  1.1M   12G   1% /dev/shm
DF: tmpfs           5.0M     0  5.0M   0% /run/lock
DF: /dev/sda16      881M  117M  703M  15% /boot
DF: /dev/sda15      105M  6.2M   99M   6% /boot/efi
DF: overlay         387G  315G   73G  82% /var/lib/docker/rootfs/overlayfs/f1cd005aa4d48a8990a5e55950e350d693efb9265bed246c3fd7280754892b27
DF: tmpfs           2.4G   84K  2.4G   1% /run/user/1000
MEM:                total        used        free      shared  buff/cache   available
MEM: Mem:            23Gi       2.2Gi        20Gi        28Mi       1.6Gi        21Gi
MEM: Swap:          2.0Gi          0B       2.0Gi

FINAL_STATUS=AUDIT_DONE
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUDIT_REPORT_20260707_090724.md
