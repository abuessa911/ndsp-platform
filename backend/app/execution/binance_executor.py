import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from app.config_trade import *

def sign(params):
    query = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"

def send_order(side, quantity):
    endpoint = "/fapi/v1/order"

    params = {
        "symbol": SYMBOL,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000)
    }

    query = sign(params)

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    url = BASE_URL + endpoint + "?" + query

    res = requests.post(url, headers=headers)
    return res.json()
