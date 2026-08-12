#!/usr/bin/env bash
set -Eeuo pipefail

# هذا الملف مولد تلقائيًا.
# لا تشغله كاملًا دفعة واحدة.
# راجع كل قسم وخدمة قبل التنفيذ.
#
# الخطوات الصحيحة لكل خدمة:
# 1. نسخ المصدر إلى empire-core-new.
# 2. اختبار الخدمة على منفذ بديل.
# 3. أخذ نسخة احتياطية من ملف systemd.
# 4. تعديل WorkingDirectory وExecStart.
# 5. daemon-reload.
# 6. restart.
# 7. health check.
# 8. rollback عند الفشل.

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"

# ==============================================================================
# الخدمة: binance-feed.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة binance-feed.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/binance-feed.service" #   "/etc/systemd/system/binance-feed.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "binance-feed.service"
# sudo systemctl status "binance-feed.service" --no-pager


# ==============================================================================
# الخدمة: decisionos-backend.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة decisionos-backend.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/decisionos-backend.service" #   "/etc/systemd/system/decisionos-backend.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "decisionos-backend.service"
# sudo systemctl status "decisionos-backend.service" --no-pager


# ==============================================================================
# الخدمة: empire-binance-feed.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة empire-binance-feed.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/empire-binance-feed.service" #   "/etc/systemd/system/empire-binance-feed.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "empire-binance-feed.service"
# sudo systemctl status "empire-binance-feed.service" --no-pager


# ==============================================================================
# الخدمة: empire-ndip-api.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة empire-ndip-api.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/empire-ndip-api.service" #   "/etc/systemd/system/empire-ndip-api.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "empire-ndip-api.service"
# sudo systemctl status "empire-ndip-api.service" --no-pager


# ==============================================================================
# الخدمة: empire-webhook.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة empire-webhook.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/empire-webhook.service" #   "/etc/systemd/system/empire-webhook.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "empire-webhook.service"
# sudo systemctl status "empire-webhook.service" --no-pager


# ==============================================================================
# الخدمة: fanno-comments.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة fanno-comments.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/fanno-comments.service" #   "/etc/systemd/system/fanno-comments.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "fanno-comments.service"
# sudo systemctl status "fanno-comments.service" --no-pager


# ==============================================================================
# الخدمة: ndip-autonomous-loop.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-autonomous-loop.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-autonomous-loop.service" #   "/etc/systemd/system/ndip-autonomous-loop.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-autonomous-loop.service"
# sudo systemctl status "ndip-autonomous-loop.service" --no-pager


# ==============================================================================
# الخدمة: ndip-autopilot.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-autopilot.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-autopilot.service" #   "/etc/systemd/system/ndip-autopilot.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-autopilot.service"
# sudo systemctl status "ndip-autopilot.service" --no-pager


# ==============================================================================
# الخدمة: ndip-auto-signal.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-auto-signal.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-auto-signal.service" #   "/etc/systemd/system/ndip-auto-signal.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-auto-signal.service"
# sudo systemctl status "ndip-auto-signal.service" --no-pager


# ==============================================================================
# الخدمة: ndip-auto-trade.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-auto-trade.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-auto-trade.service" #   "/etc/systemd/system/ndip-auto-trade.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-auto-trade.service"
# sudo systemctl status "ndip-auto-trade.service" --no-pager


# ==============================================================================
# الخدمة: ndip-backend.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-backend.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-backend.service" #   "/etc/systemd/system/ndip-backend.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-backend.service"
# sudo systemctl status "ndip-backend.service" --no-pager


# ==============================================================================
# الخدمة: ndip-engine.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-engine.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-engine.service" #   "/etc/systemd/system/ndip-engine.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-engine.service"
# sudo systemctl status "ndip-engine.service" --no-pager


# ==============================================================================
# الخدمة: ndip-frontend.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-frontend.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-frontend.service" #   "/etc/systemd/system/ndip-frontend.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-frontend.service"
# sudo systemctl status "ndip-frontend.service" --no-pager


# ==============================================================================
# الخدمة: ndip-run-server.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-run-server.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-run-server.service" #   "/etc/systemd/system/ndip-run-server.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-run-server.service"
# sudo systemctl status "ndip-run-server.service" --no-pager


