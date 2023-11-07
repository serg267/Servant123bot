import asyncio
import datetime

from aiogram import Bot
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio, InputMediaAnimation
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import ADMINCHAT
from core.db import Messages, set_telegram_msg_id
from core.keyboards import url_button_keyboard


async def post(db_message: Messages, bot: Bot, session_maker: sessionmaker) -> None:
    """This is post function"""

    commons = {'chat_id': ADMINCHAT, 'request_timeout': 20}

    # add button to msg excepts media_group and forwarded
    url_button_kb = None
    if db_message.button:
        url_button_kb = url_button_keyboard(db_message.button[0], db_message.button[1])

    match db_message.message_type:

        case 'text':
            msg = await bot.send_message(**commons,
                                         text=db_message.message_json['text'],
                                         entities=db_message.message_json['entities'],
                                         reply_markup=url_button_kb
                                         )
            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'photo':
            msg = await bot.send_photo(**commons,
                                       photo=db_message.message_json['photo'][-1]['file_id'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       has_spoiler=db_message.message_json['has_media_spoiler'],
                                       reply_markup=url_button_kb
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
                                       reply_markup=url_button_kb
                                       )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'audio':
            msg = await bot.send_audio(**commons,
                                       audio=db_message.message_json['audio']['file_id'],
                                       duration=db_message.message_json['audio']['duration'],
                                       title=db_message.message_json['audio']['title'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       reply_markup=url_button_kb
                                       )

        case 'voice':
            msg = await bot.send_voice(**commons,
                                       voice=db_message.message_json['voice']['file_id'],
                                       duration=db_message.message_json['voice']['duration'],
                                       caption=db_message.message_json['caption'],
                                       caption_entities=db_message.message_json['caption_entities'],
                                       reply_markup=url_button_kb
                                       )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'document':
            msg = await bot.send_document(**commons,
                                          document=db_message.message_json['document']['file_id'],
                                          caption=db_message.message_json['caption'],
                                          caption_entities=db_message.message_json['caption_entities'],
                                          reply_markup=url_button_kb
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
                                           reply_markup=url_button_kb
                                           )

            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'forwarded':
            msg = await bot.forward_message(**commons,
                                            from_chat_id=db_message.message_json['from_user']['id'],
                                            message_id=db_message.message_json['message_id']
                                            )
            await set_telegram_msg_id(db_message.id, msg.message_id, session_maker)

        case 'media_group':
            json_album = db_message.message_json
            print(json_album)

            medias = []
            count = 0

            for message in json_album:
                count += 1
                print('**', count, '**')
                print(message)
                print(message['photo'][-1]['file_id'])

                # add input media all types
                if message['photo']:
                    photo = InputMediaPhoto(media=message['photo'][-1]['file_id'],
                                            caption=message['caption'],
                                            caption_entities=message['caption_entities']
                                            )
                    medias.append(photo)

                elif message['video']:
                    video = InputMediaVideo(media=message['video']['file_id'],
                                            caption=message['caption'],
                                            caption_entities=message['caption_entities'],
                                            thumbnail=message['video']['thumbnail']['file_id']
                                            )
                    medias.append(video)

                elif message['document']:
                    document = InputMediaDocument(media=message['document']['file_id'],
                                                  caption=message['caption'],
                                                  caption_entities=message['caption_entities'],
                                                  thumbnail=message['document']['thumbnail']['file_id']
                                                  )
                    medias.append(document)

                elif message['audio']:
                    audio = InputMediaAudio(media=message['audio']['file_id'],
                                            caption=message['caption'],
                                            caption_entities=message['caption_entities'],
                                            thumbnail=message['audio']['thumbnail']['file_id']
                                            )
                    medias.append(audio)

                elif message.animation:
                    animation = InputMediaAnimation(media=message['audio']['file_id'],
                                                    caption=message['caption'],
                                                    caption_entities=message['caption_entities'],
                                                    thumbnail=message['audio']['thumbnail']['file_id']
                                                    )
                    medias.append(animation)
            msgs = await bot.send_media_group(**commons, media=medias)

            msgs_id = [msg.message_id for msg in msgs]
            print('msgs_id=', msgs_id)
            await set_telegram_msg_id(db_message.id, msgs_id, session_maker)
            # for msg in msgs:
            #     print(msg.model_dump_json())
            #     t = datetime.datetime.now()
            #     await asyncio.sleep(60)
            #     await bot.delete_message(**commons, message_id=msg.message_id)
            #     print('time=', datetime.datetime.now() - t)


def delayed_post(msg: Messages, bot: Bot, async_scheduler: AsyncIOScheduler):
    """adds delayed post job to the schedular """
