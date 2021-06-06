import aiohttp_jinja2
from aiohttp import web
from app import announcement

@aiohttp_jinja2.template("main.html")
async def Main(request):
    chats = request.app['chats']
    if len(chats) == 1:
        return web.HTTPFound("/"+list(chats.values())[0]['alias_id'])
    return {
        "chats": list(chats.values()),
        "auth" : request.app["auth"],
        "announcement" : announcement
    }


async def wildcard(request):
    raise web.HTTPFound('/')