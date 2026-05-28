import time
import requests

URL = "http://127.0.0.1:9001/decision?symbol=BTCUSDT"
HEADERS = {
    "x-api-key": "ndsp-dev-key-123"
}

def run():
    print("💀 SMART ALERTS STARTED")

    last = None

    while True:
        try:
            res = requests.get(URL, headers=HEADERS, timeout=8)

            print("STATUS:", res.status_code)
            print("RAW:", repr(res.text[:500]))

            if not res.text.strip():
                print("ERROR: empty response body")
                time.sleep(5)
                continue

            try:
                data = res.json()
            except Exception as json_err:
                print("ERROR: invalid json:", json_err)
                time.sleep(5)
                continue

            print("JSON:", data)

            decision = data.get("data", data)

            if decision != last:
                print("🔥 SIGNAL:", decision)
                last = decision

        except Exception as e:
            print("ERROR:", e)

        time.sleep(5)

if __name__ == "__main__":
    run()
