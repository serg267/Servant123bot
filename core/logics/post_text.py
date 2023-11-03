from core.db import Messages


def post_information(db_message: Messages) -> str:
    """Post text information"""
    if db_message.message_type == 'text':
        title = db_message.message_json['text']
        if len(title) > 50:
            title = f"{title[:50]}..."
        text = f"🗓 Пост <b>«{title}»</b>\n" \
               f"Запланирован на {db_message.post_date.day} {db_message.post_date.strftime('%d.%m.%Y')} {db_message.post_date.strftime('%H:%M')}"
    return text

    # "🗓 Пост «Карл Густав Юнг, говоря о религиях, называл их системами...» Запланирован на пт 13 окт. 10:00 для публикации в История. Исторические факты. Будет опубликован через Notepost, который выгружает статистику реакций и кликов в Google Таблицы."