from datetime import datetime, timedelta

LAST_EXECUTION_TIME = None
COOLDOWN_SECONDS = 60
MAX_TRADES_PER_CYCLE = 1


def is_cooldown_ok():
    global LAST_EXECUTION_TIME

    if LAST_EXECUTION_TIME is None:
        return True

    delta = datetime.utcnow() - LAST_EXECUTION_TIME
    return delta.total_seconds() > COOLDOWN_SECONDS


def update_execution_time():
    global LAST_EXECUTION_TIME
    LAST_EXECUTION_TIME = datetime.utcnow()


def filter_items(items):
    """
    Select best opportunity only
    """

    # remove no_bias
    valid = [i for i in items if i.get("intent") != "no_bias"]

    if not valid:
        return []

    # sort by urgency priority
    priority = {
        "aggressive": 3,
        "moderate": 2,
        "low": 1
    }

    valid.sort(key=lambda x: priority.get(x.get("urgency"), 0), reverse=True)

    return valid[:MAX_TRADES_PER_CYCLE]


def allow_execution(items):
    if not is_cooldown_ok():
        return []

    selected = filter_items(items)

    if selected:
        update_execution_time()

    return selected
