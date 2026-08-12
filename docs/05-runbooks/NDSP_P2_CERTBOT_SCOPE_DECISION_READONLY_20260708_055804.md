# NDSP P2 Certbot Scope Decision Read-only
DATE=2026-07-08T05:58:04+02:00
MODE=ROOT_READ_ONLY_CERTBOT_SCOPE_DECISION
MODIFICATIONS=None

## 1) Certbot certificates
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

## 2) Renewal configs
total 40
drwxr-xr-x 2 root root 4096 يونيو  28 19:30 .
drwxr-xr-x 9 root root 4096 يوليو   8 05:58 ..
-rw-r--r-- 1 root root  543 يونيو  16 22:15 admin.ndsp.app.conf
-rw-r--r-- 1 root root  548 أبريل  16 04:21 api.nawafo.shop.conf
-rw-r--r-- 1 root root  533 يونيو  28 19:30 api.ndsp.app.conf
-rw-r--r-- 1 root root  533 مايو   29 19:11 bot.ndsp.app.conf
-rw-r--r-- 1 root root  578 أبريل  16 04:06 dashboard.nawafo.shop.conf
-rw-r--r-- 1 root root  528 يونيو  21 22:01 my.ndsp.app.conf
-rw-r--r-- 1 root root  528 مايو    3 01:01 nawafo.shop.conf
-rw-r--r-- 1 root root  538 مايو   23 18:07 ndsp.app-0005.conf

### RENEWAL_CONF=/etc/letsencrypt/renewal/admin.ndsp.app.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/admin.ndsp.app
4:cert = /etc/letsencrypt/live/admin.ndsp.app/cert.pem
5:privkey = /etc/letsencrypt/live/admin.ndsp.app/privkey.pem
6:chain = /etc/letsencrypt/live/admin.ndsp.app/chain.pem
7:fullchain = /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem
12:authenticator = nginx
13:installer = nginx
14:server = https://acme-v02.api.letsencrypt.org/directory

### RENEWAL_CONF=/etc/letsencrypt/renewal/api.nawafo.shop.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/api.nawafo.shop
4:cert = /etc/letsencrypt/live/api.nawafo.shop/cert.pem
5:privkey = /etc/letsencrypt/live/api.nawafo.shop/privkey.pem
6:chain = /etc/letsencrypt/live/api.nawafo.shop/chain.pem
7:fullchain = /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem
12:authenticator = nginx
13:installer = nginx
14:server = https://acme-v02.api.letsencrypt.org/directory

### RENEWAL_CONF=/etc/letsencrypt/renewal/api.ndsp.app.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/api.ndsp.app
4:cert = /etc/letsencrypt/live/api.ndsp.app/cert.pem
5:privkey = /etc/letsencrypt/live/api.ndsp.app/privkey.pem
6:chain = /etc/letsencrypt/live/api.ndsp.app/chain.pem
7:fullchain = /etc/letsencrypt/live/api.ndsp.app/fullchain.pem
12:authenticator = nginx
13:server = https://acme-v02.api.letsencrypt.org/directory
15:installer = nginx

### RENEWAL_CONF=/etc/letsencrypt/renewal/bot.ndsp.app.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/bot.ndsp.app
4:cert = /etc/letsencrypt/live/bot.ndsp.app/cert.pem
5:privkey = /etc/letsencrypt/live/bot.ndsp.app/privkey.pem
6:chain = /etc/letsencrypt/live/bot.ndsp.app/chain.pem
7:fullchain = /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem
12:authenticator = nginx
13:installer = nginx
14:server = https://acme-v02.api.letsencrypt.org/directory

### RENEWAL_CONF=/etc/letsencrypt/renewal/dashboard.nawafo.shop.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/dashboard.nawafo.shop
4:cert = /etc/letsencrypt/live/dashboard.nawafo.shop/cert.pem
5:privkey = /etc/letsencrypt/live/dashboard.nawafo.shop/privkey.pem
6:chain = /etc/letsencrypt/live/dashboard.nawafo.shop/chain.pem
7:fullchain = /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem
12:authenticator = nginx
13:installer = nginx
14:server = https://acme-v02.api.letsencrypt.org/directory

