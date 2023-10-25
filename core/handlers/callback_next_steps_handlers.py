import asyncio
import json
import locale
from datetime import date, datetime, timedelta

from aiogram import Bot, Router, F
from aiogram.filters import and_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import ADMINCHAT
from core.db import Messages, add_message, set_post_job_id, set_p_d_jobs_id
from core.jobs.schedule import add_one_job
from core.keyboards import date_keyboard, hours_keyboard, hours_minutes_keyboard, delete_keyboard, string_days
from core.logics import post, delete

from core.models.States import PostStates


async def cancel_callback_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This handler drops state and it's data"""
    data = await state.get_data()
    await state.clear()
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='отмена'
                                )
    # await asyncio.sleep(30)
    # await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])


async def call_post_or_advertisement_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is post or advertisement handler"""
    json_str = json.dumps(call.__dict__, default=str)
    print(json_str)
    data = await state.get_data()
    print(data['answer_msg_id'], call.data, type(call.data))
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Дата размещения?',
                                reply_markup=date_keyboard()
                                )
    await state.set_state(PostStates.DATE)
    await state.update_data(post_type=call.data)


async def call_date_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is post date handler"""
    json_str = json.dumps(call.__dict__, default=str)
    print(json_str)
    data = await state.get_data()
    is_today = (datetime.strptime(call.data, '%d.%m.%Y').date() == datetime.today().date())

    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='В котором часе?',
                                reply_markup=hours_keyboard(is_today)
                                )
    await state.set_state(PostStates.HOURS)
    # await state.update_data(post_date=call.data)
    await state.update_data(post_date=datetime.strptime(call.data, '%d.%m.%Y'), is_today=is_today)


async def call_hours_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is post hours handler"""
    json_str = json.dumps(call.__dict__, default=str)
    print(json_str)
    data = await state.get_data()
    print(data['answer_msg_id'], call.data, type(call.data))
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Уточни..',
                                reply_markup=hours_minutes_keyboard(is_today=data['is_today'], hour=call.data)
                                )
    await state.set_state(PostStates.HOURS_MINUTES)


async def call_minutes_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext,
                               async_scheduler: AsyncIOScheduler) -> None:
    """This is post hours:minutes handler"""
    data = await state.get_data()
    the_date = datetime.combine(data['post_date'], datetime.strptime(call.data, '%H:%M').time())  # combine date
    await state.update_data(post_date=the_date)

    # form db message object
    db_message = Messages(message_json=data['message_json'],
                          message_type=data['message_type'],
                          post_type=data['post_type'],
                          post_date=the_date
                          )

    match data['post_type']:
        case 'пост':
            # save to db
            db_message = await add_message(db_message, session_maker)
            print(db_message)
            # add job
            job_id = await add_one_job(func=post, dtime=db_message.post_date,
                                       kwargs={'db_message': db_message, 'bot': bot, 'session_maker': session_maker})
            # set job id to db
            await set_post_job_id(db_message.id, job_id, session_maker)

            the_date = db_message.post_date
            text = f"Размещение поста\n{the_date.strftime('%d.%m.%Y')} в {the_date.strftime('%H:%M')}"

            await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                        message_id=data['answer_msg_id'],
                                        text=text
                                        )
        case 'реклама':
            await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                        message_id=data['answer_msg_id'],
                                        text='Автоудаление через?',
                                        reply_markup=delete_keyboard()
                                        )
            await state.update_data(db_message=db_message)
            await state.set_state(PostStates.DELETE)


async def call_delete_handler(call: CallbackQuery, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This is post delete date handler"""
    data = await state.get_data()

    # add data to db message object
    db_message: Messages = data['db_message']
    db_message.delete_date = data['post_date'] + timedelta(days=int(call.data))

    # save to db
    db_message = await add_message(db_message, session_maker)
    # add jobs
    post_job_id = await add_one_job(func=post, dtime=db_message.post_date,
                                    kwargs={'db_message': db_message, 'bot': bot, 'session_maker': session_maker})
    delete_job_id = await add_one_job(func=delete, dtime=db_message.post_date,
                                      kwargs={'db_message': db_message, 'bot': bot, 'session_maker': session_maker})
    # set jobs id to db
    await set_p_d_jobs_id(db_message.id, post_job_id, delete_job_id, session_maker)

    # bot send edited message
    the_date = data['post_date']
    text = f"Размещение рекламы \n{the_date.strftime('%d.%m.%Y')} в {the_date.strftime('%H:%M')}" \
           f"\nавтоудаление через {string_days(call.data)}"
    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'], text=text)

    # state clear
    await state.clear()


# create router instance
post_msg_next_steps_router = Router()
# register callback_query
post_msg_next_steps_router.callback_query.register(cancel_callback_handler, F.data == 'отмена', State(state="*"))
post_msg_next_steps_router.callback_query.register(call_post_or_advertisement_handler, PostStates.POST_OR_ADVERTISEMENT)
post_msg_next_steps_router.callback_query.register(call_date_handler, PostStates.DATE)
post_msg_next_steps_router.callback_query.register(call_hours_handler, PostStates.HOURS)
post_msg_next_steps_router.callback_query.register(call_minutes_handler, PostStates.HOURS_MINUTES)
post_msg_next_steps_router.callback_query.register(call_delete_handler, PostStates.DELETE)
