import sys
from os import environ
from json import loads as json_load, JSONDecodeError
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

host = environ.get("HOST", "127.0.0.1")
port = environ.get("PORT", "8080")

try:
    api_id = int(environ["TELEGRAM_API"])
    api_hash = environ["TELEGRAM_HASH"]
except KeyError as err:
    print("Set TELEGRAM_API and TELEGRAM_HASH variables.")
    sys.exit()

try:
    tg_settings = json_load(environ.get("TELEGRAM_SETTINGS"))
    if not len(tg_settings.keys()) == 6:
        print("TELEGRAM_SETTINGS have some missing keys. Add all of them before running.")
        sys.exit()
except (JSONDecodeError, TypeError):
    print("Set TELEGRAM_SETTINGS Variable to a valid JSON Format.")
    sys.exit()

results_per_page = environ.get("RESULTS_PER_PAGE", 20)
tg_session = environ.get("TELEGRAM_SESSION", None)
bot_token = environ.get("BOT_TOKEN", None)
secret_key = environ.get("SECRET", api_hash).encode('utf-8')

if tg_session:
    client = TelegramClient(StringSession(tg_session), api_id=api_id, api_hash=api_hash).start()
elif bot_token:
    client = TelegramClient(":memory:", api_id=api_id, api_hash=api_hash).start(bot_token=bot_token)
else:
    print("Set either TG_SESSION or BOT_TOKEN variable")
    sys.exit()
client.parse_mode = "html"

authorization = environ.get("AUTH", None)
if authorization:
    try:
        authorization = json_load(authorization)
        if len(authorization.items()) == 1:
            authorization = {"_":list(authorization.values())[0]}
    except:
        authorization = {"_":authorization}

announcement = environ.get("ANNOUNCEMENT", None)