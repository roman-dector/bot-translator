from loguru import logger as log
from telegram import Update, ForceReply
from telegram.ext import CallbackContext

from dict_api import parse_free_dict_api_v2


def start(update: Update, context: CallbackContext) -> None:
    """Send a greeting message when the command /start is issued."""

    user = update.effective_user
    update.message.reply_html(f"Hi, {user['username']}!")


def give_definition(update: Update, context: CallbackContext) -> None:
    phrase = update.message.text.strip()

    #log.debug(phrase)

    update.message.reply_html(
                parse_free_dict_api_v2(phrase),
            )

