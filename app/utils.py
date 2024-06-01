import re

from telethon.tl.custom.message import Message


def get_file_name(message):
    if message.file.name:
        return message.file.name.replace("\n", " ")
    ext = message.file.ext or ""
    return f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"


def get_message_info(message: Message):
    return (
        message.id,
        message.media,
        message.file.size,
        message.file.mime_type,
        get_file_name(message),
    )


convert_to_seconds_pattern = re.compile(
    r"((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?"
)


def convert_to_seconds(duration_str):
    try:
        duration = int(duration_str)
        return duration
    except ValueError:
        pass

    match = convert_to_seconds_pattern.fullmatch(duration_str)
    if not match:
        raise ValueError("Invalid duration format")

    time_data = match.groupdict()
    days = int(time_data["days"]) if time_data["days"] else 0
    hours = int(time_data["hours"]) if time_data["hours"] else 0
    minutes = int(time_data["minutes"]) if time_data["minutes"] else 0
    seconds = int(time_data["seconds"]) if time_data["seconds"] else 0

    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return total_seconds
