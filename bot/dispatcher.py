from loguru import logger as log

import telegram
from telegram.ext import (
            Dispatcher,
            Updater,
            CommandHandler,
            MessageHandler,
            Filters,
        )

from config import TELEGRAM_TOKEN
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

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    log.info(f"Polling of bot ---> {bot_link} <--- started!")

    updater.start_polling()
    updater.idle()


bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None))

