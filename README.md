# Тестовое задание для Zerocoder.

## Описание
Проект представляет собой интерфейс командной строки, позволяющий пользователю указать город, жанр, и длину текста.
По заданным параметрам будут сформированы запросы к API сервисов GigaChat и YandexGPT. Результаты запросов будут 
записаны в текстовый файл, а в консоль выведена информация о длительности запроса.

## Установка и требования к запуску
- Склонируйте репозиторий на локальную машину `git clone git@github.com:R4zeel/ZerocoderPromptCLI.git`
- Создайте виртуальное окружение `python3 -m venv venv`
- Установите зависимости `pip install -r requirements.txt`
- Запуск программы осуществляется командой `python main.py`

Программа использует переменные окружения, содержащие в себе ключи доступа к выбранным API.
Для работы программы, вам необходимо создать `.env` файл со следующими переменными:

```
SBER_CLIENT_KEY={Токен GigaChat}
SBER_AUTH_KEY={Ключ авторизации GigaChat}
MINCIF_CERT={Путь к сертификату минфицры}
YANDEX_OAUTH={OAuth токен Яндекс}
YANDEX_CATALOGUE_ID={ID каталога Yandex Foundation Models}
GEO_KEY={Токен 2GIS}
WEATHER_KEY={Токен WeatherAPI}
```
Руководства по получению необходимых ключей можно найти по ссылкам:

- YandexGPT - https://yandex.cloud/ru/docs/iam/operations/iam-token/create
(прим. Необходим только OAuth-токен, IAM-токен получается на уровне программы.)
- GigaChat - https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart
- Сертификат минцифры - GigaChat использует их в своих сервисах. Во избежание ошибок, сертификат необходимо
скачать с сайта госуслуг (указано в руководстве к GigaChat по ссылке выше) и указать путь к этому сертификату.
- 2GIS - https://docs.2gis.com/ru/api/search/geocoder/overview
- WeatherAPI - https://www.weatherapi.com/docs/
