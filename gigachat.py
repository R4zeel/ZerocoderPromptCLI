import os
import json
from datetime import datetime
import sys

import requests
from uuid import uuid4
from dotenv import load_dotenv


load_dotenv()

GIGACHAT_TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_PROMPT_URL = (
    "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
)
SBER_AUTH_KEY = os.getenv("SBER_AUTH_KEY")

rquid = str(uuid4())


def get_gigachat_token() -> str:
    """
    Получение токена для работы с API GigaChat.

    При отсутствии сертификата Минцифры необходимо
    поменять значение параметра verify на False.
    """

    access_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "authorization": f"Basic {SBER_AUTH_KEY}",
        "RqUID": rquid,
    }
    access_data = {"scope": "GIGACHAT_API_PERS"}
    try:
        response = requests.post(
            GIGACHAT_TOKEN_URL,
            headers=access_headers,
            data=access_data,
            verify=os.getenv("MINCIF_CERT"),
        )
    except requests.exceptions.ConnectionError as error:
        raise error
    data = response.json()
    return data.get("access_token")


def get_gigachat_response(
    prompt_city: str, prompt_genre: str, weather: str, prompt_len: int
) -> str:
    """
    Отправка запросов к API GigaChat.

    prompt - указание данных, используемых в запросе.
    prompt_genre - ожидаемый жанр ответа на запрос.
    weather - температура в градусах по цельсию.
    prompt_len - длина запроса.
    """

    timestamp = datetime.now()
    prompt_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {get_gigachat_token()}",
    }

    prompt_payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Напиши сказку про погоду на завтра в "
                    f"городе {prompt_city}"
                    f"в жанре {prompt_genre}. Погода будет составлять "
                    f"{weather} градусов. Длина сказки не должна "
                    f"превышать {prompt_len} символов.",
                }
            ],
            "max_tokens": prompt_len,
        }
    )
    try:
        response = requests.post(
            GIGACHAT_PROMPT_URL,
            headers=prompt_headers,
            data=prompt_payload,
            verify=os.getenv("MINCIF_CERT"),
        )
    except requests.exceptions.ConnectionError as error:
        raise error
    data = response.json()
    sys.stdout.write(
        f"GigaChat execution time: {datetime.now() - timestamp} \n"
        f"File name: result_gigachat.txt \n"
    )
    return data.get("choices")[0].get("message").get("content")
