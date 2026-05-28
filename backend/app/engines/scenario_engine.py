from app.services.live_scanner import scan_market
from app.core.intelligence_score import compute_intelligence
from app.core.black_layer_engine import compute_black_layer


def build_live_scenarios():
    try:
        market_data = scan_market()
    except Exception as e:
        return [{"error": str(e)}]

    results = []

    for item in market_data:
        sig = item.get("signal", {})

        rsi = sig.get("rsi", 50)
        confidence = sig.get("confidence", 50)

        divergence = sig.get("divergence", "none")
        zone = sig.get("zone", "none")

        data = {
            "symbol": item.get("symbol"),
            "price": item.get("price"),
            "rsi": rsi,
            "divergence": divergence,
            "zone": zone,
            "momentum": "strong" if confidence > 70 else "weak",
            "volume": 100000
        }

        intelligence = compute_intelligence(data)
        black = compute_black_layer(data)

        bias = "bullish" if confidence > 60 else "bearish" if confidence < 40 else "neutral"

        scenario = {
            "interest_zone": f"{data['price']-5} - {data['price']}",
            "invalidation_level": f"{data['price']-15} - {data['price']-10}",
            "target_zone": f"{data['price']+10} - {data['price']+20}"
        }

        results.append({
            "symbol": data["symbol"],
            "price": data["price"],
            "market_bias": bias,
            "confidence": confidence,
            "risk": black.get("pressure", {}).get("risk_level", "moderate"),
            "scenario": scenario,
            "intelligence": intelligence,
            "black_layer": black
        })

    return results


def build_single_scenario():
    data = build_live_scenarios()
    return data[0] if data else {"error": "no data"}
