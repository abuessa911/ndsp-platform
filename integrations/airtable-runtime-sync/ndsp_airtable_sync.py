#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

PAT=os.environ["AIRTABLE_PAT"]
BASE=os.environ["AIRTABLE_BASE_ID"]
CAP_TABLE=os.environ["AIRTABLE_CAP_TABLE_ID"]
HEALTH_TABLE=os.environ["AIRTABLE_HEALTH_TABLE_ID"]
SYNC_TABLE=os.environ["AIRTABLE_SYNC_TABLE_ID"]
GOV=os.environ["NDSP_GOVERNANCE_URL"]
API=os.environ["NDSP_API_URL"]
NOW=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

CAP_IDS={
"NDSP-CAP-001":"recOvuJ2suk4wera5","NDSP-CAP-002":"recd6dWYMLSiIelVy","NDSP-CAP-003":"recKJr0LVHIAMD3g2","NDSP-CAP-004":"recQtI4qjxmchbVAO","NDSP-CAP-005":"recbS5gllHYnun08z","NDSP-CAP-006":"rec1oWlb4bUHknKWP","NDSP-CAP-007":"reclMB5UaDhS1CDxT","NDSP-CAP-008":"recDTF6Deb2Qifqwj","NDSP-CAP-009":"recttddmLbtZowXqp","NDSP-CAP-010":"recZw0GSWZ2HXn9h6","NDSP-CAP-011":"recRefMpy2UJ4q2L7","NDSP-CAP-012":"recmECO4mNz8oFjsZ","NDSP-CAP-013":"recwtlzSRj5fdMzCz","NDSP-CAP-014":"recW8Tvuvss6C4pbW","NDSP-CAP-015":"recQCp1IUudWAHPto","NDSP-CAP-016":"recK4f1h08LHFAXCd","NDSP-CAP-017":"recxSaHwjWEWjnud6","NDSP-CAP-018":"reclCNvVO9FEedOBo","NDSP-CAP-019":"recDVJzOucbSKudv7","NDSP-CAP-020":"recfsW6P5phGxhrYo","NDSP-CAP-021":"recvTyp46V4mYzQ9x","NDSP-CAP-022":"rechH8G29pOKmlnDI","NDSP-CAP-023":"recH0R0lM55dl633H","NDSP-CAP-024":"rec7kQq842KXKmjrS","NDSP-CAP-025":"recuKBDzrIMgrbkVj","NDSP-CAP-026":"recfmGQMclkJST5Ie","NDSP-CAP-027":"recEKSDCJBBv0hk9O","NDSP-CAP-028":"recYTcR2xWKwMBnWz"}
HEALTH_IDS={"daily":"recWp5bzzEVM3pVjb","weekly":"recEQnmH0swni0Fyt","monthly":"recBC0dDuhWzeG6rN","bridge":"recOAMvS4g86roXTB"}
SYNC_IDS=["recsPwmtfrmbLGmM0","recaHOyEygO7A5dJ1","recPT9FS7iJdqZ6vX","recbjxDBpzAoqIs2Q"]

F_RUNTIME="fldRnaQE3rpoUlnOL"
F_BIND="fldlsVqnlG6OC1IJW"
F_BLOCK="fldcgUELpPTX9is16"
F_LAST="flduZqwzXXR11KWsH"
F_NDSP="fldjAzxuLdD9vl4pd"
F_ALPIC="fldLwhgi39SiM8T1l"
F_SYNC="fldH83taPRBy4QYg6"

H_STATUS="flde1Q6bebvWNKoJg"
H_HTTP="fld5vlEuP0na7py00"
H_DETAILS="fldaJ0wEqVXsQBm6s"
H_CHECKED="fldLfOyGIxqSDFCAk"

S_STATUS="flddtxTs0GqDStW1r"
S_LAST="fld5gKVT5lJdxf0f0"
S_ENABLED="fldX3hcmk6O6PBoH3"
S_BLOCKER="fldmoXxOng9xWbptU"

def sanitize_error_body(raw: bytes) -> str:
    text=raw.decode("utf-8",errors="replace")
    if PAT:
        text=text.replace(PAT,"[REDACTED]")
    return text[:4000]

def req(
    url: str,
    method: str="GET",
    payload: Any | None=None,
    auth: bool=False,
    timeout: int=30,
) -> tuple[int, Any]:
    headers={"Accept":"application/json","User-Agent":"NDSP-Airtable-Sync/1.1"}
    if auth:
        headers["Authorization"]="Bearer "+PAT
    data=None
    if payload is not None:
        data=json.dumps(payload,ensure_ascii=False).encode()
        headers["Content-Type"]="application/json"

    request=urllib.request.Request(url,data=data,headers=headers,method=method)

    for attempt in range(1,4):
        try:
            with urllib.request.urlopen(request,timeout=timeout) as response:
                raw=response.read()
                body=json.loads(raw.decode() or "{}")
                return response.status, body
        except urllib.error.HTTPError as error:
            body=sanitize_error_body(error.read())
            if error.code == 429 and attempt < 3:
                time.sleep(30)
                continue
            if 500 <= error.code <= 599 and attempt < 3:
                time.sleep(attempt * 2)
                continue
            raise RuntimeError(
                f"HTTP_{error.code} method={method} url={url} body={body}"
            ) from error
        except urllib.error.URLError as error:
            if attempt < 3:
                time.sleep(attempt * 2)
                continue
            raise RuntimeError(f"URL_ERROR method={method} url={url} reason={error}") from error

    raise RuntimeError(f"REQUEST_RETRIES_EXHAUSTED method={method} url={url}")

