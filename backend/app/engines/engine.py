import time

from app.core.governed_pipeline import run_governed
from app.services.price_feed import get_price
from app.core.tracking_engine import evaluate_performance

SYMBOLS = ["BTCUSDT"]

def run():

    while True:

        try:
            evaluate_performance(get_price)
        except:
            pass

        for s in SYMBOLS:
            data = run_governed(s)
            print("RUN:", data["decision"])

        time.sleep(60)

if __name__ == "__main__":
    run()
