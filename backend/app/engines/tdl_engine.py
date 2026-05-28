from app.services.base_engine import engine_output

def run(data, config):
    return engine_output(
        name="timing_model",
        state="bullish",
        score=80,
        confidence=0.8
    )
