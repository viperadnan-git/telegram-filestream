import sys
from os import environ

from cachetools import LRUCache
from dotenv import load_dotenv
from telethon.sync import TelegramClient

from .utils import convert_to_seconds

load_dotenv()

host = environ.get("HOST", "127.0.0.1")
port = int(environ.get("PORT", "8080"))
public_url = environ.get("PUBLIC_URL", f"http://{host}:{port}")

try:
    api_id = int(environ["API_ID"])
    api_hash = environ["API_HASH"]
except KeyError as err:
    api_id = 908029
    api_hash = "c976491e6a6ec68bfbd8ec55bd7aeac8"
    print(
        "API_ID and API_HASH not found in environment variables. Using default values"
    )

try:
    chat_id = int(environ["LOG_CHAT"])
except:
    print("Set LOG_CHAT variable to the chat id of log chat")
    sys.exit()

bot_token = environ.get("BOT_TOKEN", None)
expiry = convert_to_seconds(environ.get("EXPIRY", "8h"))
cache = LRUCache(maxsize=int(environ.get("CACHE_SIZE", 1000)))

if bot_token:
    client = TelegramClient("bot", api_id=api_id, api_hash=api_hash)
else:
    print("Set BOT_TOKEN variable")
    sys.exit()
