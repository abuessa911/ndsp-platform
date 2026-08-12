from __future__ import annotations

def evaluate_conflicts(layer_results):
    directional=[]
    for item in layer_results:
        output=item.get("output") or {}
        direction=output.get("direction") or output.get("governing_direction")
        if direction in {"bullish","bearish"}:
            directional.append((item.get("layer_id"),direction))
    directions={x[1] for x in directional}
    conflicts=[] if len(directions)<=1 else directional
    return {
        "status":"CONFIRMED" if not conflicts else "CONFLICT_DETECTED",
        "conflicts":conflicts,
        "decision_authority":False,
        "forward_to":["NDSP-CORE-L15","NDSP-CORE-L16"],
    }