### RENEWAL_CONF=/etc/letsencrypt/renewal/my.ndsp.app.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/my.ndsp.app
4:cert = /etc/letsencrypt/live/my.ndsp.app/cert.pem
5:privkey = /etc/letsencrypt/live/my.ndsp.app/privkey.pem
6:chain = /etc/letsencrypt/live/my.ndsp.app/chain.pem
7:fullchain = /etc/letsencrypt/live/my.ndsp.app/fullchain.pem
12:authenticator = nginx
13:server = https://acme-v02.api.letsencrypt.org/directory
15:installer = nginx

### RENEWAL_CONF=/etc/letsencrypt/renewal/nawafo.shop.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/nawafo.shop
4:cert = /etc/letsencrypt/live/nawafo.shop/cert.pem
5:privkey = /etc/letsencrypt/live/nawafo.shop/privkey.pem
6:chain = /etc/letsencrypt/live/nawafo.shop/chain.pem
7:fullchain = /etc/letsencrypt/live/nawafo.shop/fullchain.pem
12:authenticator = nginx
13:installer = nginx
14:server = https://acme-v02.api.letsencrypt.org/directory

### RENEWAL_CONF=/etc/letsencrypt/renewal/ndsp.app-0005.conf
2:version = 2.9.0
3:archive_dir = /etc/letsencrypt/archive/ndsp.app-0005
4:cert = /etc/letsencrypt/live/ndsp.app-0005/cert.pem
5:privkey = /etc/letsencrypt/live/ndsp.app-0005/privkey.pem
6:chain = /etc/letsencrypt/live/ndsp.app-0005/chain.pem
7:fullchain = /etc/letsencrypt/live/ndsp.app-0005/fullchain.pem
12:authenticator = nginx
13:installer = nginx
14:server = https://acme-v02.api.letsencrypt.org/directory

## 3) Nginx references to certificate paths
/etc/nginx/sites-enabled/bot.ndsp.app:19:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/sites-enabled/bot.ndsp.app:20:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:59:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:60:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:87:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:88:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:6:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:7:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/ndsp-bot-disabled.conf.off_20260625_090658:26:    ssl_certificate /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/ndsp-bot-disabled.conf.off_20260625_090658:27:    ssl_certificate_key /etc/letsencrypt/live/bot.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:9:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:10:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:26:    ssl_certificate /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:27:    ssl_certificate_key /etc/letsencrypt/live/admin.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-ndsp-app-root-final.conf.disabled_20260625_090629:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-ndsp-app-root-final.conf.disabled_20260625_090629:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:87:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:88:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:26:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:27:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:6:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:7:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:59:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:60:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:89:    ssl_certificate /etc/letsencrypt/live/my.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:90:    ssl_certificate_key /etc/letsencrypt/live/my.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:144:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:145:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf.disabled_20260625_090629:25:    ssl_certificate /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf.disabled_20260625_090629:26:    ssl_certificate_key /etc/letsencrypt/live/admin.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:35:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:36:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:102:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:103:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:87:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:88:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:87:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:88:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem;
/etc/nginx/sites-available/bot.ndsp.app:20:    ssl_certificate /etc/letsencrypt/live/api.ndsp.app/fullchain.pem; # managed by Certbot
/etc/nginx/sites-available/bot.ndsp.app:21:    ssl_certificate_key /etc/letsencrypt/live/api.ndsp.app/privkey.pem; # managed by Certbot
/etc/nginx/sites-available/ndsp-trading-bot.conf:19:#     ssl_certificate /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem;
/etc/nginx/sites-available/ndsp-trading-bot.conf:20:#     ssl_certificate_key /etc/letsencrypt/live/bot.ndsp.app/privkey.pem;

