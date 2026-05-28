DISCLAIMER = (
    "This system provides decision support analysis only and does not constitute "
    "financial advice or execution instruction."
)

ARABIC_DISCLAIMER = (
    "هذا النظام يقدم تحليل لدعم القرار فقط ولا يعتبر توصية استثمارية أو أمر تنفيذ."
)

def inject_disclaimer(output: dict, include_arabic: bool = True) -> dict:
    if not isinstance(output, dict):
        return output

    output["note"] = DISCLAIMER

    if include_arabic:
        output["note_ar"] = ARABIC_DISCLAIMER

    return output
