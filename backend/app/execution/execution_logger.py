import json
import os
import threading

LOG_FILE = "/home/nawaf511/empire-core-new/backend/logs/execution_learning.json"
lock = threading.Lock()


class ExecutionLogger:

    def log(self, data):

        with lock:

            if not os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w") as f:
                    json.dump([], f)

            try:
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
            except:
                logs = []

            logs.append(data)

            with open(LOG_FILE, "w") as f:
                json.dump(logs, f, indent=2)
