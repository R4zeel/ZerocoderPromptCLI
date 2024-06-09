import json
import os
import datetime

from dotenv import load_dotenv
import requests

load_dotenv()

GEOCODE_URL = "https://catalog.api.2gis.com/3.0/items/geocode"
WEATHER_URL = "http://api.weatherapi.com/v1/forecast.json"


def get_coords(city: str) -> str:
    """
    Получение координатов по заданному названию города.

    Формат возвращаемого значения определяется требованием
    API сервиса прогноза погоды.
    """

    payload = {
        "q": city,
        "key": os.getenv("GEO_KEY"),
        "fields": "items.point",
    }
    try:
        response = requests.get(GEOCODE_URL, params=payload)
    except requests.exceptions.ConnectionError as error:
        raise error
    data = response.json()
    coords = data.get("result").get("items")[0].get("point")
    return f"{coords['lat']},{coords['lon']}"


def get_weather(coords: str) -> str:
    """
    Получение температуры по заданным координатам.

    Из ответа API используется средняя дневная температура,
    для получения максимальной или минимальной температуры за день
    необходимо заменить ключ словаря 'avgtemp_c' на 'maxtemp_c'
    или 'mintemp_c' соответственно.
    """

    headers = {"Content-Type": "application/json"}
    payload = {"key": os.getenv("WEATHER_KEY"), "q": coords, "days": 2}
    try:
        response = requests.get(WEATHER_URL, headers=headers, params=payload)
    except requests.exceptions.ConnectionError as error:
        raise error
    data = response.json()
    return (
        data.get("forecast").get("forecastday")[1].get("day").get("avgtemp_c")
    )
