from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import ADMINCHAT
from core.db import Messages, set_telegram_msg_id


async def post(db_message: Messages, bot: Bot, session_maker: sessionmaker) -> None:
    """This is post function"""
    match db_message.message_type:

        case 'text':
            msg = await bot.send_message(chat_id=ADMINCHAT,
                                         text=db_message.message_json['text'],
                                         entities=db_message.message_json['entities']
                                         )
            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'photo':
            msg = await bot.send_photo(chat_id=ADMINCHAT,
                                       photo=db_message.message_json['photo'][-1]['file_id'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       has_spoiler=db_message.message_json['has_media_spoiler']
                                       )
            # await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'video':
            msg = await bot.send_video(chat_id=ADMINCHAT,
                                       video=db_message.message_json['video']['file_id'],
                                       duration=db_message.message_json['video']['duration'],
                                       width=db_message.message_json['video']['width'],
                                       height=db_message.message_json['video']['height'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       has_spoiler=db_message.message_json['has_media_spoiler']
                                       )
            # await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'audio':
            msg = await bot.send_audio(chat_id=ADMINCHAT,
                                       audio=db_message.message_json['audio']['file_id'],
                                       duration=db_message.message_json['audio']['duration'],
                                       #           width=msg.message_json['video']['width'],
                                       #          height=msg.message_json['video']['height'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       #         has_spoiler=msg.message_json['has_media_spoiler']
                                       )
            # await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)


def delayed_post(msg: Messages, bot: Bot, async_scheduler: AsyncIOScheduler):
    """adds delayed post job to the schedular """