## 4) Server names using old nawafo domains and NDSP domains
/etc/nginx/sites-enabled/bot.ndsp.app:9:    server_name bot.ndsp.app;
/etc/nginx/sites-enabled/bot.ndsp.app:18:    server_name bot.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:14:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf:55:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/ndsp-bot-disabled.conf.off_20260625_090658:8:    server_name bot.ndsp.app;
/etc/nginx/conf.d/ndsp-bot-disabled.conf.off_20260625_090658:24:    server_name bot.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:7:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:4:    server_name admin.ndsp.app;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf:24:    server_name admin.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-root-final.conf.disabled_20260625_090629:8:#     server_name ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-root-final.conf.disabled_20260625_090629:23:#     server_name ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:4:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629:24:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:14:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.before_v52_route_20260703_212358:55:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:5:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:64:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:9:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:140:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf.disabled_20260625_090629:4:    server_name admin.ndsp.app;
/etc/nginx/conf.d/000-admin-ndsp-app-canonical-only.conf.disabled_20260625_090629:23:    server_name admin.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:6:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf.disabled_20260625_090629:30:    server_name ndsp.app www.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/sites-available/bot.ndsp.app:9:    server_name bot.ndsp.app;
/etc/nginx/sites-available/bot.ndsp.app:19:    server_name bot.ndsp.app;
/etc/nginx/sites-available/ndsp:3:    server_name 161.97.144.189; # يمكنك وضع الدومين ndsp.app هنا لاحقاً
/etc/nginx/sites-available/ndsp-trading-bot.conf:6:#     server_name bot.ndsp.app;
/etc/nginx/sites-available/ndsp-trading-bot.conf:17:#     server_name bot.ndsp.app;
/etc/nginx/sites-available/bot.ndsp.app.conf.disabled.20260611_174628:5:#     server_name bot.ndsp.app;

## 5) Public HTTPS checks for NDSP domains
https://my.ndsp.app/ HTTP_CODE=200
https://api.ndsp.app/api/health HTTP_CODE=200
https://admin.ndsp.app/ HTTP_CODE=200
https://bot.ndsp.app/ HTTP_CODE=200

## 6) Public HTTPS checks for old nawafo domains
https://nawafo.shop/ HTTP_CODE=200
https://api.nawafo.shop/ HTTP_CODE=000
https://dashboard.nawafo.shop/ HTTP_CODE=000
https://admin.nawafo.shop/ HTTP_CODE=000

