from aiohttp import web

from app import chat_id, client, cache
from app.encrypter import string_encryptor
from app.telegram import download
from app.utils import get_message_info

class Download(web.View):
    async def get(self):
        return await self.handle_request()

    async def head(self):
        return await self.handle_request(head=True)

    async def get_message(self, message_hash: str):
        if cache.get(message_hash):
            return cache[message_hash]

        try:
            message_id = int(string_encryptor.decrypt(message_hash))
            print(f"Getting message: {message_id} in {chat_id}")
            message = await client.get_messages(entity=chat_id, ids=message_id)

            if not message or not message.file:
                raise ValueError(f"No result for {message_id} in {chat_id}")

            message_info = get_message_info(message)
            cache[message_hash] = message_info
            return message_info
        except Exception as err:
            print(f"Error in getting message {message_hash} : {err}")
            return None

    async def handle_request(self, head=False):
        message_info = await self.get_message(self.request.match_info["hash"])

        if not message_info:
            return web.Response(status=404, text="404: Not Found")
        
        message_id, media, size, mime_type, file_name = message_info

        try:
            range_header = self.request.headers.get("Range")
            if range_header:
                offset, limit = range_header.replace("bytes=", "").split("-")
                offset = int(offset)
                limit = int(limit) if limit else size
            else:
                offset = self.request.http_range.start or 0
                limit = self.request.http_range.stop or size
            if (limit > size) or (offset < 0) or (limit < offset):
                raise ValueError("Range not in acceptable format")
        except ValueError as err:
            return web.Response(
                status=416,
                text=f"416: {err}" if not head else None,
                headers={"Content-Range": f"bytes */{size}"},
            )

        if head:
            body = None
        else:
            body = download(media, size, offset, limit)
            print(
                f"Serving file in {message_id} (chat {chat_id}) ; Range: {offset} - {limit}"
            )

        return web.Response(
            status=206 if offset else 200,
            body=body,
            headers={
                "Content-Type": mime_type,
                "Content-Range": f"bytes {offset}-{limit}/{size}",
                "Content-Length": str(size),
                "Accept-Ranges": "bytes",
                "Content-Disposition": f'attachment; filename="{file_name}"',
            },
        )
