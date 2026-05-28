import smtplib, os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv("/home/nawaf511/empire-core-new/backend/.env")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

def send_api_key(to_email, api_key):
    msg = MIMEText(f"""
Welcome to NDSP 👑

Your API Key:
{api_key}

Use it to access the system.

🚀 Good luck
""")

    msg['Subject'] = "NDSP Access Key"
    msg['From'] = EMAIL
    msg['To'] = to_email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()
