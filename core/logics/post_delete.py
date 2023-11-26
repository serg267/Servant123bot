from aiogram import Bot
from config import CHANEL_ID
from core.db import Messages
from sqlalchemy.orm import sessionmaker

from core.db.messages import set_delete_job_id
from core.scheduler.schedule import add_one_job
from core.logics import post


async def delete(db_message: Messages, bot: Bot) -> None:
    """This is post delete function"""

    # for all messages types, excepts media_group
    if isinstance(db_message.telegram_msg_id, int):
        await bot.delete_message(chat_id=CHANEL_ID, message_id=db_message.telegram_msg_id)

    # for media_group messages
    elif isinstance(db_message.telegram_msg_id, list):
        for msg_id in db_message.telegram_msg_id:
            await bot.delete_message(chat_id=CHANEL_ID, message_id=msg_id)


async def post_then_delete(db_message: Messages, bot: Bot, session_maker: sessionmaker) -> None:
    """This is post delete function"""
    await post(db_message, bot, session_maker)
    print('del message_id', db_message.telegram_msg_id)
    delete_job_id = await add_one_job(func=delete,
                                      dtime=db_message.delete_date,
                                      kwargs={'db_message': db_message, 'bot': bot}
                                      )

    # delete_job_id = await add_one_job(func=bot.delete_message,
    #                                   dtime=db_message.delete_date,
    #                                   kwargs={'db_message': db_message, 'bot': bot}
    #                                   )
    await set_delete_job_id(db_message.id, delete_job_id, session_maker)
