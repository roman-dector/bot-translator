import json
import requests
from typing import Optional

from loguru import logger as log
from pydantic import (
        BaseModel,
        Field,
    )
from config import (
    YANDEX_API_KEY,
)


class Translation(BaseModel):
    text: str


class YandexTr(BaseModel):
    part_of_speech: str = Field(alias="pos")
    translations: list[Translation] = Field(alias="tr")


def parse_yandex_dict_api(phrase: str) -> tuple[str, bool]:
    response = requests.get(
        "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="
        + f"{YANDEX_API_KEY}&lang=en-ru&text={phrase.lower()}"
    )

    if not response:
        return "", False

    definitions = json.loads(response.text)["def"]
    if not definitions:
        return "", False

    result = []

    for data in definitions:
        content = YandexTr.parse_obj(data)

        list_of_translations = [v.text for v in content.translations]

        result.append(
            f"<b>{content.part_of_speech}</b>: {list_of_translations}\n"
        )


    return "\n".join(result), True


class Definition(BaseModel):
    definition: str
    example: Optional[str]
    synonyms: Optional[list]
    antonyms: Optional[list]


class Meaning(BaseModel):
    part_of_speech: Optional[str] = Field(alias="partOfSpeech")
    definitions: list[Definition]


class Phonetic(BaseModel):
    text: Optional[str]
    audio: Optional[str]


class PhraseSemantic(BaseModel):
    word: str
    phonetics: Optional[list[Phonetic]]
    origin: Optional[str]
    meanings: list[Meaning]


def get_phrase_audio_prononciation(phrase: str) -> tuple[list, bool]:
    response = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{phrase.lower()}"
    )
    
    if not response:
            return [], False

    result = []

    for data in json.loads(response.text):
        content = PhraseSemantic.parse_obj(data)

        if content.phonetics:
            ph = content.phonetics
            if ph[0].audio:
                result.append((
                    content.word,
                    ph[0].text,
                    "".join(("https://www", ph[0].audio.removeprefix("//ssl"))),
                ))


    return result, True


def parse_free_dict_api(phrase: str) -> tuple[str, bool]:

    response = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{phrase.lower()}"
    )
    
    if not response:
            return "", False

    result = []

    for data in json.loads(response.text):
        content = PhraseSemantic.parse_obj(data)

        result.append(f"<b>Word:</b> {content.word}\n")

        if content.phonetics:
            if content.phonetics[0].text:
                result.append(
                    f"<b>Phonetic:</b> {content.phonetics[0].text}\n"
                )

        for meaning in content.meanings:
            if meaning.part_of_speech:
                result.append(
                    f"\n<b>Part of speech:</b> <i>{meaning.part_of_speech}</i>"
                )

            for definition in meaning.definitions:
                if definition.definition:
                    result.append(
                        f"\n<b>definition:</b> <i>{definition.definition}</i>\n"
                    )
                if definition.example:
                    result.append(
                        f"<b>example:</b> <i>{definition.example}</i>\n"
                    )
                if definition.synonyms:
                    result.append(
                        f"<b>synonyms:</b> <i>{definition.synonyms}</i>\n"
                    )
                if definition.antonyms:
                    result.append(
                        f"<b>antonyms:</b> <i>{definition.antonyms}</i>\n"
                    )

        result.append("---\n")


    return "\n".join(result), True


if __name__ == "__main__":
    while True:
        print("Word below")

        phrase = input()

        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{phrase.lower()}"
    )
        print(json.loads(response.text))

