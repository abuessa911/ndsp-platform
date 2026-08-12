# NDSP — Commercial Phase 1 Runtime and Schema Mapping V1.4

- Date: 2026-07-30T01:14:47+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Active auth database resolved: YES
- Database credentials printed: NO
- Target listener: 127.0.0.1:9094
- Target PID: 2497959
- Mode: READ_ONLY
- Output: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_20260730_011442

## 1. Exact process ownership and source path

=== LISTENER ===
LISTEN 0      5          127.0.0.1:9094       0.0.0.0:*    users:(("python3",pid=2497959,fd=6))                                                                                                                                                                                                                      

=== PID BASIC DATA ===
2497959       1 nawaf511 nawaf511 ر يوليو 29 06:52:50 2026 18:21:56 Ss /usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py

=== EXECUTABLE ===
/usr/bin/python3.12

=== WORKING DIRECTORY ===
/

=== COMMAND LINE ===
/usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py 

=== CGROUP ===
0::/system.slice/ndsp-business-ops.service

=== ENVIRONMENT KEY NAMES ONLY ===
HOME
INVOCATION_ID
JOURNAL_STREAM
LANG
LOGNAME
MEMORY_PRESSURE_WATCH
MEMORY_PRESSURE_WRITE
NDSP_LANDING_BASE
NDSP_LOCAL_DECISION_BASE
NDSP_LOCAL_MAIL_USER
NDSP_LOCAL_PACKAGES_URL
NDSP_OPS_DB
NDSP_OPS_HASH_SALT
NDSP_OPS_HOST
NDSP_OPS_LATEST_MONITOR
NDSP_OPS_MONITOR_STATE
NDSP_OPS_PORT
NDSP_OPS_REPORT_DIR
NDSP_PUBLIC_BASE
PATH
SHELL
SYSTEMD_EXEC_PID
USER

=== PARENT CHAIN ===
2497959       1 nawaf511 nawaf511 ر يوليو 29 06:52:50 2026 18:21:57 Ss /usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py

=== SYSTEMD UNIT FROM CGROUP ===
CGROUP_UNIT=ndsp-business-ops.service

=== SYSTEMD SHOW ===
MainPID=2497959
ExecStart={ path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py ; ignore_errors=no ; start_time=[Wed 2026-07-29 06:52:50 CEST] ; stop_time=[n/a] ; pid=2497959 ; code=(null) ; status=0/0 }
EnvironmentFiles=/etc/ndsp/business-ops.env (ignore_errors=no)
WorkingDirectory=
User=nawaf511
Group=nawaf511
Id=ndsp-business-ops.service
Description=NDSP Business Operations V205
LoadState=loaded
ActiveState=active
SubState=running
FragmentPath=/etc/systemd/system/ndsp-business-ops.service

=== SYSTEMD UNIT CONTENT ===
# /etc/systemd/system/ndsp-business-ops.service
[Unit]
Description=NDSP Business Operations V205
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=nawaf511
Group=nawaf511
EnvironmentFile=/etc/ndsp/business-ops.env
ExecStart=/usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py
Restart=always
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/ndsp-business-ops
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
UMask=0027

[Install]
WantedBy=multi-user.target

=== FALLBACK UNIT MATCH BY MAINPID ===
ndsp-business-ops.service

## 2. Nginx include and public route map

=== DIRECT REFERENCES TO PORT 9094 ===
/etc/nginx/snippets/ndsp-business-ops-v205.conf:22:    proxy_pass http://127.0.0.1:9094/health;
/etc/nginx/snippets/ndsp-business-ops-v205.conf:32:    proxy_pass http://127.0.0.1:9094;
/etc/nginx/snippets/ndsp-business-ops-v205.conf:45:    proxy_pass http://127.0.0.1:9094;

=== NGINX EFFECTIVE CONFIG AROUND PORT 9094 ===

