import aiohttp_jinja2
from app import client
from aiohttp import web
from app.helper.utils import parseChat
from app.helper.telegram import get_message


@aiohttp_jinja2.template("preview.html")
async def IndexMessage(request):
    try:
        chat = await parseChat(request)
    except:
        return web.HTTPFound("/")

    try:
        message_id = int(request.match_info["id"])
    except Exception as err:
        return web.HTTPFound("/" + chat['alias_id'])
    
    try:
        return await get_message(chat, message_id)
    except Exception as err:
        return web.HTTPFound("/" + chat['alias_id'])