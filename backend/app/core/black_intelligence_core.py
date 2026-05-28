from app.services.market_memory_engine import update_memory, detect_pattern
from app.services.trap_replay_engine import detect_trap_replay
from app.services.pressure_index_engine import pressure_index
from app.core.intelligence_score import compute_intelligence

def run_black_layer(data):

    update_memory(data)
    memory_pattern = detect_pattern(data)
    base = compute_intelligence(data)
    trap_replay = detect_trap_replay(data, memory_pattern)

    pressure = pressure_index(
        data,
        base["trap"],
        base["intent"],
        base["hidden"]
    )

    final_score = (
        base["intelligence_score"] * 0.5 +
        pressure["pressure_score"] * 0.3 +
        (memory_pattern["memory_matches"] * 2)
    )

    return {
        "base_intelligence": base,
        "memory": memory_pattern,
        "trap_replay": trap_replay,
        "pressure": pressure,
        "black_score": round(final_score, 2)
    }
