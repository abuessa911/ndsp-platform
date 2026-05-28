from __future__ import annotations

import csv
import json
import math
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _float(v: Any) -> Optional[float]:
    try:
        x = float(v)
        if math.isfinite(x):
            return x
    except Exception:
        pass
    return None


@dataclass
class PriceSnapshot:
    ok: bool
    symbol: str
    price: Optional[float]
    source: str
    quality: str
    timestamp: str
    latency_ms: int = 0
    stale_seconds: Optional[int] = None
    fallback_used: bool = False
    reason: str = ""
    raw_symbol: Optional[str] = None

    def dict(self) -> Dict[str, Any]:
        return asdict(self)


class PriceSource:
    name = "base"

    def supports(self, symbol: str, market: str) -> bool:
        return False

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        raise NotImplementedError


class BinanceRestSource(PriceSource):
    name = "binance_rest"

    def supports(self, symbol: str, market: str) -> bool:
        return market == "crypto" and symbol.upper().endswith("USDT")

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        started = time.time()
        s = symbol.upper().replace("/", "").replace("-", "")
        url = "https://api.binance.com/api/v3/ticker/price?symbol=" + urllib.parse.quote(s)
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            price = _float(data.get("price"))
            if price is None:
                raise ValueError("invalid_price")
            return PriceSnapshot(
                ok=True,
                symbol=symbol.upper(),
                raw_symbol=s,
                price=price,
                source=self.name,
                quality="live",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
            )
        except Exception as e:
            return PriceSnapshot(
                ok=False,
                symbol=symbol.upper(),
                raw_symbol=s,
                price=None,
                source=self.name,
                quality="unavailable",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                reason=str(e)[:160],
            )


class CoinbaseRestSource(PriceSource):
    name = "coinbase_rest"

    def supports(self, symbol: str, market: str) -> bool:
        s = symbol.upper().replace("/", "").replace("-", "")
        return market == "crypto" and s.endswith("USDT")

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        started = time.time()
        s = symbol.upper().replace("/", "").replace("-", "")
        base = s[:-4] if s.endswith("USDT") else s
        product = f"{base}-USD"
        url = f"https://api.coinbase.com/v2/prices/{urllib.parse.quote(product)}/spot"
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            price = _float(data.get("data", {}).get("amount"))
            if price is None:
                raise ValueError("invalid_price")
            return PriceSnapshot(
                ok=True,
                symbol=symbol.upper(),
                raw_symbol=product,
                price=price,
                source=self.name,
                quality="fallback_live",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
            )
        except Exception as e:
            return PriceSnapshot(
                ok=False,
                symbol=symbol.upper(),
                raw_symbol=product,
                price=None,
                source=self.name,
                quality="unavailable",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                reason=str(e)[:160],
            )


class KrakenRestSource(PriceSource):
    name = "kraken_rest"

    KRAKEN_MAP = {
        "BTCUSDT": "XBTUSD",
        "ETHUSDT": "ETHUSD",
        "SOLUSDT": "SOLUSD",
        "XRPUSDT": "XRPUSD",
        "ADAUSDT": "ADAUSD",
        "DOGEUSDT": "DOGEUSD",
    }

    def supports(self, symbol: str, market: str) -> bool:
        s = symbol.upper().replace("/", "").replace("-", "")
        return market == "crypto" and (s in self.KRAKEN_MAP or s.endswith("USDT"))

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        started = time.time()
        s = symbol.upper().replace("/", "").replace("-", "")
        pair = self.KRAKEN_MAP.get(s, f"{s[:-4]}USD" if s.endswith("USDT") else s)
        url = "https://api.kraken.com/0/public/Ticker?pair=" + urllib.parse.quote(pair)
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            if data.get("error"):
                raise ValueError(",".join(data.get("error", [])))
            result = data.get("result", {})
            first = next(iter(result.values()))
            price = _float(first.get("c", [None])[0])
            if price is None:
                raise ValueError("invalid_price")
            return PriceSnapshot(
                ok=True,
                symbol=symbol.upper(),
                raw_symbol=pair,
                price=price,
                source=self.name,
                quality="fallback_live",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
            )
        except Exception as e:
            return PriceSnapshot(
                ok=False,
                symbol=symbol.upper(),
                raw_symbol=pair,
                price=None,
                source=self.name,
                quality="unavailable",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                reason=str(e)[:160],
            )


