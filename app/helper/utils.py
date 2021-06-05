import hmac
import hashlib
import secrets
from app import secret_key

algorithm = hashlib.sha256
async def sign(data: str) -> str:
    return hmac.new(secret_key, data.encode("utf-8"), algorithm).hexdigest()

async def verify(signature: str, data: str) -> bool:
    expected = await sign(data)
    if expected != signature:
        raise ValueError(f"Invalid signature for {data}")
    return True

async def parseChat(req):
    return req.app['chats'][req.match_info['chat']]

async def get_file_name(message):
    if message.file.name:         
        return message.file.name.replace('\n', ' ')
    ext = message.file.ext or ""
    return f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"

async def humanbytes(file_size):
    base = 1024.0
    sufix_list = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    for unit in sufix_list:
        if abs(file_size) < base:
            return f"{round(file_size, 2)} {unit}"
        file_size /= base

async def get_chat_name(chat):
    return getattr(
            chat,
            "title",
            getattr(chat,
            "first_name",
            "Chat")
        )

async def generate_alias(chat):
    return {
        'chat_id':chat.id,
        'alias_id':secrets.token_urlsafe(8),
        'title':await get_chat_name(chat)
    }