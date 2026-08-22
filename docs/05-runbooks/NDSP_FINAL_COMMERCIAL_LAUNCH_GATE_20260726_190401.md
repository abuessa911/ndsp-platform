# NDSP — Final Commercial Launch Gate

- Date: 2026-07-26T19:04:01+02:00
- Host: vmi2934783.contaboserver.net
- Mode: READ_ONLY_NO_PATCH_NO_RESTART
- Core: /home/nawaf511/empire-core-new
- Frontend source: /home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1

## 1. Preflight and server health
PASS | 1. Preflight and server health | Tool available: bash
PASS | 1. Preflight and server health | Tool available: curl
PASS | 1. Preflight and server health | Tool available: python3
PASS | 1. Preflight and server health | Tool available: jq
PASS | 1. Preflight and server health | Tool available: sha256sum
PASS | 1. Preflight and server health | Tool available: systemctl
PASS | 1. Preflight and server health | Tool available: ss
PASS | 1. Preflight and server health | Tool available: df
PASS | 1. Preflight and server health | Tool available: openssl
PASS | 1. Preflight and server health | Tool available: awk
PASS | 1. Preflight and server health | Tool available: grep
PASS | 1. Preflight and server health | Tool available: sed
PASS | 1. Preflight and server health | Tool available: find
PASS | 1. Preflight and server health | Tool available: stat
PASS | 1. Preflight and server health | Tool available: timeout
PASS | 1. Preflight and server health | Core directory exists
PASS | 1. Preflight and server health | main.jsx exists
PASS | 1. Preflight and server health | styles.css exists
PASS | 1. Preflight and server health | Root disk usage 64%
PASS | 1. Preflight and server health | No failed systemd units
PASS | 1. Preflight and server health | System clock synchronized

## 2. NDSP services, PM2, and ports
PASS | 2. NDSP services, PM2, and ports | Service active: ndsp-raw-cot-gateway.service
PASS | 2. NDSP services, PM2, and ports | Service enabled at boot: ndsp-raw-cot-gateway.service
PASS | 2. NDSP services, PM2, and ports | Service active: ndsp-quality-live-nmp-wrapper.service
PASS | 2. NDSP services, PM2, and ports | Service enabled at boot: ndsp-quality-live-nmp-wrapper.service
INFO | 2. NDSP services, PM2, and ports | {"details": [{"exit_code": 0, "name": "ndsp-portal", "pid": 3661, "restarts": 0, "status": "online"}, {"exit_code": 0, "name": "ndsp-trial-clock-v164", "pid": 74984, "restarts": 1, "status": "online"}, {"exit_code": 0, "name": "ndsp-launch-control-v167", "pid": 3664, "restarts": 0, "status": "online"}, {"exit_code": null, "name": "ndsp-telegram-notifications-v182", "pid": 3669, "restarts": 0, "status": "online"}], "errors": []}
PASS | 2. NDSP services, PM2, and ports | Required PM2 processes online
PASS | 2. NDSP services, PM2, and ports | PM2 boot snapshot exists
PASS | 2. NDSP services, PM2, and ports | Port listening: 9057
PASS | 2. NDSP services, PM2, and ports | Port listening: 9076
PASS | 2. NDSP services, PM2, and ports | Port listening: 9082
PASS | 2. NDSP services, PM2, and ports | Port listening: 9089

## 3. Local health and trial policy
PASS | 3. Local health and trial policy | RAW_HEALTH HTTP=200
PASS | 3. Local health and trial policy | TECH_HEALTH HTTP=200
PASS | 3. Local health and trial policy | TRIAL_HEALTH HTTP=200
INFO | 3. Local health and trial policy | {"errors": [], "trial": {"ledger": "/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/data/trial_clock.sqlite3", "ok": true, "port": 9089, "service": "ndsp-trial-clock-v164", "synthetic_clock": false, "trial_days": 16}}
PASS | 3. Local health and trial policy | Local health and 16-day trial policy valid

## 4. Governing decision contract
PASS | 4. Governing decision contract | WEEKLY_SPECULATIVE HTTP=200
PASS | 4. Governing decision contract | WEEKLY_INVESTMENT HTTP=200
INFO | 4. Governing decision contract | {"distinct": true, "errors": [], "investment": {"direction": "bullish", "errors": [], "mode": "investment", "report_age_days": 5.0, "report_date": "2026-07-21", "scenario": "قراءة أسبوعي · ضغط هابط", "score": 64.34, "timeframe": "weekly"}, "speculative": {"direction": "bearish", "errors": [], "mode": "speculative", "report_age_days": 5.0, "report_date": "2026-07-21", "scenario": "قراءة أسبوعي · ضغط هابط", "score": 75.91, "timeframe": "weekly"}}
PASS | 4. Governing decision contract | Mode, commercial score, COT governance, Golden gate, and launch readiness valid

## 5. Raw COT data
PASS | 5. Raw COT data | COT_BTCUSDT HTTP=200
INFO | 5. Raw COT data | BTCUSDT {"age": 5, "errors": [], "report_date": "2026-07-21"}
PASS | 5. Raw COT data | BTCUSDT COT complete and fresh
PASS | 5. Raw COT data | COT_ETHUSDT HTTP=200
INFO | 5. Raw COT data | ETHUSDT {"age": 5, "errors": [], "report_date": "2026-07-21"}
PASS | 5. Raw COT data | ETHUSDT COT complete and fresh

## 6. Asset registry
INFO | 6. Asset registry | {"errors": [], "frontend_count": 56, "registry_count": 56}
PASS | 6. Asset registry | Authoritative and frontend asset registries contain 56 unique assets

