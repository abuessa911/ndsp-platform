from app.engines.tdl_cot_engine import calculate_cot_tdl


def run_tdl(symbol: str, data: dict, profile: dict):
    """
    FINAL ROUTER
    يضمن أن manual timing_model يتم استخدامه دائمًا
    """

    try:
        return calculate_cot_tdl(data)
    except Exception as e:
        return {
            "tdl_lm_score": 0,
            "tdl_s_score": 0,
            "dominant": "UNKNOWN",
            "error": str(e),
        }
