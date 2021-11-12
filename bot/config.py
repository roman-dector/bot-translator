import os
from dotenv import load_dotenv


load_dotenv(".env")

DEBUG = os.getenv("DEBUG", "True")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = os.getenv("PORT", 5000)
