import json
import os

DATA_FILE = "/home/nawaf511/empire-core-new/backend/data/prices.json"

def get_price(symbol):
    if not os.path.exists(DATA_FILE):
        return 0

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data.get(symbol, 0)
    except:
        return 0
