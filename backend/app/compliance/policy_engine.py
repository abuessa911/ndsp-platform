from .sanitizer import sanitize_output
from .language_guard import enforce_output_language
from .disclaimer import inject_disclaimer

def enforce_compliance(output: dict) -> dict:
    if not isinstance(output, dict):
        return output

    # 1. sanitize forbidden content
    output = sanitize_output(output)

    # 2. enforce institutional language
    output = enforce_output_language(output)

    # 3. inject disclaimer
    output = inject_disclaimer(output)

    return output
