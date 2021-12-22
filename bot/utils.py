import csv
from sqlite3 import connect
from typing import List

from telegram import Update
from telegram.ext import CallbackContext

from config import USERS_WITH_ACCESS


def is_valid_user(func):

    def checker(update: Update, context: CallbackContext):
        if update.effective_user.id in USERS_WITH_ACCESS:
            return func(update, context)
        else:
            update.message.reply_html("Access denied.")
    
    return checker


def save_to_db(word: str, definition: str) -> None:
    with connect("bot-translator.db") as con:
        con.execute("insert into favorites values (?,?)", (word, definition))
        con.commit()


def get_list_of_favorites():
    con = connect("bot-translator.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    list_of_favorites = cur.execute("select word from favorites").fetchall()
    cur.close()

    return list_of_favorites


def convert_favorites_to_csv():
    con = connect("bot-translator.db")
    cur = con.cursor()
    for row in cur.execute("select * from favorites"):
        with open("favorites.csv", "a") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(row)


if __name__ == "__main__":
    convert_favorites_to_csv()