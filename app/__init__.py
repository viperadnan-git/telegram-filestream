import sys
from os import environ

from dotenv import load_dotenv
from telethon.sync import TelegramClient
from cachetools import LRUCache

load_dotenv()

host = environ.get("HOST", "127.0.0.1")
port = int(environ.get("PORT", "8080"))
public_url = environ.get("PUBLIC_URL", f"http://{host}:{port}")

try:
    api_id = int(environ["API_ID"])
    api_hash = environ["API_HASH"]
except KeyError as err:
    print("Set Telegram API_ID and API_HASH variables.")
    sys.exit()


try:
    chat_id = int(environ["LOG_CHAT"])
except:
    print("Set LOG_CHAT variable to the chat id of log chat")
    sys.exit()

bot_token = environ.get("BOT_TOKEN", None)
cache = LRUCache(maxsize=1024)

if bot_token:
    client = TelegramClient("bot", api_id=api_id, api_hash=api_hash)
else:
    print("Set BOT_TOKEN variable")
    sys.exit()
