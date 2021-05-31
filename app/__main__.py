import jinja2
import aiohttp_jinja2
from aiohttp import web
from app import host, port, client
from app.index import index_chat
from app.download import download_get, download_head
from app.thumbnail import get_thumbnail
from app.preview import check_file, index_message

@aiohttp_jinja2.template("main.html")
async def main_handler(request):
    return {}

async def wildcard(request):
    raise web.HTTPFound('https://viperadnan-git.github.io')

app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(
        'assets'
        )
    )
app.add_routes([
    web.get('/', main_handler),
    web.get("/check/{chat}/{id}", check_file),
    web.get('/{chat}', index_chat),
    web.get('/preview/{chat}/{id}', index_message),
    web.get('/thumbnail/{chat}/{id}', get_thumbnail),
    web.get('/{chat}/{id}', download_get, allow_head=False),
    web.get('/{chat}/{id}/{name}', download_get, allow_head=False),
    web.head('/{chat}/{id}', download_head),
    web.head('/{chat}/{id}/{name}', download_head),
    web.view(r"/{wildcard:.*}", wildcard)
])
web.run_app(app, host=host, port=port)