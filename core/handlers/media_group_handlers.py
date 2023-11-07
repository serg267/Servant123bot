import json

from aiogram import Bot, Router, F
from aiogram.types import Message, InputMediaPhoto,  InputMediaVideo, InputMediaDocument, InputMediaAudio, \
    InputMediaAnimation

from config import ADMINCHAT
from core.handlers.message_handlers import clear
from core.keyboards import choice_keyboard
from core.models.States import PostStates
from core.models.models import LinkedMessage
from static import EMO1
from aiogram.fsm.context import FSMContext


async def forward_media_to_admin_chat(message: Message, bot: Bot, album: list[Message], state: FSMContext) -> None:
    """This handler will forward a complete album of any type."""
    print(message.model_dump_json())
    # need special method to serialise Aiogram message .model_dump_json(), json.dumps do incorrect result
    json_obj = json.loads(message.model_dump_json())

    data = await state.get_data()

    if not album:
        json_album = [json.loads(message.model_dump_json())]
    else:
        json_album = [json.loads(message.model_dump_json()) for message in album]

    # delete previous bot msg
    await bot.delete_message(chat_id=data['answer_msg_chat_id'], message_id=data['answer_msg_id'])
    # send new one
    msg = await bot.send_message(chat_id=data['answer_msg_chat_id'],
                                 text='Выбери пост или реклама?',
                                 reply_markup=choice_keyboard()
                                 )
    # set state to handle callback
    await state.set_state(PostStates.POST_OR_ADVERTISEMENT)
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
