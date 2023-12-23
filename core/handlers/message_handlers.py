
import json


from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from sqlalchemy.orm import sessionmaker

from core.keyboards import date_keyboard, yes_no_keyboard
from core.logics import determine_message_type
from core.models import PostStates


async def clear(bot: Bot, state: FSMContext) -> None:
    """Catch message with set state,  clear state and edit previous bot message"""
    if await state.get_state() is not None:
        data = await state.get_data()
        await state.clear()
        # delete messages from data list before clear
        if data.get('send_msgs'):
            send_msgs = data['send_msgs']
            for db_message_id, msg_id in send_msgs.items():
                await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=msg_id)

        await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                    message_id=data['answer_msg_id'],
                                    text='отмена'
                                    )


async def msg_too_long(message: Message, bot: Bot) -> bool:
    """determine too long for telegram posts"""
    msg_type = determine_message_type(message)

    if msg_type == 'text':
        delta_length_exceed = len(message.text) - 4096
    else:
        delta_length_exceed = len(message.caption) - 1024
    print(delta_length_exceed)

    if delta_length_exceed > 0:
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Cократи пост на {delta_length_exceed} символов',
                               reply_to_message_id=message.message_id)
        return True
    return False


async def send_msg_next_step_date_or_button(state: FSMContext, bot: Bot) -> Message:
    """send next step button or date question message and change state"""
    data = await state.get_data()

    match data['post_type']:
        case 'post':
            msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                         text='Дата размещения?',
                                         reply_markup=date_keyboard()
                                         )
            await state.set_state(PostStates.DATE)
        case _:
            msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                         text='Добавить кнопку?',
                                         reply_markup=yes_no_keyboard()
                                         )
            await state.set_state(PostStates.ADD_BUTTON)
    return msg


async def cook_next_step_date_or_button(message: Message, state: FSMContext, bot: Bot, msg_type: str) -> None:
    """send message with next state: button or date, change state and store data"""
    json_obj = json.loads(message.model_dump_json())
    data = await state.get_data()
    too_long = await msg_too_long(message, bot)
    if too_long:
        return

    # delete previous bot msg
    await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])

    # send new one button or date, change state and store data
    msg = await send_msg_next_step_date_or_button(state=state, bot=bot)

    # add state data
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_obj,
                            message_type=msg_type)


async def message_handler(message: Message, bot: Bot, session_maker: sessionmaker, state: FSMContext) -> None:
    """This handler will resend a text message to admin chat"""
    # await clear(bot, state)   # clear state and edit previous bot message
    print(message.model_dump_json())

    # determine message type
    message_type = determine_message_type(message)
    print(message_type)

    if not message_type:
        await bot.send_message(chat_id=message.chat.id, text='не понимаю!', reply_to_message_id=message.message_id)

    # send message  button or date, change state and store data
    await cook_next_step_date_or_button(message=message, bot=bot, state=state, msg_type=message_type)


# create router instance
post_router = Router()
# common filters
# post_router.message.filter(F.chat.type == 'private',
#                            and_f(~F.forward_from, ~F.forward_from_chat),
#                            ~F.media_group_id)
post_router.message.filter(~F.forward_from_chat, ~F.media_group_id)
# register filtered message handlers
post_router.message.register(message_handler,
                             F.text | F.photo | F.video | F.audio | F.voice | F.document | F.animation,
                             PostStates.WAITING_FOR_POST)

