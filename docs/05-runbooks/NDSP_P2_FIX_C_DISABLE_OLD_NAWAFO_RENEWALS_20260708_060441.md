# NDSP P2 Fix C — Disable Old Nawafo Certbot Renewals
DATE=2026-07-08T06:04:41+02:00
MODE=CONTROLLED_CERTBOT_RENEWAL_SCOPE_FIX
MODIFICATION=Move old nawafo.shop renewal configs out of /etc/letsencrypt/renewal
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_CERTIFICATE_DELETE=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441

## 1) Pre-check
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Found the following certs:
  Certificate Name: admin.ndsp.app
    Serial Number: 53c2555386c244e08959a7d03e4fcd1710d
    Key Type: ECDSA
    Domains: admin.ndsp.app
    Expiry Date: 2026-09-14 19:16:28+00:00 (VALID: 68 days)
    Certificate Path: /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/admin.ndsp.app/privkey.pem
  Certificate Name: api.nawafo.shop
    Serial Number: 596f6ff6c673b9378dcfdec6934ea0ceb1f
    Key Type: ECDSA
    Domains: api.nawafo.shop
    Expiry Date: 2026-07-15 01:22:52+00:00 (VALID: 6 days)
    Certificate Path: /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/api.nawafo.shop/privkey.pem
  Certificate Name: api.ndsp.app
    Serial Number: 5514b9825a0a0668deff72724b31bd538ef
    Key Type: ECDSA
    Domains: ndsp.app api.ndsp.app bot.ndsp.app my.ndsp.app www.ndsp.app
    Expiry Date: 2026-09-26 16:32:02+00:00 (VALID: 80 days)
    Certificate Path: /etc/letsencrypt/live/api.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/api.ndsp.app/privkey.pem
  Certificate Name: bot.ndsp.app
    Serial Number: 6c699f94d44ff5f543c07dc8dd5a9d84d38
    Key Type: ECDSA
    Domains: bot.ndsp.app
    Expiry Date: 2026-08-27 16:13:14+00:00 (VALID: 50 days)
    Certificate Path: /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/bot.ndsp.app/privkey.pem
  Certificate Name: dashboard.nawafo.shop
    Serial Number: 6adc8a241341eca2cafe80d061a8b7106f7
    Key Type: ECDSA
    Domains: dashboard.nawafo.shop
    Expiry Date: 2026-07-15 01:08:12+00:00 (VALID: 6 days)
    Certificate Path: /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/dashboard.nawafo.shop/privkey.pem
  Certificate Name: my.ndsp.app
    Serial Number: 5750c4826ba90f0d77847aa481e3996a23d
    Key Type: ECDSA
    Domains: my.ndsp.app
    Expiry Date: 2026-09-19 19:03:08+00:00 (VALID: 73 days)
    Certificate Path: /etc/letsencrypt/live/my.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/my.ndsp.app/privkey.pem
  Certificate Name: nawafo.shop
    Serial Number: 565c144b329dd19d6f8a3a286ec689e3a54
    Key Type: ECDSA
    Domains: nawafo.shop admin.nawafo.shop api.nawafo.shop app.nawafo.shop ws.nawafo.shop www.nawafo.shop
    Expiry Date: 2026-07-31 22:02:27+00:00 (VALID: 23 days)
    Certificate Path: /etc/letsencrypt/live/nawafo.shop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/nawafo.shop/privkey.pem
  Certificate Name: ndsp.app-0005
    Serial Number: 60606b943519b2d8d2ab57cd34c990b05f5
    Key Type: ECDSA
    Domains: ndsp.app admin.ndsp.app api.ndsp.app my.ndsp.app www.ndsp.app
    Expiry Date: 2026-08-21 15:09:09+00:00 (VALID: 44 days)
    Certificate Path: /etc/letsencrypt/live/ndsp.app-0005/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/ndsp.app-0005/privkey.pem
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## 2) Backup and move old nawafo renewal configs only
MOVED_RENEWAL_CONF=/etc/letsencrypt/renewal/api.nawafo.shop.conf -> /home/nawaf511/ndsp_backups/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441/disabled_renewal_configs/api.nawafo.shop.conf.disabled_20260708_060441
MOVED_RENEWAL_CONF=/etc/letsencrypt/renewal/dashboard.nawafo.shop.conf -> /home/nawaf511/ndsp_backups/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441/disabled_renewal_configs/dashboard.nawafo.shop.conf.disabled_20260708_060441
MOVED_RENEWAL_CONF=/etc/letsencrypt/renewal/nawafo.shop.conf -> /home/nawaf511/ndsp_backups/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441/disabled_renewal_configs/nawafo.shop.conf.disabled_20260708_060441
MOVED_COUNT=3

## 3) Confirm remaining renewal configs
total 28
drwxr-xr-x 2 root root 4096 يوليو   8 06:04 .
drwxr-xr-x 9 root root 4096 يوليو   8 06:04 ..
-rw-r--r-- 1 root root  543 يونيو  16 22:15 admin.ndsp.app.conf
-rw-r--r-- 1 root root  533 يونيو  28 19:30 api.ndsp.app.conf
-rw-r--r-- 1 root root  533 مايو   29 19:11 bot.ndsp.app.conf
-rw-r--r-- 1 root root  528 يونيو  21 22:01 my.ndsp.app.conf
-rw-r--r-- 1 root root  538 مايو   23 18:07 ndsp.app-0005.conf

## 4) Confirm no active Nginx references to nawafo cert paths
NAWAFO_CERT_REF_COUNT=0

## 5) Certbot dry-run for remaining renewal set
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/admin.ndsp.app.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Simulating renewal of an existing certificate for admin.ndsp.app

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/api.ndsp.app.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Simulating renewal of an existing certificate for ndsp.app and 4 more domains

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/bot.ndsp.app.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Simulating renewal of an existing certificate for bot.ndsp.app

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/my.ndsp.app.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Simulating renewal of an existing certificate for my.ndsp.app

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/ndsp.app-0005.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Simulating renewal of an existing certificate for ndsp.app and 4 more domains

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations, all simulated renewals succeeded: 
  /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem (success)
  /etc/letsencrypt/live/api.ndsp.app/fullchain.pem (success)
  /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem (success)
  /etc/letsencrypt/live/my.ndsp.app/fullchain.pem (success)
  /etc/letsencrypt/live/ndsp.app-0005/fullchain.pem (success)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
CERTBOT_DRY_RUN_EXIT=0

## 6) Reset certbot failed state and check
CERTBOT_TIMER_ACTIVE=active
CERTBOT_SERVICE_ACTIVE=inactive
  UNIT                         LOAD   ACTIVE SUB    DESCRIPTION
● fanno-comments.service       loaded failed failed Fanno Comment Service
● marketpulse.service          loaded failed failed MarketPulse Backend Service
● ndip-api-new.service         loaded failed failed NDIP API - New Backend
● redis-replica.service        loaded failed failed Redis Replica
● redis-sentinel.service       loaded failed failed Redis Sentinel
● signal-engine.service        loaded failed failed Empire Core Signal Engine
● subscription-watcher.service loaded failed failed Subscription Expiry Watcher
● testapp.service              loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

8 loaded units listed.

## 7) Runtime safety
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.7%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.004mb/s[39m | [1meth0[22m: ⇓ [32m0.026mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.191mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |

## 8) Final Evaluation
P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_STATUS=OK
FINAL_STATUS=P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441
