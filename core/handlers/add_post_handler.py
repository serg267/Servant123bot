from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import CallbackQuery, Message

from core.keyboards import choice_keyboard
from core.models import PostStates


async def call_add_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is adding post handler"""
    json_str = call.model_dump_json()
    print(json_str)

    data = await state.get_data()
    await state.clear()

    msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )
    # msg = await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
    #                                   message_id=data['answer_msg_id'],
    #                                   text='Пришли пост',
    #                                   reply_markup=cancel_keyboard()
    #                                   )
    await state.update_data(command=call.data,
                            answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id)
    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    # await state.set_state(PostStates.WAITING_FOR_POST)


async def message_add_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """This is adding post handler"""
    json_str = message.model_dump_json()
    print(json_str)

    data = await state.get_data()
    try:
        await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    except KeyError:
        pass

    await state.clear()

    msg = await bot.send_message(chat_id=message.chat.id,
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )
    await state.update_data(command='add', answer_msg_id=msg.message_id, answer_msg_chat_id=msg.chat.id)
    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
    # await state.set_state(PostStates.WAITING_FOR_POST)

call_router = Router()
call_router.callback_query.register(call_add_handler, F.data == 'add', any_state)
call_router.message.register(message_add_handler,  any_state, Command(commands=['add']))
