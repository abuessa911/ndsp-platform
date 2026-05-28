MAX_DAILY_LOSS = 0.05

def check_risk(account):

    if account.get("daily_loss", 0) >= MAX_DAILY_LOSS:
        return False, "daily_loss_limit"

    return True, "ok"
