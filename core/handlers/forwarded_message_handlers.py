import json

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMINCHAT
from core.handlers.message_handlers import clear
from core.keyboards import choice_keyboard
from core.models.States import PostStates


async def forwarded_message_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """This handler will forward message to admin chat"""
    print(message.model_dump_json())
    # need special method to serialise Aiogram message .model_dump_json(), json.dumps do incorrect result
    json_obj = json.loads(message.model_dump_json())

    data = await state.get_data()

    # delete previous bot msg
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
                            message_type='forwarded')


# create router instance
forwarded_router = Router()
# common filters
forwarded_router.message.filter(~F.media_group_id)
# register filtered message handler
forwarded_router.message.register(forwarded_message_handler, F.forward_from_chat, PostStates.WAITING_FOR_POST)
