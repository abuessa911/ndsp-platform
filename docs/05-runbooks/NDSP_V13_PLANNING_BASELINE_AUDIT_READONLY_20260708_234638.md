# NDSP V1.3 Planning Baseline Audit — Read-only
DATE=2026-07-08T23:46:38+02:00
MODE=V13_PLANNING_BASELINE_AUDIT_READONLY
MODIFICATIONS=Report_and_scope_draft_only
NO_RUNTIME_CHANGE=1
NO_REBOOT=1
NO_RESTART=1
NO_START=1
NO_STOP=1
NO_ENABLE=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_PM2_CHANGE=1
ARTIFACT_DIR=/tmp/NDSP_V13_PLANNING_BASELINE_20260708_234638

## 1) P3 closure verification
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=P3_FINAL_CLEAN_HEALTH_STATUS=OK
LOCK_KEY_OK=P3_FINAL_RELEASE_PACKAGE_STATUS=CREATED
LOCK_KEY_OK=P3_CONTROLLED_REBOOT_AFTER_FIX_I_STATUS=OK
LOCK_KEY_OK=P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_STATUS=OK
LOCK_KEY_OK=P2_POST_G_FINAL_CLEAN_HEALTH_STATUS=OK

## 2) Runtime baseline
SYSTEM_RUNNING_STATE=running
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE=active
PM2_ENABLED=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 24m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.6mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.8%[39m | [1mram usage[22m: [32m7.6%[39m | [1mlo[22m: ⇓ [32m0.01mb/s[39m ⇑ [32m0.01mb/s[39m | [1meth0[22m: ⇓ [32m0.151mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ [32m0.737mb/s[39m ⇑ [32m0.295mb/s[39m [90m/[39m [1m[33m82.07%[39m[22m |

## 3) Public endpoint baseline
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200

## 4) Release package baseline
2026-07-07 10:47 6672 /home/nawaf511/ndsp_release_packages/NDSP_RELEASE_HANDOFF_20260707_104741.tar.gz
2026-07-07 10:51 113817 /home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz
2026-07-07 10:51 151 /home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz.sha256
2026-07-07 11:19 157 /home/nawaf511/ndsp_release_packages/NDSP_FINAL_GOVERNANCE_CLOSEOUT_20260707_111907.tar.gz.sha256
2026-07-07 11:19 8415 /home/nawaf511/ndsp_release_packages/NDSP_FINAL_GOVERNANCE_CLOSEOUT_20260707_111907.tar.gz
2026-07-07 14:44 114 /home/nawaf511/ndsp_release_packages/NDSP_BROWSER_QA_CLOSEOUT_20260707_154205.tar.gz.sha256
2026-07-07 14:44 124763 /home/nawaf511/ndsp_release_packages/NDSP_BROWSER_QA_CLOSEOUT_20260707_154205.tar.gz
2026-07-07 17:19 114 /home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz.sha256
2026-07-07 17:19 13517 /home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
2026-07-07 17:19 20738 /home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz
2026-07-07 23:01 118706 /home/nawaf511/ndsp_release_packages/NDSP_V1_RELEASE_PACKAGE_20260707_230119.tar.gz
2026-07-07 23:01 150 /home/nawaf511/ndsp_release_packages/NDSP_V1_RELEASE_PACKAGE_20260707_230119.tar.gz.sha256
2026-07-08 00:44 151 /home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz.sha256
2026-07-08 00:44 21737 /home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz
2026-07-08 06:43 150 /home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz.sha256
2026-07-08 06:43 63456 /home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz
2026-07-08 22:31 163 /home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz.sha256
2026-07-08 22:31 93801 /home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz
2026-07-08 22:34 163 /home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223425.tar.gz.sha256
2026-07-08 22:34 95811 /home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223425.tar.gz
2026-07-08 23:32 123384 /home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz
2026-07-08 23:32 156 /home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz.sha256

## 5) User portal pages baseline
alerts-log.html
asset-selector.html
completed-decisions.html
daily-brief.html
decision-center.html
decision-guide.html
decision-modes-guide.html
decision-radar.html
decision-support.html
disclaimer.html
dollar-impact.html
dollar-news.html
index.html
my-watchlist.html
NDSP_Asset_View.html
NDSP_Command_Center.html
NDSP_Daily_Brief.html
NDSP_Settings_Alerts.html
nmp.html
pro-guide.html
settings.html
support-center.html
usd-pulse.html
user-guide.html

## 6) Protected assets baseline
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 7) Data files baseline
drwxrwxr-x 2 nawaf511 nawaf511 4096 يوليو   8 23:46 /var/www/ndsp-my/data
-rw-r--r-- nawaf511 nawaf511 11270 2026-07-08 23:42 /var/www/ndsp-my/data/news-impact.json
-rw-r--r-- nawaf511 nawaf511 33130 2026-07-08 23:42 /var/www/ndsp-my/data/economic-calendar.json
-rw-r--r-- nawaf511 nawaf511 711 2026-07-08 23:42 /var/www/ndsp-my/data/data-quality.json
-rw-r--r-- root root 46286 2026-07-08 23:46 /var/www/ndsp-my/data/command-center-real.json

## 8) API/Nginx routing baseline
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=1358,fd=13))                                                                                                                                                                                                      
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1324,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1319,fd=33))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1317,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2691,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1328,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2702,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2720,fd=32))                                                                                                                                                                                                         
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:14:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:35:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:37:        proxy_ssl_server_name on;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:38:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:55:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:59:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:60:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:77:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:79:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:86:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:98:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:110:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:131:        proxy_pass http://127.0.0.1:9064/api/trial/seats;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:159:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:161:        proxy_ssl_server_name on;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:162:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:177:        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:184:        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:191:        proxy_pass http://127.0.0.1:9083/health;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:29:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:87:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:88:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:130:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:178:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:185:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:193:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:197:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:198:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:199:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:200:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:201:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:202:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:203:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:6:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:7:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:10:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:17:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:24:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:31:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:38:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:45:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:52:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:59:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:66:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:73:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:80:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:87:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:95:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/ndsp-bot-disabled.conf.off_20260625_090658:8:    server_name bot.ndsp.app;
/etc/nginx/conf.d/ndsp-bot-disabled.conf.off_20260625_090658:24:    server_name bot.ndsp.app;
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:9:# - Platform backend: 127.0.0.1:9001
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:19:    server 127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:10:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:44:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:145:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:193:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:200:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:208:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:212:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:213:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:214:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:215:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:216:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:217:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:218:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:7:    server_name api.ndsp.app;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:9:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:10:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:15:        proxy_pass http://127.0.0.1:9078/api/completed;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:23:        proxy_pass http://127.0.0.1:9078/api/completed/latest;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:31:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:39:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:47:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:56:        proxy_pass http://127.0.0.1:9079/health;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:64:        proxy_pass http://127.0.0.1:9079/api/governance/evaluate;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:4:    server_name admin.ndsp.app;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:24:    server_name admin.ndsp.app;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:26:    ssl_certificate /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:27:    ssl_certificate_key /etc/letsencrypt/live/admin.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:35:        proxy_pass http://127.0.0.1:9068/health;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:44:        proxy_pass http://127.0.0.1:9068/;
/etc/nginx/conf.d/000-ndsp-app-root-final.conf.disabled_20260625_090629:8:#     server_name ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-root-final.conf.disabled_20260625_090629:23:#     server_name ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:10:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:44:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:145:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:193:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:200:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:208:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:212:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:213:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:214:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:215:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:216:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:217:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:218:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:233:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:29:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:87:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:88:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:93:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:102:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:111:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:120:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:130:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:178:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:185:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:193:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:197:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:198:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:199:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:200:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:201:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:202:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:203:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:218:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:230:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:4:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:6:    return 301 https://my.ndsp.app$request_uri;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:24:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:29:    return 301 https://my.ndsp.app$request_uri;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:6:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:7:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:10:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:17:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:24:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:31:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:38:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:45:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:52:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:59:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:66:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:73:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:80:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:87:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:14:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:35:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:37:        proxy_ssl_server_name on;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:38:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:55:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:59:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:60:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:77:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:79:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:86:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:98:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:110:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:122:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:131:        proxy_pass http://127.0.0.1:9064/api/trial/seats;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:159:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:161:        proxy_ssl_server_name on;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:162:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:177:        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:184:        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:191:        proxy_pass http://127.0.0.1:9083/health;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:5:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:10:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:18:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:33:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:46:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:64:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:69:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:77:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:89:    ssl_certificate /etc/letsencrypt/live/my.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:90:    ssl_certificate_key /etc/letsencrypt/live/my.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:140:        proxy_pass http://127.0.0.1:9083/health;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:147:        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:154:        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:162:        proxy_pass http://127.0.0.1:9084/api/decision/quality-contract-v53$is_args$args;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:169:        proxy_pass https://api.ndsp.app/api/;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:170:        proxy_ssl_server_name on;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:171:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:185:        proxy_pass http://127.0.0.1:9093/api/v3/portal/;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:219:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:232:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:10:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:44:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:108:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:117:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:126:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:135:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:145:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:193:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:200:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:208:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:212:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:213:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:214:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:215:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }

## 9) Governance wording baseline scan
/var/www/ndsp-my/data/command-center-real.json:47:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:135:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:223:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:311:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:399:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:487:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:575:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:663:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:751:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/data/command-center-real.json:839:        "note_ar": "هذا تصنيف لطبيعة الاتجاه، مستقل عن TDL-M&L و TDL-S.",
/var/www/ndsp-my/assets/markets-hq.js:37:["USOIL","WTI Crude Oil","النفط الأمريكي","Energy"],["UKOIL","Brent Crude Oil","برنت","Energy"],["NATGAS","Natural Gas","الغاز الطبيعي","Energy"],["GASOLINE","Gasoline","البنزين","Energy"],
GOVERNANCE_WORDING_HITS=11

## 10) Candidate V1.3 scope draft
# NDSP V1.3 Scope Draft — 20260708_234638

## Baseline

- P3 Final is closed.
- systemctl --failed = 0.
- Nginx active = active.
- PM2 active = active.
- API health = 200.
- quality-live = 200.
- my.ndsp.app = 200.
- admin.ndsp.app = 200.
- Protected assets were checksummed in this report.
- Data files were indexed in this report.
- Release packages were indexed in this report.

## V1.3 Objective

V1.3 is not a rescue phase. V1.3 is a controlled product-improvement phase built on a clean runtime.

## Proposed V1.3 Workstreams

### 1) Decision Room UX Completion

Goal:
Improve the user-facing decision room experience without changing the backend decision logic.

Allowed:
- Better Arabic/English labels.
- Better explanation of reading states.
- Better page navigation.
- Better empty/loading/error states.
- Better beginner/advanced separation.

Not allowed:
- Buy/Sell wording.
- Trading recommendation wording.
- Execution instructions.
- Changing locked decision logic.

### 2) Data Freshness and Trust Panel

Goal:
Make users see whether the decision room is reading fresh data.

Allowed:
- Show data-quality.json summary.
- Show last update time.
- Show source health.
- Show warning when a feed is stale.

Not allowed:
- Fake freshness.
- Hiding stale-data warnings.

### 3) Completed Decisions Viewer Hardening

Goal:
Make completed decisions easier to review and audit.

Allowed:
- Filter by asset.
- Filter by state.
- Show readiness vs strength.
- Show why_not_completed.
- Show scenario levels.

Not allowed:
- Execution buttons.
- Bot trading controls inside NDSP core.

### 4) Admin Release Evidence Page

Goal:
Add internal admin page or static report link that shows:
- Current package.
- Current SHA256.
- Last post-patch report.
- Current runtime lock status.

Not allowed:
- Direct shell execution from browser.
- Direct service control from public UI.

### 5) Visual Polish Without Script Stacking

Goal:
Clean visual experience while preserving existing protected assets.

Allowed:
- CSS-only refinements.
- Component-level UI cleanup.
- Remove duplicate labels/navigation.

Not allowed:
- Replacing protected radar/menu/disclaimer scripts.
- Stacking new global scripts without removal plan.

## Hard Non-Goals

- No bot integration inside NDSP core.
- No enabling ndip-api-new.service.
- No enabling disabled legacy services.
- No changing Nginx without separate patch.
- No reboot in V1.3 unless a separate reboot drill is approved.
- No direct trading advice.
- No "Buy/Sell" wording.
- No execution workflow.

## Recommended Next Step

Create V1.3 Scope Freeze after reviewing this draft.

Required next artifact:
- NDSP_V13_SCOPE_FREEZE_AR.md
- NDSP_V13_SCOPE_FREEZE_EN.md
- NDSP_V13_IMPLEMENTATION_PLAN.md

Rule:
No V1.3 code patch before Scope Freeze + Backup + Report + Post Patch Test.

## 11) Final Evaluation
OK_EVALUATION=1
V13_PLANNING_BASELINE_STATUS=OK
FINAL_STATUS=V13_PLANNING_BASELINE_AUDIT_READONLY_OK
REPORT=docs/05-runbooks/NDSP_V13_PLANNING_BASELINE_AUDIT_READONLY_20260708_234638.md
SCOPE_DRAFT=docs/05-runbooks/NDSP_V13_SCOPE_DRAFT_20260708_234638.md
ARTIFACT_DIR=/tmp/NDSP_V13_PLANNING_BASELINE_20260708_234638
