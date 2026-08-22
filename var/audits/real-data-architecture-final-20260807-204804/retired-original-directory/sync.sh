#!/usr/bin/env bash
set -euo pipefail

LIVE="/var/www/ndsp-my"
DATA="$LIVE/data"
mkdir -p "$DATA"

LIVE_SAMPLE="$(curl -sS 'http://127.0.0.1:9057/api/decision/quality-live?symbol=ETHUSDT' || true)"

if echo "$LIVE_SAMPLE" | grep -q '"ok":true'; then
  LIVE_STATUS="connected"
else
  LIVE_STATUS="error"
fi

sudo tee "$DATA/completed-decisions.json" >/dev/null <<EOF
{
  "ok": true,
  "source": "real_binding_checked_no_completed_decisions_table_found",
  "items": []
}
EOF

sudo tee "$DATA/news-impact.json" >/dev/null <<EOF
{
  "ok": true,
  "source": "missing_real_news_provider",
  "items": []
}
EOF

sudo tee "$DATA/economic-calendar.json" >/dev/null <<EOF
{
  "ok": true,
  "source": "missing_real_calendar_provider",
  "items": []
}
EOF

sudo tee "$DATA/data-quality.json" >/dev/null <<EOF
{
  "ok": true,
  "source": "real_binding_status",
  "items": [
    {
      "name": "Live Decision API",
      "status": "$LIVE_STATUS",
      "note": "مرتبط فعلياً عبر 127.0.0.1:9057"
    },
    {
      "name": "Completed Decisions",
      "status": "missing_table",
      "note": "لا يوجد جدول قرارات مكتملة في PostgreSQL حالياً"
    },
    {
      "name": "Impact News",
      "status": "missing_provider",
      "note": "لا يوجد مزود أخبار حقيقي مربوط حالياً"
    },
    {
      "name": "Economic Calendar",
      "status": "missing_provider",
      "note": "لا يوجد مزود تقويم اقتصادي حقيقي مربوط حالياً"
    }
  ]
}
EOF
