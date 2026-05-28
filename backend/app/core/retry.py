import time

def retry_request(func, retries=3, delay=1):
    for i in range(retries):
        try:
            return func()
        except Exception:
            time.sleep(delay)
    return None
