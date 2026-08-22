# NDSP Recover Root To Decision Anchor V3

- Date: 2026-07-16T01:45:09+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Anchor: #decision-support
- Mode: REMOVE_REDIRECTS_AND_SCROLL_ROOT_TO_DECISION_SECTION
- Backup: /home/nawaf511/ndsp_launch_backups/recover_root_to_decision_anchor_v3_20260716_014509
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_RECOVER_ROOT_TO_DECISION_ANCHOR_V3_20260716_014509.md

== 1) Before state ==
$ curl -I https://my.ndsp.app/
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:45:09 GMT
content-type: text/html
content-length: 10147
last-modified: Wed, 15 Jul 2026 23:39:11 GMT
etag: "6a581a1f-27a3"
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff
accept-ranges: bytes


$ curl -L https://my.ndsp.app/
HTTP=200 FINAL=https://my.ndsp.app/ REDIRECTS=0

== 2) Backup and clean HTML redirect scripts ==
BACKUP: /var/www/ndsp-my/admin/index.html
NO_CHANGE: /var/www/ndsp-my/admin/index.html
BACKUP: /var/www/ndsp-my/data-infra/index.html
NO_CHANGE: /var/www/ndsp-my/data-infra/index.html
BACKUP: /var/www/ndsp-my/data/index.html
NO_CHANGE: /var/www/ndsp-my/data/index.html
BACKUP: /var/www/ndsp-my/decision-guide.html
NO_CHANGE: /var/www/ndsp-my/decision-guide.html
BACKUP: /var/www/ndsp-my/decision-room-v30-1/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v30-1/index.html
BACKUP: /var/www/ndsp-my/decision-room-v30/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v30/index.html
BACKUP: /var/www/ndsp-my/decision-room-v31/account/admin-owner.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v31/account/admin-owner.html
BACKUP: /var/www/ndsp-my/decision-room-v31/account/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v31/account/index.html
BACKUP: /var/www/ndsp-my/decision-room-v31/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v31/index.html
BACKUP: /var/www/ndsp-my/guide.html
NO_CHANGE: /var/www/ndsp-my/guide.html
BACKUP: /var/www/ndsp-my/index.html
UPDATED: /var/www/ndsp-my/index.html
BACKUP: /var/www/ndsp-my/login/index.html
NO_CHANGE: /var/www/ndsp-my/login/index.html
BACKUP: /var/www/ndsp-my/owner/index.html
NO_CHANGE: /var/www/ndsp-my/owner/index.html
BACKUP: /var/www/ndsp-my/register/index.html
NO_CHANGE: /var/www/ndsp-my/register/index.html
BACKUP: /var/www/ndsp-my/user-guide.html
NO_CHANGE: /var/www/ndsp-my/user-guide.html

== 3) Find and remove Nginx redirects to decision-support.html ==
No Nginx files contain decision-support redirects.

== 4) Nginx test and reload ==
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
OK: nginx -t passed.
OK: nginx reloaded.

== 5) Inject root anchor jump only into root index ==
BACKUP: /var/www/ndsp-my/index.html
OK: anchor jump injected into /var/www/ndsp-my/index.html
TOUCHED: /var/www/ndsp-my/index.html

== 6) After HTTP state ==
$ curl -I https://my.ndsp.app/?v=anchor-v3-20260716_014509
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:45:10 GMT
content-type: text/html
content-length: 10682
last-modified: Wed, 15 Jul 2026 23:45:10 GMT
etag: "6a581b86-29ba"
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff
accept-ranges: bytes


$ curl -L https://my.ndsp.app/?v=anchor-v3-20260716_014509
HTTP=200 FINAL=https://my.ndsp.app/?v=anchor-v3-20260716_014509 REDIRECTS=0

$ curl -L https://my.ndsp.app/decision-support.html?v=anchor-v3-20260716_014509
HTTP=200 FINAL=https://my.ndsp.app/decision-support.html?v=anchor-v3-20260716_014509 REDIRECTS=0

== 7) Browser check ==
STATUS=200
FINAL_URL=https://my.ndsp.app/#decision-support
SCROLL_Y=1057
FIRST_VISIBLE={"id":"","cls":"topbar ndsp-mobile-header-fix","text":"NDSP NDSP تبني غرفة قرار، لا شاشة مؤشرات AR | EN القائمة قناة البيانات نشطة"}
HAS_DECISION_SECTION=YES
HAS_EXECUTIVE_TEXT_IN_BODY=YES
VISUAL_OK=YES

== 8) Create rollback script ==
ROLLBACK: /tmp/ndsp_rollback_root_to_decision_anchor_v3_20260716_014509.sh

== 9) Final summary ==
Open on mobile:
- https://my.ndsp.app/?v=anchor-v3-20260716_014509

Expected:
- No certificate warning
- No too many redirects
- Page should visually jump to #decision-support
- Some 'النظرة التنفيذية' may still exist in body/menu, but it should not be the first visible section.

Rollback:
- bash /tmp/ndsp_rollback_root_to_decision_anchor_v3_20260716_014509.sh

FINAL_STATUS=OK
