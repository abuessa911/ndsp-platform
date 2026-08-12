# NDSP Patch — Menu Canonical Page Match V1
DATE=2026-07-07T09:48:21+02:00
FRONTEND=/var/www/ndsp-my
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_MENU_CANONICAL_PAGE_MATCH_V1_20260707_094821

## 1) Backup
[OK] Backup created

## 2) Create canonical page files from current live pages
[OK] NDSP_Asset_View.html <= asset-selector.html
[OK] decision-support.html <= decision-center.html
[OK] NDSP_Command_Center.html <= decision-radar.html
[OK] NDSP_Daily_Brief.html <= daily-brief.html
[OK] NDSP_Settings_Alerts.html <= settings.html

## 3) Replace global menu with canonical route map
[OK] Menu rewritten: /var/www/ndsp-my/assets/ndsp-global-menu.js

## 4) Bump menu script version in all live HTML files
[OK] version bump files:
 - NDSP_Asset_View.html
 - NDSP_Command_Center.html
 - NDSP_Daily_Brief.html
 - NDSP_Settings_Alerts.html
 - alerts-log.html
 - asset-selector.html
 - completed-decisions.html
 - daily-brief.html
 - decision-center.html
 - decision-guide.html
 - decision-modes-guide.html
 - decision-radar.html
 - decision-support.html
 - dollar-impact.html
 - dollar-news.html
 - index.html
 - my-watchlist.html
 - nmp.html
 - pro-guide.html
 - settings.html
 - support-center.html
 - usd-pulse.html
 - user-guide.html

## 5) Verification — canonical files
--- /var/www/ndsp-my/decision-support.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 2.5K يوليو   7 09:48 /var/www/ndsp-my/decision-support.html
<title>NDSP — دعم القرار
<h1>دعم القرار

--- /var/www/ndsp-my/NDSP_Asset_View.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 2.8K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Asset_View.html
<title>NDSP — الأسواق والأصول
<h1 data-i18n="title">الأسواق والأصول

--- /var/www/ndsp-my/NDSP_Command_Center.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 3.3K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Command_Center.html
<title>NDSP — مركز القيادة
<h1>مركز القيادة

--- /var/www/ndsp-my/NDSP_Daily_Brief.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 2.5K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Daily_Brief.html
<title>NDSP — الموجز اليومي
<h1>الموجز اليومي

--- /var/www/ndsp-my/NDSP_Settings_Alerts.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 2.5K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Settings_Alerts.html
<title>NDSP — الإعدادات والتنبيهات
<h1>الإعدادات والتنبيهات

## 6) HTTP size checks
[200] size=884 https://my.ndsp.app/
[200] size=884 https://my.ndsp.app/index.html
[200] size=2544 https://my.ndsp.app/decision-support.html
[200] size=2789 https://my.ndsp.app/NDSP_Asset_View.html
[200] size=3297 https://my.ndsp.app/NDSP_Command_Center.html
[200] size=2545 https://my.ndsp.app/NDSP_Daily_Brief.html
[200] size=2514 https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] size=4677 https://my.ndsp.app/disclaimer.html

## 7) Rollback
cd /home/nawaf511/empire-core-new
sudo tar -xzf "/home/nawaf511/ndsp_backups/NDSP_MENU_CANONICAL_PAGE_MATCH_V1_20260707_094821/ndsp-my-before-menu-canonical-match.tar.gz" -C /var/www

FINAL_STATUS=MENU_CANONICAL_PAGE_MATCH_PATCH_DONE
REPORT=docs/05-runbooks/NDSP_PATCH_MENU_CANONICAL_PAGE_MATCH_V1_20260707_094821.md