## 7) Certbot failed service snapshot
CERTBOT_TIMER_ACTIVE=active
CERTBOT_SERVICE_ACTIVE=failed
يوليو 05 06:40:26 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 05 06:40:34 vmi2934783 certbot[951716]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 05 06:40:41 vmi2934783 certbot[951716]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 05 06:40:51 vmi2934783 certbot[951716]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 05 06:40:52 vmi2934783 certbot[951716]: All renewals failed. The following certificates could not be renewed:
يوليو 05 06:40:52 vmi2934783 certbot[951716]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 05 06:40:52 vmi2934783 certbot[951716]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 05 06:40:52 vmi2934783 certbot[951716]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 05 06:40:52 vmi2934783 certbot[951716]: 3 renew failure(s), 0 parse failure(s)
يوليو 05 06:40:52 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 06:40:52 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 05 06:40:52 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 05 06:40:52 vmi2934783 systemd[1]: certbot.service: Consumed 9.988s CPU time.
-- Boot 30171be6091c48feadc15fe5b126358c --
يوليو 05 16:38:43 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 05 16:38:51 vmi2934783 certbot[1973622]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 05 16:38:58 vmi2934783 certbot[1973622]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 05 16:39:08 vmi2934783 certbot[1973622]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 05 16:39:08 vmi2934783 certbot[1973622]: All renewals failed. The following certificates could not be renewed:
يوليو 05 16:39:08 vmi2934783 certbot[1973622]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 05 16:39:08 vmi2934783 certbot[1973622]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 05 16:39:08 vmi2934783 certbot[1973622]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 05 16:39:08 vmi2934783 certbot[1973622]: 3 renew failure(s), 0 parse failure(s)
يوليو 05 16:39:08 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 16:39:08 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 05 16:39:08 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 05 16:39:08 vmi2934783 systemd[1]: certbot.service: Consumed 9.938s CPU time.
يوليو 06 11:43:18 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 06 11:43:26 vmi2934783 certbot[1822501]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 06 11:43:34 vmi2934783 certbot[1822501]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 06 11:43:44 vmi2934783 certbot[1822501]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 06 11:43:44 vmi2934783 certbot[1822501]: All renewals failed. The following certificates could not be renewed:
يوليو 06 11:43:44 vmi2934783 certbot[1822501]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 06 11:43:44 vmi2934783 certbot[1822501]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 06 11:43:44 vmi2934783 certbot[1822501]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 06 11:43:44 vmi2934783 certbot[1822501]: 3 renew failure(s), 0 parse failure(s)
يوليو 06 11:43:44 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 06 11:43:44 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 06 11:43:44 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 06 11:43:44 vmi2934783 systemd[1]: certbot.service: Consumed 10.729s CPU time.
يوليو 06 23:22:42 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 06 23:22:51 vmi2934783 certbot[2567992]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 06 23:22:58 vmi2934783 certbot[2567992]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 06 23:23:08 vmi2934783 certbot[2567992]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 06 23:23:08 vmi2934783 certbot[2567992]: All renewals failed. The following certificates could not be renewed:
يوليو 06 23:23:08 vmi2934783 certbot[2567992]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 06 23:23:08 vmi2934783 certbot[2567992]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 06 23:23:08 vmi2934783 certbot[2567992]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 06 23:23:08 vmi2934783 certbot[2567992]: 3 renew failure(s), 0 parse failure(s)
يوليو 06 23:23:08 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 06 23:23:08 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 06 23:23:08 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 06 23:23:08 vmi2934783 systemd[1]: certbot.service: Consumed 10.836s CPU time.
يوليو 07 10:28:46 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 07 10:28:54 vmi2934783 certbot[2964364]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 07 10:29:01 vmi2934783 certbot[2964364]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 07 10:29:11 vmi2934783 certbot[2964364]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 07 10:29:11 vmi2934783 certbot[2964364]: All renewals failed. The following certificates could not be renewed:
يوليو 07 10:29:11 vmi2934783 certbot[2964364]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 07 10:29:11 vmi2934783 certbot[2964364]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 07 10:29:11 vmi2934783 certbot[2964364]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 07 10:29:11 vmi2934783 certbot[2964364]: 3 renew failure(s), 0 parse failure(s)
يوليو 07 10:29:11 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 07 10:29:11 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 07 10:29:11 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 07 10:29:11 vmi2934783 systemd[1]: certbot.service: Consumed 10.271s CPU time.
يوليو 07 14:36:17 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 07 14:36:27 vmi2934783 certbot[3951735]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:34 vmi2934783 certbot[3951735]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: All renewals failed. The following certificates could not be renewed:
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: 3 renew failure(s), 0 parse failure(s)
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 07 14:36:44 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Consumed 10.925s CPU time.
يوليو 08 05:35:07 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 08 05:35:16 vmi2934783 certbot[3374784]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 08 05:35:23 vmi2934783 certbot[3374784]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 08 05:35:33 vmi2934783 certbot[3374784]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 08 05:35:33 vmi2934783 certbot[3374784]: All renewals failed. The following certificates could not be renewed:
يوليو 08 05:35:33 vmi2934783 certbot[3374784]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 08 05:35:33 vmi2934783 certbot[3374784]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 08 05:35:33 vmi2934783 certbot[3374784]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 08 05:35:33 vmi2934783 certbot[3374784]: 3 renew failure(s), 0 parse failure(s)
يوليو 08 05:35:34 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 05:35:34 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 08 05:35:34 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 08 05:35:34 vmi2934783 systemd[1]: certbot.service: Consumed 10.678s CPU time.

## 8) Runtime safety
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200

FINAL_STATUS=P2_CERTBOT_SCOPE_DECISION_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_CERTBOT_SCOPE_DECISION_READONLY_20260708_055804.md
