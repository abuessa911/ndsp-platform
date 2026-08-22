from __future__ import annotations

def reconcile_numeric_observations(observations, *, tolerance_ratio=0.002):
    valid=[x for x in observations if x.get("value") is not None]
    if not valid:
        return {"status":"DATA_BLOCKED","decision_use_allowed":False,"reason":"NO_VALID_OBSERVATIONS"}
    valid=sorted(valid,key=lambda x:int(x.get("authority_rank",999999)))
    authority=valid[0]
    base=float(authority["value"])
    conflicts=[]
    for item in valid[1:]:
        value=float(item["value"])
        denominator=max(abs(base),1e-12)
        ratio=abs(value-base)/denominator
        if ratio>tolerance_ratio:
            conflicts.append({"source_id":item.get("source_id"),"difference_ratio":ratio})
    return {
        "status":"RECONCILED" if not conflicts else "SOURCE_CONFLICT",
        "decision_use_allowed":not conflicts,
        "accepted_source_id":authority.get("source_id"),
        "accepted_value":base,
        "conflicts":conflicts,
    }
