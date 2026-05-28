import os
import json
from typing import Any, Optional

try:
    import redis
except Exception:
    redis = None

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
_client = None

def client():
    global _client
    if _client is not None:
        return _client
    if redis is None:
        return None
    try:
        _client = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_timeout=2,
            socket_connect_timeout=2,
        )
        _client.ping()
        return _client
    except Exception:
        return None

def cache_get(key: str) -> Optional[Any]:
    r = client()
    if not r:
        return None
    try:
        raw = r.get(key)
        return json.loads(raw) if raw else None
    except Exception:
        return None

def cache_set(key: str, value: Any, ttl: int = 20) -> None:
    r = client()
    if not r:
        return
    try:
        r.setex(key, ttl, json.dumps(value))
    except Exception:
        return

def health():
    r = client()
    if not r:
        return {"enabled": False, "status": "unavailable", "backend": "redis"}
    try:
        pong = r.ping()
        return {
            "enabled": True,
            "status": "ok" if pong else "degraded",
            "backend": "redis",
            "ttl_strategy_seconds": 20,
        }
    except Exception:
        return {"enabled": False, "status": "error", "backend": "redis"}
