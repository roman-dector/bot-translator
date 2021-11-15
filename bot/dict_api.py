import json
import requests
from typing import Optional

from loguru import logger as log
from pydantic import (
        BaseModel,
        ValidationError,
        validator,
        Field,
    )
from pydantic.dataclasses import dataclass
from config import (
    OXFORD_APP_ID,
    OXFORD_APP_KEY,
    YANDEX_API_KEY,
)


# Use for translating from English to Russian

def parse_yandex_dict_api(phrase: str):
    return requests.get(
        "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="
        + f"{YANDEX_API_KEY}&lang=en-ru&text={phrase}"
    ).text


#def parse_oxford_dict_api(phrase: str):
#
#    response = requests.get(
#        url=f"https://od-api.oxforddictionaries.com:443/api/v2/entries/en/{phrase.lower()}",
#        headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY},
#    )
#
#    if not response:
#        return "Sorry, no result found"
#
#    data = response.text
#    
#    return data
#
#
#class Entry(BaseModel):
#    etymologies: list
#    notes: list
#    pronunciations: list
#    senses: list
#
#
#class LexicalEntry(BaseModel):
#    entries: list[Entry]
#    language: str
#    lexicalCategory: dict
#    phrases: list
#    text: str
#
#
#class Result(BaseModel):
#    id: str
#    language: str
#    lexicalEntries: list[LexicalEntry]
#    type: str
#    word: str
#
#
#class OxfordDefinition(BaseModel):
#    id: str
#    metadata: dict
#    results: list[Result]
#    word: str


def parse_free_dict_api(phrase: str) -> str:

    response = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{phrase.lower()}"
    )
    
    if not response:
        return "Sorry, no result found"


    data = json.loads(response.text)[0]
    result = []
    log.debug(data)


    try:
        result.append(f"<b>Phonetic</b>: {data['phonetic']}\n")
    except KeyError as key_err:
        log.info(f"Didn't find key {key_err}")

        
    for meaning in data["meanings"]:
        try:
            result.append(f"""\n\
<b>Part of speech</b>: \
<i>{meaning['partOfSpeech']}</i>"""
        )
        except KeyError as key_err:
            log.info(f"Didn't find key {key_err}")

        
        for definition in meaning["definitions"]:
            #log.debug(definition) 
            try:
                for k, v in definition.items():

                    match k, v:
                        case "definition", _:
                            result.append(f"\n<b>{k}</b>: <i>{v}</i>\n") 
                        case _, []:
                            pass
                        case _, "":
                            pass
                        case _:
                            result.append(f"<b>{k}</b>: <i>{v}</i>\n") 

            except ValueError as val_err:
                log.error(val_err)
            

    return "\n".join(result)


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
    #phonetic: Optional[str]  # Useless, the same in Phonetic.text
    phonetics: Optional[list[Phonetic]]
    origin: Optional[str]
    meanings: list[Meaning]


def parse_free_dict_api_v2(phrase: str) -> str:

    response = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{phrase.lower()}"
    )
    
    if not response:
        return "Sorry, no result found"

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


    return "\n".join(result)


if __name__ == "__main__":
    data = json.loads(requests.get(
        "https://api.dictionaryapi.dev/api/v2/entries/en/up"
    ).text)

    print(PhraseSemantic.parse_obj(data))

