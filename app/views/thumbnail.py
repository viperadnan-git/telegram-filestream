import io
from PIL import Image
from app import client
from aiohttp import web
from telethon.tl import types
from app.helper.utils import parseInt

async def get_thumbnail(req):
    chat_id = await parseInt(req.match_info['chat'])
    try:
        message_id = int(req.match_info["id"])
    except ValueError:
        return web.Response(status=400, text="400: Bad Request")
    
    try:
        message = await client.get_messages(entity=chat_id, ids=message_id)
    except:
        print(f"Error in getting message {message_id} in {chat_id}")
        message = None

    if not message or not message.file:
        print(f"No result for {message_id} in {chat_id}")
        return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")

    if message.document:
        media = message.document
        thumbnails = media.thumbs
        location = types.InputDocumentFileLocation
    else:
        media = message.photo
        thumbnails = media.sizes
        location = types.InputPhotoFileLocation

    if not thumbnails or message.sticker:
        if message.audio or message.voice:
            im = Image.open("images/audio_thumbnail.png")
        elif message.sticker:
            im = Image.open("images/sticker_thumbnail.png")
        else:
            im = Image.open("images/file_thumbnail.png")
        temp = io.BytesIO()
        im.save(temp, "PNG")
        body = temp.getvalue()
    else:
        thumb_pos = int(len(thumbnails)/2)
        thumbnail = client._get_thumb(thumbnails, thumb_pos)
        if not thumbnail or isinstance(thumbnail, types.PhotoSizeEmpty):
            return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")

        if isinstance(thumbnail, (types.PhotoCachedSize, types.PhotoStrippedSize)):
            body = await client._download_cached_photo_size(thumbnail, bytes)
        else:
            actual_file = location(
                id=media.id,
                access_hash=media.access_hash,
                file_reference=media.file_reference,
                thumb_size=thumbnail.type
            )
            body = client.iter_download(actual_file)

    return web.Response(
        status=200,
        body=body,
        headers={
            "Content-Type": "image/jpeg",
            "Content-Disposition": 'inline; filename="thumbnail.jpg"'
        }
    )