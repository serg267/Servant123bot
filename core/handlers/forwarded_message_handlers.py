from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.handlers.message_handlers import cook_next_step_date_or_button
from core.logics import determine_message_type
from core.models import PostStates


async def forwarded_message_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """This handler will forward message to admin chat"""
    print(message.model_dump_json())

    data = await state.get_data()
    message_type = 'forwarded'
    if data['post_type'] == 'advertisement':
        message_type = determine_message_type(message)

    # send message  button or date, change state and store data
    await cook_next_step_date_or_button(message=message, bot=bot, state=state, msg_type=message_type)


# create router instance
forwarded_router = Router()
# common filters
forwarded_router.message.filter(~F.media_group_id)
# register filtered message handler
forwarded_router.message.register(forwarded_message_handler, F.forward_from_chat, PostStates.WAITING_FOR_POST)
