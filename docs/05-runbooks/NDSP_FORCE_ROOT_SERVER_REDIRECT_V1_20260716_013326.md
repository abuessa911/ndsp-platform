# NDSP Force Root Server Redirect V1

- Date: 2026-07-16T01:33:26+02:00
- Domain: my.ndsp.app
- Target route: /decision-support.html
- Live: /var/www/ndsp-my
- Root index: /var/www/ndsp-my/index.html
- Mode: NGINX_EXACT_ROOT_REDIRECT_WITH_HTML_FALLBACK
- Backup: /home/nawaf511/ndsp_launch_backups/force_root_server_redirect_v1_20260716_013326
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FORCE_ROOT_SERVER_REDIRECT_V1_20260716_013326.md

== 1) Current HTTP state ==
$ curl -I https://my.ndsp.app/
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:33:26 GMT
content-type: text/html
content-length: 9870
last-modified: Wed, 15 Jul 2026 23:30:37 GMT
etag: "6a58181d-268e"
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff
accept-ranges: bytes


$ curl -L https://my.ndsp.app/
HTTP=200 FINAL=https://my.ndsp.app/

$ curl -L https://my.ndsp.app/decision-support.html
HTTP=200 FINAL=https://my.ndsp.app/decision-support.html

== 2) Install HTML fallback redirect into root index ==
BACKUP: /var/www/ndsp-my/index.html
OK: HTML fallback redirect injected into /var/www/ndsp-my/index.html

== 3) Locate Nginx configs for my.ndsp.app ==
- /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
- /etc/nginx/conf.d/000-my.ndsp.app-final.conf.disabled_by_d10_d4_20260709_173339
- /etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629

== 4) Patch Nginx exact root redirect ==
BACKUP: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
UPDATED: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
BACKUP: /etc/nginx/conf.d/000-my.ndsp.app-final.conf.disabled_by_d10_d4_20260709_173339
UPDATED: /etc/nginx/conf.d/000-my.ndsp.app-final.conf.disabled_by_d10_d4_20260709_173339
BACKUP: /etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629
NO CHANGE: /etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629

== 5) Test Nginx config ==
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
OK: nginx config test passed.

== 6) Reload Nginx ==
OK: nginx reloaded via systemctl.

== 7) Create rollback script ==
ROLLBACK: /tmp/ndsp_rollback_force_root_server_redirect_v1_20260716_013326.sh

== 8) Final HTTP verification ==
$ curl -I https://my.ndsp.app/?v=root-server-fix
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:33:27 GMT
content-type: text/html
content-length: 10488
last-modified: Wed, 15 Jul 2026 23:33:26 GMT
etag: "6a5818c6-28f8"
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff
accept-ranges: bytes


$ curl -L https://my.ndsp.app/?v=root-server-fix
HTTP=200 FINAL=https://my.ndsp.app/?v=root-server-fix

$ curl -L https://my.ndsp.app/decision-support.html?v=root-server-fix
HTTP=200 FINAL=https://my.ndsp.app/decision-support.html?v=root-server-fix

== 9) Browser check ==
