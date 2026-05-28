import os
import requests
import smtplib
from email.mime.text import MIMEText

# ================================
# 📡 TELEGRAM
# ================================
def send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_ids = os.getenv("TELEGRAM_CHAT_ID", "").split(",")

    if not token or not chat_ids:
        return {"telegram": "not_configured"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    results = []
    for chat_id in chat_ids:
        try:
            res = requests.post(url, json={
                "chat_id": chat_id.strip(),
                "text": message
            })
            results.append(res.json())
        except Exception as e:
            results.append(str(e))

    return {"telegram": results}


# ================================
# 📧 EMAIL
# ================================
def send_email(subject: str, message: str):
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not user or not password:
        return {"email": "not_configured"}

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = user
        msg["To"] = user

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(user, password)
            server.send_message(msg)

        return {"email": "sent"}

    except Exception as e:
        return {"email_error": str(e)}


# ================================
# 🧠 UNIFIED NOTIFICATION
# ================================
def notify_all(message: str):
    tg = send_telegram(message)
    em = send_email("NDSP Alert", message)

    return {
        "telegram": tg,
        "email": em
    }
