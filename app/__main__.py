from aiohttp import web
from app import host, port, client, bot_token
from app.download import Download
from app.telegram import register_handler


async def wildcard(request):
    raise web.HTTPFound('https://viperadnan-git.github.io')

async def app():
    app = web.Application()
    await register_handler()
    await client.start(bot_token=bot_token)
    client.parse_mode = 'html'
    app.add_routes([
        web.view('/{id}', Download),
        web.view('/{id}/{name}', Download),
        web.view(r"/{wildcard:.*}", wildcard)
    ])
    return app

web.run_app(app(), host=host, port=port)