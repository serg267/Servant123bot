
import json


from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from sqlalchemy.orm import sessionmaker

from core.keyboards import choice_keyboard
from core.logics import determine_message_type
from core.models import PostStates


async def clear(bot: Bot, state: FSMContext) -> None:
    """Catch message with set state,  clear state and edit previous bot message"""
    if await state.get_state() is not None:
        data = await state.get_data()
        await state.clear()
        # delete messages from data list before clear
        if data.get('send_msgs'):
            send_msgs = data['send_msgs']
            for db_message_id, msg_id in send_msgs.items():
                await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=msg_id)

        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='отмена'
                                    )


async def message_handler(message: Message, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This handler will resend a text message to admin chat"""
    # await clear(bot, state)   # clear state and edit previous bot message
    print(message.model_dump_json())
    # need special method to serialise Aiogram message .model_dump_json(), json.dumps do incorrect result
    json_obj = json.loads(message.model_dump_json())
    print(type(json_obj))
    print(type(message))
    print()
    data = await state.get_data()
    print(data)
    #determine message type
    msg_type = determine_message_type(message)
    print(msg_type)
    if not msg_type:
        await bot.send_message(chat_id=message.chat.id, text='не понимаю!', reply_to_message_id=message.message_id)

    # delete previous bot msg
    #if data['answer_msg_id']:
    await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    # send new one
    msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )
    # set state to handle callback
    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    # add state data
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_obj,
                            message_type=msg_type)


# create router instance
post_router = Router()
# common filters
# post_router.message.filter(F.chat.type == 'private',
#                            and_f(~F.forward_from, ~F.forward_from_chat),
#                            ~F.media_group_id)
post_router.message.filter(~F.forward_from_chat, ~F.media_group_id)
# register filtered message handlers
post_router.message.register(message_handler,
                             F.text | F.photo | F.video | F.audio | F.voice | F.document | F.animation,
                             PostStates.WAITING_FOR_POST)

