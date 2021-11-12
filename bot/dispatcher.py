from loguru import logger as log

import telegram
from telegram.ext import (
            Dispatcher,
            Updater,
            CommandHandler,
            MessageHandler,
            Filters,
        )

from config import (
        TELEGRAM_TOKEN,
        WEBHOOK_URL,
        PORT
    )
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

    bot_info = telegram.Bot(f"{TELEGRAM_TOKEN}").get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    log.info(f"Bot ---> {bot_link} <--- started in webhook mode!")


    # NOTE
    """Changed in version 13.4: start_webhook() now always calls 
    telegram.Bot.set_webhook(), so pass webhook_url instead of calling 
    updater.bot.set_webhook(webhook_url) manually.""" 

    updater.start_webhook(
        listen="127.0.0.1",
        port=PORT,
        url_path=f"{TELEGRAM_TOKEN}",
        webhook_url=f"{WEBHOOK_URL}",
    )
    updater.idle()


bot = telegram.Bot(f"{TELEGRAM_TOKEN}")
dispatcher = setup_dispatcher(Dispatcher(bot, None))
