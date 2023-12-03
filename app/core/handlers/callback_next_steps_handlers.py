from datetime import datetime, timedelta
from typing import Dict, Callable

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker


from app.core.commands import command_help
from app.core.db import Messages, set_post_job_id, add_message, get_db_message
from app.core.models import PostStates
from app.core.scheduler import add_one_job
from app.core.keyboards import date_keyboard, hours_keyboard, hours_minutes_keyboard, days_deregister_keyboard,\
    yes_no_keyboard, some_buttons_keyboard
from app.core.logics import post, determine_message_type, post_then_delete, post_information


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
    await command_help(call, bot,  state)


async def call_post_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is call post handler"""
    print(call.model_dump_json())

    data = await state.get_data()

    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Дата размещения?',
                                reply_markup=date_keyboard()
                                )

    await state.set_state(PostStates.DATE)
    await state.update_data(post_type=call.data)


async def call_adv_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This call advertisement handler"""
    data = await state.get_data()

    # change message type to text, video or ... if forwarded
    if data['message_type'] == 'forwarded':
        message_type = determine_message_type(data['message_json'])
        await state.update_data(message_type=message_type)
        # refresh
        data = await state.get_data()

    if data['message_type'] not in ['media_group', 'forwarded']:
        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='Добавить кнопку?',
                                    reply_markup=yes_no_keyboard()
                                    )
        await state.set_state(PostStates.ADD_BUTTON)
    else:
        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='Дата размещения?',
                                    reply_markup=date_keyboard()
                                    )

        await state.set_state(PostStates.DATE)
    await state.update_data(post_type=call.data)


async def button_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is  call yes no button handler"""
    print(call.model_dump_json())

    data = await state.get_data()
    if call.data == 'да':
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
    print(call.model_dump_json())

    data = await state.get_data()
    print()
    print()
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
    data = await state.get_data()
    # add time to date (combine datetime)
    # the_date = datetime.combine(datetime.strptime(data['post_date'], '%d.%m.%Y'),
    #                             datetime.strptime(call.data, '%H:%M').time())
    # the_date = datetime.now() + timedelta(minutes=2)  # test date
    the_date = f"{data['post_date']} {call.data}"
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
        case 'пост':
            # # save to db
            # db_message = await add_message(db_message, session_maker)
            # print(db_message)

            # add job; set job id to db; bot send edited message
            await notice_and_save_jobs(post, db_message, bot, data, session_maker)

            # clear state before command_help to skip deleting previous message
            # clear state before command_help to skip deleting previous message
            await state.clear()
            await command_help(call, bot, state)

        case 'реклама':
            await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                        message_id=data['answer_msg_id'],
                                        text='Автоудаление через?',
                                        reply_markup=days_deregister_keyboard()
                                        )
            await state.update_data(db_message_id=db_message.id)
            await state.set_state(PostStates.DEREGISTER_ADVERTISEMENT)


async def call_deregister_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is post delete date handler"""
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
    await command_help(call, bot, state)

# create router instance
call_steps_router = Router()
# register callback_query
call_steps_router.callback_query.register(cancel_callback_handler, F.data == 'отмена', State(state="*"))
call_steps_router.callback_query.register(call_post_handler, F.data == 'пост', PostStates.POST_OR_ADVERTISEMENT)
call_steps_router.callback_query.register(call_adv_handler, F.data == 'реклама', PostStates.POST_OR_ADVERTISEMENT)
call_steps_router.callback_query.register(button_handler, F.data.in_(['да', 'нет']), PostStates.ADD_BUTTON)
call_steps_router.callback_query.register(call_date_handler, PostStates.DATE)
call_steps_router.callback_query.register(call_hours_handler, PostStates.HOURS)
call_steps_router.callback_query.register(call_minutes_handler, PostStates.HOURS_MINUTES)
call_steps_router.callback_query.register(call_deregister_handler, PostStates.DEREGISTER_ADVERTISEMENT)