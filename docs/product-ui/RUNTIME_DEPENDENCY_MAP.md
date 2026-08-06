# NDSP Runtime Dependency Map

Generated: 2026-08-06T10:24:33+02:00

## المشروع الرئيسي

```text
/home/nawaf511/empire-core-new
```

## الخدمات النشطة التي ما زالت تعتمد على /opt

```text
ndsp-16-layers.service | /opt/ndsp16-api | { path=/usr/bin/node ; argv[]=/usr/bin/node /opt/ndsp16-api/server.js ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-admin-user-ops.service | /opt/ndsp-admin-user-ops | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-auth-core-clean.service | /opt/ndsp-auth-core-clean/current | { path=/usr/bin/nsolid ; argv[]=/usr/bin/nsolid /opt/ndsp-auth-core-clean/current/server/dist/server.js ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-change-password-gateway.service | /opt/ndsp-change-password-gateway | { path=/opt/ndsp-change-password-gateway/venv/bin/uvicorn ; argv[]=/opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-commercial-auth-payment-staging.service | /opt/ndsp-commercial-auth-payment-staging/releases/20260730_103616-source-staging-v1-13/source | { path=/opt/ndsp-commercial-auth-payment-staging/releases/20260730_103616-source-staging-v1-13/run-staging.sh ; argv[]=/opt/ndsp-commercial-auth-payment-staging/releases/20260730_103616-source-staging-v1-13/run-staging.sh ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-current-user-display.service | /opt/ndsp-current-user-display | { path=/opt/ndsp-current-user-display/.venv/bin/uvicorn ; argv[]=/opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-decision-package-v1.service | /opt/ndsp-decision-package-v1 | { path=/opt/ndsp-decision-package-v1/venv/bin/uvicorn ; argv[]=/opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-market-data-bridge-v2.service | /opt/ndsp-market-data-bridge-v2 | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/ndsp-market-data-bridge-v2/bridge.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-news-ticker.service | /opt/ndsp-news-ticker | { path=/usr/bin/node ; argv[]=/usr/bin/node /opt/ndsp-news-ticker/server.js ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-platform-gateway-9002.service | /opt/ndsp-platform-gateway-9002 | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/ndsp-platform-gateway-9002/app.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-public-summary-v548.service | /opt/ndsp-public-summary-v548 | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/ndsp-public-summary-v548/app.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-registration-consent-v42.service |  | { path=/usr/bin/node ; argv[]=/usr/bin/node /opt/ndsp/legal-v42/ndsp-registration-consent-gateway.cjs ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-ui-bridge-api.service | /opt/ndsp-ui-bridge-api | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-v3-portal-gateway.service | /opt/ndsp-v3-portal-gateway | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/ndsp-v3-portal-gateway/app.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-v52-contract.service |  | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/ndsp-v52-contract/app.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
ndsp-v53-bridge.service |  | { path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /opt/ndsp-v53-bridge/app.py ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
```

## الخدمات ذات مسارات مفقودة أو قديمة

```text
binance-feed.service | /opt/empire-core/feeds | active=inactive
inactive
decisionos-backend.service | /opt/decisionos/backend | active=inactive
inactive
empire-binance-feed.service | /opt/empire-core/backend | active=inactive
inactive
empire-ndip-api.service | /opt/empire-core/backend | active=inactive
inactive
empire-webhook.service | /opt/empire/webhooks/universal | active=inactive
inactive
fanno-comments.service | /opt/fanno_comments | active=inactive
inactive
ndip-auto-signal.service | /opt/empire-core/backend | active=inactive
inactive
ndip-auto-trade.service | /opt/empire-core/backend | active=inactive
inactive
ndip-autonomous-loop.service | /opt/empire-core/backend | active=inactive
inactive
ndip-autopilot.service | /opt/empire-core/backend | active=inactive
inactive
ndip-backend.service | /opt/empire-core/backend | active=inactive
inactive
ndip-engine.service | /opt/empire-core/backend | active=inactive
inactive
ndip-frontend.service | /opt/empire-core/frontend | active=inactive
inactive
ndip-run-server.service | /opt/empire-core/backend | active=inactive
inactive
ndip-security-cleanup.service | /opt/ndip/backend/app | active=inactive
inactive
ndip-signal-engine.service | /opt/empire-core/backend | active=inactive
inactive
ndip-signal.service | /opt/empire-core/backend | active=inactive
inactive
ndip-trading-loop.service | /opt/empire-core/backend | active=inactive
inactive
ndip.service | /opt/empire-core/backend | active=inactive
inactive
ndsp-commercial-auth-payment-staging.service | /opt/ndsp-commercial-auth-payment-staging/releases/20260730_103616-source-staging-v1-13/source | active=active
ndsp-enterprise-api.service | /opt/ndsp-enterprise-api | active=inactive
inactive
recommendation-engine.service | /opt/recommendation_engine | active=inactive
inactive
royal-api.service | /opt/empire/api | active=inactive
inactive
signal-engine.service | /opt/empire-core/backend | active=inactive
inactive
trade-monitor.service | /opt/empire-core/backend | active=inactive
inactive
twelvedata-poller.service | /opt/empire-core/feeds | active=inactive
inactive
```

## قاعدة الحذف

لا يتم حذف أي مسار من /opt إذا كان واحد من الآتي صحيحًا:

- خدمة active تشير إليه.
- ExecStart يستخدمه.
- عملية حية تستخدمه.
- Nginx أو cron يشير إليه.
- لا يوجد بديل مختبر في empire-core-new.