# ==============================================================================
# الخدمة: ndip-security-cleanup.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-security-cleanup.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-security-cleanup.service" #   "/etc/systemd/system/ndip-security-cleanup.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-security-cleanup.service"
# sudo systemctl status "ndip-security-cleanup.service" --no-pager


# ==============================================================================
# الخدمة: ndip.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip.service" #   "/etc/systemd/system/ndip.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip.service"
# sudo systemctl status "ndip.service" --no-pager


# ==============================================================================
# الخدمة: ndip-signal-engine.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-signal-engine.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-signal-engine.service" #   "/etc/systemd/system/ndip-signal-engine.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-signal-engine.service"
# sudo systemctl status "ndip-signal-engine.service" --no-pager


# ==============================================================================
# الخدمة: ndip-signal.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-signal.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-signal.service" #   "/etc/systemd/system/ndip-signal.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-signal.service"
# sudo systemctl status "ndip-signal.service" --no-pager


# ==============================================================================
# الخدمة: ndip-trading-loop.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndip-trading-loop.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndip-trading-loop.service" #   "/etc/systemd/system/ndip-trading-loop.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndip-trading-loop.service"
# sudo systemctl status "ndip-trading-loop.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-16-layers.service
# الحالة: active
# التصنيف: ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
# المصدر: /opt/ndsp16-api
# الوجهة المقترحة: /home/nawaf511/empire-core-new/apps/ndsp-layers-api
# ==============================================================================

echo "مراجعة ndsp-16-layers.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-16-layers.service" #   "/etc/systemd/system/ndsp-16-layers.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/apps/ndsp-layers-api"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp16-api/" #   "/home/nawaf511/empire-core-new/apps/ndsp-layers-api/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-16-layers.service"
# sudo systemctl status "ndsp-16-layers.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-admin-user-ops.service
# الحالة: active
# التصنيف: ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
# المصدر: /opt/ndsp-admin-user-ops
# الوجهة المقترحة: /home/nawaf511/empire-core-new/backend/admin_users_official_api
# ==============================================================================

echo "مراجعة ndsp-admin-user-ops.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-admin-user-ops.service" #   "/etc/systemd/system/ndsp-admin-user-ops.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/backend/admin_users_official_api"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-admin-user-ops/" #   "/home/nawaf511/empire-core-new/backend/admin_users_official_api/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-admin-user-ops.service"
# sudo systemctl status "ndsp-admin-user-ops.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-auth-core-clean.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-auth-core-clean/current
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/current
# ==============================================================================

echo "مراجعة ndsp-auth-core-clean.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-auth-core-clean.service" #   "/etc/systemd/system/ndsp-auth-core-clean.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/current"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-auth-core-clean/current/" #   "/home/nawaf511/empire-core-new/legacy-import/current/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-auth-core-clean.service"
# sudo systemctl status "ndsp-auth-core-clean.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-change-password-gateway.service
# الحالة: active
# التصنيف: ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
# المصدر: /opt/ndsp-change-password-gateway
# الوجهة المقترحة: /home/nawaf511/empire-core-new/backend/password_reset_gateway
# ==============================================================================

echo "مراجعة ndsp-change-password-gateway.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-change-password-gateway.service" #   "/etc/systemd/system/ndsp-change-password-gateway.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/backend/password_reset_gateway"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-change-password-gateway/" #   "/home/nawaf511/empire-core-new/backend/password_reset_gateway/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-change-password-gateway.service"
# sudo systemctl status "ndsp-change-password-gateway.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-commercial-auth-payment-staging.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-commercial-auth-payment-staging
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-commercial-auth-payment-staging
# ==============================================================================

echo "مراجعة ndsp-commercial-auth-payment-staging.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-commercial-auth-payment-staging.service" #   "/etc/systemd/system/ndsp-commercial-auth-payment-staging.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-commercial-auth-payment-staging"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-commercial-auth-payment-staging/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-commercial-auth-payment-staging/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-commercial-auth-payment-staging.service"
# sudo systemctl status "ndsp-commercial-auth-payment-staging.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-current-user-display.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-current-user-display
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-current-user-display
# ==============================================================================

