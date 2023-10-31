from aiogram import Bot
from config import ADMINCHAT
from core.db import Messages
from sqlalchemy.orm import sessionmaker


async def delete(db_message: Messages, bot: Bot, session_maker: sessionmaker) -> None:
    """This is post delete function"""
    print('del message_id', db_message.telegram_msg_id)
    await bot.delete_message(chat_id=ADMINCHAT, message_id=db_message.telegram_msg_id)
