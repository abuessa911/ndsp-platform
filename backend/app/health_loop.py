import time
import requests
import json

STATUS = "/home/nawaf511/empire-core-new/backend/runtime/system_status.json"

def update(status):
    try:
        with open(STATUS, "w") as f:
            json.dump(status, f)
    except:
        pass

while True:

    try:
        r = requests.get("http://127.0.0.1:9001/health", timeout=2)

        if r.status_code == 200:
            update({"status":"running","api":"ok","engine":"ok"})
        else:
            update({"status":"warning","api":"error"})

    except:
        update({"status":"error","api":"down"})

    time.sleep(10)
