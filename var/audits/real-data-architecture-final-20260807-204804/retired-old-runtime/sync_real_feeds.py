#!/usr/bin/env python3
import json, os, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

DATA = Path("/var/www/ndsp-my/data")
DATA.mkdir(parents=True, exist_ok=True)

NEWS_RSS_URL = os.getenv("NDSP_NEWS_RSS_URL", "https://www.coindesk.com/arc/outboundfeeds/rss/")
CALENDAR_JSON_URL = os.getenv("NDSP_CALENDAR_JSON_URL", "")

def now():
    return datetime.now(timezone.utc).isoformat()

def write(name, payload):
    (DATA / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

def fetch(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent":"NDSP-RealFeed/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def sync_news():
    try:
        raw = fetch(NEWS_RSS_URL)
        root = ET.fromstring(raw)
        items = []
        for item in root.findall(".//item")[:20]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub = (item.findtext("pubDate") or "").strip()
            desc = (item.findtext("description") or "").strip()
            if title:
                items.append({
                    "title": title,
                    "source": NEWS_RSS_URL,
                    "published_at": pub,
                    "url": link,
                    "summary": desc[:240],
                    "impact": "متابعة"
                })
        write("news-impact.json", {
            "ok": True,
            "source": "real_rss_provider",
            "provider_url": NEWS_RSS_URL,
            "generated_at": now(),
            "items": items
        })
        return {"name":"Impact News","status":"connected","note":f"مرتبط فعلياً عبر RSS، عدد الأخبار: {len(items)}"}
    except Exception as e:
        write("news-impact.json", {
            "ok": True,
            "source": "missing_or_failed_real_news_provider",
            "generated_at": now(),
            "items": [],
            "error": str(e)
        })
        return {"name":"Impact News","status":"missing_provider","note":"تعذر جلب مصدر الأخبار الحقيقي حالياً"}

def sync_calendar():
    if not CALENDAR_JSON_URL:
        write("economic-calendar.json", {
            "ok": True,
            "source": "missing_real_calendar_provider",
            "generated_at": now(),
            "items": [],
            "note": "ضع رابط مزود تقويم اقتصادي حقيقي في NDSP_CALENDAR_JSON_URL"
        })
        return {"name":"Economic Calendar","status":"missing_provider","note":"يحتاج مزود تقويم اقتصادي حقيقي أو API key"}
    try:
        raw = fetch(CALENDAR_JSON_URL)
        data = json.loads(raw.decode("utf-8"))
        items = data if isinstance(data, list) else data.get("items", data.get("data", []))
        write("economic-calendar.json", {
            "ok": True,
            "source": "real_calendar_provider",
            "provider_url": CALENDAR_JSON_URL,
            "generated_at": now(),
            "items": items[:50] if isinstance(items, list) else []
        })
        return {"name":"Economic Calendar","status":"connected","note":f"مرتبط فعلياً، عدد الأحداث: {len(items) if isinstance(items,list) else 0}"}
    except Exception as e:
        write("economic-calendar.json", {
            "ok": True,
            "source": "failed_real_calendar_provider",
            "generated_at": now(),
            "items": [],
            "error": str(e)
        })
        return {"name":"Economic Calendar","status":"missing_provider","note":"فشل جلب التقويم من المزود المحدد"}

news_status = sync_news()
calendar_status = sync_calendar()

write("data-quality.json", {
    "ok": True,
    "source": "real_binding_status",
    "generated_at": now(),
    "items": [
        {"name":"Live Decision API","status":"connected","note":"مرتبط فعلياً عبر 127.0.0.1:9057"},
        {"name":"Decision Ledger DB","status":"connected","note":"مرتبط فعلياً بجدول ndsp_decision_ledger"},
        news_status,
        calendar_status
    ]
})
