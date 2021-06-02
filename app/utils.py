def parseInt(str):
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