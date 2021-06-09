from aiohttp import web
from app import chat_id, client
from app.telegram import download
from app.utils import get_file_name, decrypt

class Download(web.View):
    async def get(self):
        return await self.handle_request()
 
    async def head(self):
        return await self.handle_request(head=True)

    async def handle_request(self, head=False):
        try:
            message_id = int(await decrypt(self.request.match_info["id"]))
        except ValueError as err:
            return web.Response(status=400, text="400: Bad Request" if not head else None)

        try:
            message = await client.get_messages(entity=chat_id, ids=message_id)
        except Exception as err:
            print(f"Error in getting message {message_id} in {chat_id} : {err}")
            message = None

        if not message or not message.file:
            print(f"No result for {message_id} in {chat_id}")
            return web.Response(status=404, text="404: File Not Found" if not head else None)

        media = message.media
        size = message.file.size
        file_name = self.request.match_info.get("name", None) or await get_file_name(message)

        try:
            range_header = self.request.headers.get('Range', 0)
            if range_header:
                offset, limit = range_header.replace('bytes=', '').split('-')
                offset = int(offset)
                limit = int(limit) if limit else size
            else:
                offset = self.request.http_range.start or 0
                limit = self.request.http_range.stop or size
            if (limit > size) or (offset < 0) or (limit < offset):
                raise ValueError("Range not in acceptable format")
        except ValueError:
            return web.Response(
                status=416,
                text="416: Range Not Satisfiable" if not head else None,
                headers = {
                    "Content-Range": f"bytes */{size}"
                }
            )

        if head:
            body = None
        else:
            body = download(media, size, offset, limit)
            print(f"Serving file in {message.id} (chat {chat_id}) ; Range: {offset} - {limit}")

        return web.Response(
            status=206 if offset else 200,
            body=body,
            headers={
                "Content-Type": message.file.mime_type,
                "Content-Range": f"bytes {offset}-{limit}/{size}",
                "Content-Length": str(size),
                "Accept-Ranges": "bytes",
                "Content-Disposition": f'attachment; filename="{file_name}"',
            }
        )