echo "مراجعة ndsp-current-user-display.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-current-user-display.service" #   "/etc/systemd/system/ndsp-current-user-display.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-current-user-display"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-current-user-display/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-current-user-display/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-current-user-display.service"
# sudo systemctl status "ndsp-current-user-display.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-decision-package-v1.service
# الحالة: active
# التصنيف: ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
# المصدر: /opt/ndsp-decision-package-v1
# الوجهة المقترحة: /home/nawaf511/empire-core-new/backend/services/completed_decision
# ==============================================================================

echo "مراجعة ndsp-decision-package-v1.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-decision-package-v1.service" #   "/etc/systemd/system/ndsp-decision-package-v1.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/backend/services/completed_decision"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-decision-package-v1/" #   "/home/nawaf511/empire-core-new/backend/services/completed_decision/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-decision-package-v1.service"
# sudo systemctl status "ndsp-decision-package-v1.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-enterprise-api.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة ndsp-enterprise-api.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-enterprise-api.service" #   "/etc/systemd/system/ndsp-enterprise-api.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-enterprise-api.service"
# sudo systemctl status "ndsp-enterprise-api.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-market-data-bridge-v2.service
# الحالة: active
# التصنيف: ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
# المصدر: /opt/ndsp-market-data-bridge-v2
# الوجهة المقترحة: /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway
# ==============================================================================

echo "مراجعة ndsp-market-data-bridge-v2.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-market-data-bridge-v2.service" #   "/etc/systemd/system/ndsp-market-data-bridge-v2.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-market-data-bridge-v2/" #   "/home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-market-data-bridge-v2.service"
# sudo systemctl status "ndsp-market-data-bridge-v2.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-news-ticker.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-news-ticker
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-news-ticker
# ==============================================================================

echo "مراجعة ndsp-news-ticker.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-news-ticker.service" #   "/etc/systemd/system/ndsp-news-ticker.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-news-ticker"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-news-ticker/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-news-ticker/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-news-ticker.service"
# sudo systemctl status "ndsp-news-ticker.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-platform-gateway-9002.service
# الحالة: active
# التصنيف: ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER
# المصدر: /opt/ndsp-platform-gateway-9002
# الوجهة المقترحة: /home/nawaf511/empire-core-new/backend/gateway
# ==============================================================================

echo "مراجعة ndsp-platform-gateway-9002.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-platform-gateway-9002.service" #   "/etc/systemd/system/ndsp-platform-gateway-9002.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/backend/gateway"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-platform-gateway-9002/" #   "/home/nawaf511/empire-core-new/backend/gateway/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-platform-gateway-9002.service"
# sudo systemctl status "ndsp-platform-gateway-9002.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-public-summary-v548.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-public-summary-v548
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-public-summary-v548
# ==============================================================================

echo "مراجعة ndsp-public-summary-v548.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-public-summary-v548.service" #   "/etc/systemd/system/ndsp-public-summary-v548.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-public-summary-v548"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-public-summary-v548/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-public-summary-v548/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-public-summary-v548.service"
# sudo systemctl status "ndsp-public-summary-v548.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-registration-consent-v42.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp/legal-v42/ndsp-registration-consent-gateway.cjs
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-registration-consent-gateway.cjs
# ==============================================================================

echo "مراجعة ndsp-registration-consent-v42.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-registration-consent-v42.service" #   "/etc/systemd/system/ndsp-registration-consent-v42.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-registration-consent-gateway.cjs"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp/legal-v42/ndsp-registration-consent-gateway.cjs/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-registration-consent-gateway.cjs/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-registration-consent-v42.service"
# sudo systemctl status "ndsp-registration-consent-v42.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-registration-mailer-v12-1.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt/ndsp-registration-mailer-v12-1/mailer.py
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/mailer.py
# ==============================================================================

echo "مراجعة ndsp-registration-mailer-v12-1.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-registration-mailer-v12-1.service" #   "/etc/systemd/system/ndsp-registration-mailer-v12-1.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/mailer.py"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-registration-mailer-v12-1/mailer.py/" #   "/home/nawaf511/empire-core-new/legacy-import/mailer.py/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-registration-mailer-v12-1.service"
# sudo systemctl status "ndsp-registration-mailer-v12-1.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-ui-bridge-api.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-ui-bridge-api
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-ui-bridge-api
# ==============================================================================

