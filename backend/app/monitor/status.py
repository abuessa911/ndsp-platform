import requests

try:
    r = requests.get("http://127.0.0.1:9002/ndsp?symbol=BTCUSDT", timeout=2)
    print("STATUS:", r.status_code)
    print(r.text)
except:
    print("❌ SYSTEM DOWN")