## 7. Public routes and deployed identity
CRITICAL | 7. Public routes and deployed identity | Route command-center HTTP=301
PASS | 7. Public routes and deployed identity | Route command-center/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route markets HTTP=301
PASS | 7. Public routes and deployed identity | Route markets/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route prices-chart HTTP=301
PASS | 7. Public routes and deployed identity | Route prices-chart/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route opportunities HTTP=301
PASS | 7. Public routes and deployed identity | Route opportunities/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route decision-room HTTP=301
PASS | 7. Public routes and deployed identity | Route decision-room/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route portfolio HTTP=301
PASS | 7. Public routes and deployed identity | Route portfolio/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route scenarios HTTP=301
PASS | 7. Public routes and deployed identity | Route scenarios/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route layers HTTP=301
PASS | 7. Public routes and deployed identity | Route layers/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route risk HTTP=301
PASS | 7. Public routes and deployed identity | Route risk/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route completed HTTP=301
PASS | 7. Public routes and deployed identity | Route completed/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route data-health HTTP=301
PASS | 7. Public routes and deployed identity | Route data-health/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route alerts HTTP=301
PASS | 7. Public routes and deployed identity | Route alerts/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route guide HTTP=301
PASS | 7. Public routes and deployed identity | Route guide/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route support HTTP=301
PASS | 7. Public routes and deployed identity | Route support/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route account HTTP=301
PASS | 7. Public routes and deployed identity | Route account/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route plans HTTP=301
PASS | 7. Public routes and deployed identity | Route plans/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route settings HTTP=301
PASS | 7. Public routes and deployed identity | Route settings/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route context HTTP=301
PASS | 7. Public routes and deployed identity | Route context/ HTTP=200
CRITICAL | 7. Public routes and deployed identity | Route trial-expired HTTP=301
PASS | 7. Public routes and deployed identity | Route trial-expired/ HTTP=200
PASS | 7. Public routes and deployed identity | Deployed assets discovered: /portal-commercial-preview/assets/index-BbNOtHX6.js | /portal-commercial-preview/assets/index-DoraAm3r.css
PASS | 7. Public routes and deployed identity | Public JS reachable
PASS | 7. Public routes and deployed identity | Frontend marker present: فصل السيناريو الفني عن القراءة الحاكمة
PASS | 7. Public routes and deployed identity | Frontend marker present: قوة القراءة الحاكمة
PASS | 7. Public routes and deployed identity | Frontend marker present: اتجاه TDL الحاكم
PASS | 7. Public routes and deployed identity | Frontend marker present: العنوان الأصلي
PASS | 7. Public routes and deployed identity | Forbidden marker absent: العنوان العربي غير متاح من المصدر
PASS | 7. Public routes and deployed identity | Forbidden marker absent: async async function
PASS | 7. Public routes and deployed identity | Forbidden marker absent: /home/nawaf511/
PASS | 7. Public routes and deployed identity | Forbidden marker absent: vmi2934783
CRITICAL | 7. Public routes and deployed identity | Production source map publicly accessible
PASS | 7. Public routes and deployed identity | Public CSS reachable
PASS | 7. Public routes and deployed identity | Reading-separation CSS deployed

## 8. Security headers and sensitive files
PASS | 8. Security headers and sensitive files | Security header present: strict-transport-security
PASS | 8. Security headers and sensitive files | Security header present: x-content-type-options
PASS | 8. Security headers and sensitive files | Security header present: referrer-policy
PASS | 8. Security headers and sensitive files | Security header present: content-security-policy
PASS | 8. Security headers and sensitive files | Security header present: permissions-policy
CRITICAL | 8. Security headers and sensitive files | Sensitive path accessible: /portal-commercial-preview/.env
PASS | 8. Security headers and sensitive files | Sensitive path blocked: /portal-commercial-preview/package.json HTTP=404
CRITICAL | 8. Security headers and sensitive files | Sensitive path accessible: /portal-commercial-preview/src/main.jsx
PASS | 8. Security headers and sensitive files | Sensitive path blocked: /portal-commercial-preview/SHA256SUMS.txt HTTP=404
CRITICAL | 8. Security headers and sensitive files | Sensitive path accessible: /.git/config
CRITICAL | 8. Security headers and sensitive files | Sensitive path accessible: /backups/

## 9. TLS
PASS | 9. TLS | TLS my.ndsp.app valid for 55 days
PASS | 9. TLS | TLS ndsp.app valid for 61 days
PASS | 9. TLS | TLS api.ndsp.app valid for 61 days
PASS | 9. TLS | TLS bot.ndsp.app valid for 55 days

## 10. Source integrity
PASS | 10. Source integrity | Source manifest verification passed
PASS | 10. Source integrity | No prohibited test wording in source
PASS | 10. Source integrity | Reading-separation source version present
PASS | 10. Source integrity | Authoritative mode-contract source version present

## 11. Optional browser-rendered gate
CRITICAL | 11. Optional browser-rendered gate | Rendered mobile DOM missing reading separation

## 12. Final launch decision
PASS_COUNT=89
WARN_COUNT=0
FAIL_COUNT=25
CRITICAL_FAIL_COUNT=25
COMMERCIAL_LAUNCH_READY=NO
FINAL_STATUS=BLOCKED_BY_CRITICAL_FAILURES
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_COMMERCIAL_LAUNCH_GATE_20260726_190401.md
JSON_REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_COMMERCIAL_LAUNCH_GATE_20260726_190401.json
SOURCE_CHANGED=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
SERVICE_RESTARTED=NO
