from fastapi import FastAPI, Request, HTTPException, Depends
import os
import requests

app = FastAPI()

ADMIN_TOKEN = os.getenv("NDSP_ADMIN_TOKEN", "Essa#$#$1365")
CORE_API = "http://127.0.0.1:9001"

# 🔐 تحقق
async def verify_admin(request: Request):
    token = request.headers.get("X-Admin-Key")
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

# ✅ مهم: Endpoint الحالة
@app.get("/admin/status")
async def admin_status(dep=Depends(verify_admin)):
    return {"status": "ok"}

# 📡 Market
@app.get("/admin/market")
async def market(dep=Depends(verify_admin)):
    try:
        r = requests.get(f"{CORE_API}/market_state")
        return r.json()
    except:
        return {"market": "unknown"}

# 📊 Metrics
@app.get("/admin/metrics")
async def metrics(dep=Depends(verify_admin)):
    return {
        "signals": 120,
        "winrate": 87,
        "profit": 32,
        "latency": "120ms"
    }

# 🧠 NDSP
@app.get("/admin/ndsp")
async def ndsp(dep=Depends(verify_admin)):
    return {
        "score": 92,
        "divergence": "bullish",
        "liquidity": "above"
    }

# ⚙️ Control
@app.post("/admin/control")
async def control(action: str, dep=Depends(verify_admin)):
    return {"status": "ok", "action": action}
