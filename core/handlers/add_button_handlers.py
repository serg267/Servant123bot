from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.keyboards import cancel_keyboard, some_buttons_keyboard, date_keyboard
from core.models.States import PostStates
from core.models.edit_msg_addon import TextAddon


async def button_text_call_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """This is  call button text handler"""
    print(call.model_dump_json())

    data = await state.get_data()

    await bot.edit_message_text(chat_id=data['answer_msg_chat_id'],
                                message_id=data['answer_msg_id'],
                                text='Введи ссылку в формате:'
                                     '\n 1. https://...'
                                     '\n 2. телеграм https://t.me/...'
                                     '\n 3. телеграм @...',
                                reply_markup=cancel_keyboard()
                                )

    await state.update_data(button_text=call.data)
    await state.set_state(PostStates.BUTTON_LINK)


async def button_text_msg_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """This is  message button text handler"""
    print(message.model_dump_json())

    data = await state.get_data()
    quantity = 30

    await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    if message.text and len(message.text) <= quantity:
        msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                     text='Введи ссылку в одном из форматов:'
                                          '\n - https://...'
                                          '\n - телеграм https://t.me/...'
                                          '\n - телеграм @...',
                                     reply_markup=cancel_keyboard()
                                     )
        await state.update_data(button_text=message.text)
        await state.set_state(PostStates.BUTTON_LINK)
    else:
        # added_text = TextAddon()
        msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                     parse_mode='HTML',
                                     text=f'Попробуй еще..\n<b>(Текстовое сообщение не более {quantity} символов)</b>'
                                          f'\nВыбери кнопку или введи свое название',
                                     reply_markup=some_buttons_keyboard()
                                     )
    await state.update_data(answer_msg_id=msg.message_id)


async def button_link_msg_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """This is  message button link handler"""
    print(message.model_dump_json())
    data = await state.get_data()

    await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    if message.text:
        if message.text.startswith(('https://', 'https://t.me/', '@')):
            link = message.text
            if message.text.startswith('@'):
                link = f"https://t.me/{link[1:]}"
            msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                         text='Дата размещения?',
                                         reply_markup=date_keyboard()
                                         )
            await state.update_data(button_link=link)
            await state.set_state(PostStates.DATE)
        else:
            msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                         text='Попробуй еще..\nВведи ссылку в одном из форматов:'
                                              '\n - https://...'
                                              '\n - телеграм https://t.me/...'
                                              '\n - телеграм @...',
                                         reply_markup=cancel_keyboard()
                                         )
    else:
        msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                     text='Попробуй еще..\nВведи ссылку в одном из форматов:'
                                          '\n - https://...'
                                          '\n - телеграм https://t.me/...'
                                          '\n - телеграм @...',
                                     reply_markup=cancel_keyboard()
                                     )

    await state.update_data(answer_msg_id=msg.message_id)


add_button_router = Router()
# common filters
# post_router.message.filter(F.chat.type == 'private',
#                            and_f(~F.forward_from, ~F.forward_from_chat),
#                            ~F.media_group_id)
# add_button_router.message.filter(F.chat.type == 'private')
# register filtered message handlers
add_button_router.callback_query.register(button_text_call_handler, PostStates.BUTTON_TEXT)
add_button_router.message.register(button_text_msg_handler,
                                   F.text | F.photo | F.video | F.audio | F.voice | F.document | F.animation,
                                   PostStates.BUTTON_TEXT)
add_button_router.message.register(button_link_msg_handler,
                                   F.text | F.photo | F.video | F.audio | F.voice | F.document | F.animation,
                                   PostStates.BUTTON_LINK)

