from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def cancel_keyboard() -> InlineKeyboardMarkup:
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
