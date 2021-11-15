import os
from dotenv import load_dotenv


load_dotenv(".env")

DEBUG = os.getenv("DEBUG", "True")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = os.getenv("PORT", 5000)

OXFORD_APP_ID = os.getenv("OXFORD_APP_ID")
OXFORD_APP_KEY = os.getenv("OXFORD_APP_KEY")

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")

