import os
from dotenv import load_dotenv


load_dotenv(".env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

