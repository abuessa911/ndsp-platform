# /home/nawaf511/empire-core-new/backend/app/integrations/telegram/channels.py

import os
from dotenv import load_dotenv

load_dotenv("/home/nawaf511/empire-core-new/backend/.env")

CHANNELS = {
    "free": os.getenv("TELEGRAM_FREE_CHANNEL"),
    "pro": os.getenv("TELEGRAM_PRO_CHANNEL"),
    "vip": os.getenv("TELEGRAM_VIP_CHANNEL"),
}
