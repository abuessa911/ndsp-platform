from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import asyncpg

def _db_url():
    return (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("AUTH_DATABASE_URL")
        or "postgresql://ndsp_auth@127.0.0.1:5432/ndsp_auth"
    )

def mount_ndsp_market_routes(app: FastAPI):
    @app.get("/api/market/prices", include_in_schema=True)
    async def ndsp_market_prices_direct():
        try:
            conn = await asyncpg.connect(_db_url())
            try:
                rows = await conn.fetch("""
                    SELECT symbol, name_ar, name_en, category, source, is_active, updated_at
                    FROM ndsp_assets
                    WHERE is_active=true
                    ORDER BY
                      CASE category
                        WHEN 'crypto' THEN 1
                        WHEN 'forex' THEN 2
                        WHEN 'commodity' THEN 3
                        WHEN 'index' THEN 4
                        ELSE 9
                      END,
                      symbol
                """)

                fallback = {
                    "BTCUSDT": 68000, "ETHUSDT": 3600, "BNBUSDT": 590, "SOLUSDT": 160,
                    "XRPUSDT": 0.52, "ADAUSDT": 0.45, "DOGEUSDT": 0.16,
                    "EURUSD": 1.08, "GBPUSD": 1.27, "USDJPY": 157,
                    "XAUUSD": 2350, "XAGUSD": 30, "USOIL": 78, "UKOIL": 82,
                    "SPX": 5300, "NDX": 18500, "DJI": 39000, "DXY": 105
                }

                prices = []
                for r in rows:
                    sym = r["symbol"]
                    prices.append({
                        "symbol": sym,
                        "name_ar": r["name_ar"],
                        "name_en": r["name_en"],
                        "category": r["category"],
                        "source": r["source"],
                        "price": float(fallback.get(sym, 0)),
                        "change_24h": 0.0,
                        "change_pct": 0.0,
                        "updated_at": str(r["updated_at"]) if r["updated_at"] else None,
                        "status": "active",
                        "provider_status": "seeded"
                    })

                return {"ok": True, "source": "ndsp_assets", "count": len(prices), "prices": prices}
            finally:
                await conn.close()
        except Exception as e:
            return JSONResponse(
                {"ok": False, "code": "MARKET_PRICES_ERROR", "detail": str(e)[:180], "prices": []},
                status_code=500
            )

    @app.get("/api/market/supported-assets", include_in_schema=True)
    async def ndsp_supported_assets_direct():
        try:
            conn = await asyncpg.connect(_db_url())
            try:
                rows = await conn.fetch("""
                    SELECT symbol, code, name_ar, name_en, category, source, is_active, updated_at
                    FROM ndsp_assets
                    WHERE is_active=true
                    ORDER BY category, symbol
                """)
                assets = [dict(r) for r in rows]
                counts = {}
                sources = {}
                for a in assets:
                    counts[a.get("category") or "unknown"] = counts.get(a.get("category") or "unknown", 0) + 1
                    sources[a.get("source") or "unknown"] = sources.get(a.get("source") or "unknown", 0) + 1
                return {"ok": True, "count": len(assets), "counts": counts, "sources": sources, "assets": assets}
            finally:
                await conn.close()
        except Exception as e:
            return JSONResponse(
                {"ok": False, "code": "SUPPORTED_ASSETS_ERROR", "detail": str(e)[:180], "assets": []},
                status_code=500
            )
