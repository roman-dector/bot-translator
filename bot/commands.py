import os
from sqlite3 import connect

from loguru import logger as log
from telegram import Update
from telegram.ext import CallbackContext

from utils import (
    is_valid_user,
    get_list_of_favorites,
    convert_favorites_to_csv,
)


@is_valid_user
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(f"Hi, {user['username']}!")


@is_valid_user
def give_list_of_favorites(update: Update, context: CallbackContext) -> None:
    list_of_favorites = get_list_of_favorites()

    if not list_of_favorites:
        update.message.reply_html("List of favorites is empty")
        return
    update.message.reply_html("\n".join(
        map(lambda word: f"<code>{word}</code>",list_of_favorites)
    ))


@is_valid_user
def import_favorites_in_csv(update: Update, context: CallbackContext):
    convert_favorites_to_csv()
    update.message.reply_document(open("favorites.csv", "rb"))
    os.remove("favorites.csv")


@is_valid_user
def drop_favorites(update: Update, context: CallbackContext):
    with connect("bot-translator.db") as con:
        con.execute("delete from favorites")
        con.commit()
    
    update.message.reply_html("List of favorites is empty")
