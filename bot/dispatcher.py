from loguru import logger as log

import telegram
from telegram.ext import (
            Dispatcher,
            Updater,
            CommandHandler,
            MessageHandler,
            Filters,
        )

from config import TELEGRAM_TOKEN, WEBHOOK_URL, IP
from commands import (
            start,
            give_definition,
        )


def setup_dispatcher(dp) -> Dispatcher:
    
    dp.add_handler(CommandHandler("start", start)) 
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, give_definition
    )) 

    return dp


def run_polling() -> None:

    updater = Updater(TELEGRAM_TOKEN)
    setup_dispatcher(updater.dispatcher)

    bot_info = telegram.Bot(f"{TELEGRAM_TOKEN}").get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    log.info(f"Polling of bot ---> {bot_link} <--- started!")

    updater.start_polling()
    updater.idle()


def run_webhook() -> None:

    updater = Updater(TELEGRAM_TOKEN)
    setup_dispatcher(updater.dispatcher)

    updater.bot.setWebhook(
        url=WEBHOOK_URL,
        certificate="cert.pem",
    )

    updater.start_webhook(
        listen=f"{IP}",
        port=8443,
        url_path=f"{TELEGRAM_TOKEN}",
        key="private.key",
        cert="cert.pem",
    )

    updater.idle()


bot = telegram.Bot(f"{TELEGRAM_TOKEN}")
bot.setWebhook(f"{WEBHOOK_URL}")
dispatcher = setup_dispatcher(Dispatcher(bot, None))
