import os
from dotenv import load_dotenv


load_dotenv(".env")

DEBUG = os.getenv("DEBUG")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
IP = os.getenv("IP")
