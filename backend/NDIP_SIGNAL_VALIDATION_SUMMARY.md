# NDSP SaaS — Signal Validation System Summary

## الوضع قبل بداية الشغل

كان نظام NDSP SaaS مكتمل end-to-end من ناحية:

- Admin UI + Branding
- Telegram integration
- Leads + Subscriptions
- NOWPayments USDT TRC20
- إنشاء الدفع من الأدمن
- إرسال بيانات الدفع للعميل Telegram
- Webhook confirmation
- تفعيل الاشتراك تلقائيًا
- إرسال invite تلقائي
- Idempotency

لكن المشكلة الأساسية كانت أن الإشارات موجودة، لكن لا نعرف دقتها Accuracy.

الهدف كان بناء Signal Validation System لمعرفة:
- كم نسبة نجاح الإشارات
- هل النظام يستحق البيع أو لا

## PostgreSQL

تم تشغيل PostgreSQL عبر Docker باسم:

ndsp_postgres

على البورت:

5433 خارج الحاوية إلى 5432 داخل الحاوية

لأن البورت 5432 كان مستخدمًا مسبقًا من PostgreSQL موجود على السيرفر.

## الجداول

تم إنشاء الجداول:

- leads
- subscriptions
- payments
- webhook_events
- signals
- signal_decisions

جدول signals مخصص للإشارات الفعلية LONG / SHORT.

جدول signal_decisions مخصص لتسجيل كل قرارات المحرك، بما فيها neutral و skipped.

## ربط Python مع PostgreSQL

تم إنشاء:

app/pg_db.py

ويوفر:

- fetch_one
- fetch_all
- execute

ويعتمد على:

DATABASE_URL=postgresql://ndsp_user:PASSWORD@localhost:5433/ndsp

## Worker

تم تعديل:

app/worker_alerts_v6.py

ليعمل بالتدفق الصحيح:

Decision → DB Logging → Telegram

وليس:

Decision → Telegram → DB Logging

السبب أن Telegram قد يفشل أو يدخل cooldown، ولا يجب أن تضيع الإشارة.

## governed_pipeline.py

تم تعديل:

app/core/governed_pipeline.py

وإضافة fallback validation layer يعتمد على حركة السعر:

- ارتفاع السعر فوق threshold ينتج bullish
- انخفاض السعر تحت threshold ينتج bearish
- غير ذلك neutral

المتغير:

NDSP_VALIDATION_PRICE_THRESHOLD_PCT

## Evaluation Engine

تم إنشاء:

app/evaluate_signals.py

وظيفته:

- قراءة signals بحالة pending
- انتظار مدة NDSP_SIGNAL_EVAL_MINUTES
- جلب السعر الحالي
- مقارنة السعر الحالي مع entry_price
- تحويل الحالة إلى evaluated
- كتابة result = win أو loss

المتغيرات:

NDSP_SIGNAL_EVAL_MINUTES=15
NDSP_SIGNAL_MIN_MOVE_PCT=0.03

## Cron

تم تشغيل evaluator كل 5 دقائق عبر crontab:

*/5 * * * * cd /home/nawaf511/ndsp-backend && /home/nawaf511/ndsp-backend/venv/bin/python -m app.evaluate_signals >> /home/nawaf511/ndsp-backend/logs/evaluator.log 2>&1

## Worker Background

تم تشغيل worker بالخلفية عبر:

nohup /home/nawaf511/ndsp-backend/venv/bin/python -u -m app.worker_alerts_v6 >> /home/nawaf511/ndsp-backend/logs/worker_alerts_v6.log 2>&1 &

ويجب التأكد دائمًا من وجود worker واحد فقط عبر:

ps aux | grep -E "worker_alerts_v6|evaluate_signals" | grep -v grep

لو ظهر أكثر من worker:

pkill -f "app.worker_alerts_v6" || true

ثم تشغيل واحد فقط.

## النتائج الحالية

آخر نتيجة معروفة:

total evaluated = 23
wins = 9
losses = 14
accuracy = 39.13%

الاستنتاج:

- النظام التقني يعمل
- الاستراتيجية الحالية لا تصلح للبيع الآن
- يجب جمع عينة أكبر وتحسين الفلاتر

## الإعدادات المقترحة للتجربة الجادة

NDSP_ALERT_MIN_CONFIDENCE=70
NDSP_ALERT_SEND_NEUTRAL=false
NDSP_ALERT_COOLDOWN_SECONDS=900
NDSP_ALERT_SYMBOLS=BTCUSDT,ETHUSDT,SOLUSDT
NDSP_ALERT_INTERVAL_SECONDS=300
NDSP_ALERT_PLAN=pro

NDSP_VALIDATION_PRICE_THRESHOLD_PCT=0.03
NDSP_SIGNAL_EVAL_MINUTES=15
NDSP_SIGNAL_MIN_MOVE_PCT=0.05

## أوامر المتابعة

حالة worker:

ps aux | grep -E "worker_alerts_v6|evaluate_signals" | grep -v grep

مراقبة worker:

tail -f /home/nawaf511/ndsp-backend/logs/worker_alerts_v6.log

مراقبة evaluator:

tail -f /home/nawaf511/ndsp-backend/logs/evaluator.log

إجمالي الأداء:

docker exec -it ndsp_postgres psql -U ndsp_user -d ndsp -c "
SELECT
  COUNT(*) FILTER (WHERE status = 'pending') AS pending,
  COUNT(*) FILTER (WHERE status = 'evaluated') AS evaluated,
  COUNT(*) FILTER (WHERE result = 'win') AS wins,
  COUNT(*) FILTER (WHERE result = 'loss') AS losses,
  ROUND(
    COUNT(*) FILTER (WHERE result = 'win')::numeric
    / NULLIF(COUNT(*) FILTER (WHERE status = 'evaluated'), 0) * 100,
    2
  ) AS accuracy
FROM signals;
"

## الحكم النهائي

NDSP الآن صار يملك Signal Validation System فعلي.

لكن NDSP لم يصبح Decision Engine قابل للبيع بعد.

البيع يبدأ فقط بعد إثبات accuracy مقبولة على عينة كافية، ويفضل:

- 100 evaluated signals كحد أدنى
- 300 evaluated signals أفضل

الخطوة القادمة:

Strategy Filtering Layer

الأولويات:

1. منع الإشارات المتعاكسة لنفس الرمز خلال مدة قصيرة
2. رفع threshold
3. رفع min confidence
4. تحليل ETHUSDT منفصلًا
5. إيقاف الأزواج الضعيفة مؤقتًا
6. إعادة حساب confidence بناءً على النتائج الفعلية
