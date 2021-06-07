import base64
from app import secret_key

async def encrypt(text):
    enc = []
    for i in range(len(text)):
        key_c = secret_key[i % len(secret_key)]
        enc_c = chr((ord(text[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

async def decrypt(text):
    dec = []
    text = base64.urlsafe_b64decode(text).decode()
    for i in range(len(text)):
        key_c = secret_key[i % len(secret_key)]
        dec_c = chr((256 + ord(text[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

async def get_file_name(message):
    if message.file.name:         
        return message.file.name.replace('\n', ' ')
    ext = message.file.ext or ""
    return f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"