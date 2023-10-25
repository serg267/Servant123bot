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
            ]
            ,
            [
                InlineKeyboardButton(text='отмена', callback_data='отмена')
            ]
        ])

    return some_keyboard

from aiogram.utils.keyboard import InlineKeyboardBuilder


# def keyboard_yes_no() -> InlineKeyboardMarkup:
#     elements = ['да', 'нет']
#     some_keyboard = InlineKeyboardBuilder()
#     for element in elements:
#         some_keyboard.button(text=element, callback_data=element)
#
#     some_keyboard.button(text='отмена', callback_data='отмена')
#     buttons = [InlineKeyboardButton(text='element', callback_data='element'),
#                InlineKeyboardButton(text='element1', callback_data='element1')]
#     some_keyboard.row(*buttons)
#     return some_keyboard.as_markup()
