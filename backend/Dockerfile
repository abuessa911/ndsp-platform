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
EXPOSE 8001

# الأمر الافتراضي
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
