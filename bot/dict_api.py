import json
import requests

from loguru import logger as log


def get_phrase_definition(phrase: str, url: str) -> requests.models.Response:
    return requests.get(url + phrase)


def get_dict_definition(phrase: str) -> str:

    response = get_phrase_definition(
        phrase=phrase,
        url="https://api.dictionaryapi.dev/api/v2/entries/en/"
    )
    
    if not response:
        return "Sorry, no result found"

    data = json.loads(response.text)[0]
    result = []
    # log.debug(data)


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


if __name__ == "__main__":
    while True:
        print("Text the phrase below:")
        phrase = input()

        print(get_dict_definition(phrase))

