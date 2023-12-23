from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choice_keyboard() -> InlineKeyboardMarkup:
    """
    return keyboard: пост реклама отмена
    :return:
    """

    some_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='пост', callback_data='post'),

            ],
            [
                InlineKeyboardButton(text='реклама', callback_data='advertisement')
            ],
            [
                InlineKeyboardButton(text='отмена', callback_data='cancel')
            ]
        ])

    return some_keyboard
