import asyncio
import math
import traceback

from telethon import events

from app import chat_id, client, public_url, cache
from app.encrypter import string_encryptor
from app.utils import get_file_name, get_message_info


async def handle_message(evt: events.NewMessage.Event) -> None:
    if not evt.is_private:
        return
    if not evt.file:
        await evt.respond("<b>Send any document 📁🗂️🎥🎤🖼️ to get direct download link.</b>")
        return
    msg = await client.send_message(chat_id, evt.message)
    file_name = get_file_name(msg)
    message_hash = string_encryptor.encrypt(str(msg.id))
    url = f"{public_url}/{message_hash}/{file_name}"
    await evt.respond(f"<b>🔗 Link to download file\n</b> <a href='{url}'>{file_name}</a>")

    cache[message_hash] = get_message_info(msg)


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
