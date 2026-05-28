from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data" / "market_positioning" / "cot_snapshot.json"

def load_real_cot(symbol: str):
    try:
        data = json.loads(DATA.read_text())
    except Exception:
        return {}

    return data.get(symbol.upper(), {})
