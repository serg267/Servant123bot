from typing import Union

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards import start_keyboard
from static import CMDS


async def clear_for_command_help(bot: Bot, state: FSMContext) -> None:
    """clear state and delete previous bot conversation message/s"""
    # check for not empty state. if it is, clear and del previous bot msg
    data = await state.get_data()

    if data.get('answer_msg_id'):
        # try except block for old data in storage which makes bad telegram request
        try:
            await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
        except TelegramBadRequest:
            ...
        finally:
            # clean up state after all
            await state.clear()


def base_commands_string() -> str:
    """make base commands string"""
    string = ''
    for command, text in CMDS.items():
        string = string + f"{command} - {text}\n"
    return string


async def command_help(event: Union[Message, CallbackQuery], bot: Bot, state: FSMContext) -> None:
    """Command /help handler"""
    await clear_for_command_help(bot=bot, state=state)
    msg = await bot.send_message(chat_id=event.from_user.id, text=base_commands_string())
    await state.update_data(answer_msg_id=msg.message_id, answer_msg_chat_id=msg.chat.id)

