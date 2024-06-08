import os

from dotenv import load_dotenv

load_dotenv()

GIGACHAT_TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_PROMPT_URL = (
    "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
)
SBER_AUTH_KEY = os.getenv("SBER_AUTH_KEY")
