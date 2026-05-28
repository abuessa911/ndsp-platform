from typing import Dict, Any


def get_package_policy(plan: str) -> Dict[str, Any]:

    normalized = str(plan or "").lower()

    if normalized == "saas":
        return {
            "plan": "SAAS",
            "markets": [
                "BTCUSDT",
                "ETHUSDT",
                "BNBUSDT",
                "SOLUSDT",
                "XRPUSDT",
                "ADAUSDT",
                "DOGEUSDT",
                "SHIBUSDT",
                "EURUSD",
                "GBPUSD",
                "USDJPY",
                "XAUUSD",
                "US100",
                "US500",
                "US30",
                "USOIL",
                "UKOIL",
            ],
            "max_alerts": 999,
            "api_access": True,
            "governance_access": True,
            "websocket_access": True,
            "runtime_level": "FULL_INFRASTRUCTURE",
        }

    if normalized == "elite":
        return {
            "plan": "ELITE",
            "markets": [
                "BTCUSDT",
                "ETHUSDT",
                "SOLUSDT",
                "XRPUSDT",
                "EURUSD",
                "GBPUSD",
                "USDJPY",
                "AUDUSD",
                "XAUUSD",
                "XAGUSD",
                "US100",
                "US500",
                "US30",
                "USOIL",
                "UKOIL",
            ],
            "max_alerts": 100,
            "api_access": True,
            "governance_access": True,
            "websocket_access": True,
            "runtime_level": "INSTITUTIONAL",
        }

    if normalized == "pro":
        return {
            "plan": "PRO",
            "markets": [
                "BTCUSDT",
                "ETHUSDT",
                "EURUSD",
                "GBPUSD",
            ],
            "max_alerts": 25,
            "api_access": False,
            "governance_access": False,
            "websocket_access": False,
            "runtime_level": "PROFESSIONAL",
        }

    return {
        "plan": "FREE",
        "markets": [
            "AUDUSD",
        ],
        "max_alerts": 5,
        "api_access": False,
        "governance_access": False,
        "websocket_access": False,
        "runtime_level": "PREVIEW",
    }
