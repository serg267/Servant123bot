from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, any_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import sessionmaker

from core.commands import command_commands
from core.db import group_from_today, objects_from_date, get_db_message, delete_db_message
from core.scheduler import delete_job
from core.keyboards import msg_id_delete_keyboard, cancel_keyboard, db_days_delete_keyboard
from core.logics import show_information, delete_information
from core.models import PostStates


async def call_delete_show_handler(call: CallbackQuery,
                                   bot: Bot, session_maker: sessionmaker,
                                   state: FSMContext
                                   ) -> None:
    """This is command delete or show callback handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()
    await state.clear()
    dates_and_quantities = await group_from_today(session_maker)
    print(dates_and_quantities)
    msg = await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                      message_id=data['answer_msg_id'],
                                      text='Выбери дату',
                                      reply_markup=db_days_delete_keyboard(dates_and_quantities)
                                      )
    await state.update_data(command=call.data, answer_msg_id=msg.message_id, answer_msg_chat_id=msg.chat.id)
    await state.set_state(PostStates.ALL_POST_FROM_DATE)


async def message_delete_show_handler(message: Message,
                                      bot: Bot,
                                      session_maker: sessionmaker,
                                      state: FSMContext
                                      ) -> None:
    """This is command delete or show  message handler"""
    json_str = message.model_dump_json()
    print(json_str)
    data = await state.get_data()
    await state.clear()
    dates_and_quantities = await group_from_today(session_maker)

    try:
        await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    except KeyError:
        pass

    msg = await bot.send_message(chat_id=message.chat.id,
                                 text='Выбери дату',
                                 reply_markup=db_days_delete_keyboard(dates_and_quantities)
                                 )

    command = 'delete' if 'delete' in message.text else 'show'
    await state.update_data(command=command, answer_msg_id=msg.message_id, answer_msg_chat_id=msg.chat.id)
    await state.set_state(PostStates.ALL_POST_FROM_DATE)


async def remove_select_post_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is post remove handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()

    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Выбери сообщение ',
                                )
    db_messages = await objects_from_date(the_day=call.data, session_maker=session_maker)
    # add logic if no one message
    send_msgs = {}
    if data['command'] == 'delete':
        for db_message in db_messages:
            msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                         text=show_information(db_message),
                                         parse_mode='HTML',
                                         reply_markup=msg_id_delete_keyboard(db_message.id))
            send_msgs.update({str(db_message.id): msg.message_id})
    # if data['command'] == 'show'
    else:
        for db_message in db_messages:
            msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                         text=show_information(db_message),
                                         parse_mode='HTML',
                                         reply_markup=cancel_keyboard(mode=1))
            send_msgs.update({str(db_message.id): msg.message_id})

    await state.update_data(send_msgs=send_msgs)
    await state.set_state(PostStates.DELETE_THE_POST)


async def remove_post_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is post remove handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()
    send_msgs: dict = data['send_msgs']

    for db_message_id, msg_id in send_msgs.items():
        await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=msg_id)

    db_message = await get_db_message(db_message_id=int(call.data), session_maker=session_maker)
    if db_message:

        # delete scheduler from scheduler and message and message from database
        if db_message.post_job_id:
            await delete_job(db_message.post_job_id)
        if db_message.delete_job_id:
            await delete_job(db_message.delete_job_id)
        await delete_db_message(db_message, session_maker)

        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text=delete_information(db_message),
                                    parse_mode='HTML',
                                    )
    await state.clear()
    await command_commands(call, bot, state)


remove_router = Router()
remove_router.callback_query.register(call_delete_show_handler, F.data.in_(['delete', 'show']), any_state)
remove_router.message.register(message_delete_show_handler, any_state, Command(commands=['delete', 'show']))
remove_router.callback_query.register(remove_select_post_handler, PostStates.ALL_POST_FROM_DATE)
remove_router.callback_query.register(remove_post_handler, PostStates.DELETE_THE_POST)