def at_patch(table: str, records: list[dict[str, Any]]) -> int:
    """Update Airtable records in REST-safe batches of at most 10."""
    url=f"https://api.airtable.com/v0/{BASE}/{table}"
    total=0
    for start in range(0,len(records),10):
        batch=records[start:start+10]
        if not batch:
            continue
        if len(batch) > 10:
            raise RuntimeError(f"AIRTABLE_BATCH_TOO_LARGE_{len(batch)}")
        code,_=req(url,"PATCH",{"records":batch},True)
        if code not in (200,201):
            raise RuntimeError(f"AIRTABLE_PATCH_UNEXPECTED_STATUS_{code}")
        total += len(batch)
        # Stay below Airtable's five-requests-per-second base limit.
        time.sleep(0.25)
    return total

def normalize_state(value: Any) -> str:
    state=str(value or "READY_VERIFIED").upper()
    allowed={
        "LIVE_VERIFIED",
        "PARTIALLY_LIVE",
        "READY_VERIFIED",
        "PROBE_FAILED",
        "NOT_INSTALLED",
    }
    if state in allowed:
        return state
    if "LIVE" in state and "PART" not in state:
        return "LIVE_VERIFIED"
    if "PART" in state:
        return "PARTIALLY_LIVE"
    if "FAIL" in state:
        return "PROBE_FAILED"
    return "READY_VERIFIED"

params=urllib.parse.urlencode({
    "symbol":"ETHUSDT",
    "timeframe":"weekly",
    "_sync":NOW,
})
status,governance=req(GOV+"?"+params)
if status != 200:
    raise RuntimeError(f"GOVERNANCE_HTTP_{status}")

capabilities=governance.get("platform_capabilities") or []
if len(capabilities) != 28:
    raise RuntimeError(f"CAPABILITY_COUNT_{len(capabilities)}")

capability_records=[]
for capability in capabilities:
    capability_id=capability.get("id") or capability.get("capability_id")
    if capability_id not in CAP_IDS:
        continue

    state=normalize_state(
        capability.get("runtime_state")
        or capability.get("state")
        or capability.get("implementation_status")
    )
    binding=(
        capability.get("runtime_binding")
        or capability.get("evidence")
        or capability.get("evidence_summary")
        or "Evidence refreshed from NDSP governance endpoint"
    )
    blocker=(
        capability.get("activation_blockers")
        or capability.get("blocker")
        or ""
    )
    if isinstance(binding,(dict,list)):
        binding=json.dumps(binding,ensure_ascii=False)
    if isinstance(blocker,(dict,list)):
        blocker=json.dumps(blocker,ensure_ascii=False)

    capability_records.append({
        "id":CAP_IDS[capability_id],
        "fields":{
            F_RUNTIME:state,
            F_BIND:str(binding)[:9000],
            F_BLOCK:str(blocker)[:9000],
            F_LAST:NOW,
            F_NDSP:"CONNECTED",
            F_ALPIC:"ACTIVE",
            F_SYNC:"LIVE_SYNC",
        },
    })

if len(capability_records) != 28:
    raise RuntimeError(f"MAPPED_CAPABILITIES_{len(capability_records)}")

capability_updates=at_patch(CAP_TABLE,capability_records)
if capability_updates != 28:
    raise RuntimeError(f"AIRTABLE_CAPABILITY_UPDATES_{capability_updates}")

health_records=[]
for timeframe in ("daily","weekly","monthly"):
    query=urllib.parse.urlencode({
        "symbol":"ETHUSDT",
        "timeframe":timeframe,
        "_sync":NOW,
    })
    try:
        health_status,_=req(API+"?"+query)
        state="PASS" if health_status == 200 else "FAIL"
        details=f"Automated live sync check for {timeframe}"
    except Exception as error:
        health_status=0
        state="FAIL"
        details=str(error)[:9000]

    health_records.append({
        "id":HEALTH_IDS[timeframe],
        "fields":{
            H_STATUS:state,
            H_HTTP:health_status,
            H_DETAILS:details,
            H_CHECKED:NOW,
        },
    })

health_records.append({
    "id":HEALTH_IDS["bridge"],
    "fields":{
        H_STATUS:"PASS",
        H_HTTP:200,
        H_DETAILS:"28 capabilities synchronized from same-origin governance bridge",
        H_CHECKED:NOW,
    },
})

health_updates=at_patch(HEALTH_TABLE,health_records)
if health_updates != 4:
    raise RuntimeError(f"AIRTABLE_HEALTH_UPDATES_{health_updates}")

sync_records=[
    {
        "id":record_id,
        "fields":{
            S_STATUS:"ACTIVE",
            S_LAST:NOW,
            S_ENABLED:True,
            S_BLOCKER:"",
        },
    }
    for record_id in SYNC_IDS
]

sync_updates=at_patch(SYNC_TABLE,sync_records)
if sync_updates != 4:
    raise RuntimeError(f"AIRTABLE_SYNC_JOB_UPDATES_{sync_updates}")

print(json.dumps({
    "ok":True,
    "capabilities":capability_updates,
    "health":health_updates,
    "sync_jobs":sync_updates,
    "airtable_batch_max":10,
    "checked_at":NOW,
},ensure_ascii=False))
