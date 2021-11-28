from config import USERS_WITH_ACCESS
from telegram import Update
from telegram.ext import CallbackContext


def is_valid_user(func):

    def checker(update: Update, context: CallbackContext):
        if update.effective_user.id in USERS_WITH_ACCESS:
            return func(update, context)
        else:
            update.message.reply_html("Access denied.")
    
    return checker

