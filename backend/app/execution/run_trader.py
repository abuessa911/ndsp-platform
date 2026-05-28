from app.execution.trader import run_trader
import time

while True:
    run_trader()
    time.sleep(30)
