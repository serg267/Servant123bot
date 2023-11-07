import json
import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.commands import command_help
from static import SAY_HELLO


async def command_start(message: Message, bot: Bot,  state: FSMContext) -> None:
    """Command /start handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}!')
    await command_help(message, bot,  state)
    json_str = message.model_dump_json()
    logging.debug(json_str)
    print(json_str)
