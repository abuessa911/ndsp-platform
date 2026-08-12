# NDSP Emergency Recover Root History Rewrite V2

- Date: 2026-07-16T01:39:09+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Target route: /decision-support.html
- Mode: NO_REDIRECT_HISTORY_REWRITE_BEFORE_REACT
- Backup: /home/nawaf511/ndsp_launch_backups/emergency_recover_root_history_rewrite_v2_20260716_013909
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_EMERGENCY_RECOVER_ROOT_HISTORY_REWRITE_V2_20260716_013909.md

== 1) Current HTTP state before recovery ==
$ curl -I https://my.ndsp.app/
HTTP/2 302 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:39:09 GMT
content-type: text/html
content-length: 154
location: https://my.ndsp.app/decision-support.html
cache-control: no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0
pragma: no-cache
expires: 0


$ curl -L https://my.ndsp.app/
HTTP=302 FINAL=https://my.ndsp.app/decision-support.html

== 2) Backup affected live HTML files ==
BACKUP: /var/www/ndsp-my/admin/index.html
BACKUP: /var/www/ndsp-my/data-infra/index.html
BACKUP: /var/www/ndsp-my/data/index.html
BACKUP: /var/www/ndsp-my/decision-guide.html
BACKUP: /var/www/ndsp-my/decision-room-v30-1/index.html
BACKUP: /var/www/ndsp-my/decision-room-v30/index.html
BACKUP: /var/www/ndsp-my/decision-room-v31/account/admin-owner.html
BACKUP: /var/www/ndsp-my/decision-room-v31/account/index.html
BACKUP: /var/www/ndsp-my/decision-room-v31/index.html
BACKUP: /var/www/ndsp-my/guide.html
BACKUP: /var/www/ndsp-my/index.html
BACKUP: /var/www/ndsp-my/login/index.html
BACKUP: /var/www/ndsp-my/owner/index.html
BACKUP: /var/www/ndsp-my/register/index.html
BACKUP: /var/www/ndsp-my/user-guide.html

== 3) Remove old/broken HTML redirect scripts ==
NO_CHANGE: /var/www/ndsp-my/admin/index.html
NO_CHANGE: /var/www/ndsp-my/data-infra/index.html
NO_CHANGE: /var/www/ndsp-my/data/index.html
NO_CHANGE: /var/www/ndsp-my/decision-guide.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v30-1/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v30/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v31/account/admin-owner.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v31/account/index.html
NO_CHANGE: /var/www/ndsp-my/decision-room-v31/index.html
NO_CHANGE: /var/www/ndsp-my/guide.html
NO_CHANGE: /var/www/ndsp-my/index.html
NO_CHANGE: /var/www/ndsp-my/login/index.html
NO_CHANGE: /var/www/ndsp-my/owner/index.html
NO_CHANGE: /var/www/ndsp-my/register/index.html
NO_CHANGE: /var/www/ndsp-my/user-guide.html

== 4) Remove old/broken Nginx root redirects ==
No Nginx redirect candidates found.

== 5) Test and reload Nginx ==
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
OK: nginx config test passed.
OK: nginx reloaded.

== 6) Inject root history rewrite into root index only ==
BACKUP: /var/www/ndsp-my/index.html
OK: History rewrite injected into /var/www/ndsp-my/index.html

== 7) Touch root index to break stale cache ==
TOUCHED: /var/www/ndsp-my/index.html

== 8) HTTP state after recovery ==
$ curl -I https://my.ndsp.app/?v=recover-v2-20260716_013909
HTTP/2 302 
server: nginx/1.24.0 (Ubuntu)
date: Wed, 15 Jul 2026 23:39:11 GMT
content-type: text/html
content-length: 154
location: https://my.ndsp.app/decision-support.html?v=recover-v2-20260716_013909
cache-control: no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0
pragma: no-cache
expires: 0


$ curl -L https://my.ndsp.app/?v=recover-v2-20260716_013909
HTTP=200 FINAL=https://my.ndsp.app/?v=recover-v2-20260716_013909

$ curl -L https://my.ndsp.app/decision-support.html?v=recover-v2-20260716_013909
HTTP=200 FINAL=https://my.ndsp.app/decision-support.html?v=recover-v2-20260716_013909

== 9) Certificate summary ==
subject=CN = my.ndsp.app
issuer=C = US, O = Let's Encrypt, CN = YE2
notBefore=Jun 21 19:03:09 2026 GMT
notAfter=Sep 19 19:03:08 2026 GMT
X509v3 Subject Alternative Name: 
    DNS:my.ndsp.app

== 10) Browser check ==
STATUS=200
FINAL_URL=https://my.ndsp.app/decision-support.html?v=history-v2-browser-1784158753209
HAS_CORRECT_DECISION_PAGE=YES
HAS_OLD_EXECUTIVE_PAGE=YES
TEXT_PREVIEW=NDSP NDSP تبني غرفة قرار، لا شاشة مؤشرات AR | EN القائمة قناة البيانات نشطة روابط الصفحات الرسمية القائمة للجوال فقط ولا تغيّر قائمة سطح المكتب. إغلاق النظرة التنفيذية اختيار الأصول رادار القرار محرك القرار المستويات المرجعية و NMP السيناريوهات البديلة القرارات المكتملة غرفة القرار النظرة التنفيذية قراءة مؤسسية متعددة الطبقات تعرض التفسير والتحقق والاعتراض والجاهزية والمتابعة بدون أي أوامر تنفيذ. الوضع الافتراضي قراءة استثمارية قراءة مضاربية الأصل النشط الرمز الذهب - XAUUSD بيتكوين - BTCUSDT إيثريوم - ETHUSDT اليورو دولار - EURUSD النفط الأمريكي - USOIL إس آند بي 500 - SPX ٤٬٠٦٣٫٢ الذهب · 

== 11) Create rollback script ==
ROLLBACK: /tmp/ndsp_rollback_emergency_recover_root_history_rewrite_v2_20260716_013909.sh

== 12) Final summary ==
Open on mobile with a fresh query:
- https://my.ndsp.app/?v=history-v2-20260716_013909

Expected:
- No certificate warning
- No too many redirects
- Address may become /decision-support.html because of history.replaceState
- Content should be the correct decision page

Rollback:
- bash /tmp/ndsp_rollback_emergency_recover_root_history_rewrite_v2_20260716_013909.sh

FINAL_STATUS=OK