echo "مراجعة ndsp-ui-bridge-api.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-ui-bridge-api.service" #   "/etc/systemd/system/ndsp-ui-bridge-api.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-ui-bridge-api"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-ui-bridge-api/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-ui-bridge-api/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-ui-bridge-api.service"
# sudo systemctl status "ndsp-ui-bridge-api.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-v3-portal-gateway.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-v3-portal-gateway
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/ndsp-v3-portal-gateway
# ==============================================================================

echo "مراجعة ndsp-v3-portal-gateway.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-v3-portal-gateway.service" #   "/etc/systemd/system/ndsp-v3-portal-gateway.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/ndsp-v3-portal-gateway"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-v3-portal-gateway/" #   "/home/nawaf511/empire-core-new/legacy-import/ndsp-v3-portal-gateway/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-v3-portal-gateway.service"
# sudo systemctl status "ndsp-v3-portal-gateway.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-v52-contract.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-v52-contract/app.py
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/app.py
# ==============================================================================

echo "مراجعة ndsp-v52-contract.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-v52-contract.service" #   "/etc/systemd/system/ndsp-v52-contract.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/app.py"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-v52-contract/app.py/" #   "/home/nawaf511/empire-core-new/legacy-import/app.py/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-v52-contract.service"
# sudo systemctl status "ndsp-v52-contract.service" --no-pager


# ==============================================================================
# الخدمة: ndsp-v53-bridge.service
# الحالة: active
# التصنيف: ACTIVE_BLOCKED_MIGRATION_REQUIRED
# المصدر: /opt/ndsp-v53-bridge/app.py
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/app.py
# ==============================================================================

echo "مراجعة ndsp-v53-bridge.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/ndsp-v53-bridge.service" #   "/etc/systemd/system/ndsp-v53-bridge.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/app.py"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/ndsp-v53-bridge/app.py/" #   "/home/nawaf511/empire-core-new/legacy-import/app.py/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "ndsp-v53-bridge.service"
# sudo systemctl status "ndsp-v53-bridge.service" --no-pager


# ==============================================================================
# الخدمة: recommendation-engine.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة recommendation-engine.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/recommendation-engine.service" #   "/etc/systemd/system/recommendation-engine.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "recommendation-engine.service"
# sudo systemctl status "recommendation-engine.service" --no-pager


# ==============================================================================
# الخدمة: royal-api.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة royal-api.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/royal-api.service" #   "/etc/systemd/system/royal-api.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "royal-api.service"
# sudo systemctl status "royal-api.service" --no-pager


# ==============================================================================
# الخدمة: signal-engine.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة signal-engine.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/signal-engine.service" #   "/etc/systemd/system/signal-engine.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "signal-engine.service"
# sudo systemctl status "signal-engine.service" --no-pager


# ==============================================================================
# الخدمة: subscription-watcher.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة subscription-watcher.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/subscription-watcher.service" #   "/etc/systemd/system/subscription-watcher.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "subscription-watcher.service"
# sudo systemctl status "subscription-watcher.service" --no-pager


# ==============================================================================
# الخدمة: trade-monitor.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة trade-monitor.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/trade-monitor.service" #   "/etc/systemd/system/trade-monitor.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "trade-monitor.service"
# sudo systemctl status "trade-monitor.service" --no-pager


# ==============================================================================
# الخدمة: twelvedata-poller.service
# الحالة: inactive
inactive
# التصنيف: INACTIVE_ARCHIVE_CANDIDATE
# المصدر: /opt
# الوجهة المقترحة: /home/nawaf511/empire-core-new/legacy-import/opt
# ==============================================================================

echo "مراجعة twelvedata-poller.service"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a #   "/etc/systemd/system/twelvedata-poller.service" #   "/etc/systemd/system/twelvedata-poller.service.bak-20260806-100323"

# إنشاء الوجهة:
# mkdir -p "/home/nawaf511/empire-core-new/legacy-import/opt"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids #   "/opt/" #   "/home/nawaf511/empire-core-new/legacy-import/opt/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "twelvedata-poller.service"
# sudo systemctl status "twelvedata-poller.service" --no-pager

