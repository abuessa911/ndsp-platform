def should_pause(data):

    momentum = data.get("states",{}).get("momentum",{})

    if momentum.get("signal") == "neutral":
        return True

    return False
