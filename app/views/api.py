from aiohttp import web
from app.helper.utils import sign

class Api(web.View):
    async def post(self):
        if self.request.match_info["task"] == "login":
            try:
                d = await self.request.json()
                username = d.get("username") or "_"
                password = d["password"]
            except:
                return web.Response(status=400, text="400: Bad Request")
            auth = self.request.app["auth"]
            if username in auth and \
                password == auth[username]:
                r = web.Response(status=200, text="#")
                r.set_cookie("__authorization", await sign(password), max_age=60*60*24)
                r.set_cookie("username", username, max_age=60*60*24)
                return r
            return web.HTTPForbidden()
        return web.HTTPFound(self.request.path)
    
    
    async def get(self):
        if self.request.match_info["task"] == "logout":
            try:
                r = web.HTTPFound("/")
                r.del_cookie("__authorization")
                r.del_cookie("username")
                return r
            except:
                return web.Response(status=400, text="Oops! Can't logout.")
        return web.HTTPFound(self.request.path)