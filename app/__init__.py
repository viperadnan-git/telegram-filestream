import sys
from os import environ
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

host = environ.get("HOST", "127.0.0.1")
port = environ.get("PORT", "8080")

try:
    api_id = int(environ["API_ID"])
    api_hash = environ["API_HASH"]
except KeyError as err:
    print("Set Telegram API_ID and API_HASH variables.")
    sys.exit()

recommendations = list(set(x for x in environ.get("RECOMMENDATIONS", "").split()))
results_per_page = environ.get("RESULTS_PER_PAGE", 20)
tg_session = environ.get("TG_SESSION", None)
bot_token = environ.get("BOT_TOKEN", None)

if tg_session:
    client = TelegramClient(StringSession(tg_session), api_id=api_id, api_hash=api_hash).start()
elif bot_token:
    client = TelegramClient(":memory:", api_id=api_id, api_hash=api_hash).start(bot_token=bot_token)
else:
    print("Set either TG_SESSION or BOT_TOKEN variable")
    sys.exit()
client.parse_mode = "html"