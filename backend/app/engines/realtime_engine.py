import json
import threading
import websocket

########################################
# 💀 GLOBAL CACHE
########################################

price_cache = {}

########################################
# 💀 STREAM HANDLER
########################################

def on_message(ws, message):
    try:
        data = json.loads(message)
        symbol = data.get("s")
        price = float(data.get("c"))

        if symbol:
            price_cache[symbol] = price

    except Exception as e:
        print("[WS ERROR]", e)

def on_error(ws, error):
    print("[WS ERROR]", error)

def on_close(ws, close_status_code, close_msg):
    print("[WS CLOSED]")

def on_open(ws):
    print("🔥 WS CONNECTED")

########################################
# 💀 START STREAM
########################################

def start_price_stream(symbol="btcusdt"):

    socket = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"

    ws = websocket.WebSocketApp(
        socket,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open
    ws.run_forever()

########################################
# 💀 BACKGROUND THREAD
########################################

def run_stream(symbol="BTCUSDT"):
    thread = threading.Thread(
        target=start_price_stream,
        args=(symbol,),
        daemon=True
    )
    thread.start()

########################################
# 💀 GET PRICE (FAST)
########################################

def get_realtime_price(symbol):
    return price_cache.get(symbol, 0.0)
