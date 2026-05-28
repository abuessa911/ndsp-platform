#!/usr/bin/env python3
import json


def get_grade(score: float) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"


if __name__ == "__main__":
    score = 88.5
    print(json.dumps({"score": score, "grade": get_grade(score)}, indent=2))
