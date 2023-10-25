import asyncio
import json
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message

from config import ADMIN_2, ADMIN_1


class IsAdminMiddleware(BaseMiddleware):
    """This middleware is for allowed admin only."""
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        # json_str = json.dumps(event.__dict__, default=str)
        # print(json_str)
        # print(event.chat.id not in [int(ADMIN_1), int(ADMIN_2)])

        if event.chat.id not in [int(ADMIN_1), int(ADMIN_2)]:  # if it's not admin
            # await event.answer(f'{event.from_user.first_name}, реагирую только на хозяев\nИзвини.. ')
            return
        return await handler(event, data)
