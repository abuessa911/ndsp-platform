#!/usr/bin/env python3
import json, urllib.request, urllib.parse, datetime, os, sys

DATA_DIR="/var/www/ndsp-my/data"
OUT=f"{DATA_DIR}/economic-calendar.json"
DQ=f"{DATA_DIR}/data-quality.json"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write_json(path, payload):
    tmp=path+".tmp"
    with open(tmp,"w",encoding="utf-8") as f:
        json.dump(payload,f,ensure_ascii=False,indent=2)
    os.replace(tmp,path)

def http_json(url, timeout=20):
    req=urllib.request.Request(url, headers={
        "User-Agent":"Mozilla/5.0 NDSP-LiveCalendar/1.0",
        "Accept":"application/json,text/plain,*/*"
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw=r.read().decode("utf-8","replace")
    return json.loads(raw)

def normalize_te(items):
    out=[]
    for x in items[:80]:
        title=x.get("Event") or x.get("event") or x.get("Category") or "Economic event"
        country=x.get("Country") or x.get("country") or ""
        dt=x.get("Date") or x.get("date") or x.get("LastUpdate") or ""
        importance=x.get("Importance") or x.get("importance") or x.get("Impact") or ""
        actual=x.get("Actual") or x.get("actual") or ""
        forecast=x.get("Forecast") or x.get("forecast") or ""
        previous=x.get("Previous") or x.get("previous") or ""
        out.append({
            "title": str(title),
            "country": str(country),
            "published_at": str(dt),
            "impact": str(importance) if importance else "متابعة",
            "actual": str(actual),
            "forecast": str(forecast),
            "previous": str(previous),
            "source": "TradingEconomics live calendar"
        })
    return out

def update_quality(status, note):
    base={"ok":True,"source":"real_binding_status","generated_at":now(),"items":[]}
    try:
        with open(DQ,"r",encoding="utf-8") as f:
            base=json.load(f)
    except Exception:
        pass
    items=base.get("items") or []
    items=[i for i in items if i.get("name")!="Economic Calendar"]
    items.append({"name":"Economic Calendar","status":status,"note":note})
    base["items"]=items
    base["generated_at"]=now()
    write_json(DQ,base)

def main():
    errors=[]

    urls=[
        "https://api.tradingeconomics.com/calendar?c=guest:guest",
        "https://api.tradingeconomics.com/calendar/country/all?c=guest:guest"
    ]

    for url in urls:
        try:
            data=http_json(url)
            if isinstance(data,dict) and "calendar" in data:
                data=data["calendar"]
            if not isinstance(data,list):
                errors.append(f"bad_shape:{url}")
                continue

            items=normalize_te(data)
            if items:
                payload={
                    "ok":True,
                    "source":"real_live_economic_calendar",
                    "provider":"TradingEconomics",
                    "provider_url":url,
                    "generated_at":now(),
                    "refresh_mode":"systemd_timer_live",
                    "items":items
                }
                write_json(OUT,payload)
                update_quality("connected",f"مرتبط حقيقي وحي، عدد الأحداث: {len(items)}")
                print(f"OK items={len(items)} provider=TradingEconomics")
                return 0
            errors.append(f"empty:{url}")
        except Exception as e:
            errors.append(f"{url} => {e}")

    payload={
        "ok":False,
        "source":"real_live_economic_calendar",
        "generated_at":now(),
        "items":[],
        "error":"LIVE_PROVIDER_FETCH_FAILED",
        "details":errors,
        "note":"لا توجد بيانات وهمية. فشل الجلب الحي من المزود."
    }
    write_json(OUT,payload)
    update_quality("error","فشل الجلب الحي من مزود التقويم؛ لا توجد بيانات وهمية")
    print("FAILED", errors)
    return 2

if __name__=="__main__":
    sys.exit(main())
