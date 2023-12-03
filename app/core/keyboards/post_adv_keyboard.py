from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choice_keyboard() -> InlineKeyboardMarkup:
    """
    return keyboard: пост реклама отмена
    :return:
    """

    some_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='пост', callback_data='пост'),

            ],
            [
                InlineKeyboardButton(text='реклама', callback_data='реклама')
            ],
            [
                InlineKeyboardButton(text='отмена', callback_data='отмена')
            ]
        ])

    return some_keyboard
