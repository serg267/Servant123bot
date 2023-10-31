
import json


from aiogram import Bot, Router
from aiogram.filters import and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from sqlalchemy.orm import sessionmaker

from config import ADMINCHAT
# from core.db import session_maker, Messages
from core.db import Messages
from core.keyboards.post_adv_keyboard import choice_keyboard

from core.models.States import PostStates


from core.models.models import LinkedMessage
from static import EMO1


def get_replied_message_id(message: Message) -> int or None:
    """if it is replied message gets id and chat id of original"""
    if message.reply_to_message:
        return LinkedMessage.get_element(message.reply_to_message.message_id,
                                         message.reply_to_message.chat.id).first_message_id
    return None


async def clear(bot: Bot, state: FSMContext) -> None:
    """Catch message with set state,  clear state and edit previous bot message"""
    if await state.get_state() is not None:
        data = await state.get_data()
        await state.clear()
        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='отмена')


async def message_handler(message: Message, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This handler will resend a text message to admin chat"""
    await clear(bot, state)   # clear state and edit previous bot message

    print(message.model_dump_json())
    # need special method to serialise Aiogram message .model_dump_json(), json.dumps do incorrect result
    json_obj = json.loads(message.model_dump_json())

    if message.text:
        msg_type = 'text'
    elif message.photo:
        msg_type = 'photo'
    elif message.video:
        msg_type = 'video'
    elif message.audio:
        msg_type = 'audio'
    elif message.voice:
        msg_type = 'voice'
    elif message.document:
        msg_type = 'document'
    elif message.animation:
        msg_type = 'animation'
    else:
        msg_type = 'unknown'
        await bot.send_message(chat_id=message.chat.id, text='не понимаю!', reply_to_message_id=message.message_id)

    msg = await bot.send_message(chat_id=ADMINCHAT,
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )

    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_obj,
                            # message_id=message.message_id,
                            message_type=msg_type)
    # json_str = msg.model_dump_json()
    # print(json_str)


# create router instance
post_router = Router()
# common filters
# post_router.message.filter(F.chat.type == 'private',
#                            and_f(~F.forward_from, ~F.forward_from_chat),
#                            ~F.media_group_id)
post_router.message.filter(F.chat.type == 'private', ~F.forward_from_chat, ~F.media_group_id)
# register filtered message handlers
post_router.message.register(message_handler, F.text | F.photo | F.video | F.audio | F.voice | F.document | F.animation)

