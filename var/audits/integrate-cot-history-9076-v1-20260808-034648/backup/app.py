from __future__ import annotations

import csv
import json
import time
import urllib.request
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

DATA_DIR = Path("/home/nawaf511/empire-core-new/backend/data/raw_cot")
DATA_DIR.mkdir(parents=True, exist_ok=True)

TFF_URL = "https://www.cftc.gov/dea/newcot/FinFutWk.txt"
DISAGG_URL = "https://www.cftc.gov/dea/newcot/f_disagg.txt"

TFF_CURRENT = DATA_DIR / "current_tff_futures_only_FinFutWk.txt"
DISAGG_CURRENT = DATA_DIR / "current_disaggregated_futures_only_f_disagg.txt"
MANIFEST = DATA_DIR / "raw_cot_manifest.json"

app = FastAPI(title="NDSP Raw COT Gateway", version="0.2.0-current-cftc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.ndsp.app", "https://my.ndsp.app", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def download(url: str, path: Path) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "NDSP-Raw-COT-Gateway/0.2"})
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read()
    path.write_bytes(raw)
    return {"url": url, "path": str(path), "bytes": len(raw)}


def import_current() -> dict[str, Any]:
    stamp = time.strftime("%Y%m%d_%H%M%S")
    tff_snapshot = DATA_DIR / f"tff_futures_only_FinFutWk_{stamp}.txt"
    disagg_snapshot = DATA_DIR / f"disaggregated_futures_only_f_disagg_{stamp}.txt"

    tff = download(TFF_URL, tff_snapshot)
    disagg = download(DISAGG_URL, disagg_snapshot)

    TFF_CURRENT.write_bytes(tff_snapshot.read_bytes())
    DISAGG_CURRENT.write_bytes(disagg_snapshot.read_bytes())

    manifest = {
        "ok": True,
        "imported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": {
            "tff_futures_only": tff,
            "disaggregated_futures_only": disagg,
        },
        "current_files": {
            "tff": str(TFF_CURRENT),
            "disaggregated": str(DISAGG_CURRENT),
        },
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def list_files() -> list[dict[str, Any]]:
    out = []
    for p in sorted(DATA_DIR.glob("*")):
        if p.is_file():
            out.append({
                "name": p.name,
                "path": str(p),
                "size": p.stat().st_size,
                "suffix": p.suffix.lower(),
            })
    return out


def asset_aliases(asset: str) -> list[str]:
    a = (asset or "").upper().replace("-", "").replace("/", "")
    if a in {"ETH", "ETHUSD", "ETHUSDT", "ETHER"}:
        return ["ETHER", "ETH"]
    if a in {"BTC", "BTCUSD", "BTCUSDT", "BITCOIN"}:
        return ["BITCOIN", "BTC"]
    if a in {"GOLD", "XAU", "XAUUSD", "GC"}:
        return ["GOLD", "GOLD - COMMODITY EXCHANGE"]
    if a in {"SILVER", "XAG", "XAGUSD", "SI"}:
        return ["SILVER", "SILVER - COMMODITY EXCHANGE"]
    return [a]


def safe_int(v: Any) -> int:
    try:
        return int(str(v).replace(",", "").strip())
    except Exception:
        return 0


def bias_from_net(net: int) -> str:
    if net > 0:
        return "bullish"
    if net < 0:
        return "bearish"
    return "neutral"


def parse_tff_rows() -> list[list[str]]:
    if not TFF_CURRENT.exists():
        return []
    text = TFF_CURRENT.read_text(encoding="utf-8", errors="ignore")
    rows = []
    for row in csv.reader(text.splitlines()):
        if len(row) > 20:
            rows.append([x.strip() for x in row])
    return rows


def find_tff_asset(asset: str) -> dict[str, Any]:
    rows = parse_tff_rows()
    aliases = asset_aliases(asset)

    if not rows:
        return {
            "raw_cot_connected": False,
            "raw_cot_status": "WAITING_FOR_IMPORT",
            "source_family": "TFF",
            "source_file": str(TFF_CURRENT),
            "matched_rows": 0,
            "message": "No current TFF file imported yet.",
        }

    match = None
    for row in rows:
        name = row[0].upper() if row else ""
        if any(alias in name for alias in aliases):
            match = row
            break

    if not match:
        return {
            "raw_cot_connected": False,
            "raw_cot_status": "CONNECTED_NO_ASSET_MATCH",
            "source_family": "TFF",
            "source_file": str(TFF_CURRENT),
            "total_rows": len(rows),
            "matched_rows": 0,
            "aliases": aliases,
        }

    # CFTC TFF futures-only record positions:
    # 7 open interest
    # 8 dealer long, 9 dealer short
    # 11 asset manager long, 12 asset manager short
    # 14 leveraged funds long, 15 leveraged funds short
    open_interest = safe_int(match[7])
    dealer_long = safe_int(match[8])
    dealer_short = safe_int(match[9])
    asset_mgr_long = safe_int(match[11])
    asset_mgr_short = safe_int(match[12])
    leveraged_long = safe_int(match[14])
    leveraged_short = safe_int(match[15])

    dealer_net = dealer_long - dealer_short
    asset_mgr_net = asset_mgr_long - asset_mgr_short
    leveraged_net = leveraged_long - leveraged_short

    return {
        "raw_cot_connected": True,
        "raw_cot_status": "CONNECTED_MATCHED",
        "source_family": "TFF",
        "source_file": str(TFF_CURRENT),
        "market_name": match[0],
        "report_yyMMdd": match[1],
        "report_date": match[2],
        "exchange": match[4].strip() if len(match) > 4 else None,
        "open_interest": open_interest,

        "dealer_intermediary_long": dealer_long,
        "dealer_intermediary_short": dealer_short,
        "dealer_intermediary_net": dealer_net,
        "dealer_intermediary_bias": bias_from_net(dealer_net),

        "asset_managers_long": asset_mgr_long,
        "asset_managers_short": asset_mgr_short,
        "asset_managers_net": asset_mgr_net,
        "asset_managers_bias": bias_from_net(asset_mgr_net),

        "leveraged_funds_long": leveraged_long,
        "leveraged_funds_short": leveraged_short,
        "leveraged_funds_net": leveraged_net,
        "leveraged_funds_bias": bias_from_net(leveraged_net),

        "matched_rows": 1,
        "total_rows": len(rows),
        "raw_row_head": match[:18],
    }


@app.get("/api/admin/raw-cot/health")
def health() -> dict[str, Any]:
    files = list_files()
    manifest = None
    if MANIFEST.exists():
        try:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            manifest = None
    return {
        "ok": True,
        "service": "ndsp-raw-cot-gateway",
        "version": "0.2.0-current-cftc",
        "data_dir": str(DATA_DIR),
        "files_count": len(files),
        "raw_cot_status": "WAITING_FOR_IMPORT" if not TFF_CURRENT.exists() else "CURRENT_FILES_PRESENT",
        "tff_current_exists": TFF_CURRENT.exists(),
        "disagg_current_exists": DISAGG_CURRENT.exists(),
        "manifest": manifest,
        "files": files,
    }


@app.get("/api/admin/raw-cot/import-current")
def import_current_get() -> dict[str, Any]:
    result = import_current()
    eth = find_tff_asset("ETHUSDT")
    btc = find_tff_asset("BTCUSDT")
    return {"ok": True, "import": result, "ethusdt_status": eth, "btcusdt_status": btc}


@app.post("/api/admin/raw-cot/import-current")
def import_current_post() -> dict[str, Any]:
    return import_current_get()


@app.get("/api/admin/raw-cot/status")
def status(asset: str = Query("ETHUSDT")) -> dict[str, Any]:
    result = find_tff_asset(asset)
    return {
        "ok": True,
        "asset": asset,
        **result,
    }