=== BUSINESS OPS SNIPPET ===
# NDSP_BUSINESS_OPERATIONS_V205_BEGIN
location = /start { return 301 /start/; }
location ^~ /start/ { alias /var/www/ndsp-business-ops/start/; index index.html; add_header Cache-Control "no-store" always; }
location = /support { return 301 /support/; }
location ^~ /support/ { alias /var/www/ndsp-business-ops/support/; index index.html; add_header Cache-Control "no-store" always; }
location = /subscribe { return 301 /subscribe/; }
location ^~ /subscribe/ { alias /var/www/ndsp-business-ops/subscribe/; index index.html; add_header Cache-Control "no-store" always; }
location = /launch { return 301 /launch/; }
location ^~ /launch/ { alias /var/www/ndsp-business-ops/launch/; index index.html; add_header Cache-Control "no-store" always; }
location = /ndsp-ops-assets/common.css { alias /var/www/ndsp-business-ops/common.css; add_header Cache-Control "public, max-age=3600" always; }

location = /ops-admin { return 301 /ops-admin/; }
location ^~ /ops-admin/ {
    auth_basic "NDSP Operations";
    auth_basic_user_file /etc/nginx/ndsp-business-ops.htpasswd;
    alias /var/www/ndsp-business-ops/ops-admin/;
    index index.html;
    add_header Cache-Control "no-store" always;
}

location = /api/ops/health {
    proxy_pass http://127.0.0.1:9094/health;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-NDSP-Admin-Gate "";
}

location ^~ /api/ops/public/ {
    proxy_pass http://127.0.0.1:9094;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-NDSP-Admin-Gate "";
    client_max_body_size 128k;
}

location ^~ /api/ops/admin/ {
    auth_basic "NDSP Operations";
    auth_basic_user_file /etc/nginx/ndsp-business-ops.htpasswd;
    proxy_pass http://127.0.0.1:9094;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-NDSP-Admin-Gate "1";
    client_max_body_size 128k;
}
# NDSP_BUSINESS_OPERATIONS_V205_END

=== SNIPPET INCLUDE LOCATIONS ===
/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf:332:    include /etc/nginx/snippets/ndsp-business-ops-v205.conf;

## 3. Actual source and route extraction

=== SOURCE CANDIDATES ===
/etc/python3.12/sitecustomize.py
/home/nawaf511/direction_engine.py
/home/nawaf511/ndsp_alpic_remote_deployment_diagnostic_v28_4_1.py
/home/nawaf511/ndsp_alpic_remote_deployment_diagnostic_v28_4_2.py
/home/nawaf511/ndsp_alpic_remote_deployment_diagnostic_v28_4_3.py
/home/nawaf511/ndsp_canonical_live_runtime_v33.py
/home/nawaf511/ndsp_contract.py
/home/nawaf511/ndsp_cot_fetcher.py
/home/nawaf511/ndsp_explain.py
/home/nawaf511/ndsp_governance.py
/home/nawaf511/ndsp_i18n_phase2_patch_homepage.py
/home/nawaf511/ndsp_latest_16_layers_logic_functions.py
/home/nawaf511/ndsp_orchestrator.py
/home/nawaf511/ndsp_resolver.py
/home/nawaf511/NDSP_TRANSLATIONS_AR_EN.js
/home/nawaf511/quality_stack.py
/home/nawaf511/test_ws_live_connection.py
/__init__.py
/opt/empire-core.broken.1776325777/admin_api.py
/opt/ndsp16-api/server.js
/opt/ndsp-admin-user-ops/app.py
/opt/ndsp-admin-user-ops/server.py
/opt/ndsp-archive-app/admin-plans.js
/opt/ndsp-archive-app/checkout.js
/opt/ndsp-archive-app/discounts.js
/opt/ndsp-archive-app/server.js
/opt/ndsp-archive-app/webhooks-moyasar.js
/opt/ndsp-change-password-gateway/app.py
/opt/ndsp-current-user-display/app.py
/opt/ndsp-decision-package-v1/app.py
/opt/ndsp-market-data-bridge-v2/bridge.py
/opt/ndsp-news-ticker/server.js
/opt/ndsp-platform-gateway-9002/app.py
/opt/ndsp-public-summary-v548/app.py
/opt/ndsp-registration-mailer-v12-1/mailer.py
/opt/ndsp-ui-bridge-api/main.py
/opt/ndsp-v3-portal-gateway/app.py
/opt/ndsp-v471-react-gold-portal_20260701_173443/postcss.config.js
/opt/ndsp-v471-react-gold-portal_20260701_173443/tailwind.config.js
/opt/ndsp-v52-contract/app.py
/opt/ndsp-v53-bridge/app.py
/srv/testapp2/app.py
/srv/trade_control_center/app.py
/srv/trade_control_center/auto_heal.py
/srv/trade_engine/engine.py
/usr/bin/grantlee_strings_extractor.py
/usr/bin/kdelnk2desktop.py
/usr/bin/kde-systemsettings-tree.py
/usr/bin/mesa-overlay-control.py
/usr/bin/pykig.py
/usr/bin/zonetab2pot.py
/usr/local/lib/ndsp-business-ops/app.py

