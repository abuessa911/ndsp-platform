# NDSP Root To Landing Final V1

- Date: 2026-07-16T01:51:45+02:00
- Domain: my.ndsp.app
- Preferred landing: https://www.ndsp.app/
- Fallback landing: https://ndsp.app/
- Live directory: /var/www/ndsp-my
- Backup: /home/nawaf511/ndsp_launch_backups/root_to_landing_final_v1_20260716_015145
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_ROOT_TO_LANDING_FINAL_V1_20260716_015145.md

== 1) Validate landing domain and TLS ==
OK: preferred landing is reachable with valid TLS.
SELECTED_LANDING=https://www.ndsp.app/

== 2) Current public state ==
Root:
HTTP=200 FINAL=https://my.ndsp.app/ REDIRECTS=0
Login:
HTTP=200 FINAL=https://my.ndsp.app/login/ REDIRECTS=0
Register:
HTTP=200 FINAL=https://my.ndsp.app/register/ REDIRECTS=0
Decision page:
HTTP=200 FINAL=https://my.ndsp.app/decision-support.html REDIRECTS=0

== 3) Remove previous browser redirect/anchor scripts ==
BACKUP: /var/www/ndsp-my/index.html
Root browser redirect cleanup completed.

== 4) Locate the active HTTPS Nginx configuration ==
ACTIVE_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf

== 5) Backup and patch only the active HTTPS server ==
BACKUP: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
PATCHED: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf

== 6) Test Nginx configuration ==
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
OK: nginx configuration test passed.

== 7) Reload Nginx ==
OK: nginx reloaded.

== 8) Safely archive hidden old web copies ==
ARCHIVED: /var/www/ndsp-my/.decision-room-v30-1.old.20260714_181031
ARCHIVED: /var/www/ndsp-my/.decision-room-v30-1.old.20260714_182723
ARCHIVED: /var/www/ndsp-my/.decision-room-v31.v32.old.20260714_211203
ARCHIVED: /var/www/ndsp-my/.decision-room-v31.v40.old.20260715_060256
ARCHIVED: /var/www/ndsp-my/.decision-room-v31.v33.old.20260714_214956
ARCHIVED: /var/www/ndsp-my/.decision-room-v30-1.old.20260714_181904
ARCHIVED: /var/www/ndsp-my/.decision-room-v31.v41.old.20260715_064120

== 9) Public verification ==
HTTP/2 302 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:51:46 GMT
content-type: text/html
content-length: 154
location: https://www.ndsp.app/
cache-control: no-store, no-cache, must-revalidate, max-age=0
pragma: no-cache
expires: 0


Root effective result:
HTTP=200 FINAL=https://www.ndsp.app/ REDIRECTS=1
Landing result:
HTTP=200 FINAL=https://www.ndsp.app/ REDIRECTS=0
Login remains available:
HTTP=200 FINAL=https://my.ndsp.app/login/ REDIRECTS=0
Register remains available:
HTTP=200 FINAL=https://my.ndsp.app/register/ REDIRECTS=0
Decision page remains available:
HTTP=200 FINAL=https://my.ndsp.app/decision-support.html REDIRECTS=0

== 10) Create rollback script ==
ROLLBACK=/tmp/ndsp_rollback_root_to_landing_final_v1_20260716_015145.sh

== 11) Final decision ==
ROOT_STATUS=302
ROOT_LOCATION=https://www.ndsp.app/
FINAL_STATUS=OK

Opening https://my.ndsp.app/ now sends the user to:
https://www.ndsp.app/

Login, registration and direct portal routes were not deleted.
Only hidden old backup directories were archived outside the web root.
