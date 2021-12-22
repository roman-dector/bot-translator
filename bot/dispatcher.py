from loguru import logger as log

import telegram
from telegram.ext import (
        Dispatcher,
        Updater,
        CommandHandler,
        MessageHandler,
        Filters,
        CallbackQueryHandler,
    )

from config import (
        TELEGRAM_TOKEN,
        WEBHOOK_URL,
        PORT
    )
from buttons import (
        give_definition,
        give_translation,
        send_phrase_audio_prononciation,
        save_to_favorites,
    )
from commands import (
        start,
        give_list_of_favorites,
        import_favorites_in_csv,
        drop_favorites,
    )


def setup_dispatcher(dp) -> Dispatcher:
    
    # commands
    dp.add_handler(CommandHandler("start", start)) 
    dp.add_handler(CommandHandler("favorites", give_list_of_favorites))
    dp.add_handler(CommandHandler("import_csv", import_favorites_in_csv))
    dp.add_handler(CommandHandler("drop_favorites", drop_favorites))

    # messages
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, give_definition
    )) 

    # callbacks
    dp.add_handler(CallbackQueryHandler(
        give_translation,
        pattern="translate_phrase",
    ))

    dp.add_handler(CallbackQueryHandler(
        send_phrase_audio_prononciation,
        pattern="get_audio",
    ))

    dp.add_handler(CallbackQueryHandler(
        save_to_favorites,
        pattern="save_to_favorites",
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
