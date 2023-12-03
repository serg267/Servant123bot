from typing import Dict

from aiogram import Bot
from sqlalchemy.orm import sessionmaker

from app.core.db import Messages
from app.core.logics import post_information


async def notice(db_message: Messages, bot: Bot, data: Dict, session_maker: sessionmaker) -> None:

    # bot send edited message
    await bot.send_message(chat_id=data['answer_msg_chat_id'], text=post_information(db_message), parse_mode='HTML')
