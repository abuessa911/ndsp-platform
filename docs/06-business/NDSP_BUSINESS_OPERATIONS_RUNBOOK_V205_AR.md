# NDSP — دليل تشغيل الأعمال V205

## الروابط العامة
- البداية: https://my.ndsp.app/start/
- الاشتراكات: https://my.ndsp.app/subscribe/
- الدعم: https://my.ndsp.app/support/
- حملة الإطلاق: https://my.ndsp.app/launch/?utm_campaign=launch_v205
- لوحة العمليات: https://my.ndsp.app/ops-admin/

## سياسة الاشتراكات
- التجربة الرسمية: 16 يومًا.
- استقبال طلب الاشتراك يعمل فعليًا.
- لا يوجد تفعيل آلي بناءً على كلام المستخدم أو رقم مرجع فقط.
- تتحقق الإدارة من الدفع ثم تحدّث حالة الطلب.
- هذا الإصدار لا يعدّل جدول users ولا سجلات الدفع.

## إدارة العمليات من الطرفية
```sh
sudo ndsp-ops-admin summary
sudo ndsp-ops-admin list subscription_requests --limit 50
sudo ndsp-ops-admin list support_tickets --limit 50
sudo ndsp-ops-admin update support_tickets ID in_progress
sudo ndsp-ops-admin update support_tickets ID resolved
sudo ndsp-ops-admin update subscription_requests ID paid_verified
sudo ndsp-ops-admin export leads \"/home/nawaf511/ndsp_leads.csv\"
```

## المراقبة
- فحص كل خمس دقائق.
- تنبيه بريد محلي بعد ثلاثة إخفاقات متتالية.
- رسالة تعافٍ عند عودة الصحة.
- ملخص أعمال يومي الساعة 08:00 بتوقيت الرياض.
