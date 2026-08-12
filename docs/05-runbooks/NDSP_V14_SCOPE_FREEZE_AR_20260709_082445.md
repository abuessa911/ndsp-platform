# NDSP V1.4 / P4 Scope Freeze — Arabic — 20260709_082445

V1.3 مغلق على D5 ولا يتم تعديله.

## داخل النطاق

1. V14-A: اكتشاف completed decisions route/source قراءة فقط.
2. V14-B: adapter قراءة فقط إذا أثبت V14-A المصدر.
3. V14-C: تحسين ربط صفحات V1.3/V1.4 في البوابة بدون script stacking.
4. V14-D: تحسين Empty/Error states.
5. V14-E: Final Audit + Release Package.

## خارج النطاق

- لا تغيير TDL/NMP/Risk/Devil/Golden logic.
- لا توصيات تداول.
- لا Buy/Sell.
- لا أوامر تنفيذ.
- لا DB schema change بدون خطة مستقلة.
- لا Nginx/API/PM2 change قبل V14-A.
