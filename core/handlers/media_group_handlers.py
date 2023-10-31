import json

from aiogram import Bot, Router, F
from aiogram.types import Message, InputMediaPhoto,  InputMediaVideo, InputMediaDocument, InputMediaAudio, \
    InputMediaAnimation

from config import ADMINCHAT
from core.handlers.message_handlers import get_replied_message_id, clear
from core.keyboards import choice_keyboard
from core.models.States import PostStates
from core.models.models import LinkedMessage
from static import EMO1
from aiogram.fsm.context import FSMContext


async def forward_media_to_admin_chat(message: Message, bot: Bot, album: list[Message], state: FSMContext) -> None:
    """This handler will forward a complete album of any type."""
    await clear(bot, state)   # clear state and edit previous bot message

    if not album:
        json_album = [json.loads(message.model_dump_json())]
    else:
        json_album = [json.loads(message.model_dump_json()) for message in album]

    msg = await bot.send_message(chat_id=ADMINCHAT,
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )

    # set state to handle callback
    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    # add state data
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_album,
                            message_type='media_group')

    # #  *******************************************************
    # #  prototype to new function
    # at_east_one = False
    # if not album:
    #     album = [message]
    # # media group list
    # medias = []
    #
    # for obj in album:
    #     # add username to message
    #     new_message_text = None
    #     if obj.caption:
    #         new_message_text = f"{obj.caption}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    #         at_east_one = True
    #
    #     # check if it is last message and there is no caption text before, add username to message
    #     if not at_east_one:
    #         if obj == album[-1] and not obj.caption:
    #             new_message_text = f"{EMO1} {message.chat.first_name} (@{message.chat.username})"
    #
    #     # add input media all types
    #     if obj.photo:
    #         file_id = obj.photo[-1].file_id
    #         photo = InputMediaPhoto(media=file_id,
    #                                 caption=new_message_text,
    #                                 caption_entities=obj.caption_entities)
    #         medias.append(photo)
    #
    #     elif obj.video:
    #         file_id = obj.video.file_id
    #         video = InputMediaVideo(media=file_id,
    #                                 caption=new_message_text,
    #                                 caption_entities=obj.caption_entities,
    #                                 thumbnail=obj.video.thumbnail.file_id)
    #         medias.append(video)
    #
    #     elif obj.document:
    #         file_id = obj.document.file_id
    #         document = InputMediaDocument(media=file_id,
    #                                       caption=new_message_text,
    #                                       caption_entities=obj.caption_entities,
    #                                       thumbnail=obj.document.thumbnail.file_id)
    #         medias.append(document)
    #
    #     elif obj.audio:
    #         file_id = obj.audio.file_id
    #         audio = InputMediaAudio(media=file_id,
    #                                 caption=new_message_text,
    #                                 caption_entities=obj.caption_entities,
    #                                 thumbnail=obj.audio.thumbnail.file_id)
    #         medias.append(audio)
    #
    #     elif obj.animation:
    #         file_id = obj.animation.file_id
    #         animation = InputMediaAnimation(media=file_id,
    #                                         caption=new_message_text,
    #                                         caption_entities=obj.caption_entities,
    #                                         thumbnail=obj.animation.thumbnail.file_id)
    #         medias.append(animation)
    #
    # msgs = await bot.send_media_group(chat_id=ADMINCHAT,
    #                                   media=medias,
    #                                   reply_to_message_id=get_replied_message_id(message),
    #                                   allow_sending_without_reply=True)
    # linked_msg = LinkedMessage(msgs[0].message_id, msgs[0].chat.id)
    # linked_msg.set_first_msg(message)

# create router instance
media_group_router = Router()
# common filter
media_group_router.message.filter(F.media_group_id)
# register filtered message handler
media_group_router.message.register(forward_media_to_admin_chat,
                                    F.text | F.photo | F.audio | F.video | F.document | F.voice)
