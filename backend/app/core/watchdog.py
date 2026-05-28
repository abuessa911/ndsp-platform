import requests
from app.core.auto_kill import trigger_kill

def check_system():

    try:
        r = requests.get("http://127.0.0.1:9001/health", timeout=2)
        if r.status_code != 200:
            trigger_kill("health_fail")
    except:
        trigger_kill("no_response")
