from core.db import Messages
from static import DAYS_OF_WEEK, MONTH, MSG


def post_information(db_message: Messages, length: int = 70) -> str:
    """Post text information"""
    chanel = '<a href="https://t.me/world_rk">История мировых религий и религиозных культов</a>'
    the_date = f"{DAYS_OF_WEEK[db_message.post_date.weekday()]} {db_message.post_date.strftime('%d')}" \
               f" {MONTH[str(db_message.post_date.month)]} {db_message.post_date.strftime('%y г. %H:%M')}"
    posted_by = 'Будет опубликован через Lettercarrierbot'

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
    text = f"🗓 Пост <b>«{title}»</b>\nЗапланирован на <b>{the_date}</b> для публикации на канале {chanel}\n{posted_by}"
    return text

    # "🗓 Пост «Карл Густав Юнг, говоря о религиях, называл их системами...» Запланирован на пт 13 окт. 10:00 для публикации в История. Исторические факты. Будет опубликован через Notepost, который выгружает статистику реакций и кликов в Google Таблицы."