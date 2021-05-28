async def get_file_name(message):
    if message.file.name:         
        return message.file.name.replace('\n', ' ')
    ext = message.file.ext or ""
    return f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"

async def parseInt(str):
    try:
        return int(str)
    except ValueError as err:
        return str