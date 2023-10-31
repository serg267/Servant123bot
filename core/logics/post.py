from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import ADMINCHAT
from core.db import Messages, set_telegram_msg_id


async def post(db_message: Messages, bot: Bot, session_maker: sessionmaker) -> None:
    """This is post function"""

    commons = {'chat_id': ADMINCHAT, 'request_timeout': 20}

    match db_message.message_type:

        case 'text':
            msg = await bot.send_message(**commons,
                                         text=db_message.message_json['text'],
                                         entities=db_message.message_json['entities']
                                         )
            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'photo':
            msg = await bot.send_photo(**commons,
                                       photo=db_message.message_json['photo'][-1]['file_id'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       has_spoiler=db_message.message_json['has_media_spoiler']
                                       )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'video':
            msg = await bot.send_video(**commons,
                                       video=db_message.message_json['video']['file_id'],
                                       duration=db_message.message_json['video']['duration'],
                                       width=db_message.message_json['video']['width'],
                                       height=db_message.message_json['video']['height'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       has_spoiler=db_message.message_json['has_media_spoiler'],
                                       )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'audio':
            msg = await bot.send_audio(**commons,
                                       audio=db_message.message_json['audio']['file_id'],
                                       duration=db_message.message_json['audio']['duration'],
                                       title=db_message.message_json['audio']['title'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       )

        case 'voice':
            msg = await bot.send_voice(**commons,
                                       voice=db_message.message_json['voice']['file_id'],
                                       duration=db_message.message_json['voice']['duration'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities']
                                       )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'document':
            msg = await bot.send_document(**commons,
                                          document=db_message.message_json['document']['file_id'],
                                          caption=db_message.message_json['caption'],
                                          caption_entities=db_message.message_json['caption_entities'],
                                          )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'animation':
            msg = await bot.send_animation(**commons,
                                           animation=db_message.message_json['animation']['file_id'],
                                           duration=db_message.message_json['animation']['duration'],
                                           width=db_message.message_json['animation']['width'],
                                           height=db_message.message_json['animation']['height'],
                                           caption=db_message.message_json['caption'],
                                           caption_entities=db_message.message_json['caption_entities'],
                                           )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'forwarded':
            msg = await bot.forward_message(**commons,
                                            from_chat_id=db_message.message_json['from_user']['id'],
                                            message_id=db_message.message_json['message_id'],
                                            )
            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)


def delayed_post(msg: Messages, bot: Bot, async_scheduler: AsyncIOScheduler):
    """adds delayed post job to the schedular """
