from typing import Any

from app.core.db import Messages

from app.static import DAYS_OF_WEEK, MONTH, MSG


def title_and_date_information(db_message: Messages, length: int) -> tuple[str | Any, str]:
    """returns title and datetime strings"""
    the_date = f"{DAYS_OF_WEEK[db_message.post_date.weekday()]} {db_message.post_date.strftime('%d')}" \
               f" {MONTH[str(db_message.post_date.month)]} {db_message.post_date.strftime('%y г. %H:%M')}"

    # takes title of the post
    title = None
    match db_message.message_type:
        case 'media_group':
            for msg in db_message.message_json:
                if msg['caption']:
                    title = msg['caption']
                    break
        case _:
            if db_message.message_json['text']:
                title = db_message.message_json['text']
            else:
                title = db_message.message_json['caption']
    if isinstance(title, str):
        if len(title) > length:
            title = f"{title[:length]}..."
    else:
        title = MSG[db_message.message_type]

    return title, the_date


def post_information(db_message: Messages, length: int = 70) -> str:
    """Post text information"""
    chanel = '<a href="https://t.me/world_rk">История мировых религий и религиозных культов</a>'
    posted_by = 'Будет опубликован через Lettercarrierbot'
    title, the_date = title_and_date_information(db_message, length)

    text = f"🗓 Пост <b>«{title}»</b>\nЗапланирован на <b>{the_date}</b> для публикации на канале {chanel}\n{posted_by}"
    return text


def post_information(db_message: Messages, length: int = 70) -> str:
    """Post text information"""
    chanel = '<a href="https://t.me/world_rk">История мировых религий и религиозных культов</a>'
    posted_by = 'Будет опубликован через Lettercarrierbot'
    title, the_date = title_and_date_information(db_message, length)

    text = f"🗓 Пост <b>«{title}»</b>\nЗапланирован на <b>{the_date}</b> для публикации на канале {chanel}\n{posted_by}"
    return text


def show_information(db_message: Messages, length: int = 70) -> str:
    """Show text information"""
    chanel = 'История мировых религий и религиозных культов'
    title, the_date = title_and_date_information(db_message, length)

    text = f"🗓 Пост <b>«{title}»</b>\nЗапланирован на <b>{the_date}</b> для публикации на канале <b>«{chanel}»</b>"
    return text


def delete_information(db_message: Messages, length: int = 70) -> str:
    """delete text information"""
    title, the_date = title_and_date_information(db_message, length)

    text = f"❌<b>Удален</b> 🗓пост <b>«{title}»</b>, запланированный  на <b>{the_date}</b>"
    return text
