=== NDSP SYSTEM AUDIT STARTING ===
Date: الثلاثاء  7 يوليو 2026 CEST  8:06:21
Project: /home/nawaf511/empire-core-new
Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUDIT_REPORT_20260707_080621.md

--- [1/4] Directory Integrity ---
[OK] Found: docs/00-build-catalog
[OK] Found: docs/01-build-control-pack
[OK] Found: scripts/audit
[OK] Found: scripts/backup
[OK] Found: docs/05-runbooks
[OK] Found: docs/06-decision-room-contracts

--- [2/4] Service Status ---
[OK] Nginx is running.
[ALERT] PM2 runtime not found or stopped: ndsp-core-runtime

--- [3/4] Content Safety Audit ---
[OK] No forbidden term: 'Buy Now'
[OK] No forbidden term: 'Sell Now'
[OK] No forbidden term: 'اشتر الآن'
[OK] No forbidden term: 'بيع الآن'
[OK] No forbidden term: 'بيّع'
[OK] No forbidden term: 'توصية'
[OK] No forbidden term: 'ربح مضمون'
[OK] No forbidden term: 'اربح مضمون'
[OK] No forbidden term: 'دخول الآن'
[OK] No forbidden term: 'صفقة مضمونة'

--- [4/4] Final Summary ---
Audit completed.
Report saved to: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUDIT_REPORT_20260707_080621.md

=== AUDIT COMPLETE ===
