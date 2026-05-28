# استخدم صورة Python رسمية
FROM python:3.12-slim

# حدّد مجلد العمل
WORKDIR /app

# ثبّت المكتبات الأساسية
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# انسخ متطلبات المشروع
COPY requirements.txt .

# ثبّت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# انسخ كل الملفات
COPY . .

# افتح البورت
EXPOSE 8000

# الأمر الافتراضي
CMD ["python", "main.py"]
