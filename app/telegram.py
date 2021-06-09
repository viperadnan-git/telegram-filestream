import math
import asyncio
from app import client, public_url, chat_id
from app.utils import get_file_name, encrypt
from telethon import utils, events

async def register_handler():
    @client.on(events.NewMessage(incoming=True))
    async def handle_message(evt: events.NewMessage.Event) -> None:
        if not evt.is_private:
            return
        if not evt.file:
            await evt.reply("<b>Send any document 📁🗂️🎥🎤🖼️ to get direct download link.</b>")
            return
        msg = await client.send_message(chat_id, evt.message)
        url = f"{public_url}/{await encrypt(str(msg.id))}"
        await evt.reply(f"<b>🔗 Link to download file:</b> <a href='{url}'>{url}</a>")


async def download(file, file_size, offset, limit):
        part_size_kb = utils.get_appropriated_part_size(file_size)
        part_size = int(part_size_kb * 1024)
        offset -= offset % part_size
        first_part_cut = offset % part_size
        first_part = math.floor(offset / part_size)
        last_part_cut = part_size - (limit % part_size)
        last_part = math.ceil(limit / part_size)
        part_count = math.ceil(file_size / part_size)
        part = first_part
        try:
            async for chunk in client.iter_download(file, offset=first_part * part_size, request_size=part_size):
                if part == first_part:
                    yield chunk[first_part_cut:]
                elif part == last_part-1:
                    yield chunk[:last_part_cut]
                else:
                    yield chunk
                part += 1
            print("Serving Finished")
        except (GeneratorExit, StopAsyncIteration, asyncio.CancelledError):
            print("File serve interrupted")
            raise
        except Exception:
            print("File serve errored", exc_info=True)