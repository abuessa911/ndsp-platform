# NDSP /opt Migration Report

Generated: 2026-08-06T10:03:37+02:00

Project root:

```text
/home/nawaf511/empire-core-new
```

## Executive Summary

| Metric | Count |
|---|---:|
| Services referencing /opt | 95 |
| Active services | 15 |
| Active services blocked on migration | 10 |
| Services with candidate path in empire-core-new | 6 |
| Potential archive/delete candidates | 11 |

## Decision

لا يجوز حذف `/opt` كاملًا.

الأسباب:

1. توجد خدمات systemd نشطة تعتمد على مسارات داخله.
2. توجد مكونات نظامية مثل containerd وبرامج مثبتة مثل Brave وMetasploit.
3. بعض الخدمات لا يوجد لها بديل مؤكد داخل empire-core-new حتى الآن.
4. يجب نقل كل خدمة واختبارها منفردة قبل إزالة المصدر القديم.

## Active Blocked Paths

```text
ndsp-16-layers.service | /opt/ndsp16-api | ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
ndsp-admin-user-ops.service | /opt/ndsp-admin-user-ops | ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
ndsp-auth-core-clean.service | /opt/ndsp-auth-core-clean/current | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-change-password-gateway.service | /opt/ndsp-change-password-gateway | ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
ndsp-commercial-auth-payment-staging.service | /opt/ndsp-commercial-auth-payment-staging | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-current-user-display.service | /opt/ndsp-current-user-display | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-decision-package-v1.service | /opt/ndsp-decision-package-v1 | ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
ndsp-market-data-bridge-v2.service | /opt/ndsp-market-data-bridge-v2 | ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
ndsp-news-ticker.service | /opt/ndsp-news-ticker | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-platform-gateway-9002.service | /opt/ndsp-platform-gateway-9002 | ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
ndsp-public-summary-v548.service | /opt/ndsp-public-summary-v548 | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-registration-consent-v42.service | /opt/ndsp/legal-v42/ndsp-registration-consent-gateway.cjs | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-ui-bridge-api.service | /opt/ndsp-ui-bridge-api | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-v3-portal-gateway.service | /opt/ndsp-v3-portal-gateway | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-v52-contract.service | /opt/ndsp-v52-contract/app.py | ACTIVE_BLOCKED_MIGRATION_REQUIRED
ndsp-v53-bridge.service | /opt/ndsp-v53-bridge/app.py | ACTIVE_BLOCKED_MIGRATION_REQUIRED
```

## Potential Archive Candidates

هذه القائمة لا تعني أن الحذف آمن تلقائيًا. هي قائمة أولية لمجلدات لا يظهر أنها مستخدمة مباشرة من systemd أو العمليات أو cron.

```text
/opt/backups
/opt/empire-backups
/opt/empire.bak
/opt/empire-core-backup
/opt/empire-core.broken.1776325777
/opt/execution-engine
/opt/ndip-backups
/opt/ndsp-archive
/opt/ndsp-archive-app
/opt/ndsp-v471-react-gold-portal_20260701_173443
/opt/recovery
```

## Generated Files

- Services CSV: `/home/nawaf511/empire-core-new/var/audits/opt-migration-20260806-100323/OPT_SERVICES.csv`
- Services JSON: `/home/nawaf511/empire-core-new/var/audits/opt-migration-20260806-100323/OPT_SERVICES.json`
- Proposed commands: `/home/nawaf511/empire-core-new/var/audits/opt-migration-20260806-100323/PROPOSED_MIGRATION_COMMANDS.sh`
- Active blocked paths: `/home/nawaf511/empire-core-new/var/audits/opt-migration-20260806-100323/BLOCKED_ACTIVE_PATHS.txt`
- Delete candidates: `/home/nawaf511/empire-core-new/var/audits/opt-migration-20260806-100323/DELETE_CANDIDATES.txt`
- Errors: `/home/nawaf511/empire-core-new/var/audits/opt-migration-20260806-100323/ERRORS.log`

## Recommended Execution Order

1. ابدأ بالخدمات غير النشطة.
2. بعد ذلك الخدمات التي يوجد لها مسار مقابل داخل empire-core-new.
3. اختبر كل خدمة على منفذ بديل.
4. انقل ملف systemd بعد نجاح الاختبار.
5. راقب السجلات والمنافذ.
6. اترك المصدر القديم مدة استقرار.
7. انقل المصدر القديم إلى أرشيف بدل حذفه مباشرة.
8. لا تحذف أي مجلد نظامي تحت /opt.

