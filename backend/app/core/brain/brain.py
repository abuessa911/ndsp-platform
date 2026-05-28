from app.core.brain.registry import get_engines
from app.core.brain.loader import load_all

def run_brain(symbol):

    # 🔥 تحميل كل engines أول
    load_all()

    engines = get_engines()
    layers = {}

    for name, engine in engines.items():
        try:
            layers[name] = engine(symbol)
        except Exception as e:
            layers[name] = {
                "error": str(e),
                "fallback": True
            }

    return layers
