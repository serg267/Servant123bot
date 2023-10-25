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
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    await clear(bot, state)   # clear state and edit previous bot message

    msg = await bot.send_message(chat_id=ADMINCHAT,
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )

    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_str,
                            message_id=message.message_id,
                            message_type='forwarded')
    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)


# create router instance
forwarded_post_router = Router()
# register filtered message handler
forwarded_post_router.message.register(forwarded_message_handler, F.forward_from_chat, ~F.media_group_id)
