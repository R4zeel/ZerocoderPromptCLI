import os
import sys
import json
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

YANDEX_TOKEN_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
CATALOGUE_ID = os.getenv("YANDEX_CATALOGUE_ID")
YANDEX_PROMPT_URL = (
    "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
)


def get_iam_token():
    """Получение IAM токена для работы с YandexGPT."""

    headers = {
        "Content-Type": "application/json",
    }
    payload = json.dumps(
        {"yandexPassportOauthToken": f"{os.getenv('YANDEX_OAUTH')}"}
    )
    try:
        response = requests.post(
            YANDEX_TOKEN_URL, headers=headers, data=payload
        )
    except requests.exceptions.ConnectionError as error:
        raise error
    data = response.json()
    return data.get("iamToken")


def get_yandexgpt_response(
    prompt_city: str,
    prompt_genre: str,
    weather: str,
    prompt_len: int,
) -> str:
    """
    Генерация текста с помощью YandexGPT.

    prompt - указание данных, используемых в запросе.
    prompt_genre - ожидаемый жанр ответа на запрос.
    weather - температура в градусах по цельсию.
    prompt_len - длина запроса.
    """

    timestamp = datetime.now()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_iam_token()}",
    }
    payload = {
        "modelUri": f"gpt://{CATALOGUE_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": prompt_len,
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — рассказчик.",
            },
            {
                "role": "user",
                "text": f"Напиши сказку про погоду на завтра в городе "
                f"{prompt_city} в жанре {prompt_genre}. Погода на завтра "
                f"будет составлять - {weather} градусов. Если название "
                f"города на английском - переведи его на русский. "
                f"Длина сказки не должна превышать {prompt_len} символов.",
            },
        ],
    }
    try:
        response = requests.post(
            YANDEX_PROMPT_URL,
            headers=headers,
            data=json.dumps(payload),
            verify=False,
        )
    except requests.exceptions.ConnectionError as error:
        raise error
    data = response.json()
    sys.stdout.write(
        f"YandexGPT execution time: {datetime.now() - timestamp} \n"
        f"File name: result_yandexgpt.txt \n"
    )
    return data.get("result").get("alternatives")[0].get("message").get("text")
