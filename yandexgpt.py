import os
import json

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
    prompt: str, prompt_genre: str, prompt_len: int
) -> str:
    """
    Генерация текста с помощью YandexGPT.

    prompt - указание данных, используемых в запросе.
    prompt_genre - ожидаемый жанр ответа на запрос.
    prompt_len - длина запроса.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_iam_token()}",
    }
    payload = json.dumps(
        {
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
                    "text": "Вид текста: пост в телеграмме."
                    "Тема: преимущества YandexGPT в копирайтинге.",
                },
            ],
        }
    )
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
    return data
