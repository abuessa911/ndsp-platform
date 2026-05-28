# تعليمات تكوين Enhanced Tracking Protection Bypass

## الخطوات:

### إذا كنت تستخدم Node.js/Express:
```javascript
const express = require('express');
const securityHeaders = require('./security-headers');

const app = express();
app.use(securityHeaders);

app.listen(3000);
```

### إذا كنت تستخدم Nginx:
أضف المحتوى من `nginx-security-headers.conf` في server block:
```nginx
server {
    listen 80;
    server_name ndsp.app;
    
    include nginx-security-headers.conf;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### إذا كنت تستخدم Apache:
انسخ `.htaccess` إلى جذر الموقع

### في HTML:
أضف المحتوى من `head-tags.html` في `<head>`

### إذا كنت تستخدم Flask:
```python
from flask import Flask
from flask_security_headers import setup_security_headers

app = Flask(__name__)
setup_security_headers(app)
```

## النتيجة:
✅ الموقع سيفتح بدون تحذيرات
✅ Enhanced Tracking Protection لن يعيق المحتوى
✅ Third-party cookies ستعمل بشكل طبيعي

## اختبر الموقع:
افتح Firefox → ndsp.app → يجب أن يفتح بدون مشاكل
