from typing import Union

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import ADMINCHAT
from core.keyboards import start_keyboard
from core.models.States import PostStates


async def command_help(message: Union[Message, CallbackQuery], bot: Bot, state: FSMContext) -> None:
    """Command /help handler"""

    # check for not empty state. if it is, clear and del previous bot msg
    data = await state.get_data()
    if data.get('answer_msg_id'):
        await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    await state.clear()

    msg = await bot.send_message(chat_id=message.from_user.id,
                                 text='Выбери команду',
                                 reply_markup=start_keyboard()
                                 )
    # await state.set_state(PostStates.WAITING_FOR_POST)
    await state.update_data(answer_msg_id=msg.message_id, answer_msg_chat_id=msg.chat.id)