=== ROUTE DEFINITIONS ===

--- FILE: /etc/python3.12/sitecustomize.py ---

--- FILE: /home/nawaf511/direction_engine.py ---

--- FILE: /home/nawaf511/ndsp_alpic_remote_deployment_diagnostic_v28_4_1.py ---

--- FILE: /home/nawaf511/ndsp_alpic_remote_deployment_diagnostic_v28_4_2.py ---

--- FILE: /home/nawaf511/ndsp_alpic_remote_deployment_diagnostic_v28_4_3.py ---

--- FILE: /home/nawaf511/ndsp_canonical_live_runtime_v33.py ---

--- FILE: /home/nawaf511/ndsp_contract.py ---

--- FILE: /home/nawaf511/ndsp_cot_fetcher.py ---

--- FILE: /home/nawaf511/ndsp_explain.py ---

--- FILE: /home/nawaf511/ndsp_governance.py ---

--- FILE: /home/nawaf511/ndsp_i18n_phase2_patch_homepage.py ---

--- FILE: /home/nawaf511/ndsp_latest_16_layers_logic_functions.py ---

--- FILE: /home/nawaf511/ndsp_orchestrator.py ---

--- FILE: /home/nawaf511/ndsp_resolver.py ---

--- FILE: /home/nawaf511/NDSP_TRANSLATIONS_AR_EN.js ---

--- FILE: /home/nawaf511/quality_stack.py ---

--- FILE: /home/nawaf511/test_ws_live_connection.py ---

--- FILE: /__init__.py ---

--- FILE: /opt/empire-core.broken.1776325777/admin_api.py ---
17:@app.get("/admin/status")
22:@app.get("/admin/market")
31:@app.get("/admin/metrics")
41:@app.get("/admin/ndip")
50:@app.post("/admin/control")

