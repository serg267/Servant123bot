import json
import logging

from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.keyboards import date_keyboard
from core.models import PostStates


async def forward_media_to_admin_chat(message: Message, bot: Bot, album: list[Message], state: FSMContext) -> None:
    """This handler will forward a complete album of any type."""
    logging.debug('forward_media_to_admin_chat')

    print(message.model_dump_json())

    data = await state.get_data()

    json_album = [json.loads(message.model_dump_json()) for message in album]
    exceed_captions = [len(message.caption) - 1024 for message in album if message.caption]

    print(exceed_captions)

    if max(exceed_captions) > 0:
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Cократи пост на {max(exceed_captions)} символов',
                               reply_to_message_id=message.message_id)
        return

    # delete previous bot msg
    await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    # send new one
    msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                 text='Дата размещения?',
                                 reply_markup=date_keyboard()
                                 )
    # msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
    #                              text='Выбери пост или реклама?',
    #                              reply_markup=choice_keyboard()
    #                              )
    # set state to handle callback
    await state.set_state(PostStates.DATE)
    # add state data
    await state.update_data(answer_msg_id=msg.message_id,
                            answer_msg_chat_id=msg.chat.id,
                            message_json=json_album,
                            message_type='media_group')


# create router instance
media_group_router = Router()
# common filter
media_group_router.message.filter(F.media_group_id)
# register filtered message handler
media_group_router.message.register(forward_media_to_admin_chat,
                                    F.text | F.photo | F.audio | F.video | F.document | F.voice,
                                    PostStates.WAITING_FOR_POST)
