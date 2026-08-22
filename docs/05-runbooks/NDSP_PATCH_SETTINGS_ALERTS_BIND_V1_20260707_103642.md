# NDSP Settings Alerts Bind V1
DATE=2026-07-07T10:36:42+02:00
PAGE=/var/www/ndsp-my/NDSP_Settings_Alerts.html
ASSET=/var/www/ndsp-my/assets/ndsp-settings-alerts-bind.js
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_SETTINGS_ALERTS_BIND_V1_20260707_103642

== 1) Backup ==
[OK] Backup created

== 2) Verify markers ==
7:<script src="/assets/ndsp-settings-alerts-bind.js?v=1"></script>
1:/* NDSP_SETTINGS_ALERTS_BIND_V1 */
5:  if (window.NDSP_SETTINGS_ALERTS_BIND_V1) return;
6:  window.NDSP_SETTINGS_ALERTS_BIND_V1 = true;

== 3) HTTP checks ==
SETTINGS_ALERTS_HTTP=200 SIZE=2579
ASSET_JS_HTTP=200 SIZE=11545
API_HTTP=200 SIZE=7146

ROLLBACK=tar -xzf /home/nawaf511/ndsp_backups/NDSP_SETTINGS_ALERTS_BIND_V1_20260707_103642/ndsp-my-before-settings-alerts-bind-v1.tar.gz -C /var/www
FINAL_STATUS=SETTINGS_ALERTS_BIND_PATCH_DONE
REPORT=docs/05-runbooks/NDSP_PATCH_SETTINGS_ALERTS_BIND_V1_20260707_103642.md
