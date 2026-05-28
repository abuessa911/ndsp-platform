from app.core.performance import stats

MAX_LOSS = -50

def check():

    s = stats()

    if not s:
        return True

    if s.get("pnl",0) < MAX_LOSS:
        return False

    return True
