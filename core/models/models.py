from typing import Tuple

from aiogram.types import Message


class SetGetDescriptor:
    """дескриптор данных"""
    def __set_name__(self, owner, name) -> None:
        self.name = name

    def __set__(self, instance, value) -> None:
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner) -> classmethod:
        return instance.__dict__[self.name]


class LinkedMessage(object):
    __linked_messages = {}
    this_message_id = SetGetDescriptor()
    this_message_chat_id = SetGetDescriptor()
    first_message_id = SetGetDescriptor()
    first_message_chat_id = SetGetDescriptor()

    def __init__(self, this_message_id: int, this_message_chat_id: int) -> None:
        self.this_message_id = this_message_id
        self.this_message_chat_id = this_message_chat_id
        self.first_message_id = None
        self.first_message_chat_id = None

        LinkedMessage.add_element((this_message_id, this_message_chat_id), self)

    @classmethod
    def add_element(cls, msg_id_and_chat_id_tuple: Tuple[int, int], linked_msg: 'LinkedMessage') -> None:
        """adds an instance of the class to the class dictionary"""

        cls.__linked_messages[msg_id_and_chat_id_tuple] = linked_msg

    @classmethod
    def get_element(cls, this_message_id: int, this_message_chat_id: int) -> 'LinkedMessage':
        """gets an instance of the class dictionary"""
        print((this_message_id, this_message_chat_id))
        return cls.__linked_messages.get((this_message_id, this_message_chat_id))

    def set_first_msg(self, msg: Message) -> None:
        """sets message_id and chat_id to the instance"""
        self.first_message_id = msg.message_id
        self.first_message_chat_id = msg.chat.id
