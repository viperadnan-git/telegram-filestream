from telethon.tl.custom.message import Message

def get_file_name(message):
    if message.file.name:
        return message.file.name.replace("\n", " ")
    ext = message.file.ext or ""
    return f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"

def get_message_info(message:Message):
    return (
        message.id,
        message.media,
        message.file.size,
        message.file.mime_type,
        get_file_name(message),
    )