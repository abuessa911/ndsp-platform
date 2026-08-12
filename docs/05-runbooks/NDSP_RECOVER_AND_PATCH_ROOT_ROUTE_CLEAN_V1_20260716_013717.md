# NDSP Recover And Patch Root Route Clean V1

- Date: 2026-07-16T01:37:17+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Mode: REMOVE_REDIRECTS_PATCH_REACT_ROOT_ROUTE_NO_SERVER_REDIRECT
- Backup: /home/nawaf511/ndsp_launch_backups/recover_and_patch_root_route_clean_v1_20260716_013717
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_RECOVER_AND_PATCH_ROOT_ROUTE_CLEAN_V1_20260716_013717.md

== 1) Current state ==
$ curl -I https://my.ndsp.app/
HTTP/2 302 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:37:17 GMT
content-type: text/html
content-length: 154
location: https://my.ndsp.app/decision-support.html
cache-control: no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0
pragma: no-cache
expires: 0


$ curl -L https://my.ndsp.app/
HTTP=302 FINAL=https://my.ndsp.app/decision-support.html

== 2) Backup live HTML and current JS bundle ==
BACKUP: /var/www/ndsp-my/index.html
BACKUP: /var/www/ndsp-my/assets/index-CdX-Uybq.js
MAIN_JS_REL=/assets/index-CdX-Uybq.js
MAIN_JS_PATH=/var/www/ndsp-my/assets/index-CdX-Uybq.js

== 3) Remove broken HTML redirect blocks from current HTML files ==
BACKUP: /var/www/ndsp-my/admin/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/admin/index.html
BACKUP: /var/www/ndsp-my/data-infra/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/data-infra/index.html
BACKUP: /var/www/ndsp-my/data/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/data/index.html
BACKUP: /var/www/ndsp-my/decision-guide.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/decision-guide.html
BACKUP: /var/www/ndsp-my/decision-room-v30-1/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/decision-room-v30-1/index.html
BACKUP: /var/www/ndsp-my/decision-room-v30/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/decision-room-v30/index.html
BACKUP: /var/www/ndsp-my/decision-room-v31/account/admin-owner.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/decision-room-v31/account/admin-owner.html
BACKUP: /var/www/ndsp-my/decision-room-v31/account/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/decision-room-v31/account/index.html
BACKUP: /var/www/ndsp-my/decision-room-v31/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/decision-room-v31/index.html
BACKUP: /var/www/ndsp-my/guide.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/guide.html
BACKUP: /var/www/ndsp-my/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/index.html
BACKUP: /var/www/ndsp-my/login/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/login/index.html
BACKUP: /var/www/ndsp-my/owner/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/owner/index.html
BACKUP: /var/www/ndsp-my/register/index.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/register/index.html
BACKUP: /var/www/ndsp-my/user-guide.html
CLEANED HTML REDIRECT BLOCKS: /var/www/ndsp-my/user-guide.html

== 4) Remove broken Nginx redirect blocks ==
BACKUP: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
UPDATED: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
BACKUP: /etc/nginx/conf.d/000-my.ndsp.app-final.conf.disabled_by_d10_d4_20260709_173339
UPDATED: /etc/nginx/conf.d/000-my.ndsp.app-final.conf.disabled_by_d10_d4_20260709_173339

== 5) Patch React Router root route to current decision page component ==
