import jinja2
import aiohttp_jinja2
from aiohttp import web
from app.views import *
from app import host, port, client, recommendations, \
    authorization



async def app():
    routes = [web.get('/', Main)]
    middlewares = None
    if authorization:
        routes.append(web.view('/api/{task}', Api))
        middlewares = [middleware]
      
    app = web.Application(middlewares=middlewares)
    app["chat_recommendations"] = []
    app["auth"] = authorization

    for chat_id in recommendations:
        try:
            chat = await client.get_entity(await parseInt(chat_id))
            app["chat_recommendations"].append({
                "chat_id" : chat.id,
                "title" : getattr(chat, "title", getattr(chat, "first_name", "Unknown Chat"))
            })
        except Exception as err:
            print(f"Failed to get {chat_id}: {err}")

    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(
            'assets'
            )
        )
    
    routes.extend([
        web.view('/{chat}', IndexChat),
        web.view('/{chat}/{id}', IndexMessage),
        web.get('/thumbnail/{chat}/{id}', get_thumbnail),
        web.view('/download/{chat}/{id}', Download),
        web.view('/download/{chat}/{id}/{filename}', Download),
        web.view(r"/{wildcard:.*}", wildcard)
    ])
    app.add_routes(routes)
    app.on_cleanup.append(lambda *args: client.disconnect())
    return app

web.run_app(app(), host=host, port=port)