import asyncio
import math
import traceback

import humanize
from telethon import events
from telethon.errors import MediaCaptionTooLongError, MessageTooLongError

from app import cache, chat_id, client, expiry, public_url
from app.encrypter import string_encryptor
from app.utils import get_file_name, get_message_info


async def handle_message(evt: events.NewMessage.Event) -> None:
    if not evt.is_private:
        return
    
    if not evt.file:
        await evt.respond(
            "<b>Send any document 📁🗂️🎥🎤🖼️ to get direct download link.</b>"
        )
        return
    
    sender_name = evt.message.sender.first_name + " " + evt.message.sender.last_name if evt.message.sender.last_name else evt.message.sender.first_name
    sender_mention = f"<a href='tg://user?id={evt.message.sender_id}'>👤 {sender_name}</a>"
    saved_message_caption = f"{evt.message.text}\n\n{sender_mention}"
    
    try:
        saved_message = await client.send_file(chat_id, evt.message.media, caption=saved_message_caption, buttons=evt.message.reply_markup)
    except (MediaCaptionTooLongError, MessageTooLongError):
        saved_message = await client.send_file(chat_id, evt.message.media, caption=sender_mention, buttons=evt.message.reply_markup)
    
    file_name = get_file_name(saved_message)
    message_hash = string_encryptor.encrypt(str(saved_message.id))
    url = f"{public_url}/{message_hash}/{file_name}"
    await evt.respond(
        f"<b>🔗 Link to download file\n\n</b> <a href='{url}'>{file_name}</a>\n\n<i>This link will expire in {humanize.naturaldelta(expiry)}</i>"
    )

    cache[message_hash] = get_message_info(saved_message)


async def register_handler():
    client.add_event_handler(handle_message, events.NewMessage(incoming=True))


async def download(file, file_size, offset, limit):
    part_size = 512 * 1024
    first_part_cut = offset % part_size
    first_part = math.floor(offset / part_size)
    last_part_cut = part_size - (limit % part_size)
    last_part = math.ceil(limit / part_size)
    # part_count = math.ceil(file_size / part_size)
    part = first_part
    try:
        async for chunk in client.iter_download(
            file, offset=first_part * part_size, request_size=part_size
        ):
            if part == first_part:
                yield chunk[first_part_cut:]
            elif part == last_part:
                yield chunk[:last_part_cut]
            else:
                yield chunk
            part += 1
        print("Serving Finished")
    except (GeneratorExit, StopAsyncIteration, asyncio.CancelledError):
        print("File serve interrupted")
        raise
    except Exception:
        traceback.print_exc()
        print("File serve errored")
