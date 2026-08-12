# NDSP — Commercial Phase 1 Runtime and Schema Mapping V1.5

- Date: 2026-07-30T01:23:59+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Active auth database resolved: YES
- Database credentials printed: NO
- Target listener: 127.0.0.1:9094
- Target PID: 2497959
- Mode: READ_ONLY
- Output: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358

## 1. Exact process ownership and source path

=== LISTENER ===
LISTEN 0      5          127.0.0.1:9094       0.0.0.0:*    users:(("python3",pid=2497959,fd=6))                                                                                                                                                                                                                      

=== PID BASIC DATA ===
2497959       1 nawaf511 nawaf511 ر يوليو 29 06:52:50 2026 18:31:08 Ss /usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py

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
2497959       1 nawaf511 nawaf511 ر يوليو 29 06:52:50 2026 18:31:09 Ss /usr/bin/python3 /usr/local/lib/ndsp-business-ops/app.py

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

## 3. Exact runtime source and route extraction

=== EXACT MAIN SOURCE ===
MAIN_SOURCE=/usr/local/lib/ndsp-business-ops/app.py
  File: /usr/local/lib/ndsp-business-ops/app.py
  Size: 19581     	Blocks: 40         IO Block: 4096   regular file
Device: 8,1	Inode: 292252      Links: 1
Access: (0755/-rwxr-xr-x)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2026-07-29 06:53:37.702242427 +0200
Modify: 2026-07-20 18:02:34.616370514 +0200
Change: 2026-07-20 18:02:34.617370510 +0200
 Birth: 2026-07-20 18:02:34.616370514 +0200
cce1361d7ea7134873603cb4692dc2669b9ff36ee19a71f2205e045cb04ab052  /usr/local/lib/ndsp-business-ops/app.py

=== SOURCE CANDIDATES ===
/usr/local/lib/ndsp-business-ops/app.py
/usr/local/lib/ndsp-business-ops/daily_digest.py
/usr/local/lib/ndsp-business-ops/monitor.py

=== ROUTE AND HTTP PATH DEFINITIONS ===

--- FILE: /usr/local/lib/ndsp-business-ops/app.py ---
142:        conn.execute("DELETE FROM rate_events WHERE created_epoch < ?", (now - 86400,))
216:        self.send_header("Allow", "GET,POST,OPTIONS")
221:        parsed = urlparse(self.path)
222:        path = parsed.path
225:        if path == "/api/ops/public/config":
238:        if path == "/api/ops/public/plans":
240:        if path == "/api/ops/public/status":
243:        if path.startswith("/api/ops/admin/"):
246:            if path == "/api/ops/admin/summary":
248:            if path == "/api/ops/admin/export":
253:        path = urlparse(self.path).path
260:        if path.startswith("/api/ops/admin/"):
263:            if path == "/api/ops/admin/status":
266:        if path == "/api/ops/public/lead":
268:        if path == "/api/ops/public/support":
270:        if path == "/api/ops/public/subscription-request":
272:        if path == "/api/ops/public/onboarding-event":

--- FILE: /usr/local/lib/ndsp-business-ops/daily_digest.py ---
17: path=os.path.join(outbox,f'{stamp}_{safe}.eml')
49: path=os.path.join(REPORT_DIR,'NDSP_DAILY_BUSINESS_DIGEST_'+now.strftime('%Y%m%d')+'.md')

--- FILE: /usr/local/lib/ndsp-business-ops/monitor.py ---
47: path=os.path.join(outbox,f'{stamp}_{safe}.eml')
89:  c.execute('DELETE FROM monitor_checks WHERE id NOT IN (SELECT id FROM monitor_checks ORDER BY id DESC LIMIT 10000)')

=== RUNTIME SOURCE REFERENCES TO COMMERCIAL TABLES ===

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
       table_name       |                 conname                 | contype |                                                  definition                                                  