class TwelveDataSource(PriceSource):
    name = "twelvedata_rest"

    def __init__(self) -> None:
        self.api_key = os.getenv("TWELVEDATA_API_KEY", "").strip()

    def supports(self, symbol: str, market: str) -> bool:
        return bool(self.api_key) and market in {"forex", "metals", "indices", "energy"}

    def _map_symbol(self, symbol: str, market: str) -> str:
        s = symbol.upper().replace("-", "").replace("/", "")
        if market == "forex" and len(s) == 6:
            return f"{s[:3]}/{s[3:]}"
        mapped = {
            "XAUUSD": "XAU/USD",
            "XAGUSD": "XAG/USD",
            "USOIL": "WTI/USD",
            "UKOIL": "BRENT/USD",
            "US30": "DJI",
            "US500": "SPX",
            "US100": "NDX",
            "GER40": "DAX",
            "UK100": "FTSE",
            "JP225": "NIKKEI225",
        }
        return mapped.get(s, s)

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        started = time.time()
        ts_symbol = self._map_symbol(symbol, market)
        q = urllib.parse.urlencode({"symbol": ts_symbol, "apikey": self.api_key})
        url = "https://api.twelvedata.com/price?" + q
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            if data.get("status") == "error":
                raise ValueError(data.get("message", "twelvedata_error"))
            price = _float(data.get("price"))
            if price is None:
                raise ValueError("invalid_price")
            return PriceSnapshot(
                ok=True,
                symbol=symbol.upper(),
                raw_symbol=ts_symbol,
                price=price,
                source=self.name,
                quality="fallback_live",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
            )
        except Exception as e:
            return PriceSnapshot(
                ok=False,
                symbol=symbol.upper(),
                raw_symbol=ts_symbol,
                price=None,
                source=self.name,
                quality="unavailable",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                reason=str(e)[:160],
            )


class YahooChartSource(PriceSource):
    name = "yahoo_chart"

    def supports(self, symbol: str, market: str) -> bool:
        return market in {"forex", "metals", "indices", "energy", "crypto"}

    def _map_symbol(self, symbol: str, market: str) -> str:
        s = symbol.upper().replace("/", "").replace("-", "")
        if market == "forex" and len(s) == 6:
            return f"{s}=X"
        mapped = {
            "BTCUSDT": "BTC-USD",
            "ETHUSDT": "ETH-USD",
            "SOLUSDT": "SOL-USD",
            "XRPUSDT": "XRP-USD",
            "BNBUSDT": "BNB-USD",
            "ADAUSDT": "ADA-USD",
            "DOGEUSDT": "DOGE-USD",
            "XAUUSD": "GC=F",
            "XAGUSD": "SI=F",
            "USOIL": "CL=F",
            "UKOIL": "BZ=F",
            "US30": "^DJI",
            "US500": "^GSPC",
            "US100": "^IXIC",
            "GER40": "^GDAXI",
            "UK100": "^FTSE",
            "FRA40": "^FCHI",
            "JP225": "^N225",
            "HK50": "^HSI",
            "AUS200": "^AXJO",
        }
        return mapped.get(s, s)

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        started = time.time()
        ys = self._map_symbol(symbol, market)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ys)}?range=1d&interval=1m"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NDSP/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            result = data.get("chart", {}).get("result", [])
            if not result:
                raise ValueError("empty_result")
            meta = result[0].get("meta", {})
            price = _float(meta.get("regularMarketPrice") or meta.get("previousClose"))
            if price is None:
                quote = result[0].get("indicators", {}).get("quote", [{}])[0]
                closes = [x for x in quote.get("close", []) if x is not None]
                price = _float(closes[-1] if closes else None)
            if price is None:
                raise ValueError("invalid_price")
            ts = result[0].get("timestamp", [])
            stale = None
            if ts:
                stale = max(0, int(time.time() - int(ts[-1])))
            return PriceSnapshot(
                ok=True,
                symbol=symbol.upper(),
                raw_symbol=ys,
                price=price,
                source=self.name,
                quality="fallback_delayed",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                stale_seconds=stale,
            )
        except Exception as e:
            return PriceSnapshot(
                ok=False,
                symbol=symbol.upper(),
                raw_symbol=ys,
                price=None,
                source=self.name,
                quality="unavailable",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                reason=str(e)[:160],
            )


