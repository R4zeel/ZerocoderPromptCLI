import os
import sys
import json

from gigachat import get_gigachat_response
from yandexgpt import get_yandexgpt_response


def main():
    # city_data = {
    #     "name": input("Enter city name: "),
    #     "genre": input("Enter genre: "),
    # }
    print(get_gigachat_response("test", "horror", 200))


if __name__ == "__main__":
    main()