------------------------+-----------------------------------------+---------+--------------------------------------------------------------------------------------------------------------
 ndsp_legal_acceptances | ndsp_legal_acceptances_agent_hash_ck    | c       | CHECK (((user_agent_sha256 IS NULL) OR ((user_agent_sha256)::text ~ '^[0-9a-f]{64}$'::text)))
 ndsp_legal_acceptances | ndsp_legal_acceptances_email_hash_ck    | c       | CHECK (((email_sha256)::text ~ '^[0-9a-f]{64}$'::text))
 ndsp_legal_acceptances | ndsp_legal_acceptances_evidence_hash_ck | c       | CHECK (((evidence_sha256)::text ~ '^[0-9a-f]{64}$'::text))
 ndsp_legal_acceptances | ndsp_legal_acceptances_pkey             | p       | PRIMARY KEY (acceptance_id)
 ndsp_legal_acceptances | ndsp_legal_acceptances_request_uq       | u       | UNIQUE (request_id)
 ndsp_legal_acceptances | ndsp_legal_acceptances_status_ck        | c       | CHECK (((upstream_status IS NULL) OR ((upstream_status >= 100) AND (upstream_status <= 599))))
 ndsp_legal_acceptances | ndsp_legal_acceptances_versions_ck      | c       | CHECK (((length(disclaimer_version) > 0) AND (length(terms_version) > 0) AND (length(privacy_version) > 0)))
 ndsp_subscriptions     | ndsp_subscriptions_pkey                 | p       | PRIMARY KEY (id)
 ndsp_subscriptions     | ndsp_subscriptions_plan_id_fkey         | f       | FOREIGN KEY (plan_id) REFERENCES ndsp_plans(id) ON DELETE SET NULL
(9 rows)


=== INDEXES ===
       tablename        |                indexname                |                                                                             indexdef                                                                              
------------------------+-----------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 ndsp_legal_acceptances | ndsp_legal_acceptances_email_time_idx   | CREATE INDEX ndsp_legal_acceptances_email_time_idx ON public.ndsp_legal_acceptances USING btree (email_sha256, accepted_at DESC)
 ndsp_legal_acceptances | ndsp_legal_acceptances_pkey             | CREATE UNIQUE INDEX ndsp_legal_acceptances_pkey ON public.ndsp_legal_acceptances USING btree (acceptance_id)
 ndsp_legal_acceptances | ndsp_legal_acceptances_request_uq       | CREATE UNIQUE INDEX ndsp_legal_acceptances_request_uq ON public.ndsp_legal_acceptances USING btree (request_id)
 ndsp_legal_acceptances | ndsp_legal_acceptances_subject_time_idx | CREATE INDEX ndsp_legal_acceptances_subject_time_idx ON public.ndsp_legal_acceptances USING btree (subject_key, accepted_at DESC) WHERE (subject_key IS NOT NULL)
 ndsp_subscriptions     | idx_ndsp_subscriptions_user             | CREATE INDEX idx_ndsp_subscriptions_user ON public.ndsp_subscriptions USING btree (user_id)
 ndsp_subscriptions     | ndsp_subscriptions_pkey                 | CREATE UNIQUE INDEX ndsp_subscriptions_pkey ON public.ndsp_subscriptions USING btree (id)
 ndsp_subscriptions     | ndsp_subscriptions_user_idx             | CREATE INDEX ndsp_subscriptions_user_idx ON public.ndsp_subscriptions USING btree (user_id)
(7 rows)


=== REFERENCING VIEWS ===
 schemaname | viewname | definition 
------------+----------+------------
(0 rows)


=== REFERENCING FUNCTIONS ===

=== TABLE PRIVILEGES ===
       table_name       |  grantee  | privilege_type 
------------------------+-----------+----------------
 ndsp_legal_acceptances | ndsp_auth | DELETE
 ndsp_legal_acceptances | ndsp_auth | INSERT
 ndsp_legal_acceptances | ndsp_auth | REFERENCES
 ndsp_legal_acceptances | ndsp_auth | SELECT
 ndsp_legal_acceptances | ndsp_auth | TRIGGER
 ndsp_legal_acceptances | ndsp_auth | TRUNCATE
 ndsp_legal_acceptances | ndsp_auth | UPDATE
 ndsp_subscriptions     | ndsp_auth | DELETE
 ndsp_subscriptions     | ndsp_auth | INSERT
 ndsp_subscriptions     | ndsp_auth | REFERENCES
 ndsp_subscriptions     | ndsp_auth | SELECT
 ndsp_subscriptions     | ndsp_auth | TRIGGER
 ndsp_subscriptions     | ndsp_auth | TRUNCATE
 ndsp_subscriptions     | ndsp_auth | UPDATE
