import json

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker

from core.db import group_from_today, objects_from_date
from core.keyboards.db_keyboards import db_days_delete_keyboard
from core.models.States import PostStates


async def remove_date_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is date remove handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()
    dates_and_quantities = await group_from_today(session_maker)
    print(dates_and_quantities)
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Выбери дату',
                                reply_markup=db_days_delete_keyboard(dates_and_quantities)
                                )
    await state.set_state(PostStates.DELETE_THIS_POST)


async def remove_post_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is post remove handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()
    dates_and_quantities = await objects_from_date(the_day=call.data, session_maker=session_maker)
    for x in dates_and_quantities:
        await bot.send_message(chat_id=data['answer_msg_chat_id'], text=x.message_type)
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Выбери сообщение',
                                # reply_markup=db_days_delete_keyboard(dates_and_quantities)
                                )
    await state.set_state(State())


remove_router = Router()
remove_router.callback_query.register(remove_date_handler, F.data == 'удалить', State())
remove_router.callback_query.register(remove_post_handler, PostStates.DELETE_THIS_POST)
