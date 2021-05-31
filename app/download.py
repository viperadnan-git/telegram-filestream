from app import client
from aiohttp import web
from app.telegram import download
from app.utils import get_file_name, parseInt
from telethon.tl import types


async def download_get(request):
    return await handle_request(request)
 
async def download_head(request):
    return await handle_request(request, head=True)

async def handle_request(req, head=False):
    chat_id = await parseInt(req.match_info.get("chat", None))
    try:
        message_id = int(req.match_info.get("id", None))
    except ValueError as err:
        return web.Response(status=400, text="400: Bad Request" if not head else None)

    try:
        message = await client.get_messages(entity=chat_id, ids=message_id)
    except Exception as err:
        print(f"Error in getting message {message_id} in {chat_id}")
        return web.Response(status=404, text="404: File Not Found" if not head else None)

    if not message.file or isinstance(message.media, types.MessageMediaWebPage):
        print(f"No result for {message_id} in {chat_id}")
        return web.Response(status=200, text=message.raw_text if not head else None)

    media = message.media
    size = message.file.size
    file_name = req.match_info.get("name", None) or await get_file_name(message)
    mime_type = message.file.mime_type

    try:
        offset = req.http_range.start or 0
        limit = req.http_range.stop or size
        if (limit > size) or (offset < 0) or (limit < offset):
            raise ValueError("range not in acceptable format")
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

    headers = {
        "Content-Type": mime_type,
        "Content-Range": f"bytes {offset}-{limit}/{size}",
        "Content-Length": str(limit - offset),
        "Accept-Ranges": "bytes",
        "Content-Disposition": f'attachment; filename="{file_name}"'
    }

    return web.Response(
        status=206 if offset else 200,
        body=body,
        headers=headers
    )