(14 rows)


## 6. Commercial source-to-service mapping

=== SYSTEMD REFERENCES TO COMMERCIAL SOURCE FILES ===
/etc/systemd/system/multi-user.target.wants/ndsp-user-login.service:17:ExecStart=/usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs
/etc/systemd/system/ndsp-user-login.service:17:ExecStart=/usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs

=== ACTIVE PROCESS REFERENCES ===
nawaf511 2498163       1  0 يوليو29 ? 00:01:55 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs

=== NGINX PAYMENT / SUBSCRIPTION / LEGAL ROUTES ===
/etc/nginx/snippets/ndsp-business-ops-v205.conf:6:location = /subscribe { return 301 /subscribe/; }
/etc/nginx/snippets/ndsp-business-ops-v205.conf:7:location ^~ /subscribe/ { alias /var/www/ndsp-business-ops/subscribe/; index index.html; add_header Cache-Control "no-store" always; }

=== PROJECT PACKAGE AND SERVICE REFERENCES ===
/home/nawaf511/empire-core-new/backend/ndsp_api_compat_gateway.cjs:222:    if (await tableExists('ndsp_nowpayments_payments')) {
/home/nawaf511/empire-core-new/backend/ndsp_api_compat_gateway.cjs:225:        FROM ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/ndsp_api_compat_gateway.cjs:235:      provider:'nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_admin_actions_bypass_old_middleware.cjs:207:    'nowpayments_payments',
/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:23:NOWPAYMENTS_API_BASE="https://api.nowpayments.io/v1"
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:80:  const sig = req.headers['x-nowpayments-sig'];
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:117:    INSERT INTO public.ndsp_subscriptions
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:120:      ($1,$2,$3,$4,'active','nowpayments',$5,$6,$7)
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:163:  router.get('/nowpayments/health', (_req, res) => {
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:166:      provider: 'nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:229:        INSERT INTO public.ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:249:        ipn_callback_url: `${PUBLIC_URL}/api/webhooks/nowpayments`,
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:254:      const npRes = await fetch('https://api.nowpayments.io/v1/invoice', {
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:274:          UPDATE public.ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:288:        UPDATE public.ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:306:          ('nowpayments','invoice_created',$1,'invoice_created',$2)
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:311:        provider: 'nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:318:      console.error('NOWPayments checkout error:', err);
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:328:  router.get('/webhooks/nowpayments', (_req, res) => {
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:331:      provider: 'nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:332:      endpoint: '/api/webhooks/nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:334:      message: 'NOWPayments IPN endpoint is active. Browser GET is only a health check.'
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:338:  router.post('/webhooks/nowpayments', async (req, res) => {
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:354:          ('nowpayments','ipn',$1,$2,$3)
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:362:        UPDATE public.ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:381:          FROM public.ndsp_subscriptions
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:393:      console.error('NOWPayments IPN error:', err);
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments.cjs:403:  console.log('✅ NDSP NOWPayments mounted: /api/checkout/create and /api/webhooks/nowpayments');
/home/nawaf511/empire-core-new/backend/.env.bak.20260527_025723:60:# NOWPayments
/home/nawaf511/empire-core-new/backend/migrations/001_postgres_core.sql:31:    provider TEXT NOT NULL DEFAULT 'nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_admin_actions_authoritative.cjs:187:    'nowpayments_payments',
/home/nawaf511/empire-core-new/backend/ndsp_admin_actions_gateway.cjs:218:    'nowpayments_payments',
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:15:    CREATE TABLE IF NOT EXISTS public.ndsp_nowpayments_payments (
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:35:    CREATE INDEX IF NOT EXISTS ndsp_nowpayments_user_idx
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:36:      ON public.ndsp_nowpayments_payments (user_id);
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:38:    CREATE INDEX IF NOT EXISTS ndsp_nowpayments_status_idx
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:39:      ON public.ndsp_nowpayments_payments (payment_status);
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:41:    CREATE TABLE IF NOT EXISTS public.ndsp_subscriptions (
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:48:      provider TEXT NOT NULL DEFAULT 'nowpayments',
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:58:    CREATE INDEX IF NOT EXISTS ndsp_subscriptions_user_idx
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:59:      ON public.ndsp_subscriptions (user_id);
/home/nawaf511/empire-core-new/backend/ndsp_nowpayments_migrate.cjs:72:  console.log('✅ NOWPayments tables ready');
/home/nawaf511/empire-core-new/backend/ndsp_admin_ui_proxy.cjs:373:    const paymentsA = await safeCount('ndsp_nowpayments_payments')
/home/nawaf511/empire-core-new/backend/ndsp_admin_ui_proxy.cjs:423:    const out = await queryExistingTables(['ndsp_nowpayments_payments','payments','payment_requests'], 200)
/home/nawaf511/empire-core-new/backend/ndsp_admin_ui_proxy.cjs:720:      const p1 = await updateByIdentity('ndsp_nowpayments_payments', 'approved', id, email, payment_id)
/home/nawaf511/empire-core-new/backend/ndsp_admin_ui_proxy.cjs:727:      const p1 = await updateByIdentity('ndsp_nowpayments_payments', 'rejected', id, email, payment_id)
/home/nawaf511/empire-core-new/backend/ndsp_checkout_plans_package/database/migrations/20260524_001_checkout_plans.sql:40:    provider TEXT NOT NULL DEFAULT 'manual_or_nowpayments',
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:13:router = APIRouter(tags=["ndsp-nowpayments-create-alias"])
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:70:@router.get("/api/ndsp/nowpayments-create-alias/health")
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:74:        "service": "ndsp-nowpayments-create-alias",
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:77:            "/api/v6/payments/nowpayments/subscription/create",
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:78:            "/api/payments/nowpayments/subscription/create",
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:82:@router.post("/api/v6/payments/nowpayments/subscription/create")
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:83:@router.post("/api/payments/nowpayments/subscription/create")
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:108:            INSERT INTO ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:147:                json.dumps({"provider": "nowpayments", "mode": "manual_review_required"}, ensure_ascii=False),
/home/nawaf511/empire-core-new/backend/app/api/compat/nowpayments_create_alias.py:153:        "provider": "nowpayments",
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:127:            "/api/v6/payments/nowpayments/subscription/create",
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:128:            "/api/payments/nowpayments/subscription/create",
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:206:@router.get("/api/v6/payments/nowpayments/subscription/status")
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:207:@router.get("/api/payments/nowpayments/subscription/status")
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:218:                FROM ndsp_subscriptions
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:240:@router.post("/api/v6/payments/nowpayments/subscription/create")
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:241:@router.post("/api/payments/nowpayments/subscription/create")
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:247:    audit("/api/v6/payments/nowpayments/subscription/create", email, payload)
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:258:                CREATE TABLE IF NOT EXISTS ndsp_nowpayments_payments (
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:273:                INSERT INTO ndsp_nowpayments_payments(user_email, plan_code, status, currency, network)
/home/nawaf511/empire-core-new/backend/app/api/compat/user_operational_compat.py:281:            "provider": "nowpayments",
/home/nawaf511/empire-core-new/backend/server.js:54:  const { installNowPayments } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs');
/home/nawaf511/empire-core-new/backend/server.js:57:  console.warn('⚠ NDSP NOWPayments skipped during V1:', e.message);
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_api_compat_gateway.cjs:222:    if (await tableExists('ndsp_nowpayments_payments')) {
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_api_compat_gateway.cjs:225:        FROM ndsp_nowpayments_payments
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_api_compat_gateway.cjs:235:      provider:'nowpayments',
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_actions_bypass_old_middleware.cjs:207:    'nowpayments_payments',
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs:774:    `INSERT INTO public.ndsp_legal_acceptances
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs:777:     ON CONFLICT (request_id) DO UPDATE SET upstream_status=COALESCE(EXCLUDED.upstream_status,public.ndsp_legal_acceptances.upstream_status)
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_actions_authoritative.cjs:187:    'nowpayments_payments',
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_actions_gateway.cjs:218:    'nowpayments_payments',
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_ui_proxy.cjs:373:    const paymentsA = await safeCount('ndsp_nowpayments_payments')
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_ui_proxy.cjs:423:    const out = await queryExistingTables(['ndsp_nowpayments_payments','payments','payment_requests'], 200)
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_ui_proxy.cjs:720:      const p1 = await updateByIdentity('ndsp_nowpayments_payments', 'approved', id, email, payment_id)
/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_ui_proxy.cjs:727:      const p1 = await updateByIdentity('ndsp_nowpayments_payments', 'rejected', id, email, payment_id)
/home/nawaf511/empire-core-new/backend/auth_api/.env:50:# NOWPayments
/home/nawaf511/empire-core-new/backend/.env:50:# NOWPayments

## 7. Safe GET/HEAD runtime probes


=== local_health ===
URL=http://127.0.0.1:9094/health
HTTP=200
--- HEADERS ---
HTTP/1.0 200 OK
Server: NDSPBusinessOps/204 Python/3.12.3
Date: Wed, 29 Jul 2026 23:24:30 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 74
Cache-Control: no-store
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

--- BODY (FIRST 4000 BYTES) ---
{"ok":true,"service":"ndsp-business-ops","version":"V205","database":true}

=== local_root ===
URL=http://127.0.0.1:9094/
HTTP=404
--- HEADERS ---
HTTP/1.0 404 Not Found
Server: NDSPBusinessOps/204 Python/3.12.3
Date: Wed, 29 Jul 2026 23:24:30 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 43
Cache-Control: no-store
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

--- BODY (FIRST 4000 BYTES) ---
{"ok":false,"error":"NOT_FOUND","path":"/"}

=== local_public_plans ===
URL=http://127.0.0.1:9094/api/ops/public/plans
HTTP=200
--- HEADERS ---
HTTP/1.0 200 OK
Server: NDSPBusinessOps/204 Python/3.12.3
Date: Wed, 29 Jul 2026 23:24:30 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 1112
Cache-Control: no-store
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

--- BODY (FIRST 4000 BYTES) ---
{"ok":true,"source":"existing_ndsp_packages_api","packages":[{"code":"trial","name":"Free","price":"0.00","description":"تجربة مجانية لمدة 16 يوم","trial_days":16,"features":["دخول أساسي","استبيان نهاية التجربة"],"limits":{"assets":3,"layers":"basic"},"is_active":true},{"code":"free","name":"Free","price":"0.00","description":"باقة دخول وتجربة أساسية","trial_days":16,"features":["BTC","ETH","GOLD","طبقات أساسية"],"limits":{"assets":3,"layers":"basic"},"is_active":true},{"code":"pro","name":"Pro","price":"49.00","description":"باقة احترافية لدعم القرار والسياق والتحليل","trial_days":16,"features":["BTC","ETH","XRP","SOL","GOLD","NASDAQ","طبقات متقدمة"],"limits":{"assets":6,"layers":"advanced"},"is_active":true},{"code":"elite","name":"Elite","price":"149.00","description":"باقة Elite بكامل تجربة NDSP","trial_days":16,"features":["كل الأصول","كل الطبقات","صلاحيات سيادية"],"limits":{"assets":"all","layers":"all"},"is_active":true}]}

=== local_subscriptions ===
URL=http://127.0.0.1:9094/api/subscriptions
HTTP=404
--- HEADERS ---
HTTP/1.0 404 Not Found
Server: NDSPBusinessOps/204 Python/3.12.3
Date: Wed, 29 Jul 2026 23:24:30 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 60
Cache-Control: no-store
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

--- BODY (FIRST 4000 BYTES) ---
{"ok":false,"error":"NOT_FOUND","path":"/api/subscriptions"}

=== public_ops_health ===
URL=https://my.ndsp.app/api/ops/health
HTTP=200
--- HEADERS ---
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 29 Jul 2026 23:24:30 GMT
content-type: application/json; charset=utf-8
content-length: 74
cache-control: no-store
x-content-type-options: nosniff
referrer-policy: same-origin
strict-transport-security: max-age=31536000
x-content-type-options: nosniff
referrer-policy: strict-origin-when-cross-origin
x-frame-options: SAMEORIGIN
content-security-policy: default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https: wss:; frame-ancestors 'self'; base-uri 'self'; object-src 'none';
permissions-policy: geolocation=(), microphone=(), camera=()
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff

--- BODY (FIRST 4000 BYTES) ---
{"ok":true,"service":"ndsp-business-ops","version":"V205","database":true}

=== public_plans ===
URL=https://my.ndsp.app/api/ops/public/plans
HTTP=200
--- HEADERS ---
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 29 Jul 2026 23:24:30 GMT
content-type: application/json; charset=utf-8
content-length: 1112
cache-control: no-store
x-content-type-options: nosniff
referrer-policy: same-origin
strict-transport-security: max-age=31536000
x-content-type-options: nosniff
referrer-policy: strict-origin-when-cross-origin
x-frame-options: SAMEORIGIN
content-security-policy: default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https: wss:; frame-ancestors 'self'; base-uri 'self'; object-src 'none';
permissions-policy: geolocation=(), microphone=(), camera=()
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff

--- BODY (FIRST 4000 BYTES) ---
{"ok":true,"source":"existing_ndsp_packages_api","packages":[{"code":"trial","name":"Free","price":"0.00","description":"تجربة مجانية لمدة 16 يوم","trial_days":16,"features":["دخول أساسي","استبيان نهاية التجربة"],"limits":{"assets":3,"layers":"basic"},"is_active":true},{"code":"free","name":"Free","price":"0.00","description":"باقة دخول وتجربة أساسية","trial_days":16,"features":["BTC","ETH","GOLD","طبقات أساسية"],"limits":{"assets":3,"layers":"basic"},"is_active":true},{"code":"pro","name":"Pro","price":"49.00","description":"باقة احترافية لدعم القرار والسياق والتحليل","trial_days":16,"features":["BTC","ETH","XRP","SOL","GOLD","NASDAQ","طبقات متقدمة"],"limits":{"assets":6,"layers":"advanced"},"is_active":true},{"code":"elite","name":"Elite","price":"149.00","description":"باقة Elite بكامل تجربة NDSP","trial_days":16,"features":["كل الأصول","كل الطبقات","صلاحيات سيادية"],"limits":{"assets":"all","layers":"all"},"is_active":true}]}

## 8. Classification

- Current-source reference lines: 8
- Exact 9094 runtime table-reference lines: 0
- Commercial service/provider reference lines: 87
- Nginx/runtime reference lines: 6
- Listener PID: 2497959
- Cgroup unit resolved: YES
- Local health HTTP: 200
- Classification: `ACTIVE_BUSINESS_OPS_RUNTIME_PLUS_SEPARATE_COMMERCIAL_DB_CONTRACTS`

## 9. Final result

- Database writes: NO
- Source changes: NO
- Nginx changes: NO
- Service changes/restarts: NO
- Deletion authorization: NO
- Process report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/PROCESS_RUNTIME.txt
- Nginx map: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/NGINX_ROUTE_MAP.txt
- Route map: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/SOURCE_ROUTE_MAP.txt
- Source references: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/SOURCE_TABLE_REFERENCES.txt
- Database schema map: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/DATABASE_SCHEMA_MAP.txt
- HTTP probes: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/READ_ONLY_HTTP_PROBES.txt
- Commercial service map: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_20260730_012358/COMMERCIAL_SERVICE_MAP.txt
- FINAL_STATUS: `NDSP_COMMERCIAL_PHASE1_RUNTIME_SCHEMA_MAP_V1_5_COMPLETE`
