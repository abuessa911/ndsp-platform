# NDSP Daily Brief Live Bind Clean
DATE=2026-07-07T10:29:50+02:00
PAGE=/var/www/ndsp-my/NDSP_Daily_Brief.html
ASSET=/var/www/ndsp-my/assets/ndsp-daily-brief-live-bind.js
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_DAILY_BRIEF_RESCUE_CLEAN_20260707_102950

== 1) Backup ==
[OK] Backup created

== 2) Verify markers ==
7:<script src="/assets/ndsp-daily-brief-live-bind.js?v=1"></script>
1:/* NDSP_DAILY_BRIEF_LIVE_BIND_V1 */
5:  if (window.NDSP_DAILY_BRIEF_LIVE_BIND_V1) return;
6:  window.NDSP_DAILY_BRIEF_LIVE_BIND_V1 = true;

== 3) HTTP checks ==
DAILY_BRIEF_HTTP=200 SIZE=2611
ASSET_JS_HTTP=200 SIZE=9632
API_HTTP=200 SIZE=7146

ROLLBACK=tar -xzf /home/nawaf511/ndsp_backups/NDSP_DAILY_BRIEF_RESCUE_CLEAN_20260707_102950/ndsp-my-before-daily-brief-clean.tar.gz -C /var/www
FINAL_STATUS=DAILY_BRIEF_CLEAN_PATCH_DONE
REPORT=docs/05-runbooks/NDSP_PATCH_DAILY_BRIEF_LIVE_BIND_V1_20260707_102950.md
