import hmac
import hashlib
from app import secret_key

algorithm = hashlib.sha256
async def sign(data: str) -> str:
    return hmac.new(secret_key, data.encode("utf-8"), algorithm).hexdigest()

async def verify(signature: str, data: str) -> bool:
    expected = await sign(data)
    if expected != signature:
        raise ValueError(f"Invalid signature for {data}")
    return True

async def parseInt(str):
    try:
        return int(str)
    except ValueError as err:
        return str

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