#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import xml.etree.ElementTree as ET
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

HOST = os.environ.get("BRIDGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("BRIDGE_PORT", "9094"))
TWELVE_KEY = os.environ.get("TWELVE_DATA_API_KEY", "").strip()
USER_AGENT = "NDSP-Market-Data-Bridge/2.1"
CACHE: dict[str, tuple[float, Any]] = {}
CACHE_LOCK = threading.Lock()

# NDSP_NEWS_CACHE_THROTTLE_V5
NEWS_CACHE_DIR = os.environ.get(
    "NEWS_CACHE_DIR",
    "/var/lib/ndsp-market-data-bridge-v2",
)
NEWS_CACHE_TTL = max(60, int(os.environ.get("NEWS_CACHE_TTL", "900")))
NEWS_STALE_TTL = max(
    NEWS_CACHE_TTL,
    int(os.environ.get("NEWS_STALE_TTL", "86400")),
)
NEWS_MIN_UPSTREAM_INTERVAL = max(
    5.0,
    float(os.environ.get("NEWS_MIN_UPSTREAM_INTERVAL", "6")),
)
NEWS_UPSTREAM_LOCK = threading.Lock()
NEWS_LAST_UPSTREAM_AT = 0.0

# NDSP_MULTI_SOURCE_FINANCIAL_NEWS_V6
NEWS_FAILURE_TTL = max(10, int(os.environ.get("NEWS_FAILURE_TTL", "30")))
NEWS_FETCH_BATCH = max(10, min(int(os.environ.get("NEWS_FETCH_BATCH", "50")), 75))
NEWS_GOOGLE_LANGUAGE = os.environ.get("NEWS_GOOGLE_LANGUAGE", "en-US")
NEWS_GOOGLE_COUNTRY = os.environ.get("NEWS_GOOGLE_COUNTRY", "US")

CRYPTO_INTERVALS = {
    "1m": "1m", "minute": "1m",
    "5m": "5m", "15m": "15m", "30m": "30m",
    "1h": "1h", "hour": "1h", "hourly": "1h",
    "4h": "4h",
    "1d": "1d", "day": "1d", "daily": "1d",
    "1w": "1w", "week": "1w", "weekly": "1w",
    "1M": "1M", "month": "1M", "monthly": "1M",
}

TWELVE_INTERVALS = {
    "1m": "1min", "minute": "1min",
    "5m": "5min", "15m": "15min", "30m": "30min",
    "1h": "1h", "hour": "1h", "hourly": "1h",
    "4h": "4h",
    "1d": "1day", "day": "1day", "daily": "1day",
    "1w": "1week", "week": "1week", "weekly": "1week",
    "1M": "1month", "month": "1month", "monthly": "1month",
}

TWELVE_SYMBOLS = {
    "BTCUSDT": "BTC/USD",
    "ETHUSDT": "ETH/USD",
    "SOLUSDT": "SOL/USD",
    "XAUUSD": "XAU/USD",
    "XAGUSD": "XAG/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "USDCHF": "USD/CHF",
    "USDCAD": "USD/CAD",
    "AUDUSD": "AUD/USD",
    "NZDUSD": "NZD/USD",
    "USOIL": "WTI/USD",
    "WTI": "WTI/USD",
    "UKOIL": "BRENT/USD",
    "BRENT": "BRENT/USD",
    "SPX": "SPX",
    "NDX": "NDX",
    "DXY": "DXY",
}

NEWS_QUERIES = {
    "BTC": '(Bitcoin OR BTC OR cryptocurrency)',
    "ETH": '(Ethereum OR Ether OR cryptocurrency)',
    "SOL": '(Solana OR SOL OR cryptocurrency)',
    "XAU": '(gold OR bullion OR precious metals)',
    "XAG": '(silver OR precious metals)',
    "EUR": '(euro OR ECB OR "European Central Bank")',
    "GBP": '(sterling OR "Bank of England" OR UK inflation)',
    "JPY": '(yen OR "Bank of Japan")',
    "CHF": '(Swiss franc OR "Swiss National Bank")',
    "CAD": '(Canadian dollar OR "Bank of Canada")',
    "AUD": '(Australian dollar OR "Reserve Bank of Australia")',
    "NZD": '(New Zealand dollar OR "Reserve Bank of New Zealand")',
    "USOIL": '(oil OR WTI OR OPEC OR crude)',
    "WTI": '(oil OR WTI OR OPEC OR crude)',
    "UKOIL": '(Brent OR oil OR OPEC OR crude)',
    "BRENT": '(Brent OR oil OR OPEC OR crude)',
    "SPX": '("S&P 500" OR US stocks OR Wall Street)',
    "NDX": '(Nasdaq OR technology stocks OR Wall Street)',
    "DXY": '("US dollar" OR DXY OR "Federal Reserve")',
}

class BridgeError(Exception):
    def __init__(self, message: str, status: int = 502, details: Any = None):
        super().__init__(message)
        self.status = status
        self.details = details


def cache_get(key: str, ttl: int) -> Any | None:
    now = time.time()
    with CACHE_LOCK:
        row = CACHE.get(key)
        if not row:
            return None
        created, value = row
        if now - created > ttl:
            CACHE.pop(key, None)
            return None
        return value


def cache_put(key: str, value: Any) -> None:
    with CACHE_LOCK:
        CACHE[key] = (time.time(), value)


def get_json(url: str, timeout: int = 15) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(8_000_000)
            return json.loads(body.decode("utf-8", errors="strict"))
    except urllib.error.HTTPError as exc:
        body = exc.read(1000).decode("utf-8", errors="replace")
        raise BridgeError(
            f"Upstream HTTP {exc.code}",
            502,
            body[:500],
        ) from exc
    except Exception as exc:
        raise BridgeError(
            "Upstream connection failed",
            502,
            str(exc),
        ) from exc


def clean_symbol(value: str) -> str:
    symbol = re.sub(r"[^A-Za-z0-9._/-]", "", value or "").upper()
    if not 2 <= len(symbol) <= 24:
        raise BridgeError("Invalid symbol", 400)
    return symbol


def clean_limit(value: str | None) -> int:
    try:
        limit = int(value or "260")
    except ValueError as exc:
        raise BridgeError("Invalid limit", 400) from exc
    return max(20, min(limit, 1000))


def clean_news_limit(value: str | None) -> int:
    try:
        limit = int(value or "30")
    except ValueError as exc:
        raise BridgeError("Invalid news limit", 400) from exc
    return max(1, min(limit, 75))


def is_crypto(symbol: str) -> bool:
    return symbol.endswith("USDT") or symbol in {
        "BTCUSD", "ETHUSD", "SOLUSD", "BNBUSDT", "XRPUSDT", "ADAUSDT"
    }


def binance_symbol(symbol: str) -> str:
    if symbol.endswith("USD") and not symbol.endswith("USDT"):
        return symbol[:-3] + "USDT"
    return symbol


def binance_candles(symbol: str, timeframe: str, limit: int) -> dict[str, Any]:
    interval = CRYPTO_INTERVALS.get(timeframe)
    if not interval:
        raise BridgeError(f"Unsupported timeframe: {timeframe}", 400)

    params = urllib.parse.urlencode({
        "symbol": binance_symbol(symbol),
        "interval": interval,
        "limit": min(limit, 1000),
    })

    hosts = (
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com",
    )
    last_error: BridgeError | None = None
    raw = None
    for host in hosts:
        try:
            raw = get_json(f"{host}/api/v3/klines?{params}", timeout=12)
            if isinstance(raw, list):
                break
        except BridgeError as exc:
            last_error = exc
            continue

    if not isinstance(raw, list):
        raise last_error or BridgeError("Binance returned no candle array", 502)

    candles = []
    for row in raw:
        if not isinstance(row, list) or len(row) < 6:
            continue
        try:
            candles.append({
                "time": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
            })
        except (TypeError, ValueError):
            continue

    if len(candles) < 20:
        raise BridgeError("Insufficient Binance candles", 502, len(candles))

    return {
        "ok": True,
        "provider": "BINANCE_SPOT_PUBLIC",
        "symbol": symbol,
        "timeframe": timeframe,
        "count": len(candles),
        "candles": candles,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def parse_twelve_time(value: str) -> int:
    value = value.strip()
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        dt = datetime.strptime(value, "%Y-%m-%d")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def twelve_candles(symbol: str, timeframe: str, limit: int) -> dict[str, Any]:
    if not TWELVE_KEY:
        raise BridgeError(
            "Non-crypto candles require an existing Twelve Data API key",
            503,
            "TWELVE_DATA_API_KEY_NOT_CONFIGURED",
        )

    interval = TWELVE_INTERVALS.get(timeframe)
    if not interval:
        raise BridgeError(f"Unsupported timeframe: {timeframe}", 400)

    provider_symbol = TWELVE_SYMBOLS.get(symbol, symbol)
    params = urllib.parse.urlencode({
        "symbol": provider_symbol,
        "interval": interval,
        "outputsize": min(limit, 5000),
        "apikey": TWELVE_KEY,
        "format": "JSON",
        "timezone": "UTC",
        "order": "ASC",
    })
    raw = get_json(f"https://api.twelvedata.com/time_series?{params}", timeout=18)

    if not isinstance(raw, dict):
        raise BridgeError("Twelve Data returned an invalid response", 502)
    if raw.get("status") == "error" or raw.get("code"):
        raise BridgeError(
            "Twelve Data rejected the request",
            502,
            raw.get("message") or raw.get("code"),
        )

    values = raw.get("values")
    if not isinstance(values, list):
        raise BridgeError("Twelve Data returned no values", 502)

    candles = []
    for row in values:
        if not isinstance(row, dict):
            continue
        try:
            candles.append({
                "time": parse_twelve_time(str(row["datetime"])),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row.get("volume") or 0),
            })
        except (KeyError, TypeError, ValueError):
            continue

    candles.sort(key=lambda item: item["time"])
    if len(candles) < 20:
        raise BridgeError("Insufficient Twelve Data candles", 502, len(candles))

    return {
        "ok": True,
        "provider": "TWELVE_DATA",
        "symbol": symbol,
        "provider_symbol": provider_symbol,
        "timeframe": timeframe,
        "count": len(candles),
        "candles": candles[-limit:],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def get_candles(symbol: str, timeframe: str, limit: int) -> dict[str, Any]:
    key = f"candles:{symbol}:{timeframe}:{limit}"
    cached = cache_get(key, 180)
    if cached is not None:
        return {**cached, "cached": True}

    if is_crypto(symbol):
        try:
            result = binance_candles(symbol, timeframe, limit)
        except BridgeError as binance_error:
            if TWELVE_KEY:
                result = twelve_candles(symbol, timeframe, limit)
                result["fallback_from"] = "BINANCE_SPOT_PUBLIC"
            else:
                raise binance_error
    else:
        result = twelve_candles(symbol, timeframe, limit)

    cache_put(key, result)
    return result


def news_query(symbol: str) -> str:
    if not symbol:
        return '(markets OR economy OR inflation OR "central bank" OR commodities)'
    for prefix, query in NEWS_QUERIES.items():
        if symbol.startswith(prefix):
            return query
    base = symbol.replace("USDT", "").replace("USD", "")
    return f'("{base}" OR markets OR economy)'


def normalize_news_date(value: Any) -> str:
    text = str(value or "").strip()
    if re.fullmatch(r"\d{14}", text):
        try:
            return datetime.strptime(text, "%Y%m%d%H%M%S").replace(
                tzinfo=timezone.utc
            ).isoformat()
        except ValueError:
            pass
    return text


def _news_cache_path(symbol: str) -> str:
    safe_symbol = re.sub(r"[^A-Z0-9_-]", "_", symbol or "MARKETS")
    return os.path.join(NEWS_CACHE_DIR, f"news_{safe_symbol}.json")


def _read_news_disk_cache(symbol: str, max_age: int) -> dict[str, Any] | None:
    path = _news_cache_path(symbol)
    try:
        stat = os.stat(path)
        age = time.time() - stat.st_mtime
        if age > max_age:
            return None
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
            return None
        payload["cache_age_seconds"] = round(max(0.0, age), 3)
        payload["cache_source"] = "disk"
        return payload
    except (FileNotFoundError, PermissionError, OSError, ValueError, TypeError):
        return None


def _write_news_disk_cache(symbol: str, payload: dict[str, Any]) -> None:
    try:
        os.makedirs(NEWS_CACHE_DIR, mode=0o750, exist_ok=True)
        target = _news_cache_path(symbol)
        temporary = f"{target}.tmp-{os.getpid()}-{threading.get_ident()}"
        with open(temporary, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    except (PermissionError, OSError, TypeError, ValueError):
        # Disk cache is a resilience layer; memory cache remains available.
        return


def _slice_news_result(
    payload: dict[str, Any],
    limit: int,
    **extra: Any,
) -> dict[str, Any]:
    items = payload.get("items")
    if not isinstance(items, list):
        items = []
    selected = items[:limit]
    return {
        **payload,
        **extra,
        "count": len(selected),
        "items": selected,
        "requested_limit": limit,
    }


def _news_profile(symbol: str) -> dict[str, Any]:
    normalized = (symbol or "MARKETS").upper()
    profiles = (
        (("BTC",), "crypto", 'Bitcoin OR "BTC price" OR cryptocurrency', "BTC",
         ("bitcoin", "btc", "crypto", "cryptocurrency", "blockchain", "binance", "coinbase")),
        (("ETH",), "crypto", 'Ethereum OR Ether OR "ETH price"', "ETH",
         ("ethereum", "ether", "eth", "crypto", "cryptocurrency", "blockchain")),
        (("SOL",), "crypto", 'Solana OR "SOL price" OR cryptocurrency', "SOL",
         ("solana", "sol", "crypto", "cryptocurrency", "blockchain")),
        (("BNB",), "crypto", 'BNB OR Binance OR cryptocurrency', "BNB",
         ("bnb", "binance", "crypto", "cryptocurrency")),
        (("XRP",), "crypto", 'XRP OR Ripple OR cryptocurrency', "XRP",
         ("xrp", "ripple", "crypto", "cryptocurrency")),
        (("ADA",), "crypto", 'Cardano OR ADA OR cryptocurrency', "ADA",
         ("cardano", "ada", "crypto", "cryptocurrency")),
        (("XAU",), "market", 'gold price OR bullion OR XAUUSD', None,
         ("gold", "bullion", "xau", "precious metal")),
        (("XAG",), "market", 'silver price OR XAGUSD OR precious metals', None,
         ("silver", "xag", "precious metal")),
        (("EUR",), "market", 'EURUSD OR euro dollar OR ECB', None,
         ("eurusd", "eur/usd", "euro", "ecb", "european central bank")),
        (("GBP",), "market", 'GBPUSD OR sterling dollar OR Bank of England', None,
         ("gbpusd", "gbp/usd", "sterling", "pound", "bank of england")),
        (("JPY",), "market", 'USDJPY OR Japanese yen OR Bank of Japan', None,
         ("usdjpy", "usd/jpy", "yen", "bank of japan")),
        (("USOIL", "WTI"), "market", 'WTI crude oil OR oil price OR OPEC', None,
         ("wti", "crude oil", "oil price", "opec")),
        (("UKOIL", "BRENT"), "market", 'Brent crude oil OR oil price OR OPEC', None,
         ("brent", "crude oil", "oil price", "opec")),
        (("SPX", "SP500"), "market", 'S&P 500 OR Wall Street stocks', None,
         ("s&p 500", "sp500", "spx", "wall street", "us stocks")),
        (("NDX", "NASDAQ"), "market", 'Nasdaq OR technology stocks OR Wall Street', None,
         ("nasdaq", "ndx", "technology stocks", "wall street")),
        (("DXY",), "market", 'US dollar index OR DXY OR Federal Reserve', None,
         ("dxy", "dollar index", "us dollar", "federal reserve", "fed")),
    )

    for prefixes, family, query, crypto_category, keywords in profiles:
        if normalized.startswith(prefixes):
            return {
                "family": family,
                "query": query,
                "crypto_category": crypto_category,
                "keywords": keywords,
            }

    base = normalized.replace("USDT", "").replace("USD", "")
    return {
        "family": "market",
        "query": f'"{base}" financial market OR economy',
        "crypto_category": None,
        "keywords": tuple(filter(None, (base.lower(), "market", "economy"))),
    }


def _news_text(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _normalize_rss_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return normalize_news_date(text)


def _news_is_relevant(item: dict[str, Any], keywords: tuple[str, ...]) -> bool:
    if not keywords:
        return True
    haystack = " ".join(
        str(item.get(field) or "")
        for field in ("title", "summary", "source", "category")
    ).lower()
    return any(keyword.lower() in haystack for keyword in keywords)


def _get_xml(url: str, timeout: int = 20) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.5",
            "User-Agent": "Mozilla/5.0 (compatible; NDSP-News/6.0; +https://ndsp.app)",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(4_000_000)
    except urllib.error.HTTPError as exc:
        body = exc.read(800).decode("utf-8", errors="replace")
        raise BridgeError(
            f"RSS upstream HTTP {exc.code}",
            502,
            body[:400],
        ) from exc
    except Exception as exc:
        raise BridgeError("RSS upstream connection failed", 502, str(exc)) from exc


def _fetch_cryptocompare_news(symbol: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    category = profile.get("crypto_category")
    if not category:
        return []

    params = urllib.parse.urlencode({
        "lang": "EN",
        "sortOrder": "latest",
        "categories": category,
        "extraParams": "NDSP",
    })
    raw = get_json(
        f"https://min-api.cryptocompare.com/data/v2/news/?{params}",
        timeout=20,
    )
    rows = raw.get("Data") if isinstance(raw, dict) else None
    if not isinstance(rows, list):
        return []

    items = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = _news_text(row.get("title"))
        url = str(row.get("url") or "").strip()
        if not title or not url:
            continue
        source_info = row.get("source_info")
        source = ""
        if isinstance(source_info, dict):
            source = _news_text(source_info.get("name"))
        source = source or _news_text(row.get("source"))
        published = row.get("published_on")
        try:
            published_iso = datetime.fromtimestamp(
                int(published),
                tz=timezone.utc,
            ).isoformat()
        except (TypeError, ValueError, OSError, OverflowError):
            published_iso = ""
        item = {
            "title": title,
            "summary": _news_text(row.get("body"))[:500],
            "url": url,
            "source": source,
            "country": "",
            "language": "English",
            "time": published_iso,
            "category": "أخبار الأصل",
            "symbol": symbol or "MARKETS",
            "provider": "CRYPTOCOMPARE_NEWS",
        }
        if _news_is_relevant(item, profile["keywords"]):
            items.append(item)
        if len(items) >= NEWS_FETCH_BATCH:
            break
    return items


def _fetch_google_news_rss(symbol: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    query = f'{profile["query"]} when:2d'
    params = urllib.parse.urlencode({
        "q": query,
        "hl": NEWS_GOOGLE_LANGUAGE,
        "gl": NEWS_GOOGLE_COUNTRY,
        "ceid": f"{NEWS_GOOGLE_COUNTRY}:en",
    })
    body = _get_xml(f"https://news.google.com/rss/search?{params}", timeout=22)
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise BridgeError("Google News RSS returned invalid XML", 502, str(exc)) from exc

    items = []
    for node in root.findall(".//item"):
        title = _news_text(node.findtext("title"))
        url = str(node.findtext("link") or "").strip()
        source_node = node.find("source")
        source = _news_text(source_node.text if source_node is not None else "")
        description = _news_text(node.findtext("description"))
        if not title or not url:
            continue
        item = {
            "title": title,
            "summary": description[:500] or source,
            "url": url,
            "source": source or "Google News",
            "country": "",
            "language": "English",
            "time": _normalize_rss_date(node.findtext("pubDate")),
            "category": "أخبار الأصل",
            "symbol": symbol or "MARKETS",
            "provider": "GOOGLE_NEWS_RSS",
        }
        if _news_is_relevant(item, profile["keywords"]):
            items.append(item)
        if len(items) >= NEWS_FETCH_BATCH:
            break
    return items


def _fetch_gdelt_news(symbol: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    global NEWS_LAST_UPSTREAM_AT

    params = urllib.parse.urlencode({
        "query": profile["query"],
        "mode": "artlist",
        "maxrecords": NEWS_FETCH_BATCH,
        "timespan": "2d",
        "sort": "datedesc",
        "format": "json",
    })

    wait_for = NEWS_MIN_UPSTREAM_INTERVAL - (time.time() - NEWS_LAST_UPSTREAM_AT)
    if wait_for > 0:
        time.sleep(wait_for)

    try:
        raw = get_json(
            f"https://api.gdeltproject.org/api/v2/doc/doc?{params}",
            timeout=25,
        )
    finally:
        NEWS_LAST_UPSTREAM_AT = time.time()

    if isinstance(raw, dict):
        rows = raw.get("articles") or raw.get("items") or raw.get("data") or []
    elif isinstance(raw, list):
        rows = raw
    else:
        rows = []

    items = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = _news_text(row.get("title") or row.get("name"))
        url = str(row.get("url") or row.get("external_url") or "").strip()
        if not title or not url:
            continue
        domain = _news_text(row.get("domain") or row.get("source"))
        country = _news_text(row.get("sourcecountry"))
        language = _news_text(row.get("language"))
        item = {
            "title": title,
            "summary": " · ".join(part for part in (domain, country, language) if part),
            "url": url,
            "source": domain,
            "country": country,
            "language": language,
            "time": normalize_news_date(
                row.get("seendate") or row.get("date_published") or row.get("date")
            ),
            "category": "أخبار الأصل",
            "symbol": symbol or "MARKETS",
            "provider": "GDELT_DOC_2_0",
        }
        if _news_is_relevant(item, profile["keywords"]):
            items.append(item)
        if len(items) >= NEWS_FETCH_BATCH:
            break
    return items


def _deduplicate_news(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    seen = set()
    for item in items:
        title_key = re.sub(r"\W+", " ", str(item.get("title") or "").lower()).strip()
        url_key = str(item.get("url") or "").strip().lower()
        key = title_key or url_key
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
    output.sort(key=lambda row: str(row.get("time") or ""), reverse=True)
    return output[:NEWS_FETCH_BATCH]


def _fetch_news_upstream(symbol: str) -> dict[str, Any]:
    profile = _news_profile(symbol)
    provider_errors: list[str] = []
    all_items: list[dict[str, Any]] = []
    provider_sources: list[str] = []

    providers = []
    if profile["family"] == "crypto":
        providers.append(("CRYPTOCOMPARE_NEWS", _fetch_cryptocompare_news))
    providers.append(("GOOGLE_NEWS_RSS", _fetch_google_news_rss))
    providers.append(("GDELT_DOC_2_0", _fetch_gdelt_news))

    for provider_name, provider_function in providers:
        try:
            rows = provider_function(symbol, profile)
            if rows:
                all_items.extend(rows)
                provider_sources.append(provider_name)
            if len(_deduplicate_news(all_items)) >= 20:
                break
        except BridgeError as exc:
            provider_errors.append(f"{provider_name}: {exc}")
        except Exception as exc:
            provider_errors.append(f"{provider_name}: {type(exc).__name__}: {exc}")

    items = _deduplicate_news(all_items)
    if not items:
        raise BridgeError(
            "All financial news providers are temporarily unavailable",
            502,
            provider_errors,
        )

    return {
        "ok": True,
        "provider": "MULTI_SOURCE_FINANCIAL_NEWS_V6",
        "provider_sources": provider_sources,
        "symbol": symbol or None,
        "count": len(items),
        "items": items,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "degraded": False,
        "relevance_filtered": True,
    }


def _valid_news_payload(payload: Any) -> bool:
    return (
        isinstance(payload, dict)
        and isinstance(payload.get("items"), list)
        and len(payload.get("items")) > 0
    )


def get_news(symbol: str, limit: int) -> dict[str, Any]:
    requested_limit = max(1, min(int(limit), 75))
    cache_symbol = symbol or "MARKETS"
    key = f"news:{cache_symbol}"
    failure_key = f"news-failure:{cache_symbol}"

    cached = cache_get(key, NEWS_CACHE_TTL)
    if _valid_news_payload(cached):
        return _slice_news_result(cached, requested_limit, cached=True)

    disk_fresh = _read_news_disk_cache(cache_symbol, NEWS_CACHE_TTL)
    if _valid_news_payload(disk_fresh):
        cache_put(key, disk_fresh)
        return _slice_news_result(disk_fresh, requested_limit, cached=True)

    recent_failure = cache_get(failure_key, NEWS_FAILURE_TTL)
    if isinstance(recent_failure, dict):
        return _slice_news_result(
            recent_failure,
            requested_limit,
            cached=True,
        )

    try:
        with NEWS_UPSTREAM_LOCK:
            cached = cache_get(key, NEWS_CACHE_TTL)
            if _valid_news_payload(cached):
                return _slice_news_result(cached, requested_limit, cached=True)

            disk_fresh = _read_news_disk_cache(cache_symbol, NEWS_CACHE_TTL)
            if _valid_news_payload(disk_fresh):
                cache_put(key, disk_fresh)
                return _slice_news_result(disk_fresh, requested_limit, cached=True)

            result = _fetch_news_upstream(symbol)
            if not _valid_news_payload(result):
                raise BridgeError("News providers returned no relevant articles", 502)
            cache_put(key, result)
            _write_news_disk_cache(cache_symbol, result)
            return _slice_news_result(result, requested_limit, cached=False)
    except BridgeError as exc:
        stale = _read_news_disk_cache(cache_symbol, NEWS_STALE_TTL)
        if _valid_news_payload(stale):
            stale_payload = {
                **stale,
                "stale": True,
                "degraded": True,
                "warning": str(exc),
                "upstream_details": exc.details,
            }
            cache_put(key, stale_payload)
            return _slice_news_result(
                stale_payload,
                requested_limit,
                cached=True,
            )

        degraded_result = {
            "ok": True,
            "provider": "MULTI_SOURCE_FINANCIAL_NEWS_V6",
            "provider_sources": [],
            "symbol": symbol or None,
            "count": 0,
            "items": [],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "degraded": True,
            "temporarily_unavailable": True,
            "retry_after_seconds": NEWS_FAILURE_TTL,
            "warning": str(exc),
            "upstream_details": exc.details,
            "relevance_filtered": True,
        }
        cache_put(failure_key, degraded_result)
        return _slice_news_result(
            degraded_result,
            requested_limit,
            cached=False,
        )


class Handler(BaseHTTPRequestHandler):
    server_version = "NDSPMarketBridge/2.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        print(
            json.dumps(
                {
                    "at": datetime.now(timezone.utc).isoformat(),
                    "remote": self.client_address[0],
                    "message": fmt % args,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )

    def send_json(self, status: int, payload: Any) -> None:
        body = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = urllib.parse.parse_qs(parsed.query)

        try:
            if path in {"/", "/health", "/api/market-data-bridge/health"}:
                self.send_json(200, {
                    "ok": True,
                    "service": "NDSP_MARKET_DATA_BRIDGE_V2",
                    "crypto_provider": "BINANCE_SPOT_PUBLIC",
                    "non_crypto_provider": "TWELVE_DATA" if TWELVE_KEY else "NOT_CONFIGURED",
                    "news_provider": "MULTI_SOURCE_FINANCIAL_NEWS_V6",
                    "news_provider_order": ["CRYPTOCOMPARE_NEWS", "GOOGLE_NEWS_RSS", "GDELT_DOC_2_0"],
                    "news_failure_ttl_seconds": NEWS_FAILURE_TTL,
                    "news_cache_ttl_seconds": NEWS_CACHE_TTL,
                    "news_stale_ttl_seconds": NEWS_STALE_TTL,
                    "news_min_upstream_interval_seconds": NEWS_MIN_UPSTREAM_INTERVAL,
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                })
                return

            candle_paths = {
                "/api/market/candles",
                "/api/market-data/candles",
                "/api/ohlcv",
                "/api/candles",
                "/api/market/ohlcv",
                "/api/technical/candles",
            }
            if path in candle_paths:
                symbol = clean_symbol((query.get("symbol") or [""])[0])
                timeframe = (query.get("timeframe") or ["weekly"])[0]
                limit = clean_limit((query.get("limit") or ["260"])[0])
                self.send_json(200, get_candles(symbol, timeframe, limit))
                return

            news_paths = {
                "/api/news",
                "/api/market/news",
                "/api/events",
                "/api/economic-calendar",
            }
            if path in news_paths:
                raw_symbol = (query.get("symbol") or [""])[0]
                symbol = clean_symbol(raw_symbol) if raw_symbol else ""
                limit = clean_news_limit((query.get("limit") or ["30"])[0])
                self.send_json(200, get_news(symbol, limit))
                return

            self.send_json(404, {
                "ok": False,
                "error": "NOT_FOUND",
                "path": path,
                "service": "NDSP_MARKET_DATA_BRIDGE_V2",
            })
        except BridgeError as exc:
            self.send_json(exc.status, {
                "ok": False,
                "error": str(exc),
                "details": exc.details,
                "path": path,
                "service": "NDSP_MARKET_DATA_BRIDGE_V2",
            })
        except Exception as exc:
            self.send_json(500, {
                "ok": False,
                "error": "INTERNAL_ERROR",
                "details": str(exc),
                "path": path,
                "service": "NDSP_MARKET_DATA_BRIDGE_V2",
            })


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(
        json.dumps(
            {
                "event": "startup",
                "host": HOST,
                "port": PORT,
                "twelve_data_configured": bool(TWELVE_KEY),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    server.serve_forever()
