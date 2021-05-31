import aiohttp_jinja2
from app import client
from aiohttp import web
from app.utils import parseInt
from app.telegram import get_message


async def check_file(req):
    chat_id = await parseInt(req.match_info.get("chat", None))
    try:
        message_id = int(req.match_info.get("id", None))
    except ValueError as err:
        return web.Response(status=400, text="400: Bad Request! Invalid Url provided enter a valid Telegram Link")

    try:
        message = await client.get_messages(entity=chat_id, ids=message_id)
    except Exception as err:
        message = None
    
    if not message or not message.file:
        print(f"No check result for {message_id} in {chat_id}")
        return web.Response(status=404, text="404: File Not Found! Telegram File not found, make sure its publically available.")
    return web.Response(status=200, text="https" if req.secure else "http" + f"://{req.host}/{chat_id}/{message_id}")

@aiohttp_jinja2.template("preview.html")
async def index_message(req):
    chat_id = await parseInt(req.match_info["chat"])
    try:
        message_id = int(req.match_info["id"])
    except Exception as err:
        return web.HTTPFound("/" + chat_id)
    
    message = await get_message(chat_id, message_id)
    if message:
        return message
    else:
        return web.HTTPFound("/" + chat_id)