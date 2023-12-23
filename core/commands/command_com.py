from typing import Union

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.commands.command_help import clear_for_command_help
from core.keyboards import start_keyboard


async def command_commands(message: Union[Message, CallbackQuery], bot: Bot, state: FSMContext) -> None:
    """Command /commands handler"""

    await clear_for_command_help(bot=bot, state=state)

    msg = await bot.send_message(chat_id=message.from_user.id,
                                 text='Выбери команду',
                                 reply_markup=start_keyboard()
                                 )
    # await state.set_state(PostStates.WAITING_FOR_POST)
    await state.update_data(answer_msg_id=msg.message_id, answer_msg_chat_id=msg.chat.id)
