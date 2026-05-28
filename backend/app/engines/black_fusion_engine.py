from app.services.market_memory_engine import analyze_memory
from app.services.deception_engine import detect_deception
from app.services.pressure_index_engine import compute_pressure

def run_black_layer(data):
    memory = analyze_memory(data)
    deception = detect_deception(data)
    pressure = compute_pressure(data)

    return {
        "memory": memory,
        "deception": deception,
        "pressure": pressure
    }
