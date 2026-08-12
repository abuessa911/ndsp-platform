#!/usr/bin/env python3
import json, os, urllib.request, datetime

DATA="/var/www/ndsp-my/data"
OUT=f"{DATA}/economic-calendar.json"
DQ=f"{DATA}/data-quality.json"

def now():
    return datetime.datetime.now(datetime.timezone.utc)

def iso(dt):
    return dt.isoformat().replace("+00:00","Z")

def write(path,obj):
    tmp=path+".tmp"
    with open(tmp,"w",encoding="utf-8") as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
    os.replace(tmp,path)

def update_quality(status,note):
    try:
        q=json.load(open(DQ,encoding="utf-8"))
    except Exception:
        q={"ok":True,"source":"real_binding_status","items":[]}
    items=[i for i in q.get("items",[]) if i.get("name")!="Economic Calendar"]
    items.append({"name":"Economic Calendar","status":status,"note":note})
    q["items"]=items
    q["generated_at"]=iso(now())
    write(DQ,q)

def fetch_json(url):
    req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0",
        "Accept":"application/json,text/plain,*/*",
        "Origin":"https://www.tradingview.com",
        "Referer":"https://www.tradingview.com/economic-calendar/"
    })
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read().decode("utf-8","replace"))

def impact(v):
    s=str(v or "").lower()
    if "high" in s or s=="3": return "مرتفع"
    if "medium" in s or s=="2": return "متوسط"
    return "منخفض"

def main():
    start=now()-datetime.timedelta(hours=12)
    end=now()+datetime.timedelta(days=7)
    url="https://economic-calendar.tradingview.com/events?from=%s&to=%s" % (iso(start), iso(end))

    try:
        raw=fetch_json(url)
        events=raw.get("result") if isinstance(raw,dict) else raw
        if not isinstance(events,list):
            events=[]

        items=[]
        for e in events[:120]:
            title=e.get("title") or e.get("event") or e.get("name") or ""
            country=e.get("country") or e.get("country_code") or ""
            if not title:
                continue
            items.append({
                "title": title,
                "country": country,
                "published_at": e.get("date") or e.get("datetime") or e.get("time") or "",
                "impact": impact(e.get("importance") or e.get("impact")),
                "actual": e.get("actual"),
                "forecast": e.get("forecast"),
                "previous": e.get("previous"),
                "source": "TradingView Economic Calendar"
            })

        payload={
            "ok": bool(items),
            "source":"real_live_tradingview_calendar",
            "provider":"TradingView",
            "generated_at":iso(now()),
            "items":items,
            "note":"جلب حي حقيقي بدون بيانات وهمية"
        }
        write(OUT,payload)
        update_quality("connected" if items else "empty", f"مرتبط حي من TradingView، عدد الأحداث: {len(items)}")
        print("ITEMS=",len(items))
    except Exception as e:
        write(OUT,{
            "ok":False,
            "source":"real_live_tradingview_calendar",
            "provider":"TradingView",
            "generated_at":iso(now()),
            "items":[],
            "error":str(e),
            "note":"فشل الجلب الحي؛ لم يتم وضع بيانات وهمية"
        })
        update_quality("error","فشل الجلب الحي من TradingView")
        raise

main()
