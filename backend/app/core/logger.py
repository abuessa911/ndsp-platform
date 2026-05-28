import json
import time

LOG = "/home/nawaf511/empire-core-new/backend/logs/system.log"

def log(data):

    entry = {
        "time": time.time(),
        "data": data
    }

    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
