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
    await clear(bot, state)   # clear state and edit previous bot message

    print('88')
    print(message.model_dump_json())
    json_obj = json.loads(message.model_dump_json())

    msg = await bot.send_message(chat_id=ADMINCHAT,
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )

    # set state to handle callback
    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    # add state data
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_obj,
                            # message_id=message.message_id,
                            message_type='forwarded')


# create router instance
forwarded_router = Router()
# common filters
forwarded_router.message.filter(~F.media_group_id)
# register filtered message handler
forwarded_router.message.register(forwarded_message_handler, F.forward_from_chat)
