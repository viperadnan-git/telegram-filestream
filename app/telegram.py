import math
import asyncio
from telethon import utils
from telethon.tl import types
from app.utils import humanbytes, get_file_name, get_chat_name
from app import client, results_per_page


async def get_chat_messages(chat_id, offset:int, search_query=None):
    results = []
    kwargs = {
        'entity': chat_id,
        'limit': results_per_page,
        'add_offset': results_per_page*offset
    }
    if search_query:
        kwargs.update({'search': search_query})
    messages = (await client.get_messages(**kwargs)) or []
    
    for msg in messages:
        entry = None
        if msg.file and not isinstance(msg.media, types.MessageMediaWebPage):
            entry = {
                'id' : f"/{chat_id}/{msg.id}",
                'message' : msg.text.replace('\n','<br>'),
                'file' : {
                    'mime_type' : msg.file.mime_type,
                    'file_ext' : msg.file.ext.replace('.','').upper(),
                    'file_size' : await humanbytes(msg.file.size),
                }
            }
        elif msg.message:
            entry = {
                'id' : f"/{chat_id}/{msg.id}",
                'message' : msg.text.replace('\n','<br>'),
                'file' : False
            }
        if entry:
            results.append(entry)
    return results, await get_chat_name(messages, chat_id)

async def get_message(chat_id, message_id:int):
    try:
        message = await client.get_messages(entity=chat_id, ids=message_id)
    except:
        return None
    reply_btns = []
    if message.reply_markup:
        if isinstance(message.reply_markup, types.ReplyInlineMarkup):
            for button_row in message.reply_markup.rows:
                btns = []
                for button in button_row.buttons:
                    if isinstance(button, types.KeyboardButtonUrl):
                        btns.append({'url': button.url, 'text': button.text})
                reply_btns.append(btns)
    if message.media and not isinstance(message.media, types.MessageMediaWebPage):
        return {
            "id" : f"/{chat_id}/{message.id}",
            "message_type" : "Media",
            "message" : message.text.replace('\n', '<br>'),
            "buttons" : reply_btns,
            "file" : {
                'mime_type' : message.file.mime_type,
                'file_name' : await get_file_name(message),
                'file_ext' : message.file.ext.replace('.','').upper(),
                'file_size' : await humanbytes(message.file.size),
            }
        }
    else:
        return {
            "id" : f"/{chat_id}/{message.id}",
            "message_type" : "Message",
            "message" : message.text.replace('\n', '<br>'),
            "buttons" : reply_btns,
            "file" : False
        }
        

async def download(file, file_size, offset, limit):
        part_size_kb = utils.get_appropriated_part_size(file_size)
        part_size = int(part_size_kb * 1024)
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
            print("File serve errored")