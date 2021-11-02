import json
import requests

from loguru import logger as log


def get_dict_definition(phrase: str) -> str:

    api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    response = requests.get(api_url + phrase)
    
    if response:
        data = json.loads(response.text)[0]

        result = []

        result.append(f"<b>Phonetic</b>: {data['phonetic']}\n")

        #log.debug(data)
        
        meanings = data["meanings"]

        for meaning in meanings:
            result.append(f"""\
<b>Part of speech</b>: \
<i>{meaning['partOfSpeech']}</i>\n"""
            )
            
            for definition in meaning["definitions"]:

                #log.debug(definition) 
                try:
                    for k, v in definition.items():

                        if k == "antonyms":
                            result.append(f"<b>{k}</b>: <i>{v}</i>\n\n") 
                        else:
                            result.append(f"<b>{k}</b>: <i>{v}</i>")

                except ValueError as val_err:
                    log.error(val_err)

                
        return "\n".join(result)

    else:
        return "Sorry, no result found"


if __name__ == "__main__":
    while True:
        print("Text the phrase below:")
        phrase = input()

        print(get_dict_definition(phrase))

