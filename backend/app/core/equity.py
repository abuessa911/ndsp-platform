import json

FILE = "/home/nawaf511/empire-core-new/backend/data/paper_portfolio.json"

def get_equity():

    try:
        with open(FILE) as f:
            data = json.load(f)
            return data.get("balance",1000)
    except:
        return 1000
