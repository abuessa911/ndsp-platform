import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_ADMIN_TO = os.getenv("SMTP_ADMIN_TO", SMTP_USER)

def _send(to_email: str, subject: str, body: str):

    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP CONFIG MISSING")
        return False

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, to_email, msg.as_string())
        server.quit()

        print(f"MAIL SENT => {to_email}")
        return True

    except Exception as e:
        print(f"MAIL ERROR => {e}")
        return False

def send_trial_token(user_email: str, token: str):

    body = f"""
Welcome to NDSP Elite Trial.

Your activation token:

{token}

NDSP
"""

    return _send(
        user_email,
        "NDSP Elite Trial Token",
        body
    )

def notify_admin(user_email: str):

    body = f"""
New NDSP Elite Registration

User Email:
{user_email}
"""

    return _send(
        SMTP_ADMIN_TO,
        "NDSP New Registration",
        body
    )
