import jinja2
import aiohttp_jinja2
from aiohttp import web
from app import host, port, client, recommendations
from app.index import index_chat
from app.utils import parseInt
from app.preview import check_file, index_message
from app.download import download_get, download_head
from app.thumbnail import get_thumbnail

recommendations_chat = []

@aiohttp_jinja2.template("main.html")
async def main_handler(request):
    return {"chats":recommendations_chat}

async def wildcard(request):
    raise web.HTTPFound('/')

for chat_id in recommendations:
    try:
        chat = client.get_entity(parseInt(chat_id))
        recommendations_chat.append({
            "chat_id" : chat.id,
            "title" : getattr(chat, "title", getattr(chat, "first_name", "Unknown Chat"))
        })
    except Exception as err:
        print(f"Failed to get {chat_id}: {err}")

app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(
        'assets'
        )
    )
app.add_routes([
    web.get('/', main_handler),
    web.get('/{chat}', index_chat),
    web.get('/{chat}/{id}', index_message),
    web.get("/check/{chat}/{id}", check_file),
    web.get('/thumbnail/{chat}/{id}', get_thumbnail),
    web.get('/download/{chat}/{id}', download_get),
    web.get('/download/{chat}/{id}/{filename}', download_get),
    web.head('/download/{chat}/{id}', download_head),
    web.head('/download/{chat}/{id}/{filename}', download_head),
    web.view(r"/{wildcard:.*}", wildcard)
])
web.run_app(app, host=host, port=port)