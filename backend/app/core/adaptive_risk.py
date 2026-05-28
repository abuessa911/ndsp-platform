from app.core.equity import get_equity

START = 1000

def get_risk():

    equity = get_equity()

    drawdown = (START - equity) / START

    if drawdown > 0.2:
        return 0  # توقف

    if drawdown > 0.1:
        return 0.005

    return 0.01
