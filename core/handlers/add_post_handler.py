from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery

from core.keyboards import cancel_keyboard
from core.models import PostStates


async def call_add_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is adding post handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Пришли пост',
                                reply_markup=cancel_keyboard()
                                )
    await state.update_data(command=call.data)
    await state.set_state(PostStates.WAITING_FOR_POST)

call_router = Router()
call_router.callback_query.register(call_add_handler, F.data == 'add', State())
