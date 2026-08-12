# NDSP Runtime Port Owner Diagnostics
DATE=2026-07-07T09:18:40+02:00

## Port 9002 owner
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=1390,fd=3))                                                                                                                                                                                                                               

## Other likely ports
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=1387,fd=13))                                                                                                                                                                                                                              
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=1390,fd=3))                                                                                                                                                                                                                               
LISTEN 0      511          0.0.0.0:3000      0.0.0.0:*    users:(("MainThread",pid=1099167,fd=21))                                                                                                                                                                                                                        

## Nginx upstream references
/etc/nginx/sites-enabled/bot.ndsp.app:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/sites-enabled/bot.ndsp.app:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9064/api/trial/seats;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:        proxy_pass http://127.0.0.1:9083/health;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:    server_name api.ndsp.app;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:# - Bot backend: 127.0.0.1:9002
/etc/nginx/conf.d/ndsp.conf_broken_1781102491:    server 127.0.0.1:9002;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:    server_name api.ndsp.app;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9078/api/completed;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9078/api/completed/latest;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9079/health;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:        proxy_pass http://127.0.0.1:9079/api/governance/evaluate;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:        proxy_pass http://127.0.0.1:9068/health;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:        proxy_pass http://127.0.0.1:9068/;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:    return 301 https://my.ndsp.app$request_uri;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:    return 301 https://my.ndsp.app$request_uri;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:    server_name api.ndsp.app;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9064/api/trial/seats;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass https://api.ndsp.app/api/auth/reset-password;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:        proxy_pass http://127.0.0.1:9083/health;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9092;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:    ssl_certificate /etc/letsencrypt/live/my.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:    ssl_certificate_key /etc/letsencrypt/live/my.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9083/health;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9084/api/decision/quality-contract-v53$is_args$args;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass https://api.ndsp.app/api/;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9093/api/v3/portal/;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    if ($host = api.ndsp.app) {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9082/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9082/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9078/api/completed;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9078/api/completed/latest;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9078$request_uri;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9079/health;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9079/api/governance/evaluate;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9028/api/register;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:        proxy_pass http://127.0.0.1:9028/api/auth/register;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9068/health;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9068/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_set_header Host api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9019/api/trial/register/health;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9019/api/trial/register/;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9019/api/trial/invites/validate;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9001/api/trial/status;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9064/api/trial/seats;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9061/api/decision/package-v2;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/login;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/me;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9020/api/auth/logout;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9001;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9067/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9066;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/ui-bridge/health { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/market-structure { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/technical-confirmation { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/macro-analysis { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/risk-layer { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/nawaf-signal { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/alerts { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:    location = /api/settings { proxy_pass http://127.0.0.1:9066; proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:        proxy_pass http://127.0.0.1:9061/api/decision/package-live;

## systemd unit files
# /etc/systemd/system/ndsp-api.service
[Unit]
Description=NDSP FastAPI Backend
After=network.target

[Service]
User=nawaf511
Group=www-data
WorkingDirectory=/home/nawaf511/empire-core-new/backend
Environment="PYTHONUNBUFFERED=1"
Environment="ENV=production"
EnvironmentFile=-/home/nawaf511/empire-core-new/backend/.env

ExecStart=/home/nawaf511/empire-core-new/backend/venv/bin/gunicorn app.main:app   -k uvicorn.workers.UvicornWorker   --bind 127.0.0.1:9001   --workers 4   --timeout 120

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/ndip-api-new.service
[Unit]
Description=NDIP API - New Backend
After=network.target

[Service]
Type=simple
User=nawaf511
WorkingDirectory=/home/nawaf511/empire-core-new/backend
EnvironmentFile=/home/nawaf511/empire-core-new/backend/.env
ExecStart=/home/nawaf511/empire-core-new/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 9000
Restart=always
RestartSec=5
TimeoutStopSec=20
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/ndip-api-new.service.d/10-mt4-dir.conf
[Service]
Environment=NDIP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4
Environment=NDSP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4

## backend package files
-rw-rw-r-- 1 nawaf511 nawaf511 421 يونيو  25 17:31 backend/package.json
-rw-rw-r-- 1 nawaf511 nawaf511 57K يونيو  25 17:31 backend/package-lock.json

{
  "name": "ndsp-auth-api",
  "version": "1.0.0",
  "main": "server.js",
  "type": "commonjs",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.6.1",
    "express": "^4.22.2",
    "helmet": "^7.1.0",
    "jsonwebtoken": "^9.0.3",
    "otplib": "^13.4.1",
    "pg": "^8.21.0",
    "qrcode": "^1.5.4",
    "speakeasy": "^2.0.0"
  }
}

## otplib dependency check
ndsp-auth-api@1.0.0 /home/nawaf511/empire-core-new/backend
└── (empty)

