import sys
from os import environ
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

host = environ.get("HOST", "127.0.0.1")
port = environ.get("PORT", "8080")
public_url = environ.get("PUBLIC_URL", f"http://{host}:{port}")

try:
    api_id = int(environ["API_ID"])
    api_hash = environ["API_HASH"]
except KeyError as err:
    print("Set Telegram API_ID and API_HASH variables.")
    sys.exit()

secret_key = environ.get('SECRET', api_hash)
bot_token = environ.get("BOT_TOKEN", None)

try:
    chat_id = int(environ["LOG_CHAT"])
except:
    print("Set LOG_CHAT variable to the chat id of log chat")
    sys.exit()

if bot_token:
    client = TelegramClient(":memory:", api_id=api_id, api_hash=api_hash)
else:
    print("Set BOT_TOKEN variable")
    sys.exit()