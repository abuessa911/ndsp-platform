#!/usr/bin/env python3
import json, os, re, urllib.request, urllib.parse, datetime
from html import unescape

DATA="/var/www/ndsp-my/data"
OUT=f"{DATA}/economic-calendar.json"
DQ=f"{DATA}/data-quality.json"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write(path,obj):
    tmp=path+".tmp"
    with open(tmp,"w",encoding="utf-8") as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
    os.replace(tmp,path)

def req(url, data=None, headers=None):
    h={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome Safari",
        "Accept":"text/html,application/json,*/*",
        "Accept-Language":"en-US,en;q=0.9",
        "Referer":"https://www.investing.com/economic-calendar/",
        "Origin":"https://www.investing.com",
        "X-Requested-With":"XMLHttpRequest",
    }
    if headers: h.update(headers)
    body=None
    if data is not None:
        body=urllib.parse.urlencode(data, doseq=True).encode()
        h["Content-Type"]="application/x-www-form-urlencoded"
    r=urllib.request.Request(url, data=body, headers=h)
    with urllib.request.urlopen(r, timeout=25) as x:
        return x.read().decode("utf-8","replace")

def clean(s):
    s=re.sub(r"<[^>]+>"," ",s or "")
    s=unescape(s)
    return re.sub(r"\s+"," ",s).strip()

def update_quality(status,note):
    try:
        q=json.load(open(DQ,encoding="utf-8"))
    except Exception:
        q={"ok":True,"source":"real_binding_status","items":[]}
    items=[i for i in q.get("items",[]) if i.get("name")!="Economic Calendar"]
    items.append({"name":"Economic Calendar","status":status,"note":note})
    q["items"]=items
    q["generated_at"]=now()
    write(DQ,q)

def main():
    url="https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"
    post={
        "country[]":["5","4","17","72","26","10","6","37","25","35","43","56"],
        "importance[]":["1","2","3"],
        "timeZone":"8",
        "timeFilter":"timeRemain",
        "currentTab":"today",
        "submitFilters":"1",
        "limit_from":"0"
    }

    try:
        raw=req(url, post)
        obj=json.loads(raw)
        html=obj.get("data","") if isinstance(obj,dict) else raw
        rows=re.findall(r"<tr[^>]*js-event-item[^>]*>(.*?)</tr>", html, re.S|re.I)
        items=[]
        for row in rows[:80]:
            tds=re.findall(r"<td[^>]*>(.*?)</td>", row, re.S|re.I)
            title=clean(re.search(r'event-title[^>]*>(.*?)</', row, re.S|re.I).group(1)) if re.search(r'event-title[^>]*>(.*?)</', row, re.S|re.I) else ""
            time=clean(tds[0]) if len(tds)>0 else ""
            country=clean(tds[1]) if len(tds)>1 else ""
            actual=clean(tds[-3]) if len(tds)>=3 else ""
            forecast=clean(tds[-2]) if len(tds)>=2 else ""
            previous=clean(tds[-1]) if len(tds)>=1 else ""
            impact="مرتفع" if "bull3" in row or "importance3" in row else ("متوسط" if "bull2" in row or "importance2" in row else "منخفض")
            if title:
                items.append({
                    "title": title,
                    "country": country,
                    "published_at": time,
                    "impact": impact,
                    "actual": actual,
                    "forecast": forecast,
                    "previous": previous,
                    "source": "Investing.com Economic Calendar"
                })

        payload={
            "ok": bool(items),
            "source":"real_live_investing_calendar",
            "provider":"Investing.com",
            "generated_at":now(),
            "items":items,
            "note":"لا توجد بيانات وهمية؛ هذا جلب حي مباشر من Investing.com"
        }
        write(OUT,payload)
        update_quality("connected" if items else "empty", f"مرتبط حي من Investing.com، عدد الأحداث: {len(items)}")
        print("ITEMS=",len(items))
    except Exception as e:
        write(OUT,{
            "ok":False,
            "source":"real_live_investing_calendar",
            "provider":"Investing.com",
            "generated_at":now(),
            "items":[],
            "error":str(e),
            "note":"فشل الجلب الحي؛ لم يتم وضع بيانات وهمية"
        })
        update_quality("error","فشل الجلب الحي من Investing.com")
        raise

main()
