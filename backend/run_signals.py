import time
import json
from datetime import datetime, timezone

from app.core.governed_pipeline import run_governed
from app.pg_db import execute

# الرموز اللي تبي تتداولها
symbols = ["XAUUSD"]

while True:
    for symbol in symbols:
        try:
            # تشغيل الاستراتيجية
            r = run_governed(symbol)

            decision = r.get("decision") or {}
            direction = decision.get("direction")
            confidence = decision.get("confidence", 50)

            # حماية من الأخطاء
            meta = r.get("meta") or {}
            entry = meta.get("entry") or {}

            # فقط إذا فيه دخول فعلي
            if not entry.get("is_trade_entry", False):
                print(f"[-] skipped (no entry): {symbol}")
                continue

            # SQL insert
            query = """
            INSERT INTO signals (
                symbol,
                direction,
                confidence,
                status,
                created_at,
                raw_result
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            execute(
                query,
                (
                    symbol,
                    direction,
                    confidence,
                    "pending",
                    datetime.now(timezone.utc),
                    json.dumps(r),
                ),
            )

            print(f"[+] signal added: {symbol} {direction} ({confidence})")

        except Exception as e:
            print("[ERROR]", symbol, "→", e)

    print("=== cycle done ===\n")

    # كل دقيقة
    time.sleep(60)
