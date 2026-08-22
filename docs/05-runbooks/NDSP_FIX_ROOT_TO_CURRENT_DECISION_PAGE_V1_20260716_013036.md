# NDSP Fix Root To Current Decision Page V1

- Date: 2026-07-16T01:30:36+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Root index: /var/www/ndsp-my/index.html
- Target route: /decision-support.html
- Mode: ROOT_BROWSER_REDIRECT_NO_BUNDLE_EDIT_NO_REBUILD_NO_RESTART
- Backup: /home/nawaf511/ndsp_launch_backups/root_to_current_decision_page_v1_20260716_013036
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_ROOT_TO_CURRENT_DECISION_PAGE_V1_20260716_013036.md

== 1) Before HTTP checks ==
https://my.ndsp.app/ => HTTP 200
https://my.ndsp.app/decision-support.html => HTTP 200

== 2) Backup root index ==
BACKUP: /var/www/ndsp-my/index.html

== 3) Inject root canonical redirect ==
INJECTED: root redirect block into /var/www/ndsp-my/index.html

== 4) Verify injection ==
OK: Root redirect block exists.

== 5) Create rollback script ==
ROLLBACK: /tmp/ndsp_rollback_root_canonical_redirect_v1_20260716_013036.sh

== 6) After HTTP checks ==
https://my.ndsp.app/ => HTTP 200
https://my.ndsp.app/decision-support.html => HTTP 200
https://my.ndsp.app/?v=root-fix => HTTP 200
https://my.ndsp.app/decision-support.html?v=root-fix => HTTP 200

== 7) Browser redirect check if Playwright exists ==
FINAL_URL=https://my.ndsp.app/decision-support.html?v=root-fix-browser
HAS_DECISION_TEXT=YES
HAS_OLD_EXECUTIVE_TEXT=YES

== 8) Final summary ==
Root now redirects in browser from:
- https://my.ndsp.app/
to:
- https://my.ndsp.app/decision-support.html

To bypass redirect for debugging:
- https://my.ndsp.app/?noRootRedirect=1

Rollback:
- bash /tmp/ndsp_rollback_root_canonical_redirect_v1_20260716_013036.sh

FINAL_STATUS=OK
