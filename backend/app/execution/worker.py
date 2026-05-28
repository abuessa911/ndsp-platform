import time
from app.services.scanner import scan_market
from app.execution.interpreter import interpret_item
from app.execution.decision_explainer import generate_explanation

def run():

    while True:
        print("\n📡 Fetching market data...")
        data = scan_market()

        interpreted = [interpret_item(i) for i in data]

        results = []

        for raw, inter in zip(data, interpreted):
            explanation = generate_explanation(raw, inter)
            results.append(explanation)

        print("\n🧠 DECISION OUTPUT:")
        for r in results:
            print("\n---------------------------")
            print(r["explanation"])

        time.sleep(10)

if __name__ == "__main__":
    run()
