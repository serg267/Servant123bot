from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


def start_keyboard() -> InlineKeyboardMarkup:
    """
    return keyboard: добавить посмотреть удалить
    :return:
    """

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='добавить', callback_data='добавить'),
            ],
            [
                InlineKeyboardButton(text='посмотреть', callback_data='посмотреть')
            ]
            ,
            [
                InlineKeyboardButton(text='удалить', callback_data='удалить')
            ]
        ])

    return keyboard


def yes_no_keyboard() -> InlineKeyboardMarkup:
    """
    return keyboard: да нет отмена
    :return:
    """

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='да', callback_data='да'),
            ],
            [
                InlineKeyboardButton(text='нет', callback_data='нет')
            ],
            [
                InlineKeyboardButton(text='отмена', callback_data='отмена'),
            ],
        ])

    return keyboard


def cancel_keyboard(mode: int = 0) -> InlineKeyboardMarkup:
    """
    return keyboard: отмена
    :return:
    """

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='отмена', callback_data='отмена'),
            ],
        ])
    if mode == 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='<<', callback_data='отмена'),
                ],
            ])

    return keyboard


def some_buttons_keyboard() -> InlineKeyboardMarkup:
    """
    return keyboard: перейти подписаться жми подробнее отмена
    :return:
    """

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='перейти', callback_data='перейти'),
                InlineKeyboardButton(text='подписаться', callback_data='подписаться'),
            ],
            [
                InlineKeyboardButton(text='жми', callback_data='жми'),
                InlineKeyboardButton(text='подробнее', callback_data='подробнее'),
            ],
            [
                InlineKeyboardButton(text='отмена', callback_data='отмена'),
            ],
        ])

    return keyboard


def url_button_keyboard(text, url_link) -> InlineKeyboardMarkup:
    """
    return keyboard: url_button
    :return:
    """

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, url=url_link)
            ]
        ])

    return keyboard


def msg_id_delete_keyboard(db_msg_id: Union[str, int]) -> InlineKeyboardMarkup:
    """
    return keyboard: db_msg_id_button отмена
    :return:
    """
    if isinstance(db_msg_id, int):
        db_msg_id = str(db_msg_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='удалить', callback_data=db_msg_id),
                InlineKeyboardButton(text='отмена', callback_data='отмена')
            ],
        ])

    return keyboard
