# NDSP Approved Pages After Cleanup Final

Generated: 2026-05-26T23:11:45+02:00

## Approved Live Pages

| # | Page | URL | Server Path |
|---:|---|---|---|
| 1 | الموقع الرئيسي | https://ndsp.app/ | /var/www/ndsp/index.html |
| 2 | بوابة المستخدم | https://my.ndsp.app/ | /var/www/ndsp-my/index.html |
| 3 | داشبورد المستخدم | https://my.ndsp.app/pages/dashboard.html | /var/www/ndsp-my/pages/dashboard.html |
| 4 | صفحة الأدمن داخل بوابة المستخدم | https://my.ndsp.app/pages/admin.html | /var/www/ndsp-my/pages/admin.html |
| 5 | لوحة الأدمن الرسمية | https://admin.ndsp.app/ | /var/www/ndsp-admin/index.html |
| 6 | صفحة التسجيل | https://my.ndsp.app/pages/register.html | /var/www/ndsp-my/pages/register.html |
| 7 | صفحة الدخول | https://my.ndsp.app/pages/login.html | /var/www/ndsp-my/pages/login.html |

## Approved Files Remaining Under /var/www/ndsp-my/pages

```text
admin.html
dashboard.html
login.html
register.html
```

## Rules

- Official API base is /api only.
- Retired API base /api/v7 must return 404.
- Public frontend must not expose secrets.
- Public frontend must not show /api/v7.
