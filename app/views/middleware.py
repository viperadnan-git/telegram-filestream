import aiohttp_jinja2
from aiohttp import web
from app.helper.utils import verify, sign

@web.middleware
async def middleware(request, handler):
    if request.path != "/api/login": 
        try:
            username = request.cookies.get('username') or request.query.get('username', '_')
            __authorization = request.cookies.get('__authorization') or await sign(request.query['password'])
            await verify(__authorization, request.app['auth'][username])
            return await handler(request)
        except Exception as err:
            response = aiohttp_jinja2.render_template('login.html', request, {"username":len(request.app['auth'].items()) != 1})
            return response
    return await handler(request)