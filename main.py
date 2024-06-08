import os
import json
from uuid import uuid4

import requests
from dotenv import load_dotenv

import constants

load_dotenv()

rquid = str(uuid4())


def get_gigachat_token():
    """Получение токена для работы с API GigaChat."""

    access_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "authorization": f"Basic {constants.SBER_AUTH_KEY}",
        "RqUID": rquid,
    }
    access_data = {"scope": "GIGACHAT_API_PERS"}
    response = requests.request(
        "POST",
        constants.GIGACHAT_TOKEN_URL,
        headers=access_headers,
        data=access_data,
        verify=os.getenv("MINCIF_CERT"),
    )
    data = response.json()
    return data.get("access_token")


prompt_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {get_gigachat_token()}",
}

prompt_payload = json.dumps(
    {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Напиши Hello World на Python."}
        ],
        "max_tokens": 524,
    }
)


def get_gigachat_response(prompt):
    """Отправка запросов к API GigaChat."""

    response = requests.request(
        "POST",
        constants.GIGACHAT_PROMPT_URL,
        headers=prompt_headers,
        data=prompt_payload,
        verify=os.getenv("MINCIF_CERT"),
    )
    data = response.json()
    return data


def main():
    # city_data = {
    #     "name": input("Enter city name: "),
    #     "genre": input("Enter genre: "),
    # }
    print(get_gigachat_response("test"))


if __name__ == "__main__":
    main()