class MT4CsvSource(PriceSource):
    name = "mt4_csv_bridge"

    def __init__(self) -> None:
        self.paths = [
            Path(os.getenv("NDSP_MT4_CSV_DIR", "")),
            Path(os.getenv("MT4_CSV_DIR", "")),
            Path.home() / "NDSP_MT4_CANDLES",
            Path.home() / "NDIP_MT4_CANDLES",
            Path("/home/nawaf511/NDSP_MT4_CANDLES"),
            Path("/home/nawaf511/NDIP_MT4_CANDLES"),
        ]

    def supports(self, symbol: str, market: str) -> bool:
        return market in {"forex", "metals", "indices", "energy"}

    def _candidate_files(self, symbol: str) -> List[Path]:
        s = symbol.upper().replace("/", "").replace("-", "")
        names = [f"{s}.csv", f"{s}_M1.csv", f"{s}_m1.csv", f"{s}.CSV"]
        files: List[Path] = []
        for d in self.paths:
            if not str(d):
                continue
            if d.exists() and d.is_dir():
                for n in names:
                    files.append(d / n)
                files.extend(sorted(d.glob(f"*{s}*.csv"), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)[:5])
        return files

    def fetch(self, symbol: str, market: str, timeout: float = 5.0) -> PriceSnapshot:
        started = time.time()
        try:
            candidates = [p for p in self._candidate_files(symbol) if p.exists() and p.is_file()]
            if not candidates:
                raise FileNotFoundError("no_mt4_csv_found")
            path = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            rows: List[List[str]] = []
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                sample = f.read(8192)
                f.seek(0)
                dialect = csv.Sniffer().sniff(sample) if sample.strip() else csv.excel
                reader = csv.reader(f, dialect)
                for row in reader:
                    if row:
                        rows.append(row)
            if not rows:
                raise ValueError("empty_csv")
            last = rows[-1]
            nums = [_float(x) for x in last]
            nums = [x for x in nums if x is not None]
            if not nums:
                raise ValueError("no_numeric_price")
            price = nums[-1]
            stale = int(time.time() - path.stat().st_mtime)
            quality = "live" if stale <= 180 else "fallback_stale"
            return PriceSnapshot(
                ok=True,
                symbol=symbol.upper(),
                raw_symbol=str(path),
                price=price,
                source=self.name,
                quality=quality,
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                stale_seconds=stale,
            )
        except Exception as e:
            return PriceSnapshot(
                ok=False,
                symbol=symbol.upper(),
                price=None,
                source=self.name,
                quality="unavailable",
                timestamp=utc_now_iso(),
                latency_ms=int((time.time() - started) * 1000),
                reason=str(e)[:160],
            )


def resolve_market(symbol: str) -> str:
    s = symbol.upper().replace("/", "").replace("-", "")
    crypto = {"BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "SHIBUSDT"}
    forex = {
        "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
        "EURJPY", "GBPJPY", "EURGBP", "AUDJPY", "CADJPY"
    }
    metals = {"XAUUSD", "XAGUSD"}
    energy = {"USOIL", "UKOIL", "WTI", "BRENT"}
    indices = {
        "US30", "US500", "US100", "GER40", "UK100", "FRA40", "EU50",
        "JP225", "HK50", "AUS200", "CHINA50", "ES35"
    }
    if s in crypto or s.endswith("USDT"):
        return "crypto"
    if s in forex:
        return "forex"
    if s in metals:
        return "metals"
    if s in energy:
        return "energy"
    if s in indices:
        return "indices"
    return "unknown"


def source_order_for_market(market: str) -> List[PriceSource]:
    if market == "crypto":
        return [BinanceRestSource(), CoinbaseRestSource(), KrakenRestSource(), YahooChartSource()]
    if market in {"forex", "metals", "indices", "energy"}:
        return [MT4CsvSource(), TwelveDataSource(), YahooChartSource()]
    return [YahooChartSource()]
