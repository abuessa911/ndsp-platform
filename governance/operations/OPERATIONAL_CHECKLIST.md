# NDSP Operational Checklist

Services:
- systemctl status nginx --no-pager
- systemctl status postgresql --no-pager
- systemctl status ndsp-api.service --no-pager
- systemctl status ndsp-telegram-alert.timer --no-pager

Nginx:
- sudo nginx -t
- sudo systemctl reload nginx

API GET checks:
- curl -sS http://127.0.0.1:9001/api/runtime/health
- curl -sS http://127.0.0.1:9001/api/seats/status
- curl -sS https://ndsp.app/api/seats/status
- curl -sS https://my.ndsp.app/api/seats/status
- curl -sS https://admin.ndsp.app/api/seats/status

Retired namespace:
- curl -I https://ndsp.app/api/v7/trial/activation-policy
- curl -I https://my.ndsp.app/api/v7/trial/activation-policy
- curl -I https://admin.ndsp.app/api/v7/trial/activation-policy

Expected for retired namespace: 404

Public secret scan:
- sudo grep -RInE 'TELEGRAM_BOT_TOKEN=|DATABASE_URL=|PGPASSWORD=|DB_PASSWORD=|ADMIN_KEY=|NOWPAYMENTS_API_KEY=|NOWPAYMENTS_IPN_SECRET=' /var/www/ndsp /var/www/ndsp-my /var/www/ndsp-admin

Expected: no results.

---

## Final Readiness After API Namespace Unification — 20260527_171503

Required checks:
- systemctl is-active nginx
- systemctl is-active postgresql
- systemctl is-active ndsp-api.service
- systemctl is-active ndsp-telegram-alert.timer
- nginx -t
- curl http://127.0.0.1:9001/openapi.json
- verify VERSIONED_TOTAL=0
- verify NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
- verify PUBLIC_SECRET_HITS=0

Latest report:
/home/nawaf511/ndsp_launch_reports/NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_20260527_171035.md

---

## Final Readiness After API Namespace Unification — 20260528_093513

Required checks:
- systemctl is-active nginx
- systemctl is-active postgresql
- systemctl is-active ndsp-api.service
- systemctl is-active ndsp-telegram-alert.timer
- nginx -t
- curl http://127.0.0.1:9001/openapi.json
- verify VERSIONED_TOTAL=0
- verify NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
- verify PUBLIC_SECRET_HITS=0

Latest report:
/home/nawaf511/ndsp_launch_reports/NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_20260527_171035.md
