from __future__ import annotations

import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


BACKEND = Path("/home/nawaf511/empire-core-new/backend")
MT4_DIR = Path(os.getenv("NDSP_MT4_CSV_DIR") or os.getenv("NDIP_MT4_CSV_DIR") or BACKEND / "data" / "mt4")
RUNTIME_DIR = BACKEND / "runtime"
STATUS_JSON = RUNTIME_DIR / "mt4_freshness_status.json"
STATUS_CSV = RUNTIME_DIR / "mt4_freshness_status.csv"

WATCH = {
    "EURUSD": ["NDIP_MT4_CANDLES_EURUSD_M1.csv", "NDSP_MT4_CANDLES_EURUSD_M1.csv"],
    "GBPUSD": ["NDIP_MT4_CANDLES_GBPUSD_M1.csv", "NDSP_MT4_CANDLES_GBPUSD_M1.csv"],
    "XAUUSD": ["NDIP_MT4_CANDLES_XAUUSD_M1.csv", "NDSP_MT4_CANDLES_XAUUSD_M1.csv"],
    "USOIL": ["NDIP_MT4_CANDLES_USOilSpot_M1.csv", "NDIP_MT4_CANDLES_USOil_M1.csv", "NDSP_MT4_CANDLES_USOIL_M1.csv"],
    "UKOIL": ["NDIP_MT4_CANDLES_UKOilSpot_M1.csv", "NDIP_MT4_CANDLES_UKOil_M1.csv", "NDSP_MT4_CANDLES_UKOIL_M1.csv"],
}

MAX_AGE_SECONDS = int(os.getenv("NDSP_MT4_MAX_AGE_SECONDS", "180"))
INTERVAL_SECONDS = int(os.getenv("NDSP_MT4_GUARD_INTERVAL_SECONDS", "30"))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def find_file(names: list[str]) -> Path | None:
    for name in names:
        p = MT4_DIR / name
        if p.exists() and p.is_file():
            return p
    return None


def last_csv_row(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        if len(rows) < 2:
            return {}
        header = [x.strip() for x in rows[0]]
        last = rows[-1]
        return {header[i]: last[i] for i in range(min(len(header), len(last)))}
    except Exception:
        return {}


def check_symbol(symbol: str, names: list[str]) -> dict:
    p = find_file(names)
    if not p:
        return {
            "symbol": symbol,
            "ok": False,
            "state": "missing",
            "file": None,
            "mtime": None,
            "age_seconds": None,
            "last_row": {},
        }

    st = p.stat()
    age = max(0, int(time.time() - st.st_mtime))
    ok = age <= MAX_AGE_SECONDS

    return {
        "symbol": symbol,
        "ok": ok,
        "state": "fresh" if ok else "stale",
        "file": str(p),
        "mtime": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
        "age_seconds": age,
        "max_age_seconds": MAX_AGE_SECONDS,
        "last_row": last_csv_row(p),
    }


def write_status(payload: dict) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    tmp = STATUS_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATUS_JSON)

    rows = payload.get("symbols", [])
    with STATUS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["checked_at", "symbol", "ok", "state", "age_seconds", "file"])
        for r in rows:
            writer.writerow([
                payload.get("checked_at"),
                r.get("symbol"),
                r.get("ok"),
                r.get("state"),
                r.get("age_seconds"),
                r.get("file"),
            ])


def run_once() -> dict:
    symbols = [check_symbol(sym, names) for sym, names in WATCH.items()]
    all_ok = all(x.get("ok") for x in symbols)

    payload = {
        "system": "NDSP",
        "component": "mt4_freshness_guard",
        "checked_at": now_utc().isoformat(),
        "mt4_dir": str(MT4_DIR),
        "all_ok": all_ok,
        "state": "live" if all_ok else "stale_or_missing",
        "max_age_seconds": MAX_AGE_SECONDS,
        "symbols": symbols,
    }

    write_status(payload)
    return payload


def main() -> None:
    while True:
        payload = run_once()
        print(
            f"{payload['checked_at']} state={payload['state']} "
            f"all_ok={payload['all_ok']} mt4_dir={payload['mt4_dir']}",
            flush=True,
        )
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