--- FILE: /opt/ndsp16-api/server.js ---
700:  for(const p of paths) app.get(p, handler);
703:app.get('/api/health', (req,res)=>res.json({
886:app.get('/api/layers/status', (req,res)=>res.json({
904:app.get('/api/assets', (req,res)=>res.json({
919:app.get('/api/analysis/complete/:assetId/:userId', async (req,res)=>{

--- FILE: /opt/ndsp-admin-user-ops/app.py ---
23:@app.get("/health")
27:@app.post("/{user_id}")

--- FILE: /opt/ndsp-admin-user-ops/server.py ---

--- FILE: /opt/ndsp-archive-app/admin-plans.js ---

--- FILE: /opt/ndsp-archive-app/checkout.js ---

--- FILE: /opt/ndsp-archive-app/discounts.js ---

--- FILE: /opt/ndsp-archive-app/server.js ---

--- FILE: /opt/ndsp-archive-app/webhooks-moyasar.js ---

--- FILE: /opt/ndsp-change-password-gateway/app.py ---
159:@app.get("/api/account/change-password/health")
170:@app.post("/api/account/change-password")

--- FILE: /opt/ndsp-current-user-display/app.py ---
332:@app.get("/api/account/me-display/health")
342:@app.get("/api/account/me-display")

--- FILE: /opt/ndsp-decision-package-v1/app.py ---
49:@app.get("/health")
53:@app.get("/api/decision/package-live")
280:@app.get("/api/decision/package-v2")

--- FILE: /opt/ndsp-market-data-bridge-v2/bridge.py ---

--- FILE: /opt/ndsp-news-ticker/server.js ---

--- FILE: /opt/ndsp-platform-gateway-9002/app.py ---

--- FILE: /opt/ndsp-public-summary-v548/app.py ---

--- FILE: /opt/ndsp-registration-mailer-v12-1/mailer.py ---

--- FILE: /opt/ndsp-ui-bridge-api/main.py ---
38:@app.get("/api/ui-bridge/health")
60:@app.get("/api/dashboard/overview")
92:@app.get("/api/market/assets")
129:@app.get("/api/layers")
177:@app.get("/api/market-structure")
201:@app.get("/api/technical-confirmation")
224:@app.get("/api/macro-analysis")
243:@app.get("/api/risk-layer")
264:@app.get("/api/nawaf-signal")
283:@app.get("/api/alerts")
314:@app.get("/api/settings")
326:@app.get("/api/account/profile")

--- FILE: /opt/ndsp-v3-portal-gateway/app.py ---

--- FILE: /opt/ndsp-v471-react-gold-portal_20260701_173443/postcss.config.js ---

--- FILE: /opt/ndsp-v471-react-gold-portal_20260701_173443/tailwind.config.js ---

--- FILE: /opt/ndsp-v52-contract/app.py ---

--- FILE: /opt/ndsp-v53-bridge/app.py ---
826:@app.get("/api/decision/public-summary")
830:@app.get("/api/decision/public-contract-v548")
892:@app.get("/api/decision/public-summary")
896:@app.get("/api/decision/public-contract-v548")

--- FILE: /srv/testapp2/app.py ---

--- FILE: /srv/trade_control_center/app.py ---

--- FILE: /srv/trade_control_center/auto_heal.py ---

--- FILE: /srv/trade_engine/engine.py ---

--- FILE: /usr/bin/grantlee_strings_extractor.py ---

--- FILE: /usr/bin/kdelnk2desktop.py ---

--- FILE: /usr/bin/kde-systemsettings-tree.py ---

--- FILE: /usr/bin/mesa-overlay-control.py ---

--- FILE: /usr/bin/pykig.py ---

--- FILE: /usr/bin/zonetab2pot.py ---

--- FILE: /usr/local/lib/ndsp-business-ops/app.py ---

## 4. Current source references to commercial tables

=== CURRENT SOURCE REFERENCES ===
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:117:    INSERT INTO public.ndsp_subscriptions
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:381:          FROM public.ndsp_subscriptions
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:41:    CREATE TABLE IF NOT EXISTS public.ndsp_subscriptions (
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:58:    CREATE INDEX IF NOT EXISTS ndsp_subscriptions_user_idx
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:59:      ON public.ndsp_subscriptions (user_id);
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:218:                FROM ndsp_subscriptions
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs:774:    `INSERT INTO public.ndsp_legal_acceptances
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs:777:     ON CONFLICT (request_id) DO UPDATE SET upstream_status=COALESCE(EXCLUDED.upstream_status,public.ndsp_legal_acceptances.upstream_status)

=== HASHES OF REFERENCING SOURCE FILES ===
b7189c7278c0e45ce71f66fb1c1b2b5debeaeb9b77331aa5c745f142af1b7448  /home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py
932cbbdda617f2189741843bb11d74b8218e837c61004f9e7ee07c7995854421  /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs
c86c22a98ab21e9c4befc6ba3cc35f3f4336432f573dbf398ee80ab259ba08ef  /home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs
574137c8bbc1b5de7e6215677225b5b9be3e0b7ff875374a92927508cd454beb  /home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs

## 5. Exact active database schema and dependencies

=== DATABASE IDENTITY ===
ndsp_auth|ndsp_auth|127.0.0.1/32|5432

=== TABLE ROW COUNTS ===
ndsp_legal_acceptances|0
ndsp_subscriptions|0

=== COLUMNS ===
       table_name       | ordinal_position |     column_name     |        data_type         | is_nullable |                 column_default                 
------------------------+------------------+---------------------+--------------------------+-------------+------------------------------------------------
 ndsp_legal_acceptances |                1 | acceptance_id       | bigint                   | NO          | 
 ndsp_legal_acceptances |                2 | subject_key         | text                     | YES         | 
 ndsp_legal_acceptances |                3 | email_sha256        | character varying        | NO          | 
 ndsp_legal_acceptances |                4 | request_id          | text                     | NO          | 
 ndsp_legal_acceptances |                5 | disclaimer_version  | text                     | NO          | 
 ndsp_legal_acceptances |                6 | terms_version       | text                     | NO          | 
 ndsp_legal_acceptances |                7 | privacy_version     | text                     | NO          | 
 ndsp_legal_acceptances |                8 | acceptance_source   | text                     | NO          | 
 ndsp_legal_acceptances |                9 | upstream_status     | smallint                 | YES         | 
 ndsp_legal_acceptances |               10 | user_agent_sha256   | character varying        | YES         | 
 ndsp_legal_acceptances |               11 | evidence_sha256     | character varying        | NO          | 
 ndsp_legal_acceptances |               12 | accepted_at         | timestamp with time zone | NO          | 
 ndsp_legal_acceptances |               13 | recorded_at         | timestamp with time zone | NO          | now()
 ndsp_legal_acceptances |               14 | metadata            | jsonb                    | NO          | '{}'::jsonb
 ndsp_subscriptions     |                1 | id                  | bigint                   | NO          | nextval('ndsp_subscriptions_id_seq'::regclass)
 ndsp_subscriptions     |                2 | user_id             | text                     | NO          | 
 ndsp_subscriptions     |                3 | user_email          | text                     | YES         | 
 ndsp_subscriptions     |                4 | plan_id             | integer                  | YES         | 
 ndsp_subscriptions     |                5 | plan_code           | text                     | YES         | 
 ndsp_subscriptions     |                6 | status              | text                     | NO          | 'active'::text
 ndsp_subscriptions     |                7 | provider            | text                     | NO          | 'nowpayments'::text
 ndsp_subscriptions     |                8 | provider_order_id   | text                     | YES         | 
 ndsp_subscriptions     |                9 | provider_payment_id | text                     | YES         | 
 ndsp_subscriptions     |               10 | billing_cycle       | text                     | NO          | 'monthly'::text
 ndsp_subscriptions     |               11 | starts_at           | timestamp with time zone | NO          | now()
 ndsp_subscriptions     |               12 | ends_at             | timestamp with time zone | YES         | 
 ndsp_subscriptions     |               13 | created_at          | timestamp with time zone | NO          | now()
 ndsp_subscriptions     |               14 | updated_at          | timestamp with time zone | NO          | now()
(28 rows)


=== CONSTRAINTS ===


- FINAL_STATUS: `NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_FAILED`
- FINAL_STATUS: `NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_FAILED`
- FAIL: UNEXPECTED_EXIT_CODE_1_AT_LINE_432
- FAIL: UNEXPECTED_EXIT_CODE_1_AT_LINE_432
- Database writes: NO
- Database writes: NO
- Source changes: NO
- Source changes: NO
- Nginx changes: NO
- Nginx changes: NO
- Service changes/restarts: NO
- Service changes/restarts: NO
- REPORT: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_20260730_011442/REPORT.md
- REPORT: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_20260730_011442/REPORT.md

- FINAL_STATUS: `NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_FAILED`
- FAIL: UNEXPECTED_EXIT_CODE_1_AT_LINE_502
- Database writes: NO
- Source changes: NO
- Nginx changes: NO
- Service changes/restarts: NO
- REPORT: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_4_20260730_011442/REPORT.md
