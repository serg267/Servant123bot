from typing import Dict, Any

from aiogram.types import Message


# def determine_message_type(message: Message) -> str | None:
#     """determine message type: text, photo, video, audio, voice, document, animation or None"""
#     if message.text:
#         msg_type = 'text'
#     elif message.photo:
#         msg_type = 'photo'
#     elif message.video:
#         msg_type = 'video'
#     elif message.audio:
#         msg_type = 'audio'
#     elif message.voice:
#         msg_type = 'voice'
#     elif message.document:
#         msg_type = 'document'
#     elif message.animation:
#         msg_type = 'animation'
#     else:
#         msg_type = None
#     return msg_type

def determine_message_type(message: Message | dict) -> str | None:
    """determine message type: text, photo, video, audio, voice, document, animation or None"""
    names = ['text', 'photo', 'video', 'audio', 'voice', 'document', 'animation']

    if isinstance(message, Message):
        func = message.__getattribute__
    elif isinstance(message, dict):
        func = message.get
    else:
        raise ValueError

    for name in names:
        if func(name):
            return name
    else:
        return None



    # if isinstance(message, Message):
    #     for name in names:
    #         if message.__getattribute__(name):
    #             print(name)
    #             return name
    #     else:
    #         return None
    # elif isinstance(message, dict):
    #     for name in names:
    #         if message.get(name):
    #             return name
    #     else:
    #         return None
    # else:
    #     raise ValueError
