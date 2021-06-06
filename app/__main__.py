import jinja2
import aiohttp_jinja2
from aiohttp import web
from app.views import *
from telethon.tl.types import Channel, Chat, User
from app.helper.utils import generate_alias
from app import host, port, client, tg_settings, \
    authorization



async def app():
    routes = [web.get('/', Main)]
    middlewares = None
    if authorization:
        routes.append(web.view('/api/{task}', Api))
        middlewares = [middleware]
      
    app = web.Application(middlewares=middlewares)
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(
            'assets'
            )
        )
    
    app["auth"] = authorization
    app['chats'] = {}

    if tg_settings.get("all", False):
        async for chat in client.iter_dialogs():
            if chat.id in tg_settings.get('exclude', []):
                continue
            if not chat.id in tg_settings.get('include', []):
                if isinstance(chat.entity, User) and not tg_settings.get('private', False):
                    continue
                elif isinstance(chat.entity, Channel) and not tg_settings.get('channel', False):
                    continue
                elif isinstance(chat.entity, Chat) and not tg_settings.get('group', False):
                    continue
            alias = await generate_alias(chat)
            app['chats'][alias['alias_id']] = alias
    else:
        for chat_id in tg_settings.get('include', []):
            chat = await client.get_entity(chat_id)
            alias = await generate_alias(chat)
            app['chats'][alias['alias_id']] = alias
      
    for alias_id in app['chats'].keys():
        chat = "{chat:" + alias_id + "}"
        routes.extend([
            web.view('/'+chat, IndexChat),
            web.get('/'+chat+'/{id}', IndexMessage),
            web.get('/thumbnail/'+chat+'/{id}', get_thumbnail),
            web.view('/download/'+chat+'/{id}', Download),
            web.view('/download/'+chat+'/{id}/{filename}', Download),
        ])
    routes.append(web.view(r"/{wildcard:.*}", wildcard))
    app.add_routes(routes)
    app.on_cleanup.append(lambda *args: client.disconnect())
    return app

web.run_app(app(), host=host, port=port)