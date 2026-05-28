REPLACEMENTS = {
    "buy": "bullish bias",
    "sell": "bearish bias",
    "entry": "interest zone",
    "stop loss": "invalidation level",
    "take profit": "target zone"
}

def enforce_language(text: str) -> str:
    if not text:
        return text

    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
        text = text.replace(k.capitalize(), v.capitalize())

    return text


def enforce_output_language(output: dict) -> dict:
    if not isinstance(output, dict):
        return output

    result = {}

    for k, v in output.items():
        if isinstance(v, str):
            result[k] = enforce_language(v)
        elif isinstance(v, dict):
            result[k] = enforce_output_language(v)
        else:
            result[k] = v

    return result
