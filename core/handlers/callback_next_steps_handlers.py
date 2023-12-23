import logging
from datetime import datetime, timedelta
from typing import Dict, Callable

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker


from core.commands import command_commands
from core.db import Messages, set_post_job_id, add_message, get_db_message
from core.models import PostStates
from core.scheduler import add_one_job
from core.keyboards import date_keyboard, hours_keyboard, hours_minutes_keyboard, days_deregister_keyboard, \
    some_buttons_keyboard, cancel_keyboard
from core.logics import post, post_then_delete, post_information


async def notice_and_save_jobs(func: Callable, db_message: Messages, bot: Bot, data: Dict,
                               session_maker: sessionmaker) -> None:
    # add job
    job_id = await add_one_job(func=func, dtime=db_message.post_date,
                               kwargs={'db_message': db_message, 'bot': bot, 'session_maker': session_maker})
    # set job id to db
    await set_post_job_id(db_message.id, job_id, session_maker)

    # bot send edited message
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text=post_information(db_message),
                                parse_mode='HTML')


async def cancel_callback_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This handler drops state and it's data"""
    data = await state.get_data()
    send_msgs: dict = data.get('send_msgs')
    if send_msgs is not None:
        for db_message_id, msg_id in send_msgs.items():
            print(msg_id)
            await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=msg_id)
    await command_commands(call, bot, state)


async def call_post_type_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is call post handler"""
    logging.debug('call_post_type_handler')
    print(call.model_dump_json())

    data = await state.get_data()

    msg = await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                      message_id=data['answer_msg_id'],
                                      text='Пришли пост',
                                      reply_markup=cancel_keyboard()
                                      )

    await state.update_data(post_type=call.data,
                            answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id)
    await state.set_state(PostStates.WAITING_FOR_POST)


async def button_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is  call yes no button handler"""
    logging.debug('button_handler')
    print(call.model_dump_json())

    data = await state.get_data()
    if call.data == 'yes':
        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='Выбери кнопку или введи свое название',
                                    reply_markup=some_buttons_keyboard()
                                    )
        await state.set_state(PostStates.BUTTON_TEXT)
    else:
        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='Дата размещения?',
                                    reply_markup=date_keyboard()
                                    )

        await state.set_state(PostStates.DATE)


async def call_date_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is post date handler"""
    logging.debug('call_date_handler')
    print(call.model_dump_json())

    data = await state.get_data()
    is_today = (datetime.strptime(call.data, '%d.%m.%Y').date() == datetime.today().date())

    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='В котором часу?',
                                reply_markup=hours_keyboard(is_today)
                                )
    await state.set_state(PostStates.HOURS)
    # await state.update_data(post_date=call.data)
    # await state.update_data(post_date=datetime.strptime(call.data, '%d.%m.%Y'), is_today=is_today)
    await state.update_data(post_date=call.data, is_today=is_today)


async def call_hours_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is post hours handler"""
    logging.debug('call_hours_handler')
    print(call.model_dump_json())

    data = await state.get_data()
    print()
    print(data)
    # print(data['answer_msg_id'], call.data, type(call.data))
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Уточни..',
                                reply_markup=hours_minutes_keyboard(is_today=data['is_today'], hour=call.data)
                                )
    await state.set_state(PostStates.HOURS_MINUTES)


async def call_minutes_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is post hours:minutes handler"""
    logging.debug('call_minutes_handler')

    data = await state.get_data()
    # the_date = f"{data['post_date']} {call.data}"

    # add time to date (combine datetime)
    # the_date = datetime.combine(datetime.strptime(data['post_date'], '%d.%m.%Y'),
    #                             datetime.strptime(call.data, '%H:%M').time())
    the_date = datetime.now() + timedelta(minutes=2)  # test date
    the_date = the_date.strftime('%d.%m.%Y %H:%M')

    print('the date :', the_date)
    await state.update_data(post_date=the_date)

    # form db message object
    db_message = Messages(message_json=data['message_json'],
                          message_type=data['message_type'],
                          post_type=data['post_type'],
                          post_date=datetime.strptime(the_date, '%d.%m.%Y %H:%M')
                          )
    if data.get('button_text') and data.get('button_link'):
        db_message.button = [data.get('button_text'), data.get('button_link')]
    # save to db
    db_message = await add_message(db_message, session_maker)

    match data['post_type']:
        case 'post':
            # # save to db
            # db_message = await add_message(db_message, session_maker)
            # print(db_message)

            # add job; set job id to db; bot send edited message
            await notice_and_save_jobs(post, db_message, bot, data, session_maker)

            # clear state before command_help to skip deleting previous message
            # clear state before command_help to skip deleting previous message
            await state.clear()

        case 'advertisement':
            await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                        message_id=data['answer_msg_id'],
                                        text='Автоудаление через?',
                                        reply_markup=days_deregister_keyboard()
                                        )
            await state.update_data(db_message_id=db_message.id)
            await state.set_state(PostStates.DEREGISTER_ADVERTISEMENT)


async def call_deregister_handler(call: CallbackQuery,
                                  bot: Bot,
                                  session_maker: sessionmaker,
                                  state: FSMContext
                                  ) -> None:
    """This is post delete date handler"""
    logging.debug('call_deregister_handler')

    data = await state.get_data()

    # add data to db message object
    db_message: Messages = await get_db_message(data['db_message_id'], session_maker)
    db_message.delete_date = datetime.strptime(data['post_date'], '%d.%m.%Y %H:%M') + timedelta(days=int(call.data))

    # save to db
    db_message = await add_message(db_message, session_maker)

    # add job; set job id to db; bot send edited message
    await notice_and_save_jobs(post_then_delete, db_message, bot, data, session_maker)

    # clear state before command_help to skip deleting previous message
    await state.clear()

# create router instance
call_steps_router = Router()
# register callback_query
call_steps_router.callback_query.register(cancel_callback_handler, F.data == 'cancel', any_state)
call_steps_router.callback_query.register(call_post_type_handler, PostStates.POST_OR_ADVERTISEMENT)
call_steps_router.callback_query.register(button_handler, F.data.in_(['yes', 'no']), PostStates.ADD_BUTTON)
call_steps_router.callback_query.register(call_date_handler, PostStates.DATE)
call_steps_router.callback_query.register(call_hours_handler, PostStates.HOURS)
call_steps_router.callback_query.register(call_minutes_handler, PostStates.HOURS_MINUTES)
call_steps_router.callback_query.register(call_deregister_handler, PostStates.DEREGISTER_ADVERTISEMENT)
