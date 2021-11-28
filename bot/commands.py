from loguru import logger as log
from telegram import (
        Update,
        ForceReply,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
    )
from telegram.ext import CallbackContext

from dict_api import (
        parse_free_dict_api,
        parse_yandex_dict_api,
        get_phrase_audio_prononciation,
    )

from utils import is_valid_user


import tempfile
from pydub import AudioSegment
from urllib.request import urlopen


@is_valid_user
def send_phrase_audio_prononciation(
        update: Update, context: CallbackContext
    ) -> None:

    query = update.callback_query
    query.answer()

    phrase = query.message.text.split("\n", 1)[0][len("Word: "):]

    data, ok = get_phrase_audio_prononciation(phrase)

    if ok:
        for phrase, transcription, audio_link in data:

            audio_file = urlopen(audio_link).read()

            with tempfile.NamedTemporaryFile() as f:
                f.write(audio_file)
                query.message.reply_voice(
                    AudioSegment.from_mp3(f.name).export("translation.ogg", format="ogg"),
                    caption=" -- ".join((phrase, transcription)),
                )
    else:
        query.message.reply_html("Sorry, no audio found")


@is_valid_user
def start(update: Update, context: CallbackContext) -> None:
    """Send a greeting message when the command /start is issued."""

    user = update.effective_user
    update.message.reply_html(f"Hi, {user['username']}!")


@is_valid_user
def give_definition(update: Update, context: CallbackContext) -> None:
    phrase = update.message.text.strip()

    #log.debug(phrase)

    favorite = InlineKeyboardButton("⭐", callback_data="save_to_favorites")
    audio = InlineKeyboardButton("▶️", callback_data="get_audio")
    translate = InlineKeyboardButton("🇷🇺", callback_data="translate_phrase")

    definition, ok = parse_free_dict_api(phrase)

    if ok:
        update.message.reply_html(
            definition,
            reply_markup=InlineKeyboardMarkup([[
                favorite, audio, translate 
            ]]),
        )
    elif not ok:
        translation, ok = parse_yandex_dict_api(phrase)
        if ok:
            update.message.reply_html(
                "Sorry, no definition found,\nbut translation is available"
            )
            update.message.reply_html(
                translation,
                reply_markup=InlineKeyboardMarkup([[
                    favorite
                ]]),
            )
        else:
            update.message.reply_html(
                "Sorry, no result found"
            )



@is_valid_user
def give_translation(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    phrase = query.message.text.split("\n", 1)[0][len("Word: "):]

    translation, ok = parse_yandex_dict_api(phrase)

    if ok:
        query.message.reply_html(translation)
    else:
        query.message.reply_html("Sorry, no translation found")

