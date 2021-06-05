import aiohttp_jinja2
from aiohttp import web
from app import announcement

@aiohttp_jinja2.template("main.html")
async def Main(request):
    return {
        "chats": list(request.app["chats"].values()),
        "auth" : request.app["auth"],
        "announcement" : announcement
    }


async def wildcard(request):
    raise web.HTTPFound('/')