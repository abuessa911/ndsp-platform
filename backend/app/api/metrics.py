import json

FILE = "/home/nawaf511/empire-core-new/backend/data/dashboard.json"

def get_metrics():
    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {"status":"no_data"}
