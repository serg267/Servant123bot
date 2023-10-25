import json
import logging

from aiogram import Bot
from aiogram.types import Message

from static import SAY_HELLO


async def command_start(message: Message, bot: Bot) -> None:
    """Command /start handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}!')

    json_str = json.dumps(message.__dict__, default=str)
    logging.debug(json_str)
    print(json_str)