import aiohttp_jinja2
from app import client
from aiohttp import web
from app.helper.utils import parseInt
from app.helper.telegram import get_message


class IndexMessage(web.View):
    async def post(self):
        chat_id = await parseInt(self.request.match_info["chat"])
        try:
            message_id = int(self.request.match_info.get("id", None))
        except ValueError as err:
            return web.Response(status=400, text="400: Bad Request! Invalid Url provided enter a valid Telegram Link")

        try:
            message = await client.get_messages(entity=chat_id, ids=message_id)
        except Exception as err:
            message = None
     
        if not message or not message.file:
            print(f"No check result for {message_id} in {chat_id}")
            return web.Response(status=404, text="404: File Not Found! Telegram File not found, make sure its publically available.")
        return web.Response(status=200, text="https" if self.request.secure else "http" + f"://{self.request.host}/{chat_id}/{message_id}")

    @aiohttp_jinja2.template("preview.html")
    async def get(self):
        chat_id = await parseInt(self.request.match_info["chat"])
        try:
            message_id = int(self.request.match_info["id"])
        except Exception as err:
            return web.HTTPFound("/" + chat_id)
    
        try:
            return await get_message(chat_id, message_id)
        except Exception as e:
            return web.HTTPFound("/" + chat_id)