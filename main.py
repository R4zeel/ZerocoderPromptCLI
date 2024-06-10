import os
import sys
import json
import threading
from datetime import datetime, timedelta
from time import thread_time_ns

from gigachat import get_gigachat_response
from yandexgpt import get_yandexgpt_response
from geodata import get_coords, get_weather


def write_gigachat(name: str, genre: str, weather: str, length: int):
    with open("result_gigachat.txt", "a") as file:
        file.write(
            f"GigaChat: \n {
            get_gigachat_response(
                name,
                genre,
                weather,
                length,
            )} \n"
        )
        file.close()


def write_yandexgpt(name: str, genre: str, weather: str, length: int):
    with open("result_yandexgpt.txt", "a") as file:
        file.write(
            f"GigaChat: \n {
            get_yandexgpt_response(
                name,
                genre,
                weather,
                length,
            )} \n"
        )
        file.close()


def main():
    """
    Входная точка программы.

    На вход принимаются данные, введенные пользователем
    с последующим обращением к API текстогенерации.
    В целях демонстрации параллельного выполнения функций,
    запросы к GigaChat и YangexGPT были вынесены в отдельные потоки.
    """

    city_data = {
        "name": input("Enter city name: "),
        "genre": input("Enter genre: "),
        "length": input("Enter length: "),
    }
    now = datetime.now()
    coords = get_coords(city_data["name"])
    weather = get_weather(coords)
    gigachat_thread = threading.Thread(
        target=write_gigachat(
            city_data["name"],
            city_data["genre"],
            weather,
            int(city_data["length"]),
        )
    )
    yandexgpt_thread = threading.Thread(
        target=write_yandexgpt(
            city_data["name"],
            city_data["genre"],
            weather,
            int(city_data["length"]),
        )
    )
    gigachat_thread.start()
    yandexgpt_thread.start()

    gigachat_thread.join()
    yandexgpt_thread.join()


if __name__ == "__main__":
    main()
