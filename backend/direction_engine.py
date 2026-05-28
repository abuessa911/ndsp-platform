#!/usr/bin/env python3
import json
from typing import Tuple


def calculate_direction(controller: str, lm_dir: str, s_dir: str) -> Tuple[str, str]:
    if controller == "L&M":
        return lm_dir, "Weekly_LM"

    return s_dir, "Weekly_S"


if __name__ == "__main__":
    res_dir, res_source = calculate_direction("L&M", "bullish", "bearish")
    print(json.dumps({"direction": res_dir, "source": res_source}, indent=2))
